"""Generate reproducible statistical tables in Markdown or LaTeX."""

from __future__ import annotations

from math import sqrt
from pathlib import Path


def _records(data, columns=None):
    if hasattr(data, "to_dict"):
        rows = data.to_dict(orient="records")
    elif isinstance(data, dict):
        keys = list(columns or data)
        length = len(data[keys[0]]) if keys else 0
        rows = [{key: data[key][index] for key in keys} for index in range(length)]
    else:
        rows = list(data)
        if rows and not isinstance(rows[0], dict):
            names = list(columns or [f"x{index + 1}" for index in range(len(rows[0]))])
            rows = [dict(zip(names, row)) for row in rows]
    return rows


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _format(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _latex_escape(value):
    text = str(value)
    for source, target in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#")):
        text = text.replace(source, target)
    return text


def _render(headers, rows, output=None, caption=""):
    path = Path(output) if output else None
    if path and path.suffix.lower() == ".tex":
        alignment = "l" + "r" * (len(headers) - 1)
        lines = [r"\begin{table}[htbp]", r"\centering"]
        if caption:
            lines.append(r"\caption{" + _latex_escape(caption) + "}")
        lines.extend([rf"\begin{{tabular}}{{{alignment}}}", r"\toprule", " & ".join(map(_latex_escape, headers)) + r" \\", r"\midrule"])
        lines.extend(" & ".join(_latex_escape(_format(value)) for value in row) + r" \\" for row in rows)
        lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])
    else:
        lines = ["| " + " | ".join(map(str, headers)) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
        lines.extend("| " + " | ".join(_format(value) for value in row) + " |" for row in rows)
    text = "\n".join(lines) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return text


def descriptive_table(data, columns=None, output=None, caption="Descriptive statistics"):
    rows = _records(data, columns)
    names = list(columns or (rows[0].keys() if rows else []))
    output_rows = []
    for name in names:
        values = [_number(row.get(name)) for row in rows]
        values = [value for value in values if value is not None]
        if not values:
            continue
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / max(1, len(values) - 1)
        output_rows.append([name, len(values), mean, sqrt(variance), min(values), max(values)])
    return _render(["Variable", "N", "Mean", "SD", "Min", "Max"], output_rows, output, caption)


def correlation_table(data, columns=None, output=None, caption="Correlation matrix"):
    rows = _records(data, columns)
    names = list(columns or (rows[0].keys() if rows else []))
    vectors = {name: [_number(row.get(name)) for row in rows] for name in names}
    output_rows = []
    for left in names:
        row = [left]
        for right in names:
            pairs = [(a, b) for a, b in zip(vectors[left], vectors[right]) if a is not None and b is not None]
            if len(pairs) < 2:
                row.append(None)
                continue
            av = sum(a for a, _ in pairs) / len(pairs)
            bv = sum(b for _, b in pairs) / len(pairs)
            numerator = sum((a - av) * (b - bv) for a, b in pairs)
            denominator = sqrt(sum((a - av) ** 2 for a, _ in pairs) * sum((b - bv) ** 2 for _, b in pairs))
            row.append(numerator / denominator if denominator else 0.0)
        output_rows.append(row)
    return _render(["Variable", *names], output_rows, output, caption)


def regression_table(results, model_names=None, output=None, caption="Regression results"):
    models = list(results if isinstance(results, (list, tuple)) else [results])
    names = list(model_names or [f"Model {index + 1}" for index in range(len(models))])
    parameter_names = []
    extracted = []
    for model in models:
        params = getattr(model, "params", model if isinstance(model, dict) else {})
        if hasattr(params, "to_dict"):
            params = params.to_dict()
        params = dict(params)
        extracted.append(params)
        for key in params:
            if key not in parameter_names:
                parameter_names.append(key)
    rows = [[parameter, *[model.get(parameter) for model in extracted]] for parameter in parameter_names]
    return _render(["Variable", *names], rows, output, caption)

