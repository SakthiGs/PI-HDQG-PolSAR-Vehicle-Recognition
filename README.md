# PI-HDQG — PolSAR Vehicle Recognition

**PRIVATE REPRODUCIBILITY WORKSPACE — NOT A PUBLIC RELEASE**

This repository is being assembled for *Physics-Informed Hierarchical Dual-Quantum Graph Learning for PolSAR Vehicle Recognition* (IEEE Access), by S. P. Gunasekar and P. K. Rangarajan.

## Evidence reconciled against the manuscript

| Study | Evidence | Verification |
|---|---|---|
| R1.1 retrospective Full-model inference latency | [CSV, JSON and README](results/R1C1_forward_latency_200/README.md) plus [Python add-on](scripts/PI_HDQG_R1C1_200_CPU_GPU_Benchmark_FIXED.py) and [Colab add-on](notebooks/PI_HDQG_R1C1_200_CPU_GPU_Benchmark_FIXED_Addon.ipynb) | 200 chips × 5 passes per device; CPU median **42.89 ms/chip**, matching updated manuscript |
| LOAO unseen-angle generalization / Table 7 | [Per-seed data and audit](results/LOAO/README.md) | Five seeds per held-out angle; accuracy and Macro-F1 means/SDs independently recalculated and matched |
| Graph-size / affinity sensitivity / Table 10 | [Forty-run data and audit](results/GRAPH_SENSITIVITY/README.md) | Seven reported five-seed variant rows match; additional graph-sensitivity baseline kept separate from original Full reference |

**Not yet audited/uploaded:** primary paired Full–NoEnt ten-run results, classical/hybrid reviewer controls, NoGlobal, physics-descriptor ablations, finite-shot noise evaluation, and full IBM QPU outputs. See [complete inventory](docs/EXPERIMENT_INDEX.md).

**Important distinction:** Recalculating published metrics from the archived run records is **not** the same as successfully rerunning the experiment in a clean environment. Original training notebooks, full model sources, checkpoints, requirements and dataset-access workflow remain to be audited and incorporated.

## Dataset and availability

Original PolSAR image chips, MATLAB files and image-derived arrays are **not** included. Dataset provider rights must be confirmed before releasing any source images or derived data; see [data access notes](docs/DATA_ACCESS.md).

This private repository should **not** be cited as a completed public reproducibility package until code, dependencies, license, data-policy and full-manuscript evidence have been checked against the [release checklist](docs/RELEASE_CHECKLIST.md).
