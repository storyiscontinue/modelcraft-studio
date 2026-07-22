"""Check a rendered TikZ preview for dimensions, blankness, and clipping."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    try:
        from PIL import Image, ImageChops

        with Image.open(args.image).convert("RGB") as image:
            if image.width < 300 or image.height < 200:
                raise ValueError("rendered diagram is too small")
            background = Image.new("RGB", image.size, "white")
            difference = ImageChops.difference(image, background).convert("L")
            box = difference.point(lambda value: 255 if value > 8 else 0).getbbox()
            if box is None:
                raise ValueError("rendered diagram is blank")
            left, top, right, bottom = box
            margin = min(left, top, image.width - right, image.height - bottom)
            if margin <= 1:
                raise ValueError("diagram content touches the image boundary")
            coverage = ((right - left) * (bottom - top)) / (image.width * image.height)
            if coverage < 0.08:
                raise ValueError("diagram content occupies less than 8% of the canvas")
            print(f"TIKZ_VISION_OK={image.width}x{image.height};coverage={coverage:.3f}")
            return 0
    except (ImportError, OSError, ValueError) as exc:
        print(f"TIKZ_VISION_FAIL={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
