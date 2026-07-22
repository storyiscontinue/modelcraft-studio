"""Validate uncompressed DrawIO XML structure and basic diagram geometry."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.etree import ElementTree


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def graph_model(document):
    root = document.getroot()
    if local_name(root.tag) == "mxGraphModel":
        return root
    for element in root.iter():
        if local_name(element.tag) == "mxGraphModel":
            return element
    raise ValueError("no uncompressed mxGraphModel found")


def geometry(cell):
    for child in cell:
        if local_name(child.tag) == "mxGeometry":
            try:
                return tuple(float(child.get(name, "0")) for name in ("x", "y", "width", "height"))
            except ValueError as exc:
                raise ValueError(f"cell {cell.get('id')} has non-numeric geometry") from exc
    return None


def overlap_ratio(left, right):
    lx, ly, lw, lh = left
    rx, ry, rw, rh = right
    width = max(0.0, min(lx + lw, rx + rw) - max(lx, rx))
    height = max(0.0, min(ly + lh, ry + rh) - max(ly, ry))
    intersection = width * height
    base = min(lw * lh, rw * rh)
    return intersection / base if base > 0 else 0.0


def validate(path: Path, mode: str) -> list[str]:
    try:
        document = ElementTree.parse(path)
        model = graph_model(document)
    except (OSError, ValueError, ElementTree.ParseError) as exc:
        return [f"invalid DrawIO XML: {exc}"]
    cells = [element for element in model.iter() if local_name(element.tag) == "mxCell"]
    ids = [cell.get("id", "") for cell in cells]
    problems = []
    if not ids or any(not value for value in ids):
        problems.append("every mxCell must have an id")
    if len(ids) != len(set(ids)):
        problems.append("mxCell ids must be unique")
    known = set(ids)
    vertices = []
    edges = []
    for cell in cells:
        parent = cell.get("parent")
        if parent and parent not in known:
            problems.append(f"cell {cell.get('id')} has missing parent {parent}")
        if cell.get("vertex") == "1":
            box = geometry(cell)
            if not box or box[2] <= 0 or box[3] <= 0:
                problems.append(f"vertex {cell.get('id')} has invalid geometry")
            else:
                vertices.append((cell, box))
        if cell.get("edge") == "1":
            edges.append(cell)
            if cell.get("source") not in known or cell.get("target") not in known:
                problems.append(f"edge {cell.get('id')} has a missing source or target")
    for index, (left, left_box) in enumerate(vertices):
        for right, right_box in vertices[index + 1 :]:
            if left.get("parent") == right.get("parent") and overlap_ratio(left_box, right_box) > 0.4:
                problems.append(f"vertices {left.get('id')} and {right.get('id')} overlap")
    minimum_vertices = 4 if mode == "roadmap" else 3
    if len(vertices) < minimum_vertices:
        problems.append(f"{mode} requires at least {minimum_vertices} vertices")
    if len(edges) < max(1, minimum_vertices - 1):
        problems.append(f"{mode} has too few connecting edges")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("mode", choices=("roadmap", "flow"), nargs="?", default="flow")
    args = parser.parse_args()
    problems = validate(args.path, args.mode)
    for problem in problems:
        print(f"DRAWIO_FAIL={problem}")
    if problems:
        return 1
    print("DRAWIO_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

