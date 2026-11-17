# R1.1 retrospective Full-model forward-pass benchmark (200 chips)

## Verified manuscript-relevant result

The separately executed `V3IQ2_Full / graph_N12_K3_BASE / seed 0` frozen-checkpoint forward-only benchmark reports **42.8909155 ms/chip median CPU latency**, rounded to **42.89 ms/chip** in the manuscript. The Tesla T4 GPU median was **76.888773 ms/chip**; retained here as supplemental evidence and not used for a quantum or hardware-speedup claim.

- Selection: 200 held-out samples, twenty per class among ten vehicle classes.
- CPU and GPU each: 5 timing passes; 1,000 forward-call timings per device; 10 warm-ups.
- Batch size 1, CPU threads 2, PyTorch 2.14.1+cu130, Tesla T4 CUDA 13.0.
- Median CPU 42.8909155 ms; mean 43.540244687 ms.
- Median GPU 76.888773 ms; mean 77.937454092 ms.
- 100% CPU/GPU prediction agreement on 200 selected examples.
- Training was **not** performed. The checkpoint was not modified.
- The benchmark excludes preprocessing, graph extraction, dataset I/O, device transfer, backward pass, optimizer updates, and QPU jobs.

## Provenance and boundaries

This frozen checkpoint belongs to a **separate graph-sensitivity series**, NOT the manuscript's primary ten-run Full accuracy series. The recorded checkpoint test accuracy of 79.318% must not be substituted for the manuscript's primary results. The timing data are not directly comparable to archived classical-control latencies due to different evaluation provenance and unverified hardware/environment equivalence.

The raw CSV and JSON summary were independently cross-checked: **2,000 rows total**, 1,000 per device, and the CSV medians reproduce the JSON values.

Source notebook used in the original execution environment: `SQG_V3IQ2_GRAPH_SENSITIVITY_5SEED_AUTORESUME_CPU_READY.ipynb`. The included add-on is **not standalone**; rerunning it requires the original model/data definitions and an authorized copy of the dataset. The source notebook and checkpoint have **not yet been audited/imported here**.

## File integrity (SHA-256 on archived local copies)

- `R1C1_forward_latency_raw.csv`: `567051b5e86cf21d1f0ff160d89764ee1ad58ea79c4e25a285499deba4b7f705`
- `R1C1_forward_latency_summary.json`: `8e56da19b4606cb6248da6d5331378aba738caeccdddc103630471fc992c5cc5`
- `PI_HDQG_R1C1_200_CPU_GPU_Benchmark_FIXED.py`: `1c955d32b8957377838ee247cd10fcc9e6191eeca28236313d7a513d58d9a9da`
- `PI_HDQG_R1C1_200_CPU_GPU_Benchmark_FIXED_Addon.ipynb`: `03698284478d2529a0a43dd234b52b5cd7ab6ef2580fdffc306d7f26ba811372`

**Publication status:** evidence uploaded to a PRIVATE working repository; this alone does not constitute complete reproduction of the full paper.
