# Quant Projects — Progress Tracker

| Project | Stage | Acceptance |
|---|---|---|
| 01 — Single-stock Monte Carlo | Source + initial checks published | Local numerical test review required |
| 02 — Two-stock Monte Carlo and correlation | Previously built source published | Re-run and inspect plots locally |
| 03 — Five-stock portfolio optimization | Previously tested source and checks published | Tests pass in prior local context; verify after GitHub publication |
| 04 — Historical portfolio backtesting | Code, validation, downloadable-data workflow published | Synthetic-fixture tests; live provider refresh and point-in-time market-data review outstanding |

| 05 — Regime stress and parameter stability | Synthetic-first source, tests, and documentation published | Prototype 7/7 local tests passed; follow-up risk-calibration module 6/6 local tests passed; exact GitHub revision CI and independent review pending |

| 06 — Tail risk and bootstrap uncertainty | Synthetic-first source, tests, docs and runnable CLI published | 7/7 local tests on prepared source; exact-revision CI and independent review pending |

| 07 — Multi-horizon portfolio risk | Synthetic-first implementation, documentation, and tests published | Local prototype 12/12 tests passed; published revision CI and independent review pending |

Next: verify exact published Project 05 revision in CI, assess non-overlapping calibration and licensed 2020/2022 data provenance. Project 06 block bootstrap and conditional coverage extension authored; local prototype 7/7 tests passed, exact published revision CI pending. Project 07 extension: circular moving-block horizon bootstrap helper and 10 local deterministic tests added; exact published-revision CI and integration into forecast CSV remain pending. Point-in-time provenance checklist documented. Next: integrate bootstrap forecasts with walk-forward scoring and test exact published revision, then Project 08.

Do **not** label production-certified; this is an educational research series. No live trading or broker integration.

### Project 07 integrated bootstrap checkpoint (2026-11-08)

Published `bootstrap_walkforward.py` and `test_bootstrap_walkforward.py`: non-overlapping walk-forward horizons, origin-specific seeded circular-block draws, historical/normal baseline alignment, bootstrap VaR/CVaR and realized breach flags. Added documentation and reproducible CLI. **Integration tests authored but not executed in this run; exact-revision CI remains unverified.** Next: run the full Project 07 test suite on the published SHA, review CI and fix failures; then begin Project 08 if green.

### Project 07 exact-revision CI coverage checkpoint (2026-11-08)

GitHub Actions run [42533470625](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42533470625) passed on commit `2e211d5f6b7c0d1875a7f84000083ddaca425554`, but its workflow executed only `test_multi_horizon.py` for Project 07; it **did not execute** `test_dependent_bootstrap.py` or `test_bootstrap_walkforward.py`. The workflow is now extended to run both missing suites on pushes to `quant-projects/`. Treat these new checks as **pending until the workflow run for this commit finishes successfully**; neither the earlier green run nor previously reported local prototype passes certify the integrated bootstrap revision. Next: inspect exact SHA's workflow jobs and address failures before advancing to Project 08 (portfolio risk attribution/component VaR).

### Project 08 initial publication (2026-11-08)

Published `08-risk-attribution/` with a synthetic three-sector Euler volatility/component VaR lab, positive-semidefinite covariance checks, negative hedge contribution example, and ten numerical/guardrail tests. **10/10 local prototype tests passed**, but exact published-revision execution and independent review are pending. Project 07's previously missing dependent-bootstrap CI suites are now confirmed green on GitHub Actions run [42538054210](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42538054210) for commit `dea228397b36589d91f7b325b48a8165a5c43a4e`. Next: add Project 08 to dedicated CI, run published tests, then extend risk attribution to covariance estimation stability and finite-difference marginal sensitivity; keep historical tail-risk attribution separate.

### Project 08 covariance stability extension (2026-11-08)

Added `08-risk-attribution/stability.py` and `test_stability.py`: synthetic sample covariance, fixed diagonal shrinkage scenarios, and finite-difference Euler marginal-risk validation. 13 related local prototype tests passed; the published integration is not yet exact-revision executed and GitHub CI is unverified. Next: run both Project 08 suites on the published commit, inspect CI status, add an out-of-sample covariance-estimation stability comparison with train/test isolation, and then plan Project 09. No market data, production certification, or independent review is claimed.

### Project 08 exact-revision CI coverage follow-up (2026-11-08)

Reconciled current main: the dedicated workflow previously ran `test_risk_attribution.py` but **omitted** `test_stability.py`. Updated `.github/workflows/quant-projects.yml` to execute both suites independently on quant-projects changes (workflow commit `3efdb444fae844c4e216c7d0a363cc6fbb6dab41`). This is **coverage configuration only**, not evidence that either suite passed at this new revision. Prior 13/13 results belong to an isolated prototype, not the exact published code. Next: inspect the Actions run for the updated SHA, repair any failures, then implement a training-only/out-of-sample covariance stability comparison. Independent review and market-data validation remain unverified.
