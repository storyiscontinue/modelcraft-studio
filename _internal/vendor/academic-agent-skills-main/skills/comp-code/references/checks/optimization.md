# Optimization Verification

Apply all five layers.

## Layer 1: Input feasibility

- Check dimensions, bounds, capacity totals, and obvious necessary conditions.
- Explain any unit conversion or horizon multiplier.

## Layer 2: Solver outcome

- Record solver name/version, status, message, objective, and optimality gap when available.
- Stop if no valid primal solution exists. Never label a timeout or numerical failure as optimal.

## Layer 3: Primal validation

- Recompute equality residuals, inequality slacks, variable bounds, and integrality error.
- Report the maximum violation and the tolerance used.
- Recompute objective components independently.

## Layer 4: Independent structural validation

- Enumerate small discrete decisions and solve continuous subproblems when practical.
- Compare with a hand-calculated lower bound, dual bound, shortest-path invariant, or flow balance.
- Test a deliberately infeasible case to prove constraints are active.

## Layer 5: Sensitivity and stability

- Re-optimize every requested perturbation.
- Report decision changes, active-set changes, objective changes, and infeasibility.
- Verify monotonic properties implied by nested feasible regions or uniformly scaled costs.

The result JSON should include `solver`, `status`, `objective`, `objective_components`,
`max_equality_residual`, `max_inequality_violation`, `max_integrality_error`, and scenario records.
