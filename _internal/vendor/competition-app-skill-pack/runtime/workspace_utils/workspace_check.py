"""Strict local validation and cleanup commands used by shell wrappers."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER|XXX)\b|待补充|待完成|未完成", re.I)
LATEX_REF = re.compile(r"\\(?:includegraphics|input|include)(?:\[[^]]*])?\{([^}]+)}")


def files(root: Path, suffix: str):
    return sorted(path for path in root.rglob(f"*{suffix}") if path.is_file())


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def resolve_reference(root: Path, source: Path, token: str) -> bool:
    raw = Path(token.strip())
    candidates = [source.parent / raw, root / raw]
    if not raw.suffix:
        candidates.extend(candidate.with_suffix(ext) for candidate in tuple(candidates) for ext in (".tex", ".png", ".pdf", ".jpg", ".jpeg"))
    for candidate in candidates:
        resolved = candidate.resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            continue
        if resolved.is_file():
            return True
    return False


def figure_check(root: Path) -> list[str]:
    problems = []
    figures = root / "figures"
    for script in files(figures, ".py"):
        text = read(script)
        if re.search(r"\bplt\.title\s*\(|\.set_title\s*\(", text):
            problems.append(f"{relative(script, root)}: in-figure title is forbidden")
        if "savefig" not in text and "save_fig" not in text:
            problems.append(f"{relative(script, root)}: no figure save call")
    for image in files(figures, ".png"):
        try:
            from PIL import Image, ImageStat

            with Image.open(image) as opened:
                opened.verify()
            with Image.open(image).convert("RGB") as opened:
                if opened.width < 16 or opened.height < 16:
                    problems.append(f"{relative(image, root)}: image dimensions are too small")
                extrema = ImageStat.Stat(opened).extrema
                if all(low == high for low, high in extrema):
                    problems.append(f"{relative(image, root)}: image is blank")
        except (ImportError, OSError, ValueError) as exc:
            problems.append(f"{relative(image, root)}: invalid PNG ({exc})")
    includes = figures / "latex_includes.tex"
    if includes.is_file():
        for token in LATEX_REF.findall(read(includes)):
            if not resolve_reference(root, includes, token):
                problems.append(f"figures/latex_includes.tex: missing reference {token}")
    return problems


def writing_check(root: Path) -> list[str]:
    problems = []
    paper = root / "paper" if (root / "paper").is_dir() else root
    tex_files = files(paper, ".tex")
    if not tex_files:
        return ["paper: no TeX source files"]
    for path in tex_files:
        text = read(path)
        if PLACEHOLDER.search(text):
            problems.append(f"{relative(path, root)}: placeholder text remains")
        if "TODO__" in text:
            problems.append(f"{relative(path, root)}: unresolved citation key remains")
        same_level_empty = any(
            re.search(
                rf"\\{level}\{{[^}}]+}}\s*\\{level}\{{",
                text,
            )
            for level in ("section", "subsection")
        )
        if same_level_empty:
            problems.append(f"{relative(path, root)}: consecutive empty sections")
    joined = "\n".join(read(path) for path in tex_files)
    if "\\begin{document}" in joined and "\\end{document}" not in joined:
        problems.append("paper: document environment is not closed")
    return problems


def compile_cleanup(root: Path) -> list[str]:
    paper = root / "paper" if (root / "paper").is_dir() else root
    if not (paper / "main.tex").is_file():
        return ["paper/main.tex is missing"]
    for path in files(paper, ".tex"):
        text = read(path)
        original = text
        if path.parent.name == "sections":
            text = re.sub(r"(?m)^\s*\\(?:newpage|clearpage|nopagebreak)\s*$\n?", "", text)
        text = text.replace("figures/figures/", "../figures/")
        if path.parent.name == "sections" or path.name == "main.tex":
            text = re.sub(r"(?<!\.\./)figures/", "../figures/", text)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"CLEANED={relative(path, root)}")
    included = "\n".join(read(path) for path in files(paper, ".tex"))
    figures = root / "figures"
    for path in sorted(figures.glob("fig_*")) if figures.is_dir() else []:
        if path.is_file() and path.suffix.lower() in {".png", ".pdf", ".tex"} and path.name not in included:
            print(f"UNEMBEDDED={path.relative_to(root).as_posix()}")
    return []


def compile_check(root: Path) -> list[str]:
    problems = writing_check(root)
    paper = root / "paper" if (root / "paper").is_dir() else root
    pdf = paper / "main.pdf"
    if not pdf.is_file() or pdf.stat().st_size < 10_000:
        problems.append("paper/main.pdf is missing or too small")
    log = next(
        (
            candidate
            for candidate in (paper / "main.log", paper / "build" / "main.log")
            if candidate.is_file()
        ),
        None,
    )
    if log is None:
        problems.append("paper/main.log is missing")
    else:
        text = read(log)
        fatal_patterns = (
            "Fatal error occurred",
            "Undefined control sequence",
            "Emergency stop",
            "There were undefined references",
            "There were undefined citations",
        )
        for pattern in fatal_patterns:
            if pattern in text:
                problems.append(f"paper/main.log: {pattern}")
    return problems


def tikz_check(path: Path) -> list[str]:
    if not path.is_file():
        return [f"{path}: file is missing"]
    text = read(path)
    problems = []
    if "\\begin{tikzpicture}" not in text or "\\end{tikzpicture}" not in text:
        problems.append(f"{path}: tikzpicture environment is incomplete")
    if PLACEHOLDER.search(text):
        problems.append(f"{path}: placeholder text remains")
    if text.count("{") != text.count("}"):
        problems.append(f"{path}: unbalanced braces")
    if re.search(r"\\node[^;]*\b(?:title|标题)\b", text, re.I):
        problems.append(f"{path}: in-figure title is forbidden")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("figure", "writing", "compile-cleanup", "compile", "tikz"))
    parser.add_argument("target", nargs="?", default=".")
    args = parser.parse_args()
    target = Path(args.target).resolve()
    root = target if target.is_dir() else Path.cwd().resolve()
    try:
        if args.mode == "figure":
            problems = figure_check(root)
        elif args.mode == "writing":
            problems = writing_check(root)
        elif args.mode == "compile-cleanup":
            problems = compile_cleanup(root)
        elif args.mode == "compile":
            problems = compile_check(root)
        else:
            problems = tikz_check(target)
    except (OSError, UnicodeDecodeError) as exc:
        problems = [f"validation failed: {exc}"]
    for problem in problems:
        print(f"FAIL={problem}")
    if problems:
        print(f"HC_CHECK_FAILED={len(problems)}")
        return 1
    print("HC_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
