# Leave-one-angle-out (LOAO) evidence — manuscript Table 7

The `LOAO_SEED_RESULTS.csv` contains 15 completed seed results (5 seeds for each held-out angle) and split SHA-256 identifiers. We independently computed means and sample standard deviations from these rows and confirmed agreement with `LOAO_REVIEWER_TABLE.csv` and the manuscript.

| Held-out angle | Accuracy, mean ± sample SD | Macro-F1, mean ± sample SD | n |
|---|---|---|---|
| 25° | 25.61 ± 2.36% | 19.70 ± 2.55% | 5 |
| 30° | 42.76 ± 3.54% | 38.83 ± 3.70% | 5 |
| 45° | 48.97 ± 2.20% | 47.66 ± 2.40% | 5 |

**Scope:** Separate LOAO evaluations trained/validated on two angles and tested on the held-out third. Do not conflate with mixed-angle accuracy or claim cross-angle invariance.

## SHA-256 of original Drive exports

- `LOAO_REVIEWER_TABLE.csv`: `089dc865489a9828bd3d79661a84e3d81b32c6ba2a82b7aac426e9104d5f99d8`
- `LOAO_SEED_RESULTS.csv`: `92c5e2630b3086982722e66f5e932e019d6d13dc6fd56f70f662879eab77ece8`

Original notebook and split reconstruction code have **not** yet been imported or independently re-executed here. Numbers are independently reconciled against the archived seed-level outputs.
