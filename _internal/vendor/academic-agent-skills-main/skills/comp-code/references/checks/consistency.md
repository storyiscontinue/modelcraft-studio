# Model-Code Consistency

## Contract table

Create a compact mapping before coding:

| Mathematical item | Code object | Shape | Unit | Validation |
| --- | --- | --- | --- | --- |
| set/index | list or integer range | expected cardinality | none | exact membership |
| parameter | scalar/array | declared dimensions | declared unit | finite/range check |
| variable | solver slice | declared dimensions | declared unit | bounds/integrality |
| constraint | matrix/function | one row per indexed rule | compatible | residual/slack |
| objective | scalar expression | scalar | one common unit | independent recomputation |

## Required checks

- Assert every parameter shape before creating solver matrices.
- Preserve one documented flattening order and test its inverse mapping.
- Verify objective coefficients and constraint rows against at least one hand-calculated entry.
- Keep baseline inputs immutable; scenario functions receive explicit copies.
- Recompute all reported metrics from final variables, not cached intermediate values.
- Include a data fingerprint or exact parameter echo in `all_results.json`.

## Result linkage

Every number in `RESULTS.md` must be traceable to a stable JSON key. Figures must read
the JSON/CSV output rather than contain manually retyped result arrays. The paper should
cite the same keys or tables, with display rounding applied only at presentation time.
