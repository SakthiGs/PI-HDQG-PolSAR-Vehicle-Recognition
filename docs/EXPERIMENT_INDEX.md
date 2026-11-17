# Manuscript evidence inventory

This is an audit status index, **not** a claim that all manuscript results have already been reproduced or uploaded. Manuscript data and run series must be kept separate.

| Evidence block | Reported manuscript finding | Status |
|---|---|---|
| R1.1 retrospective CPU inference (separate checkpoint) | 42.89 ms/chip, 200 held-out chips, batch 1, five timing passes | **Raw evidence, summary and benchmark code uploaded; arithmetic verified** |
| Primary Full vs NoEnt | Ten paired evaluations; Full 81.02 ± 2.02% accuracy vs NoEnt 76.61 ± 2.68% | Pending raw-output reconciliation |
| Classical/hybrid reviewer controls | EdgeGATv2 83.14 ± 2.60%, EdgeConv 82.05 ± 3.70%, five-seed separate series | Pending raw-output reconciliation |
| NoGlobal control | 79.73 ± 2.96%, separate five-seed series | Pending raw-output reconciliation |
| LOAO unseen-angle tests | 25.61 ± 2.36%, 42.76 ± 3.54%, 48.97 ± 2.20% | Pending raw-output reconciliation |
| Graph/affinity variants | Seven five-seed configurations | Pending raw-output reconciliation |
| Physics-descriptor ablation | Multiple five-seed configurations | Pending raw-output reconciliation |
| Finite-shot/noise audit | 1,024 and 4,096 shots on selected held-out chips | Pending raw-output reconciliation |
| IBM physical-QPU evaluation | 20 held-out chips; 75% vs 80% simulator | Pending run-log reconciliation |

**Release rule:** Do not publish original PolSAR images or image-derived artifacts without verifying the original data provider's redistribution terms. Preserve seed, split, model, environment, hardware, and run-series provenance.
