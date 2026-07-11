#!/usr/bin/env python3
"""CERBERUS Vigil synthetic independence-decay experiment.

Reproducible reference experiment for CERBERUS v3.3.
It demonstrates three claims only:
  1. conditioning on an observed common stimulus suppresses benign correlation;
  2. a latent shared pathway produces rising residual dependence;
  3. a conservative upper bound can drive authority demotion before a chosen
     behavioral-symptom time.

This is an explanatory simulation, not flight validation.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class Config:
    n: int = 1800
    commissioning_end: int = 500
    coupling_onset: int = 700
    behavioral_symptom: int = 1300
    window: int = 120
    coupling_max: float = 1.4
    alpha_one_sided: float = 0.05
    consecutive_alarm_samples: int = 10
    calibration_runs: int = 100
    evaluation_runs: int = 200
    representative_seed: int = 20260711


def rolling_corr(a: np.ndarray, b: np.ndarray, window: int) -> np.ndarray:
    """Fast rolling Pearson correlation using cumulative sums."""
    n = len(a)
    out = np.full(n, np.nan)
    ca = np.concatenate(([0.0], np.cumsum(a)))
    cb = np.concatenate(([0.0], np.cumsum(b)))
    ca2 = np.concatenate(([0.0], np.cumsum(a * a)))
    cb2 = np.concatenate(([0.0], np.cumsum(b * b)))
    cab = np.concatenate(([0.0], np.cumsum(a * b)))
    for t in range(window - 1, n):
        s, e = t - window + 1, t + 1
        sa, sb = ca[e] - ca[s], cb[e] - cb[s]
        saa, sbb = ca2[e] - ca2[s], cb2[e] - cb2[s]
        sab = cab[e] - cab[s]
        cov = sab - sa * sb / window
        va = saa - sa * sa / window
        vb = sbb - sb * sb / window
        out[t] = cov / np.sqrt(max(va * vb, 1e-12))
    return out


def simulate(seed: int, cfg: Config, coupling: bool) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = cfg.n

    environment = np.zeros(n)
    latent_common = np.zeros(n)
    for t in range(1, n):
        environment[t] = 0.92 * environment[t - 1] + rng.normal(0.0, 0.35)
        latent_common[t] = 0.75 * latent_common[t - 1] + rng.normal(0.0, 0.50)
    environment += 0.70 * np.sin(np.arange(n) / 45.0)

    coupling_gain = np.zeros(n)
    if coupling:
        start, stop = cfg.coupling_onset, cfg.behavioral_symptom
        coupling_gain[start:stop] = np.linspace(0.0, cfg.coupling_max, stop - start)
        coupling_gain[stop:] = cfg.coupling_max

    y1 = 0.90 * environment + rng.normal(0.0, 0.75, n) + coupling_gain * latent_common
    y2 = -0.50 * environment + rng.normal(0.0, 0.75, n) + coupling_gain * latent_common

    c = cfg.commissioning_end
    X = np.column_stack((np.ones(c), environment[:c]))
    beta1 = np.linalg.lstsq(X, y1[:c], rcond=None)[0]
    beta2 = np.linalg.lstsq(X, y2[:c], rcond=None)[0]
    residual1 = y1 - (beta1[0] + beta1[1] * environment)
    residual2 = y2 - (beta2[0] + beta2[1] * environment)

    raw_corr = rolling_corr(y1, y2, cfg.window)
    residual_corr = rolling_corr(residual1, residual2, cfg.window)

    zcrit = 1.6448536269514722
    r_abs = np.clip(np.abs(residual_corr), 0.0, 0.999999)
    upper = np.tanh(np.arctanh(r_abs) + zcrit / np.sqrt(cfg.window - 3))

    return {
        "environment": environment,
        "latent_common": latent_common,
        "coupling_gain": coupling_gain,
        "channel_1": y1,
        "channel_2": y2,
        "raw_corr": raw_corr,
        "residual_corr": residual_corr,
        "upper_bound": upper,
    }


def first_sustained_crossing(values: np.ndarray, threshold: float, start: int, run: int) -> int | None:
    count = 0
    for t in range(start, len(values)):
        if np.isfinite(values[t]) and values[t] > threshold:
            count += 1
            if count >= run:
                return t - run + 1
        else:
            count = 0
    return None


def authority_level(upper_bound: float) -> str:
    if not np.isfinite(upper_bound):
        return "A3"
    if upper_bound >= 0.70:
        return "A0"
    if upper_bound >= 0.55:
        return "A1"
    if upper_bound >= 0.35:
        return "A2"
    return "A3"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    cfg = Config()

    nominal_maxima = []
    for seed in range(1000, 1000 + cfg.calibration_runs):
        d = simulate(seed, cfg, coupling=False)
        nominal_maxima.append(float(np.nanmax(d["upper_bound"][cfg.commissioning_end:])))
    alarm_threshold = float(np.percentile(nominal_maxima, 95))

    false_alarm_count = 0
    for seed in range(3000, 3000 + cfg.evaluation_runs):
        d = simulate(seed, cfg, coupling=False)
        hit = first_sustained_crossing(
            d["upper_bound"], alarm_threshold, cfg.commissioning_end,
            cfg.consecutive_alarm_samples,
        )
        false_alarm_count += hit is not None

    detections: list[int] = []
    for seed in range(5000, 5000 + cfg.evaluation_runs):
        d = simulate(seed, cfg, coupling=True)
        hit = first_sustained_crossing(
            d["upper_bound"], alarm_threshold, cfg.coupling_onset,
            cfg.consecutive_alarm_samples,
        )
        if hit is not None:
            detections.append(hit)

    leads = [cfg.behavioral_symptom - d for d in detections]
    rep = simulate(cfg.representative_seed, cfg, coupling=True)
    rep_detection = first_sustained_crossing(
        rep["upper_bound"], alarm_threshold, cfg.coupling_onset,
        cfg.consecutive_alarm_samples,
    )

    levels = [authority_level(x) for x in rep["upper_bound"]]
    level_num = {"A3": 3, "A2": 2, "A1": 1, "A0": 0}

    summary = {
        "experiment": "Vigil synthetic independence-decay experiment",
        "status": "implemented explanatory prototype; not flight validation",
        "config": asdict(cfg),
        "calibrated_alarm_threshold_upper_bound": alarm_threshold,
        "nominal_false_alarm_runs": false_alarm_count,
        "nominal_evaluation_runs": cfg.evaluation_runs,
        "nominal_run_false_alarm_rate": false_alarm_count / cfg.evaluation_runs,
        "coupling_detection_runs": len(detections),
        "coupling_evaluation_runs": cfg.evaluation_runs,
        "coupling_detection_rate": len(detections) / cfg.evaluation_runs,
        "median_detection_sample": float(np.median(detections)),
        "median_detection_lead_samples": float(np.median(leads)),
        "lead_samples_p10": float(np.percentile(leads, 10)),
        "lead_samples_p90": float(np.percentile(leads, 90)),
        "representative_detection_sample": rep_detection,
        "representative_first_A2": next((i for i, x in enumerate(levels) if x == "A2"), None),
        "representative_first_A1": next((i for i, x in enumerate(levels) if x == "A1"), None),
        "representative_first_A0": next((i for i, x in enumerate(levels) if x == "A0"), None),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (out / "representative_trace.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sample", "environment", "coupling_gain", "channel_1", "channel_2",
            "raw_corr", "conditioned_residual_corr", "upper_bound_abs_corr",
            "alarm_threshold", "authority_level",
        ])
        for i in range(cfg.n):
            writer.writerow([
                i, rep["environment"][i], rep["coupling_gain"][i],
                rep["channel_1"][i], rep["channel_2"][i], rep["raw_corr"][i],
                rep["residual_corr"][i], rep["upper_bound"][i], alarm_threshold,
                levels[i],
            ])

    with (out / "monte_carlo_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in summary.items():
            if key != "config":
                writer.writerow([key, value])

    x = np.arange(cfg.n)
    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
    axes[0].plot(x, rep["raw_corr"], label="Raw channel correlation")
    axes[0].plot(x, rep["residual_corr"], label="Conditioned residual correlation")
    axes[0].axvline(cfg.coupling_onset, linestyle="--", label="Hidden coupling begins")
    axes[0].set_ylabel("Rolling correlation")
    axes[0].legend(loc="upper left")
    axes[0].grid(alpha=0.25)

    axes[1].plot(x, rep["upper_bound"], label="95% upper bound on |residual r|")
    axes[1].axhline(alarm_threshold, linestyle="--", label="Calibrated alarm threshold")
    axes[1].axvline(cfg.behavioral_symptom, linestyle=":", label="Behavioral symptom time")
    if rep_detection is not None:
        axes[1].axvline(rep_detection, linestyle="-.", label="Vigil detection")
    axes[1].set_ylabel("Conservative overlap proxy")
    axes[1].legend(loc="upper left")
    axes[1].grid(alpha=0.25)

    axes[2].step(x, [level_num[v] for v in levels], where="post")
    axes[2].set_yticks([0, 1, 2, 3], ["A0", "A1", "A2", "A3"])
    axes[2].set_ylabel("Authority")
    axes[2].set_xlabel("Sample")
    axes[2].grid(alpha=0.25)

    fig.suptitle("CERBERUS Vigil: Synthetic Independence Decay")
    fig.tight_layout()
    fig.savefig(out / "vigil_independence_decay.png", dpi=180)
    plt.close(fig)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
