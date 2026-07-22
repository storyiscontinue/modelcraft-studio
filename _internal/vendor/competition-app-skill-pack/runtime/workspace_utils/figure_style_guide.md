# HC Figure Style Guide

Use `from _utils.plot_utils import setup_style, save_fig, PALETTE` at the top
of every generated figure script, then call `setup_style()` once.

## Non-negotiable rules

- Write each figure generator as `figures/gen_fig_<name>.py` and read values from JSON or CSV.
- Use `save_fig(fig, "figures/<name>.png")`; create PDF only when the paper output requires it.
- Do not use `plt.title()` or `Axes.set_title()`. Put titles in the paper caption.
- Use at least 9 pt text, a white background, and distinguishable colors in grayscale.
- Keep figures under 8 inches high. Use legends only when a caption cannot identify series.

## Palette selection

| Use case | `setup_style` palette |
| --- | --- |
| General mathematical modeling | `soft` |
| Dense comparison tables | `tableau` |
| Biomedical-style result panels | `nature` or `nejm` |
| Color-accessible output | `colorblind` |

## Selection guide

| Evidence | Recommended chart |
| --- | --- |
| Categories across methods | grouped bar chart |
| Time or iteration sequence | multi-line trend |
| Distribution and outliers | box plot plus individual points |
| Pairwise relationship | scatter plot with fitted line only when justified |
| Variable association | annotated heatmap |
| Estimate and confidence interval | forest plot |
| Multi-criterion score | radar chart, only for 3-8 normalized dimensions |

