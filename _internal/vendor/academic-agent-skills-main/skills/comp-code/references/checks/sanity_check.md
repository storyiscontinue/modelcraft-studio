# Numerical and Domain Sanity Checks

## Automatic numeric checks

- All output numbers are finite.
- Counts are integers and nonnegative where required.
- Probabilities and rates stay in their declared ranges.
- Totals equal the sum of components within a documented tolerance.
- Equality residuals and inequality violations are reported with their maxima.
- Repeated execution with the same inputs produces the same results.

## Nine review questions

1. Do units match on both sides of every equation?
2. Does the result scale plausibly with the input magnitudes?
3. Are signs and monotonic directions physically/economically plausible?
4. Are capacity, conservation, and boundary conditions satisfied?
5. Are percentages distinguished from fractions?
6. Are daily, annual, per-item, and total values kept separate?
7. Is every scenario independently solved and labeled?
8. Is the solver/model status preserved rather than inferred from a numeric vector?
9. Can every reported value be regenerated from the saved machine-readable output?

## Programming review

- Reject silent broadcasting that changes the intended axis.
- Reject accidental integer truncation and chained in-place scenario mutation.
- Check empty collections before min/max/mean operations.
- Normalize JSON types and use `allow_nan=False`.
- Capture exceptions with enough context to reproduce the failed scenario.
