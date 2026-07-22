# Empirical Figure Recipes

## 1. Main-effect comparison
```python
fig, ax = bar_compare(outcomes, model_estimates)
```

## 2. Ablation trajectory
```python
fig, ax = trend_plot(components, scores, marker="s")
```

## 3. Subgroup distribution
```python
fig, ax = box_plot(subgroup_values, labels=subgroup_names)
```

## 4. Robustness scatter
```python
fig, ax = scatter_plot(reference_scores, perturbed_scores)
```
