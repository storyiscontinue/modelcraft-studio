# Basic Figure Recipes

## 1. Single trend
```python
fig, ax = trend_plot(x, y, label="objective"); ax.set(xlabel="Iteration", ylabel="Objective")
```

## 2. Grouped comparison
```python
fig, ax = bar_compare(categories, {"Method A": values_a, "Method B": values_b})
```

## 3. Scatter relationship
```python
fig, ax = scatter_plot(x, y); ax.set(xlabel="Input", ylabel="Output")
```

## 4. Distribution histogram
```python
fig, ax = distribution_plot(values, bins=18); ax.set(xlabel="Value", ylabel="Frequency")
```

## 5. Box plot comparison
```python
fig, ax = box_plot([values_a, values_b], labels=["A", "B"])
```

## 6. Correlation heatmap
```python
fig, ax = heatmap(matrix, row_labels=names, col_labels=names, cmap="Blues")
```

## 7. Multi-series trend
```python
fig, ax = multi_line_plot(x, {"Scenario 1": y1, "Scenario 2": y2})
```

## 8. Estimate with uncertainty
```python
fig, ax = forest_plot(estimates, lower_bounds, upper_bounds, labels=names)
```

