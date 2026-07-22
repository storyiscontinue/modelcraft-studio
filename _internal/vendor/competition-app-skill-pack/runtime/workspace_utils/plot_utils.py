"""Stable plotting helpers used by the bundled academic Skills."""

from __future__ import annotations

from math import pi
from pathlib import Path
from typing import Iterable, Mapping, Sequence


PALETTES = {
    "soft": ["#3B6FB6", "#D95F59", "#4C956C", "#E0A458", "#7A5195", "#5C677D"],
    "tableau": ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"],
    "nature": ["#3C5488", "#E64B35", "#00A087", "#4DBBD5", "#F39B7F", "#8491B4"],
    "npg": ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F", "#8491B4"],
    "nejm": ["#BC3C29", "#0072B5", "#E18727", "#20854E", "#7876B1", "#6F99AD"],
    "science": ["#3B4992", "#EE0000", "#008B45", "#631879", "#008280", "#BB0021"],
    "colorblind": ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"],
}
PALETTE = list(PALETTES["soft"])


def _plt():
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    return plt


def setup_style(palette: str = "soft") -> list[str]:
    """Apply a publication-oriented Matplotlib baseline and return its palette."""
    plt = _plt()
    selected = PALETTES.get(str(palette).lower())
    if selected is None:
        raise ValueError(f"unknown palette: {palette}")
    PALETTE[:] = selected
    plt.rcParams.update(
        {
            "axes.prop_cycle": __import__("cycler").cycler(color=PALETTE),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": False,
            "axes.labelsize": 10,
            "font.size": 10,
            "legend.frameon": False,
            "legend.fontsize": 9,
            "lines.linewidth": 1.8,
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    return list(PALETTE)


def save_fig(fig, output, dpi: int = 350, **kwargs) -> Path:
    path = Path(output)
    if path.suffix.lower() not in {".png", ".pdf", ".svg"}:
        raise ValueError("figure output must use .png, .pdf, or .svg")
    path.parent.mkdir(parents=True, exist_ok=True)
    options = {"bbox_inches": "tight", "facecolor": "white"}
    options.update(kwargs)
    if path.suffix.lower() == ".png":
        options.setdefault("dpi", max(300, int(dpi)))
    fig.savefig(path, **options)
    return path


def _axes(ax=None, figsize=(6.4, 4.0), polar=False):
    if ax is not None:
        return ax.figure, ax
    plt = _plt()
    return plt.subplots(figsize=figsize, subplot_kw={"polar": True} if polar else None)


def heatmap(data, row_labels=None, col_labels=None, ax=None, cmap="Blues", annotate=True):
    fig, ax = _axes(ax)
    image = ax.imshow(data, cmap=cmap, aspect="auto")
    if row_labels is not None:
        ax.set_yticks(range(len(row_labels)), labels=row_labels)
    if col_labels is not None:
        ax.set_xticks(range(len(col_labels)), labels=col_labels, rotation=30, ha="right")
    if annotate:
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                ax.text(j, i, f"{value:.3g}" if isinstance(value, (int, float)) else str(value), ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, fraction=0.045, pad=0.04)
    return fig, ax


def forest_plot(estimates, lower, upper, labels=None, ax=None):
    fig, ax = _axes(ax)
    y = list(range(len(estimates)))
    errors = [[e - lo for e, lo in zip(estimates, lower)], [hi - e for e, hi in zip(estimates, upper)]]
    ax.errorbar(estimates, y, xerr=errors, fmt="o", color=PALETTE[0], capsize=3)
    ax.axvline(0, color="#666666", linewidth=1, linestyle="--")
    if labels is not None:
        ax.set_yticks(y, labels=labels)
    return fig, ax


def trend_plot(x, y, ax=None, label=None, color=None, marker="o"):
    fig, ax = _axes(ax)
    ax.plot(x, y, label=label, color=color or PALETTE[0], marker=marker)
    if label:
        ax.legend()
    return fig, ax


def bar_compare(categories, series, ax=None, labels=None):
    fig, ax = _axes(ax)
    values = list(series.values()) if isinstance(series, Mapping) else list(series)
    names = list(series) if isinstance(series, Mapping) else list(labels or range(len(values)))
    width = 0.8 / max(1, len(values))
    positions = list(range(len(categories)))
    for index, row in enumerate(values):
        offset = (index - (len(values) - 1) / 2) * width
        ax.bar([x + offset for x in positions], row, width=width, label=str(names[index]))
    ax.set_xticks(positions, labels=categories)
    if len(values) > 1:
        ax.legend()
    return fig, ax


def distribution_plot(values, ax=None, bins=20, label=None):
    fig, ax = _axes(ax)
    ax.hist(values, bins=bins, color=PALETTE[0], alpha=0.8, label=label, edgecolor="white")
    if label:
        ax.legend()
    return fig, ax


def scatter_plot(x, y, ax=None, groups=None):
    fig, ax = _axes(ax)
    if groups is None:
        ax.scatter(x, y, color=PALETTE[0], alpha=0.8)
    else:
        unique = list(dict.fromkeys(groups))
        for index, group in enumerate(unique):
            selected = [i for i, value in enumerate(groups) if value == group]
            ax.scatter([x[i] for i in selected], [y[i] for i in selected], label=str(group), color=PALETTE[index % len(PALETTE)])
        ax.legend()
    return fig, ax


def residual_diagnostic(fitted, residuals, ax=None):
    fig, ax = scatter_plot(fitted, residuals, ax=ax)
    ax.axhline(0, color="#666666", linestyle="--", linewidth=1)
    ax.set_xlabel("Fitted value")
    ax.set_ylabel("Residual")
    return fig, ax


def multi_line_plot(x, series, ax=None):
    fig, ax = _axes(ax)
    rows = series.items() if isinstance(series, Mapping) else enumerate(series)
    for label, values in rows:
        ax.plot(x, values, marker="o", label=str(label))
    ax.legend()
    return fig, ax


def box_plot(data, labels=None, ax=None):
    fig, ax = _axes(ax)
    ax.boxplot(data, labels=labels, patch_artist=True, boxprops={"facecolor": PALETTE[0], "alpha": 0.55})
    return fig, ax


def radar_plot(labels, values, ax=None):
    count = len(labels)
    if count < 3 or len(values) != count:
        raise ValueError("radar_plot requires at least three labels and matching values")
    fig, ax = _axes(ax, figsize=(5.2, 5.2), polar=True)
    angles = [2 * pi * index / count for index in range(count)]
    closed_angles = angles + angles[:1]
    closed_values = list(values) + list(values[:1])
    ax.plot(closed_angles, closed_values, color=PALETTE[0])
    ax.fill(closed_angles, closed_values, color=PALETTE[0], alpha=0.2)
    ax.set_xticks(angles, labels=labels)
    return fig, ax


def subplot_grid(count: int, columns: int = 2, figsize=None):
    if count < 1 or columns < 1:
        raise ValueError("count and columns must be positive")
    rows = (count + columns - 1) // columns
    plt = _plt()
    fig, axes = plt.subplots(rows, columns, figsize=figsize or (6.2 * columns, 3.8 * rows), squeeze=False)
    for ax in axes.flat[count:]:
        ax.set_visible(False)
    return fig, axes


setup_style()

