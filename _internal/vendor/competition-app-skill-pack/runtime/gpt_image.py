#!/usr/bin/env python3
"""Generate a paper illustration through an OpenAI-compatible Images API."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import ssl
import sys
import time
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import HTTPSHandler, HTTPRedirectHandler, Request, build_opener


MAX_IMAGE_BYTES = 50 * 1024 * 1024
BLOCKED_HOSTS = frozenset({"mingheng.xin", "mhcoding.xyz"})


def blocked_host(hostname: str | None) -> bool:
    host = (hostname or "").lower().rstrip(".")
    return any(host == item or host.endswith("." + item) for item in BLOCKED_HOSTS)


class SameHostRedirectHandler(HTTPRedirectHandler):
    def __init__(self, host: str):
        super().__init__()
        self.host = host.lower()

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlsplit(newurl)
        if (
            target.scheme not in {"http", "https"}
            or blocked_host(target.hostname)
            or (target.hostname or "").lower() != self.host
        ):
            raise ValueError("cross-host API redirect blocked")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def image_endpoint(base_url: str) -> str:
    parsed = urlsplit(str(base_url or "").strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("GPT_IMAGE_BASE_URL must be an HTTP(S) URL")
    if parsed.username or parsed.password or parsed.fragment:
        raise ValueError("GPT_IMAGE_BASE_URL must not contain credentials or a fragment")
    if blocked_host(parsed.hostname):
        raise ValueError("GPT_IMAGE_BASE_URL host is blocked by local policy")
    path = parsed.path.rstrip("/")
    if path.endswith("/images/generations"):
        output_path = path
    elif path.endswith("/v1"):
        output_path = path + "/images/generations"
    else:
        output_path = path + "/v1/images/generations"
    return urlunsplit((parsed.scheme, parsed.netloc, output_path, parsed.query, ""))


def aspect_to_size(value: str) -> str:
    ratio = str(value or "").strip()
    if ratio in {"16:9", "3:2", "4:3"}:
        return "1536x1024"
    if ratio in {"9:16", "2:3", "3:4"}:
        return "1024x1536"
    return "1024x1024"


def build_prompt(prompt: str, language: str) -> str:
    language_rule = (
        "Use accurate Simplified Chinese labels and preserve Latin mathematical variables."
        if language == "zh"
        else "Use concise English labels and preserve mathematical notation."
    )
    return (
        "Create a publication-quality academic paper illustration. "
        + language_rule
        + " White background, no title above the figure, no watermark, no signature, "
        "and no decorative frame. Do not generate identifiable faces; use abstract icons.\n\n"
        + prompt.strip()
    )


def read_limited(response, limit: int = MAX_IMAGE_BYTES) -> bytes:
    value = response.read(limit + 1)
    if len(value) > limit:
        raise ValueError("image response exceeds 50 MB")
    return value


def download_image(url: str, timeout: int) -> bytes:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("image URL in the response is invalid")
    if blocked_host(parsed.hostname):
        raise ValueError("image URL host is blocked by local policy")
    request = Request(url, headers={"User-Agent": "ModelCraft-Image/1.0"})
    opener = build_opener(
        SameHostRedirectHandler(parsed.hostname),
        HTTPSHandler(context=ssl.create_default_context()),
    )
    with opener.open(request, timeout=timeout) as response:
        return read_limited(response)


def decode_image(payload: dict, timeout: int) -> bytes:
    items = payload.get("data")
    if not isinstance(items, list) or not items or not isinstance(items[0], dict):
        raise ValueError("image response contains no data item")
    item = items[0]
    encoded = item.get("b64_json")
    if isinstance(encoded, str) and encoded:
        return base64.b64decode(encoded, validate=True)
    url = item.get("url")
    if isinstance(url, str) and url.startswith("data:") and "," in url:
        return base64.b64decode(url.split(",", 1)[1], validate=True)
    if isinstance(url, str) and url:
        return download_image(url, timeout)
    raise ValueError("image response has neither b64_json nor url")


def generate_image(base_url: str, api_key: str, model: str, prompt: str, size: str, timeout: int) -> bytes:
    endpoint = image_endpoint(base_url)
    host = (urlsplit(endpoint).hostname or "").lower()
    raw = json.dumps(
        {"model": model, "prompt": prompt, "n": 1, "size": size},
        ensure_ascii=False,
    ).encode("utf-8")
    request = Request(
        endpoint,
        data=raw,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "ModelCraft-Image/1.0",
        },
    )
    opener = build_opener(
        SameHostRedirectHandler(host),
        HTTPSHandler(context=ssl.create_default_context()),
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            payload = json.loads(read_limited(response).decode("utf-8"))
    except HTTPError as exc:
        try:
            detail = exc.read(2000).decode("utf-8", "replace")
        finally:
            exc.close()
        raise RuntimeError(f"image API HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"image API request failed: {exc}") from exc
    return decode_image(payload, timeout)


def bounded_output(raw_path: str) -> Path:
    root = Path(os.environ.get("OMA_WORKSPACE_DIR") or os.getcwd()).resolve()
    candidate = Path(raw_path)
    target = (root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("image output must stay inside the workspace") from exc
    if target.suffix.lower() != ".png":
        raise ValueError("image output must use the .png extension")
    return target


def safe_error(exc: Exception, *secrets: str) -> str:
    message = str(exc)
    for secret in secrets:
        if secret:
            message = message.replace(secret, "<REDACTED_SECRET>")
    return message[:2000]


def failure_marker(workspace: Path, raw_output: str) -> Path:
    digest = hashlib.sha256(str(raw_output).encode("utf-8")).hexdigest()[:20]
    return workspace / "_utils" / "gpt_image_failures" / f"{digest}.json"


def record_failure(workspace: Path, raw_output: str, error: str) -> None:
    marker = failure_marker(workspace, raw_output)
    marker.parent.mkdir(parents=True, exist_ok=True)
    temporary = marker.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(
            {"output": Path(raw_output).name, "error": error[:2000]},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(marker)


def clear_failure(workspace: Path, raw_output: str) -> None:
    failure_marker(workspace, raw_output).unlink(missing_ok=True)


def save_png_and_pdf(image_bytes: bytes, output: Path) -> Path | None:
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image

        image = Image.open(BytesIO(image_bytes))
        image.load()
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.getchannel("A"))
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
        image.save(output, "PNG")
        pdf_path = output.with_suffix(".pdf")
        image.save(pdf_path, "PDF", resolution=300)
        return pdf_path
    except ImportError:
        if not image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError("Pillow is required to convert a non-PNG image response")
        output.write_bytes(image_bytes)
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--lang", choices=("zh", "en"), default="zh")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--max-retries", type=int, default=3)
    args = parser.parse_args(argv)

    base_url = os.environ.get("GPT_IMAGE_BASE_URL", "").strip()
    api_key = os.environ.get("GPT_IMAGE_API_KEY", "").strip()
    model = os.environ.get("GPT_IMAGE_MODEL", "").strip()
    workspace = Path(os.environ.get("OMA_WORKSPACE_DIR") or os.getcwd()).resolve()
    configured = bool(base_url and api_key and model)
    if args.check:
        print("GPT_IMAGE_AVAILABLE=YES" if configured else "GPT_IMAGE_AVAILABLE=NO")
        return 0 if configured else 1
    if not configured:
        if args.output:
            record_failure(
                workspace,
                args.output,
                "image Base URL, model, and API key are required",
            )
        print("GPT_IMAGE_NOT_CONFIGURED")
        return 1
    if not args.prompt or not args.output:
        if args.output:
            record_failure(
                workspace,
                args.output,
                "--prompt and --output are required",
            )
        print("ERROR: --prompt and --output are required")
        return 1

    try:
        timeout = max(
            30,
            min(int(os.environ.get("GPT_IMAGE_TIMEOUT_SECONDS", "300")), 86400),
        )
        output = bounded_output(args.output)
    except (TypeError, ValueError) as exc:
        error = safe_error(exc, api_key)
        record_failure(workspace, args.output, error)
        print(f"GPT_IMAGE_CONFIG_ERROR={error}")
        return 1

    attempts = max(1, min(int(args.max_retries), 5))
    error = "unknown error"
    for attempt in range(1, attempts + 1):
        try:
            image_bytes = generate_image(
                base_url,
                api_key,
                model,
                build_prompt(args.prompt, args.lang),
                aspect_to_size(args.aspect_ratio),
                timeout,
            )
            pdf_path = save_png_and_pdf(image_bytes, output)
            clear_failure(workspace, args.output)
            print(f"GPT_IMAGE_OK={output.relative_to(workspace).as_posix()}")
            if pdf_path:
                print(f"GPT_IMAGE_PDF={pdf_path.relative_to(workspace).as_posix()}")
            return 0
        except Exception as exc:
            error = safe_error(exc, api_key)
            print(f"GPT_IMAGE_ATTEMPT_{attempt}_FAILED={error}")
            if attempt < attempts:
                time.sleep(min(6, attempt * 2))
    record_failure(workspace, args.output, error)
    print(f"GPT_IMAGE_FAILED={error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
