# Academic Figure Recipes

## 1. Confidence interval forest plot
```python
fig, ax = forest_plot(beta, ci_low, ci_high, labels=variables)
```

## 2. Correlation matrix
```python
fig, ax = heatmap(correlation, row_labels=variables, col_labels=variables, cmap="RdBu_r")
```

## 3. Residual diagnostic
```python
fig, ax = residual_diagnostic(predicted, residuals)
```

## 4. Paired outcome trend
```python
fig, ax = multi_line_plot(periods, {"Observed": observed, "Predicted": predicted})
```

