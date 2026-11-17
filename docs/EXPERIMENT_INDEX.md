# Manuscript evidence inventory

A private audit ledger, **not** a claim that all paper experiments have already been reproduced. All series, seeds and checkpoint provenance must be preserved.

| Evidence block | Manuscript values | Current audit status |
|---|---|---|
| R1.1 Full forward latency (separate checkpoint) | 42.89 ms/chip CPU, 200 chips × 5 passes | **Raw timing, summary and add-on uploaded; independent arithmetic verified** |
| LOAO unseen-angle / Table 7 | 25.61 ± 2.36%, 42.76 ± 3.54%, 48.97 ± 2.20% | **Fifteen per-seed results and reviewer table uploaded; mean/SD independently matched** |
| Graph / affinity sensitivity / Table 10 | Seven five-seed variants, 76.82–78.86% | **Forty-run progress and mean/SD uploaded; seven variants independently matched. The eighth baseline is a separate series** |
| Primary Full vs NoEnt / Table 8 | Ten paired runs; Full 81.02 ± 2.02%, NoEnt 76.61 ± 2.68% | Pending archived outputs and paired validation |
| Classical/hybrid controls / Table 12 | EdgeGATv2 83.14 ± 2.60%, EdgeConv 82.05 ± 3.70% | Pending five-seed raw output and provenance |
| NoGlobal control | 79.73 ± 2.96%, separate five-seed series | Pending archived outputs and provenance |
| Physics-descriptor ablation | Five-seed descriptor variants | Pending archived outputs and provenance |
| Finite-shot/noise audit | 1,024 and 4,096 shots on selected test chips | Pending audit |
| IBM physical-QPU audit | 20-chip hardware 75% accuracy vs 80% exact simulation | Pending full QPU job output reconciliation; do not treat partial backend metadata as full result |

**Release rules:** No original PolSAR image files. Validate dataset rights, code secrets, model checkpoints, experimental series and per-run statistics before public release. 'Numbers independently matched' does not mean notebooks have been rerun in a clean environment.
