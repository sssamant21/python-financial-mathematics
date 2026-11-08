# Project 06 validation evidence — 2026-11-08

Prepared source tested locally before GitHub publication. No CI result or independent acceptance claimed.

- `python -m pytest -q` in Project 06 folder: **7 passed in 0.96s**.
- `python tail_risk.py --bootstrap 100 --output /mnt/data/quant06/reports`: completed; 208 out-of-sample synthetic weeks.
- Synthetic historical VaR breaches: 18/208 = 8.6538%; exact binomial p = 0.024100.
- Synthetic normal VaR breaches: 12/208 = 5.7692%; exact binomial p = 0.630903.
- Tests: reproducibility, chronological training cutoff, future perturbation invariance, known VaR/CVaR, breach-summary bounds, invalid inputs, insufficient history.
- Local environment: NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, pytest 9.0.2.

**Scope:** synthetic data only. Binomial diagnostic independence is unverified; no real market data, 2020/2022 empirical validation, point-in-time vendor audit, or production certification.

## Dependent-return extension — 2026-11-08

A local prototype of fixed-length circular moving-block bootstrap and first-order Markov coverage diagnostics passed **7/7 pytest tests** after correcting an initially over-specific test fixture (the first run had 6 passes, 1 assertion failure because both fixture scenarios breached VaR). Tests cover block continuity, block=1 equivalence to iid resampling, deterministic bootstrap intervals, transition counts, degenerate all-zero breach series, no look-ahead, and input rejection. The published extension is a compact refactoring of that prototype, **not the exact tested source**; its exact-revision CI and independent numerical review remain pending. The diagnostic p-values are asymptotic and should not be used as compliance acceptance. No licensed 2020/2022 data was downloaded or redistributed.
