# PI-HDQG — PolSAR Vehicle Recognition

**Status: PRIVATE REPRODUCIBILITY WORKSPACE — NOT A PUBLIC RELEASE**

This repository is being assembled to support *Physics-Informed Hierarchical Dual-Quantum Graph Learning for PolSAR Vehicle Recognition* (IEEE Access), by S. P. Gunasekar and P. K. Rangarajan.

It is an evidence-tracked archive. **Only the R1.1 retrospective CPU/GPU inference-latency evidence is uploaded and independently checked so far**; other manuscript studies remain pending reconciliation. Results from separate execution series must not be treated as paired.

## Currently audited and uploaded

- [R1.1 benchmark summary and protocol](results/R1C1_forward_latency_200/README.md)
- [Raw 2,000 timing observations](results/R1C1_forward_latency_200/R1C1_forward_latency_raw.csv)
- [Original experiment summary](results/R1C1_forward_latency_200/R1C1_forward_latency_summary.json)
- [Benchmark Python add-on](scripts/PI_HDQG_R1C1_200_CPU_GPU_Benchmark_FIXED.py)
- [Benchmark Colab notebook add-on](notebooks/PI_HDQG_R1C1_200_CPU_GPU_Benchmark_FIXED_Addon.ipynb)

The manuscript's **42.89 ms/chip CPU median** is independently recalculated from this raw CSV. The benchmark uses a separate frozen Full checkpoint, not the primary Full/NoEnt series, and is forward-pass only. Running this add-on still requires the original graph-sensitivity model notebook, the archived checkpoint, and authorized PolSAR input data.

## Evidence still to reconcile

See [manuscript experiment index](docs/EXPERIMENT_INDEX.md) for primary Full/NoEnt, classical and hybrid controls, LOAO, graph/physics ablations, finite-shot noise and IBM physical-QPU audit. Unuploaded evidence has **not** been claimed reproduced.

## Data policy

The original Wang et al. PolSAR images and MATLAB datasets are **not stored here**. Dataset access and redistribution rights require independent verification. See [data access policy](docs/DATA_ACCESS.md) and [pre-publication checklist](docs/RELEASE_CHECKLIST.md).

## Status of public reproducibility

Do not cite this private repository as a completed public reproducibility release. The dataset provider's rights, full manuscript evidence, code hygiene, dependencies, reproduction instructions and license must be audited before the repository can be made public.
