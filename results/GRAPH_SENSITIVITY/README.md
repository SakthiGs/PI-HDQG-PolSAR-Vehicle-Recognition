# Graph topology and edge-affinity sensitivity — manuscript Table 10

`RESULTS_PROGRESS.csv` contains **40 completed runs** (5 seeds each for 8 configurations), with source model/config/split hashes. `RESULTS_MEAN_SD.csv` contains their aggregate statistics. Independent regrouping by configuration and calculation of the sample standard deviation reproduces these aggregate values.

The following **seven variants**, and only these seven, correspond to the manuscript's seven-variant sensitivity table:

| Configuration | Accuracy mean ± sample SD |
|---|---|
| N=12, K=2 | 77.55 ± 3.86% |
| N=12, K=4 | 76.82 ± 3.58% |
| N=12, K=5 | 77.14 ± 0.99% |
| N=8, K=3 | 77.50 ± 3.25% |
| N=16, K=3 | 78.86 ± 2.17% |
| Spatial-affinity-only | 77.64 ± 3.38% |
| Polarimetric/phase-affinity-only | 77.55 ± 2.22% |

**Critical provenance:** The archived `graph_N12_K3_BASE` line is a separate five-seed graph-sensitivity run with accuracy 77.05 ± 3.80%, **NOT** the original five-run Full reference reported as 81.00 ± 0.67% in the manuscript's Table 10. It must not be substituted for the original reference or included in paired inferences against that reference. The graph archive contains one additional baseline run-series entry, which is why the raw files cover eight configurations but the manuscript comparison reports seven variants.

## SHA-256 of original Drive exports

- `RESULTS_MEAN_SD.csv`: `f1852622c6948ee7eca4ab0408ef31f33b0c3f174d4528804e7170b38de8647e`
- `RESULTS_PROGRESS.csv`: `e942a952118fd641299d5602c20995330061d9d689522c645441598d4633a724`

Original training code and matched external data have not yet been independently re-executed or fully imported. This is a metric provenance verification.
