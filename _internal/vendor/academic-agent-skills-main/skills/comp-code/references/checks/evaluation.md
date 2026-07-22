# Evaluation and Ranking Verification

- State whether each indicator is benefit, cost, interval, or target type.
- Validate normalization direction and handle constant columns explicitly.
- Show weights, prove they sum to one, and distinguish subjective from objective weights.
- Preserve the original alternative order and stable identifiers through every matrix operation.
- Recompute final scores from saved normalized values and weights.
- Test rank stability under reasonable weight and normalization perturbations.
- Report ties and near-ties instead of forcing false precision.
- For AHP, report the consistency ratio and reject matrices outside the declared threshold.
