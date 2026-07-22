from __future__ import annotations

import argparse
import json
from pathlib import Path

from docx_tools import fill


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--workspace", default=".", type=Path)
    args = parser.parse_args()
    try:
        result = fill(args.template, args.source, args.output, args.workspace.resolve())
        print("DOCX_FILL_OK=" + json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"DOCX_FILL_FAIL={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

