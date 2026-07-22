from __future__ import annotations

import argparse
from pathlib import Path

from docx_tools import write_analysis


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    args = parser.parse_args()
    try:
        write_analysis(args.template, args.output, args.summary)
        print(f"DOCX_ANALYZE_OK={args.output}")
        return 0
    except Exception as exc:
        print(f"DOCX_ANALYZE_FAIL={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

