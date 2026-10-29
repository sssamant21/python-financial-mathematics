# Chapter 16 — Per-candidate calibration acceptance follow-up

**Date:** 2026-10-29
**Scope:** Section 16.9 portion of COV-74.
**Status:** Candidate metric/report gap addressed and selected rejection cases checked; independent review pending.

## Confirmed gap and correction

Previously, all six iterative rates/statuses/gradients were checked, but raw training and holdout metrics were evaluated only at the analytical benchmark. Each iterative result now carries training and holdout residuals, MAE/RMSE/bias/maximum absolute error, recomputed normalized loss/gradient and its own provisional decision. Overall acceptance requires all candidate decisions plus the retained analytical benchmark checks.

The manuscript explicitly distinguishes the top-level benchmark metrics from each candidate's metrics. The fit still uses TRAIN only. Holdout evaluation occurs after fitting and is not used to select the fitted rate.

## Independent reference and rejection evidence

For each candidate rate, the checker forms price residuals using Fraction arithmetic from the reported decimal rate and observations, independently of the engine's pricing/metric helpers. It checks all five metrics for training and holdout. The closed-form objective and gradient references are 7(r-0.05)^2 and 14(r-0.05).

Selected failed cases cover unsuccessful termination at the exact reference rate, an incorrect rate despite successful status, a false reported gradient, small rate offsets with misleading zero gradients, a changed holdout observation, and a real one-iteration budget run. The changed holdout leaves the fitted/analytical rate unchanged but fails acceptance. Invalid metric observations include empty data, zero time, nonfinite prices, boolean times and malformed rows.

These cases are not a complete boundary enumeration for every acceptance threshold. Production calibration acceptance, arbitrary datasets, scale/range extremes and general optimizer claims remain outside this fixed synthetic example.

## Runtime and publication

Baseline tree: `fb5f6814e8b6da8307d5608bbf65d36af0bda475`. All 20 Chapter 16 Python files were fetched at that revision; the local snapshot replaced only the project and checker. Python 3.12.14/Linux: 20/20 sources compiled and 10/10 check scripts exited zero, with assertions enabled, their code directory as working directory and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_16_09.py](../chapter-16/code/section_16_09.py) | `df881ee0655e18272577c28ea9b68221e3145819` | `8252a7eabe8c6010aa280c175a745ee109019029` |
| [check_section_16_09.py](../chapter-16/code/check_section_16_09.py) | `d61b3d244ee175b98f79d0ec487c26a525411d59` | `434ec323f799ab51c511918e7237feb43aec206d` |
| [16.09-chapter-project-deterministic-calibration-optimizer.md](../chapter-16/16.09-chapter-project-deterministic-calibration-optimizer.md) | `b2fa15f2c8cd40a7dd1af6880480caca3fe79a9a` | `ae1fefa2dfb827e8258d3d9a354aceb15e104796` |

This scoped change follows the latest full-book refresh; that run remains tied to its recorded source. COV-74 is partially remediated, with broader invalid-data, optimizer/threshold and independent-review obligations still open.

[Chapter 16 map](coverage-chapter-16.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
