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

### Project 08 out-of-sample covariance checkpoint (2026-11-09)

Added `08-risk-attribution/oos_covariance.py` and `test_oos_covariance.py` with training-only rolling covariance estimates, non-overlapping future scoring, fixed shrinkage scenarios, future-mutation isolation and guardrails. The previous exact-revision [GitHub Actions run 42554137031](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42554137031) **passed** both earlier Project 08 suites on SHA `7b5c0962e2294b43efa8476fd6cd3a7488408d32`. The new module's isolated local tests passed **11/11**, but the published module is not yet covered by a confirmed exact-revision CI run. No real-market validation or independent review. Next: confirm CI for the new suite and proceed to Project 09, a distinct risk-modeling exercise.

### Project 09 initial publication (2026-11-09)

Published `09-drawdown-recovery/` with synthetic wealth/high-water-mark drawdown diagnostics, censored recovery and underwater duration, and circular-block bootstrap scenarios. **8 local prototype tests passed** and CLI smoke test completed; exact published-revision CI, independent review and licensed historical validation remain pending. Project 08 CI [run 42559320574](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42559320574) completed successfully for SHA `fe67244403e1dec067d09e9767948c1d48fdfcc4`. Next: confirm Project 09 CI and implement training-only walk-forward drawdown scoring and block-length sensitivity.

### Project 09 walk-forward extension (2026-11-09)

Added `09-drawdown-recovery/walkforward.py` and `test_walkforward.py`: 104-week training-only rolling forecasts, 26-week non-overlapping forward drawdown scoring, fixed block-length sensitivity, seeded reproducibility, and future-mutation isolation. Nine local tests passed using a local stand-in for the existing drawdown API, plus CLI smoke and compilation. **Exact published-revision CI is pending**; no independent review or licensed historical-data validation. Next: verify CI on the exact SHA and address failures, then proceed to Project 10 as a distinct portfolio-risk exercise.

### Project 10 initial milestone (2026-11-09)

Added synthetic liquidity-aware rebalancing capacity and transaction-cost stress with input guardrails, a tutorial, and 15 deterministic tests. Local equivalent prototype tests passed 15/15 with a CLI smoke test and compilation. Exact published-revision CI and independent review remain unverified until checked. Project 09's [GitHub Actions run 42571151319](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42571151319) passed on SHA 53a9cbcec725e83f9343ce523a4fc06d132018ba. Next: confirm Project 10 CI, add lagged rolling ADV forecasts and held-out liquidity shocks. No licensed market data or production certification.

### Project 10 lagged ADV walk-forward extension (2026-11-09)

Added `10-liquidity-rebalancing/adv_walkforward.py` and `test_adv_walkforward.py`: training-only trailing dollar-volume estimates, fixed stress factors, non-overlapping forward liquidity outcomes, future-mutation isolation, and input guardrails. Local source-equivalent tests **16/16 passed** with compilation and seeded CLI smoke test. Project 10's previous exact-revision [CI run 42577042076](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42577042076) **passed** on SHA `b7080cc53824753c682f19139acb17068f69aa4c`, but that run did not include this extension. New extension exact-revision CI, licensed market-data validation, and independent review remain pending until confirmed. Next: confirm new CI, add capacity-forecast calibration and uncertainty diagnostics, then Project 11.

### Project 10 prequential calibration checkpoint (2026-11-09)

Confirmed corrected GitHub Actions [run 42585780257](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42585780257) **passed** on commit `07f754a014fe72f397055c6c507a8497c1a8f722`, covering the existing Project 10 tests. Added `calibration.py` and `test_calibration.py`: conservative empirical capacity-day upper multipliers estimated from **previously completed** held-out windows, warm-up suppression, deterministic synthetic data, future-mutation and invalid-input tests. New exact-revision CI is **pending**; local execution was blocked by network isolation when retrieving the GitHub revision. No licensed market validation, independent review, or production certification. Next: verify new CI, address any failures, then begin Project 11 as a distinct quantitative-finance lab.

### Project 11 — Rolling factor exposure stability (2026-11-09)

Published `11-factor-exposure-stability/` with training-only rolling OLS/ridge factor loadings, non-overlapping held-out ex-post decomposition, synthetic exposure shift, finite/rank guardrails, beginner tutorial, and nine tests. **9/9 authored-source local tests passed**, as did compilation and seeded CLI smoke. Exact published-revision CI, independent review, and licensed point-in-time factor-data validation are **unverified**. Realized held-out factor returns are used only for ex-post scoring, not available at forecast origin. Next: confirm exact-revision CI, assess coefficient uncertainty and ridge sensitivity, then proceed to a distinct Project 12.

### Project 11 beta uncertainty and release-lag extension (2026-11-09)

Added `beta_diagnostics.py` and `test_beta_diagnostics.py`: training-only residual bootstrap coefficient intervals, rolling L2 beta drift, fixed synthetic factor-release lag, seeded reproducibility, collinearity guardrails, and future-data mutation checks. Prior exact-revision [CI run 42598191371](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42598191371) passed for initial Project 11. **New extension tests were authored but not locally executed; exact-revision CI and independent review remain pending.** Factor release lags are synthetic assumptions, not verified vendor publication calendars. Next: confirm extension CI, evaluate ridge sensitivity and bootstrap interval coverage under structural breaks, then Project 12.

### Project 12 initial publication (2026-11-09)

Added `12-volatility-targeting/` with trailing-window realized-volatility exposure scaling, cash fallback on zero volatility, capped leverage, turnover and linear transaction-cost accounting, seeded synthetic regime shift, and regression tests. Project 11's [exact-revision GitHub Actions run 42605206329](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42605206329) **passed** on SHA `93b2aefb2f1d10157b469d850766595654f9514c`. Project 12 exact-revision CI and licensed historical validation remain pending until verified. Next: confirm Project 12 CI, add walk-forward realized-volatility target calibration and cost/leverage sensitivity; independent review and production certification remain unverified.

### Project 12 held-out calibration extension (2026-11-09)

Confirmed initial Project 12 exact-revision [GitHub Actions run 42613813969](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42613813969) completed **successfully** on SHA `08c860dbb306b5a2a6bf3338e8211fcd7d1b99ff`. Added `calibration_walkforward.py` and `test_calibration_walkforward.py`: historical-only origin estimates, non-overlapping forward volatility tracking errors, fixed leverage-cap/cost grid, and synthetic future-mutation tests. **New extension tests have not been executed locally; exact-revision CI is pending.** Historical-data provenance, independently assessed calibration, and production certification remain unverified. Next: verify exact-revision CI, repair any failures, then proceed to a distinct Project 13.

### Project 13 — Inverse-volatility allocation (2026-11-09)

Added `13-risk-parity/` with seeded synthetic regime-shift returns, trailing-window inverse-volatility weights, long-only cap, non-overlapping held-out outcomes, transaction-cost sensitivity, and ten authored test cases. Project 12's exact-revision [CI run 42623425870](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42623425870) passed on SHA `180513d2df6292c9544b983301abb1138c283f57`. Project 13's exact-revision CI, local execution, historical-market validation and independent review are **pending**. The constant-mix evaluation versus drifted turnover reference is an educational approximation, not a self-financing backtest. Next: confirm Project 13 CI and correct any failures, then implement covariance-aware equal-risk-contribution estimation and sensitivity in a subsequent incremental milestone.
