# Code Error Prevention

Use this checklist before declaring a modeling solver complete.

## Runtime contract

- Use the injected `HC_PYTHON`; do not replace it or probe for another Python.
- Keep every generated path inside the current workspace.
- Pin randomness with an explicit seed and record library versions.
- Never install a dependency during a workflow. Report a missing dependency as an error.

## Data and units

- Define source data once and validate array shapes before optimization.
- Keep a unit table beside the parameters. Convert units exactly once.
- Reject missing, non-finite, negative, or out-of-range values when the model forbids them.
- Distinguish daily values from planning-horizon totals.

## Optimization

- Check solver success/status before reading a solution vector.
- Recompute the objective from the returned decision variables.
- Recompute every equality residual, inequality slack, bound, and integrality condition.
- Do not round variables before validation. Round only display values.
- For small discrete spaces, independently enumerate configurations and solve their continuous subproblems.

## Sensitivity

- Rebuild or copy parameters for every scenario; never mutate the baseline in place.
- Re-optimize each scenario. Do not score a perturbed scenario with the baseline decision unless it is explicitly a stress test.
- Record infeasible scenarios separately from numeric results.
- Check directional invariants that follow from the model.

## Output contract

- `code/main.py` must run from the workspace root with `"$HC_PYTHON" code/main.py`.
- `figures/all_results.json` must contain only valid JSON and finite numeric values.
- `RESULTS.md` must cite values from `all_results.json`, including units and solver status.
- Use stable keys and deterministic ordering so validators can compare outputs.

## Common bugs

- Wrong objective sign or a missing horizon multiplier.
- Capacity constraints not linked to binary activation variables.
- Demand constraints transposed across axes.
- Reusing a stale solver result after changing parameters.
- Treating an unsuccessful solver result as an optimum.
- Serializing NumPy scalars, `NaN`, or `Infinity` directly to JSON.
- Writing files through fragile long shell heredocs when `Edit` or a local Python file writer is safer.
