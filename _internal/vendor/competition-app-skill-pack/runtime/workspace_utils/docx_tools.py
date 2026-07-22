"""DOCX template inspection and conservative body replacement helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path


def _document(path: Path):
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("python-docx is required for DOCX template tools") from exc
    return Document(str(path))


def analyze(template: Path) -> dict:
    document = _document(template)
    paragraphs = [
        {
            "index": index,
            "text": paragraph.text,
            "style": paragraph.style.name if paragraph.style else "",
        }
        for index, paragraph in enumerate(document.paragraphs)
    ]
    tables = []
    for index, table in enumerate(document.tables):
        tables.append(
            {
                "index": index,
                "rows": len(table.rows),
                "columns": len(table.columns),
                "cells": [[cell.text for cell in row.cells] for row in table.rows],
            }
        )
    joined = "\n".join(item["text"] for item in paragraphs)
    language = "zh" if re.search(r"[\u4e00-\u9fff]", joined) else "en"
    return {"format": "hc-docx-template-v1", "language": language, "paragraphs": paragraphs, "tables": tables}


def write_analysis(template: Path, output: Path, summary: Path) -> None:
    payload = analyze(template)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"=== Template structure (language: {payload['language']}) ==="]
    for item in payload["paragraphs"]:
        text = item["text"].strip()
        if text:
            lines.append(f"[Paragraph {item['index']:>4}] [{item['style']}] {text}")
    for item in payload["tables"]:
        lines.append(f"[Table {item['index']:>4}] {item['rows']} rows x {item['columns']} columns")
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _source_sections(path: Path) -> dict[str, list[str] | str]:
    text = path.read_text(encoding="utf-8")
    title = ""
    sections: dict[str, list[str]] = {"abstract": [], "body": [], "references": [], "appendix": []}
    current = "body"
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        heading = re.sub(r"^#+\s*", "", line).strip().casefold() if line.startswith("#") else ""
        if heading:
            if "abstract" in heading or "摘要" in heading:
                current = "abstract"
            elif "reference" in heading or "参考文献" in heading:
                current = "references"
            elif "appendix" in heading or "附录" in heading:
                current = "appendix"
            else:
                current = "body"
                sections[current].append(re.sub(r"^#+\s*", "", line))
            continue
        if line and not line.startswith("<!--"):
            sections[current].append(line)
    return {"title": title or path.stem, **sections}


def _find_anchor(paragraphs, words):
    for index, paragraph in enumerate(paragraphs):
        text = paragraph.text.strip().casefold()
        if any(word in text for word in words):
            return index
    return None


def _replace(paragraph, lines: list[str] | str) -> int:
    values = [lines] if isinstance(lines, str) else list(lines)
    paragraph.text = values[0] if values else ""
    parent = paragraph._p.getparent()
    position = parent.index(paragraph._p)
    inserted = 1 if values else 0
    if len(values) > 1:
        from docx.oxml import OxmlElement
        from docx.text.paragraph import Paragraph

        previous = paragraph._p
        for value in values[1:]:
            element = OxmlElement("w:p")
            previous.addnext(element)
            created = Paragraph(element, paragraph._parent)
            if paragraph.style:
                created.style = paragraph.style
            created.add_run(value)
            previous = element
            inserted += 1
    return inserted


def fill(template: Path, source: Path, output: Path, workspace: Path) -> dict:
    document = _document(template)
    source_data = _source_sections(source)
    map_path = workspace / "_template_map.json"
    mapping = json.loads(map_path.read_text(encoding="utf-8")) if map_path.is_file() else {}
    paragraphs = list(document.paragraphs)
    anchors = {
        "title": mapping.get("title_anchor_para_idx"),
        "abstract": mapping.get("abstract_anchor_para_idx"),
        "body": mapping.get("body_anchor_para_idx"),
        "references": mapping.get("references_anchor_para_idx"),
        "appendix": mapping.get("appendix_anchor_para_idx"),
    }
    defaults = {
        "title": ("title", "标题", "题目"),
        "abstract": ("abstract", "摘要"),
        "body": ("body", "正文", "绪论", "introduction"),
        "references": ("references", "参考文献", "bibliography"),
        "appendix": ("appendix", "附录", "annex"),
    }
    for name, value in tuple(anchors.items()):
        if value is None:
            anchors[name] = _find_anchor(paragraphs, defaults[name])
    required = ("title", "abstract", "body", "references")
    missing = [name for name in required if anchors[name] is None]
    if missing:
        raise ValueError("template anchors not found: " + ", ".join(missing))
    used = set()
    for name in ("title", "abstract", "body", "references", "appendix"):
        index = anchors[name]
        if index is None:
            continue
        if not isinstance(index, int) or not 0 <= index < len(paragraphs):
            raise ValueError(f"invalid {name} anchor index: {index}")
        value = source_data[name]
        _replace(paragraphs[index], value)
        used.add(index)
        print(f"{name.capitalize()} inserted via template_map at paragraph {index}")
    delete_indices = set(mapping.get("delete_paragraph_indices") or [])
    conflict = delete_indices & used
    if conflict:
        raise ValueError(f"anchor indices cannot be deleted: {sorted(conflict)}")
    for index in sorted(delete_indices, reverse=True):
        if isinstance(index, int) and 0 <= index < len(paragraphs):
            element = paragraphs[index]._element
            element.getparent().remove(element)
    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output))
    return {"output": str(output), "anchors": anchors, "deleted": len(delete_indices)}

