# Prediction Verification

- Split data in time/order-aware fashion when leakage is possible.
- Fit preprocessing only on training data and serialize the fitted transformation.
- Compare against a simple baseline using the same folds or forecast horizon.
- Report train/validation/test sample counts and target distribution.
- Use metrics appropriate to the task and preserve their units.
- Include residual/error distribution, calibration where relevant, and subgroup checks.
- Fix random seeds and record the full feature list.
- Never report test performance from a model selected on that same test set.
