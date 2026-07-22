# Advanced Figure Recipes

## 1. Pareto frontier
```python
fig, ax = scatter_plot(cost, benefit); ax.set(xlabel="Cost", ylabel="Benefit")
```

## 2. Uncertainty ribbon
```python
fig, ax = trend_plot(x, mean); ax.fill_between(x, lower, upper, color=PALETTE[0], alpha=.2)
```

## 3. Calibration comparison
```python
fig, ax = multi_line_plot(probability_bins, {"Perfect": probability_bins, "Model": observed_frequency})
```

## 4. Multi-panel diagnostic
```python
fig, axes = subplot_grid(4, columns=2)
```

