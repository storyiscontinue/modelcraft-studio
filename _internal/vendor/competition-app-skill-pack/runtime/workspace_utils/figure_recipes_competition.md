# Competition Figure Recipes

## 1. Normalized multi-criterion radar chart
```python
fig, ax = radar_plot(criteria, normalized_scores)
```

## 2. Method-by-metric grouped bars
```python
fig, ax = bar_compare(metrics, {"Proposed": proposed, "Baseline": baseline})
```

## 3. Sensitivity curve
```python
fig, ax = trend_plot(parameter_values, objective_values, marker="o")
```

## 4. Allocation distribution
```python
fig, ax = distribution_plot(allocation_values, bins=15)
```

## 5. Scenario comparison
```python
fig, ax = multi_line_plot(horizons, scenario_series)
```

## 6. Error decomposition
```python
fig, ax = bar_compare(error_components, component_by_method)
```

## 7. Province schematic map
```python
# Join values to the bundled province GeoJSON by the `name` property, then plot polygons.
```

