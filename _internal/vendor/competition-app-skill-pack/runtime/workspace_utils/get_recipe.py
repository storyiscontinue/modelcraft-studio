"""Print one numbered recipe from the bundled figure recipe library."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CATEGORIES = {"advanced", "basic", "academic", "competition", "empirical"}


def extract_recipe(category: str, number: int) -> str:
    if category not in CATEGORIES:
        raise ValueError(f"unknown recipe category: {category}")
    if number < 1:
        raise ValueError("recipe number must be positive")
    path = Path(__file__).with_name(f"figure_recipes_{category}.md")
    text = path.read_text(encoding="utf-8")
    heading = re.compile(rf"^##\s+{number}(?:\.|\s|:)", re.MULTILINE)
    match = heading.search(text)
    if not match:
        raise ValueError(f"recipe {category} {number} does not exist")
    next_heading = re.search(r"^##\s+\d+(?:\.|\s|:)", text[match.end() :], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.start() : end].rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("category", choices=sorted(CATEGORIES))
    parser.add_argument("number", type=int)
    args = parser.parse_args()
    try:
        print(extract_recipe(args.category, args.number), end="")
    except (OSError, ValueError) as exc:
        print(f"RECIPE_ERROR={exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
