"""PI-HDQG R1.1 RETROSPECTIVE FORWARD-PASS LATENCY BENCHMARK — 200 CHIPS.

Run in the LIVE KERNEL of the original
SQG_V3IQ2_GRAPH_SENSITIVITY_5SEED_AUTORESUME_CPU_READY.ipynb
AFTER running setup / class / dataset definitions, BEFORE the seed-training loop.
No training, no optimizer, no checkpoint writes.

Notebook usage:
    %run -i /content/PI_HDQG_R1C1_200_CPU_GPU_Benchmark.py
(or paste this file as a new final cell in the original notebook)

Target: graph-sensitivity N12_K3_BASE Full model, seed=0 (a separate
historical series, NOT the primary ten-run seed-0 manuscript result).
"""

from pathlib import Path
import csv
import datetime as _dt
import hashlib
import json
import os
import platform
import statistics
import time
import traceback

import numpy as np
import torch

# This experiment intentionally REQUIRES CUDA. Do not silently repeat CPU-only
# if Colab assigned a CPU backend or a CPU-only PyTorch distribution.
if not torch.cuda.is_available():
    raise RuntimeError(
        "R1.1 GPU timing was requested but CUDA is unavailable. "
        f"torch={torch.__version__}; torch.version.cuda={torch.version.cuda}. "
        "Select a GPU runtime in Colab and restart the session; "
        "if the Python environment has CPU-only PyTorch, use Colab's "
        "GPU-compatible PyTorch installation before rerunning. "
        "No timing output was written."
    )
print("R1.1 CUDA runtime confirmed:", torch.cuda.get_device_name(0))
print("PyTorch:", torch.__version__, "CUDA:", torch.version.cuda)

# ----- Researcher-controlled benchmark protocol -----
SEED = 0
N_SAMPLES = 200         # Select 20 deterministic held-out samples per class
WARMUP = 10            # Untimed forward passes per device
REPEATS = 5            # Repeated timing passes over the same 200 samples
CPU_THREADS_BENCH = 2
TARGET_MODEL = "V3IQ2_Full"
TARGET_COMPARISON = "graph_N12_K3_BASE"
EXPECTED_PARAMS = 23033
EXPECTED_MODEL_SHA = "cd91487c120141fa80c825d42f7c82f8807fa9070191d0237298db0dae97034a"

# Original notebook symbols. This script deliberately refuses to reconstruct
# architecture or features from guessed settings.
_required = (
    "CFG", "CLASSES", "OUT", "manifest", "GRAPH_VARIANT",
    "PhysicsEntangledSQGV3IQ2Global", "loaders_for_seed", "split_csv",
)
missing = [s for s in _required if s not in globals()]
if missing:
    raise RuntimeError(
        "Run the graph-sensitivity notebook setup + model/data-definition "
        "cells (Sections 0-14), but DO NOT run its five-seed training cell. "
        f"Missing notebook symbols: {missing}"
    )
if GRAPH_VARIANT != "N12_K3_BASE" or int(CFG["n_nodes"]) != 12 or int(CFG["n_neighbors"]) != 3:
    raise RuntimeError("Expected GRAPH_VARIANT=N12_K3_BASE with N=12, K=3; refusing mismatched model")

# Path inferred from original notebook's explicitly defined OUT, model,
# comparison and seed subfolder. Do not use the older original seed0 folder.
run_dir = Path(OUT) / TARGET_MODEL / TARGET_COMPARISON / f"seed{SEED}"
checkpoint = run_dir / "best_model.pt"
scalers_path = run_dir / "standardizers.npz"
result_path = run_dir / "result.json"
split_path = run_dir / "split.csv"
for path in (checkpoint, scalers_path, result_path, split_path):
    if not path.is_file():
        raise FileNotFoundError(f"Missing archived Full graph-sensitivity artifact: {path}")

result = json.loads(result_path.read_text(encoding="utf-8"))
if (result.get("model") != TARGET_MODEL or result.get("comparison") != TARGET_COMPARISON
        or int(result.get("seed", -1)) != SEED
        or int(result.get("parameter_count", -1)) != EXPECTED_PARAMS):
    raise AssertionError("Result metadata does not describe the chosen Full reference")
if result.get("model_sha256") != EXPECTED_MODEL_SHA:
    raise AssertionError("Source-model provenance differs from the expected graph-sensitivity code")
if "MODEL_SHA" in globals() and MODEL_SHA != EXPECTED_MODEL_SHA:
    raise AssertionError("Current notebook model source hash differs from the archived graph checkpoint")

# Only use original protocol's split function / cached standardized loader.
# loaders_for_seed computes standardization from the saved TRAIN split;
# compare computed normalizers against the archived values before timing.
loaded = loaders_for_seed(SEED)
tr, va, tests, train_dl, val_dl, test_dls, labels, angles, ns, es, gs, ps = loaded
if "combined" not in test_dls:
    raise AssertionError("Missing combined mixed-angle held-out loader")
if N_SAMPLES != 200 or len(CLASSES) != 10 or N_SAMPLES % len(CLASSES):
    raise AssertionError("200-sample benchmark requires exactly 10 classes")

expected_split_sha = result.get("split_sha256")
computed_split_sha = hashlib.sha256(split_csv(tr, va, tests).encode("utf-8")).hexdigest()
on_disk_split_sha = hashlib.sha256(split_path.read_bytes()).hexdigest()
if not (expected_split_sha == computed_split_sha == on_disk_split_sha):
    raise AssertionError("Split hashes do not match the archived graph-sensitivity seed-0 run")

with np.load(scalers_path, allow_pickle=False) as archive:
    for attr, standardizer, key in (
        ("mu", ns, "node_mu"), ("sd", ns, "node_sd"),
        ("mu", es, "edge_mu"), ("sd", es, "edge_sd"),
        ("mu", gs, "global_mu"), ("sd", gs, "global_sd"),
        ("mu", ps, "patch_mu"), ("sd", ps, "patch_sd"),
    ):
        got = np.asarray(getattr(standardizer, attr))
        saved = np.asarray(archive[key])
        if got.shape != saved.shape or not np.allclose(got, saved, rtol=1e-5, atol=1e-6):
            raise AssertionError(f"Preprocessing mismatch against archived {key}")

# Dataset positions correspond to tests['combined'] via the original loader.
heldout_indices = np.asarray(tests["combined"], dtype=int)
heldout_labels = np.asarray(labels, dtype=int)[heldout_indices]
positions = []
for c in range(len(CLASSES)):
    pos = np.flatnonzero(heldout_labels == c)
    if len(pos) < (N_SAMPLES // len(CLASSES)):
        raise AssertionError(f"Not enough held-out samples from class {c}")
    positions.extend(int(i) for i in pos[: N_SAMPLES // len(CLASSES)])
if len(positions) != N_SAMPLES:
    raise AssertionError("Expected exactly 200 selected samples")

dataset = test_dls["combined"].dataset
# Materialize preprocessed inputs OUTSIDE measured region.
raw_items = [dataset[pos] for pos in positions]
prepared = []
true_labels = []
observed_item_lengths = set()
for pos, item in zip(positions, raw_items):
    # The archived V3IQGlobalGraphDataset.__getitem__ returns 13 fields:
    #   [0:11] model inputs, [11] incidence angle in degrees (metadata),
    #   [12] class label. The training notebook's _batch_args uses batch[:11]
    #   as model inputs and batch[-1] as label. Some dataset variants omit
    #   field [11] and return 12 fields. Neither should pass angle metadata
    #   into PhysicsEntangledSQGV3IQ2Global.forward().
    if not isinstance(item, (tuple, list)) or len(item) not in (12, 13):
        raise AssertionError(
            "Expected 11 model tensors plus class label, optionally followed "
            "by incidence-angle metadata before the label; "
            f"dataset returned type={type(item).__name__}, "
            f"length={len(item) if isinstance(item, (tuple, list)) else 'N/A'}"
        )
    observed_item_lengths.add(len(item))
    if len(item) == 13:
        got_angle = int(item[11].item())
        expected_angle = int(np.asarray(angles)[heldout_indices[pos]])
        if got_angle != expected_angle:
            raise AssertionError(
                f"Incidence-angle metadata mismatch at test position {pos}: "
                f"{got_angle} vs {expected_angle}"
            )
    got_label = int(item[-1].item())
    expected_label = int(heldout_labels[pos])
    if got_label != expected_label:
        raise AssertionError(
            f"Class-label mismatch at test position {pos}: "
            f"{got_label} vs {expected_label}"
        )
    xs = tuple(t.unsqueeze(0).contiguous() for t in item[:11])
    for t in xs:
        if t.is_floating_point() and not torch.isfinite(t).all():
            raise ValueError("Found non-finite preprocessed input")
    prepared.append(xs)
    true_labels.append(got_label)
if observed_item_lengths != {13}:
    print("R1.1 dataset item lengths observed:", sorted(observed_item_lengths),
          "(archived source notebook returns 13)")

state = torch.load(checkpoint, map_location="cpu", weights_only=True)
if not isinstance(state, dict) or not all(isinstance(v, torch.Tensor) for v in state.values()):
    raise RuntimeError("Expected an archived state_dict of tensors")

# Original notebook class + original config, not a surrogate network.
def load_frozen_model(device):
    m = PhysicsEntangledSQGV3IQ2Global(
        CFG["node_dim"], CFG["patch_channels"], CFG["edge_dim"], len(CLASSES), CFG
    )
    found_params = sum(p.numel() for p in m.parameters() if p.requires_grad)
    if found_params != EXPECTED_PARAMS:
        raise AssertionError(f"Model parameter count mismatch: {found_params}")
    m.load_state_dict(state, strict=True)
    m = m.to(device)
    m.eval()
    return m


def summarize(times_by_repeat):
    arr = np.asarray(times_by_repeat, dtype=np.float64)
    if arr.shape != (REPEATS, N_SAMPLES):
        raise AssertionError(f"Unexpected timings matrix shape {arr.shape}")
    sample_medians = np.median(arr, axis=0)
    return {
        "median_ms_all_calls": float(np.median(arr)),
        "mean_ms_all_calls": float(arr.mean()),
        "sample_median_ms": float(np.median(sample_medians)),
        "sample_mean_of_medians_ms": float(sample_medians.mean()),
        "sample_p05_of_medians_ms": float(np.percentile(sample_medians, 5)),
        "sample_p95_of_medians_ms": float(np.percentile(sample_medians, 95)),
        "sample_min_median_ms": float(sample_medians.min()),
        "sample_max_median_ms": float(sample_medians.max()),
        "repeat_pass_median_ms": [float(np.median(row)) for row in arr],
    }


def measure(device):
    torch.set_num_threads(CPU_THREADS_BENCH)
    m = load_frozen_model(device)
    on_device = [tuple(v.to(device, non_blocking=False) for v in item) for item in prepared]

    def sync():
        if device.type == "cuda":
            torch.cuda.synchronize(device)

    # Confirm no model parameter values change while benchmarking.
    before = [p.detach().cpu().clone() for p in m.parameters()]
    times = []
    first_predictions = []
    with torch.no_grad():
        for j in range(WARMUP):
            _ = m(*on_device[j % N_SAMPLES])
            sync()
        for rep in range(REPEATS):
            row = []
            for ix, args in enumerate(on_device):
                sync()
                t0 = time.perf_counter_ns()
                logits = m(*args)
                sync()
                dt_ms = (time.perf_counter_ns() - t0) / 1e6
                if logits.shape != (1, len(CLASSES)) or not torch.isfinite(logits).all():
                    raise AssertionError("Model produced invalid logits")
                if rep == 0:
                    first_predictions.append(int(logits.argmax(dim=-1).item()))
                row.append(dt_ms)
            times.append(row)
    for p, old in zip(m.parameters(), before):
        if not torch.equal(p.detach().cpu(), old):
            raise AssertionError("Model parameter changed during inference-only benchmark")
    del m
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return {
        "device": str(device),
        "summary": summarize(times),
        "timings_ms": times,
        "predictions": first_predictions,
    }

results = {}
device_errors = {}
for device_name in (["cpu", "cuda:0"] if torch.cuda.is_available() else ["cpu"]):
    dev = torch.device(device_name)
    print(f"R1.1: benchmarking Full model on {dev} (no training)...")
    try:
        results[device_name] = measure(dev)
        print(f"  median: {results[device_name]['summary']['median_ms_all_calls']:.3f} ms/chip")
    except Exception as exc:
        if device_name == "cpu":
            raise  # A CPU failure invalidates this benchmark.
        device_errors[device_name] = repr(exc)
        print(f"  GPU measurement FAILED (not reported): {exc!r}")
if not torch.cuda.is_available():
    print("GPU unavailable in this runtime; GPU timing NOT measured.")

if "cuda:0" not in results:
    raise RuntimeError(
        "GPU forward timing failed; see CUDA error above. "
        "No benchmark results were written; CPU-only archive is preserved."
    )

checkpoint_sha = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
output_dir = Path(OUT) / "R1C1_FORWARD_LATENCY_200_CPU_GPU"
output_dir.mkdir(parents=True, exist_ok=True)
if (output_dir / "R1C1_forward_latency_summary.json").exists() or (output_dir / "R1C1_forward_latency_raw.csv").exists():
    output_dir = Path(OUT) / ("R1C1_FORWARD_LATENCY_200_CPU_GPU_" + _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output_dir.mkdir(parents=True, exist_ok=False)

metadata = {
    "status": "retrospective inference-only benchmark (200 held-out chips); not a manuscript-primary 10-seed result",
    "date_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    "original_notebook": "SQG_V3IQ2_GRAPH_SENSITIVITY_5SEED_AUTORESUME_CPU_READY.ipynb",
    "model": TARGET_MODEL,
    "comparison": TARGET_COMPARISON,
    "seed": SEED,
    "checkpoint": str(checkpoint),
    "checkpoint_sha256": checkpoint_sha,
    "model_code_sha256": EXPECTED_MODEL_SHA,
    "split_sha256": expected_split_sha,
    "trainable_parameter_count": EXPECTED_PARAMS,
    "archived_seed0_accuracy": result.get("test_combined_accuracy"),
    "source_test_chips": int(len(heldout_indices)),
    "sample_selection": "first twenty per class in source test-set order",
    "dataset_item_lengths": sorted(observed_item_lengths),
    "input_mapping": "first 11 tensors to model; optional angle metadata at index 11 ignored; label from last position",
    "test_label_consistency_checked": True,
    "selected_original_indices": [int(heldout_indices[p]) for p in positions],
    "selected_class_indices": [int(v) for v in true_labels],
    "selected_class_names": [CLASSES[v] for v in true_labels],
    "n_samples": N_SAMPLES,
    "timed_forward_passes_per_device": N_SAMPLES * REPEATS,
    "warmup_calls": WARMUP,
    "repeats": REPEATS,
    "batch_size": 1,
    "counted_forward": "model(*11_already_preprocessed_tensors); no file I/O, graph extraction, normalization, batch transfer, optimizer, backward or QPU",
    "gpu_synchronization": True,
    "torch_version": torch.__version__,
    "python_version": platform.python_version(),
    "cpu_threads": CPU_THREADS_BENCH,
    "cpu": platform.processor(),
    "cuda_available": bool(torch.cuda.is_available()),
    "cuda_device_name": (torch.cuda.get_device_name(0) if torch.cuda.is_available() else None),
    "results": {k: {"device": v["device"], **v["summary"]} for k, v in results.items()},
    "device_errors": device_errors,
}
if "cuda:0" in results:
    metadata["cpu_gpu_prediction_agreement_fraction"] = float(np.mean(
        np.asarray(results["cpu"]["predictions"]) == np.asarray(results["cuda:0"]["predictions"])
    ))

with (output_dir / "R1C1_forward_latency_summary.json").open("w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)
with (output_dir / "R1C1_forward_latency_raw.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["device", "pass", "sample_position", "original_test_index", "class_name", "elapsed_ms"])
    for device_name, d in results.items():
        for rep_i, row in enumerate(d["timings_ms"], 1):
            for sample_i, milliseconds in enumerate(row):
                writer.writerow([device_name, rep_i, sample_i,
                    int(heldout_indices[positions[sample_i]]), CLASSES[true_labels[sample_i]],
                    f"{milliseconds:.9f}"])

print("\n=== R1.1 RETROSPECTIVE FORWARD-ONLY BENCHMARK ===")
print("Source:", TARGET_MODEL, TARGET_COMPARISON, "seed", SEED)
print("Archival test accuracy (different series from manuscript main run):", result.get("test_combined_accuracy"))
for d, v in results.items():
    stats = v["summary"]
    print(f"{d}: median {stats['median_ms_all_calls']:.3f} ms/chip; "
          f"mean {stats['mean_ms_all_calls']:.3f} ms/chip; "
          f"sample-median p05-p95 {stats['sample_p05_of_medians_ms']:.3f} - "
          f"{stats['sample_p95_of_medians_ms']:.3f} ms")
print("Saved:", output_dir)
print("No training performed; checkpoint left unchanged.")
