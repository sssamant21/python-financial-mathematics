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

### Project 13 covariance-aware ERC extension (2026-11-09)

Confirmed Project 13 baseline GitHub Actions [run 42631357529](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42631357529) completed successfully, including `test_risk_parity.py`. Added `13-risk-parity/erc.py` and `test_erc.py` with positive-definite covariance checks, fixed diagonal shrinkage, coordinate-descent ERC, training-only weights, held-out risk-contribution drift, future-mutation isolation, and seeded synthetic scenarios. An equivalent local prototype passed **12/12** tests, compiled, and completed a CLI smoke test; the exact published revision and new CI coverage remain unverified until the updated workflow finishes. ERC is uncapped, unlike the baseline capped inverse-volatility method. No licensed market-data validation, self-financing ledger, independent review, or production certification. Next: verify exact-revision CI and add a controlled baseline-vs-ERC held-out comparison with matched cost and weight constraints before Project 14.

### Project 13 matched-method comparison checkpoint (2026-11-09)

Added `13-risk-parity/compare.py` and `test_compare.py`: both inverse-volatility and covariance-aware ERC use matched long-only uncapped fully invested constraints, a 52-week training lookback, non-overlapping 13-week held-out blocks, origin-only rebalancing with buy-and-hold share drift, and matched 10-bps turnover costs. Ex-post covariance is used only to score realized risk-contribution drift. **11/11 local tests passed** on a source-equivalent fixture using locally recreated existing ERC and inverse-volatility helpers, with Python compilation and synthetic CLI smoke test; full exact published-revision integration and CI remain unverified. No licensed historical market data or independent review. Next: confirm exact-revision CI and inspect the full published integration, then advance to Project 14 as a distinct exercise.

### Project 14 — Minimum-variance hedge ratio stability (2026-11-09)

Published `14-hedge-ratio-stability/` with training-only rolling hedge ratios, signed exposure caps, non-overlapping held-out variance scoring, a seeded beta-regime shift, transaction-cost sensitivity, and 12 authored synthetic tests. **Local tests and exact-revision CI have not yet been confirmed.** No licensed historical-market validation, self-financing hedge ledger, independent review, or production certification. Next: verify CI and compare window/shrinkage sensitivity with regime-specific uncertainty diagnostics.

### Project 14 hedge estimator sensitivity checkpoint (2026-11-09)

Added `sensitivity.py` and `test_sensitivity.py` with common historical-only
origins, fixed window/shrinkage grids, non-overlapping held-out variance
reduction, synthetic early/late regime labels, and future-data mutation
checks. **Tests authored but not executed locally in this run; exact-revision
CI unverified.** This is not nested model selection, and regime-specific
uncertainty intervals remain pending. No licensed market data, independent
review, or production certification. Next: verify new CI and address failures,
then add block-bootstrap regime uncertainty with predeclared evaluation rules.

### Project 14 regime uncertainty checkpoint (2026-11-09)

Verified previous exact-revision [GitHub Actions run 42671128465](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42671128465) **passed** on SHA `6f85c17d192d373feeaa04ebcaefe13607053d13`. Added `regime_uncertainty.py` and `test_regime_uncertainty.py`: seeded whole-held-out-block resampling, predeclared 52-week zero-shrinkage estimator, early/late synthetic regime separation, minimum-block and nonfinite-result suppression, and future-mutation checks. A source-equivalent local prototype passed **13/13** tests and compiled; **exact published-revision CI is not yet confirmed**. This is descriptive uncertainty, not calibrated interval coverage. No licensed historical data, independent review, or production certification. Next: verify new CI, then begin Project 15 as a distinct exercise.

### Project 15 — Bond duration and convexity (2026-11-09)

Project 14 exact-revision [GitHub Actions run 42678936819](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42678936819) passed on SHA `9b43d0249a855627f3feebc0a7465ab18de8c0ce`. Project 15 introduces hypothetical annual-coupon cash flows, exact repricing under fixed parallel yield shocks, modified duration, convexity, analytical/finite-difference checks, and input guardrails. No external data or trading integration. New exact-revision CI and independent review remain unverified until checked. Next: verify CI, then add multi-bond key-rate curve scenarios and nonparallel-shock validation.

### Project 15 spot-curve and key-rate extension (2026-11-09)

Confirmed initial Project 15 exact-revision [CI run 42689667185](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42689667185) passed on SHA 83d9a5aeb689f08c1c7ba4665515ef266c050e38. Added a deterministic annual spot-curve portfolio model, central-difference key-rate DV01, parallel/steepener/flattener scenarios, guardrails and regression tests. A source-equivalent local prototype passed **17/17 tests**, compiled, and completed CLI smoke; the published code is not yet independently executed. New exact-revision CI, historical yield-curve provenance, independent review and production certification remain unverified. Next: inspect new CI and extend with alternative interpolation / key-rate aggregation stability.

### Project 15 interpolation sensitivity checkpoint (2026-11-09)

Reconciled `main` at `b06ec207f4f995af60d45af2c78f038af1de252c`; corrected Project 15 CI [run 42698308497](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42698308497) **passed** on that SHA. Added `interpolation_stability.py` and `test_interpolation_stability.py`: deterministic rate-linear versus log-discount interpolation, matched parallel/nonparallel stress, key-rate DV01 aggregation and guardrails. An isolated local source-equivalent baseline run passed **21/21** tests plus CLI smoke; it was **not** a checkout of the exact GitHub revision because DNS blocked cloning. The new exact-revision CI and independent review remain unverified until the updated workflow runs. Next: verify CI for this extension and review nodewise sensitivities and forward-rate behavior before starting Project 16. No historical market data or production certification.

### Project 15 annual forward-rate diagnostics (2026-11-09)

Added `forward_diagnostics.py` and `test_forward_diagnostics.py` to compare one-year effective forward rates implied by rate-linear and log-discount interpolation on a fixed synthetic 1/3/5/10-year curve, including predeclared node shocks. An isolated source-equivalent local run passed **11/11 tests**, Python compilation, and a CLI smoke test; exact published-revision integration and GitHub Actions execution remain **unverified**. The fixture's maximum absolute method gap was approximately 32.122 bp, which is not historical evidence or a general result. No licensed yield-curve data, independent review, arbitrage-free calibration, or production certification. Next: verify the exact SHA's CI and address failures before proceeding to Project 16.

### Project 16 — Option expiry payoff stress (2026-11-09)

Published a self-contained European-style expiry P&L exercise with long/short calls and puts, multi-leg aggregation, synthetic scenario CLI, beginner mathematics, and eight deterministic `unittest` test methods. **Tests authored but not executed in this run; exact published-revision CI is unverified.** No market data, pricing calibration, independent review, or production certification. Next: verify full Project 15 CI and Project 16 tests on the published SHA, then extend Project 16 with independently checked Black–Scholes valuation, put-call parity and Greeks under explicit assumptions.

### Project 16 Black–Scholes extension (2026-11-09)

Added `black_scholes.py` and `test_black_scholes.py`: continuous-dividend European theoretical valuation, put-call parity residual, central finite-difference delta/gamma/vega, a published numerical benchmark, nine deterministic unit tests and finite-input guardrails. **9/9 authored-source tests passed locally**, compilation and synthetic CLI smoke test passed. Existing Project 16 payoff tests and full exact-revision integration have not yet been rerun. CI integration was configured; **new exact-revision CI and independent review remain unverified**. No historical data or live trading. Next: confirm Project 16 full CI and examine volatility/maturity stress, numerical edge cases, then Project 17.

### Project 16 CI YAML repair (2026-11-09)

Inspected GitHub Actions [run 42733238811](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42733238811) for SHA `16ea92b6f658755347c2cb3551ea03c6f86659e1`: **failure with zero jobs created**. The dedicated workflow's Project 16 step contained literal `\\n` escapes rather than YAML line breaks, preventing workflow parsing. Replaced them with a proper multiline `run: |` block, preserving the existing suite commands. Also repaired a literal `\\n` in the master TOC between Projects 15 and 16. **New exact-revision CI result is pending confirmation**; neither the earlier failed workflow nor authored-source tests establish full published integration. Next: inspect the repaired workflow run and job logs, fix any runtime test failures, then add volatility/maturity sensitivity and numerical edge-case coverage. No historical data, independent review, or production certification.

### Project 16 — volatility/maturity sensitivity extension (2026-11-09)

Confirmed repaired Project 16 GitHub Actions [run 42740390505](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42740390505) **passed** all workflow steps, including the original Project 16 option payoff and Black–Scholes suites. Added `sensitivity.py` and `test_sensitivity.py` with a predeclared 3 × 3 synthetic volatility/maturity grid, put-call parity checks, deterministic CLI, invalid-grid guardrails and deep-out-of-money finite-value checks. **9/9 tests passed locally** in an isolated source-equivalent setup using a reconstructed copy of the published pricing core; compilation and CLI smoke also passed. The full published revision has not been executed locally; the extension's exact-revision CI is **pending verification**. No licensed historical-market validation, independent review or production certification. Next: confirm CI for the new suite, investigate near-expiry/low-volatility finite-difference stability, then begin Project 17.

### Project 16 — numerical stability checkpoint (2026-11-10)

Published `stability_diagnostics.py` and `test_stability_diagnostics.py`: analytical delta/gamma/vega benchmarks, deterministic near-expiry/low-volatility comparison to central differences, descriptive error tolerance and invalid-input guardrails. **Six test methods authored; no local execution or exact-revision CI result confirmed** because local GitHub clone failed DNS resolution. Dedicated workflow extended to cover this suite. No market data, independent review or production certification. Next: confirm full Project 16 CI and address any failures, then begin Project 17.

### Project 16 — exact-revision CI acceptance (2026-11-10)

Verified GitHub Actions [run 42753181413](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42753181413) for exact `main` commit `267ff793c069d64650de128be35d2a02fe7e0e80`: **completed successfully** on 2026-11-10 04:02:16 UTC. The `quant-labs` job and its `Validate Project 16 European option payoff and theoretical pricing` step both concluded **success**. At that revision, the dedicated workflow executes `python -m unittest -v test_option_payoff.py test_black_scholes.py test_sensitivity.py test_stability_diagnostics.py` from Project 16. All other configured quant-labs validation steps also concluded success. This is exact-revision hosted CI evidence, not an independently reproduced local run; individual test counts and numerical tolerance outcomes have not been independently extracted from logs. No licensed market calibration, independent review, or production certification. **Next:** begin Project 17 as a distinct educational lab (suggested: implied-volatility inversion and no-arbitrage quote validation using deterministic synthetic option prices), with numerical solver guards, synthetic regression fixtures, documentation, TOC/tracker update and dedicated CI coverage.

### Project 17 initial lab (2026-11-10)

Synthetic-first European implied-volatility bisection, theoretical quote bounds, eight regression tests, and reproducible tutorial added. Exact-revision CI, market-data calibration, and independent model review pending. Next: inspect CI, add cross-quote put-call parity and bid/ask consistency checks.


### Project 17 synthetic quote consistency extension (2026-11-10)

Added `quote_validation.py` and `test_quote_validation.py`: finite/nonnegative uncrossed call/put bid-ask checks, discounted European no-arbitrage bounds, feasible put-call parity intervals, and bounded synthetic implied-volatility ranges. Eight new regression test methods were authored. **No local execution or exact-revision CI pass is claimed at publication**; CI integration is being updated. No actual option-chain provenance, transaction-cost execution model, independent review, or production certification. Next: verify complete Project 17 CI and repair failures; then assess strike/calendar consistency or begin Project 18 as a distinct exercise.

### Project 17 — exact-revision CI acceptance (2026-11-10)

Verified GitHub Actions [run 42772350562](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42772350562) on commit `df90b81c53a9dd4a436d12d1d786cc0f5537ee62`: **completed successfully** on 2026-11-10 07:01:53 UTC. The `quant-labs` job and `Validate Project 17 implied-volatility inversion` step passed. Downloaded hosted job logs show `python -m unittest -v test_implied_vol.py test_quote_validation.py` executed **16/16 tests successfully** (eight inversion tests and eight bid/ask/parity tests). All other configured job steps passed. This is exact-revision hosted CI, not an independent local reproduction or real-market calibration. Historical option-chain provenance, cross-strike/calendar consistency, bid/ask execution costs, independent model review and production certification remain **unverified**. **Next:** add a separate synthetic strike/calendar consistency screen with mathematically justified conditions, tests and workflow coverage; verify its own exact-revision CI before proceeding to Project 18.

### Project 17 — strike/calendar surface screen (2026-11-10)

Added `surface_checks.py` and `test_surface_checks.py` for necessary European call strike monotonicity, discounted vertical-spread bounds, convexity/butterfly consistency, and restricted calendar monotonicity (zero dividends, nonnegative rates). The screen uses bid/ask feasibility bounds and deterministic hypothetical inputs. **12/12 source-equivalent local tests passed**, Python compilation and synthetic CLI smoke passed using a locally reconstructed pricing helper; the full published revision was **not** executed locally. Exact-revision hosted CI, actual option-chain provenance, executable bid/ask arbitrage, independent model review and production certification remain **unverified**. Next: inspect exact-revision CI and correct any failures, then begin a distinct Project 18.


### Project 17 — exact-revision strike/calendar CI acceptance (2026-11-10)

Verified [GitHub Actions run 42786961895](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42786961895) for exact commit `aa536de372952757b4b9b8d42d00b0d8631d0b1b`: completed **successfully** on 2026-11-10. The hosted `quant-labs` job and all configured steps passed. Job logs confirm `python -m unittest -v test_implied_vol.py test_quote_validation.py test_surface_checks.py` executed, including all **12/12** new surface-check tests passing (the previous 16 inversion/quote tests also executed). This verifies the published code under hosted CI, not a separate independent local reproduction. Synthetic assumptions only: no real option-chain provenance, bid/ask execution or transaction-cost validation, independent model review, or production certification. **Next:** begin Project 18 as a distinct quantitative-finance lab, with beginner-friendly mathematics, deterministic synthetic fixtures, tests and dedicated workflow integration.

### Project 18 — Credit expected loss and concentration (2026-11-10)

Published a synthetic-only one-year borrower-level EAD × PD × LGD expected-loss lab, EAD Herfindahl concentration, capped PD/LGD stress, deterministic CLI and ten regression tests. **10/10 tests passed locally** in the authored-source environment, as did Python compilation and CLI smoke. Example baseline EL 21,000, stressed EL 50,000, on hypothetical EAD 1,750,000. Exact published-revision CI, point-in-time default/recovery data calibration, correlated default-tail risk, independent model review and production certification remain **unverified**. Next: confirm exact-revision CI; add correlated-default loss distribution and concentration tail sensitivity with seeded synthetic simulation, without representing EL as unexpected loss.

### Project 18 correlated-default simulation checkpoint (2026-11-10)

Added `18-credit-loss-concentration/correlated_defaults.py` and `test_correlated_defaults.py` with a seeded one-factor Gaussian latent asset model, borrower PD boundary handling, analytical EL versus simulated mean, empirical 99% loss VaR, tail average, and explicit illustrative unexpected-loss calculation. **10/10 local source-equivalent regression tests passed**, Python compilation and synthetic CLI smoke passed; these tests used a locally recreated minimal `credit_risk.summarize` helper, **not the complete published revision**. Exact-revision GitHub Actions, independent review, and calibration to observed defaults/recoveries remain **unverified**. Next: confirm full Project 18 hosted CI including the new suite, then add rho-grid/seed sensitivity with Monte Carlo uncertainty and borrower-concentration tail attribution. No production certification or regulatory capital claims.

### Project 18 correlated-default — exact-revision hosted CI acceptance (2026-11-10)

Verified [GitHub Actions run 42812680689](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42812680689) on exact commit `27028305afa0b98878dd66da1dc4b088da5acd6d`: completed **successfully** on 2026-11-10 (run updated 12:05:34 UTC). The `quant-labs` job, dependency installation, and `Validate Project 18 credit expected loss and concentration` step all passed; all other configured steps passed too. The workflow includes both `test_credit_risk.py` and `test_correlated_defaults.py`, but individual unittest counts were **not independently extracted from hosted logs in this checkpoint**. This is hosted CI evidence, not independent reproduction or empirical credit-risk validation. No observed default/recovery calibration, model risk approval, regulatory capital validation, or production certification. **Next:** add a seeded rho-grid and repeated-seed Monte Carlo uncertainty analysis, with concentration-tail attribution and regression tests; keep any newly added suite's CI status unverified until checked.

### Project 18 — asset-correlation and repeated-seed sensitivity (2026-11-10)

Added `correlation_sensitivity.py` and `test_correlation_sensitivity.py`: rho grid (0, 0.2, 0.5), common predeclared seeds, analytical EL invariance, mean/VaR/tail-average dispersion, finite-input and 2-million-scenario budget guardrails. **10/10 tests passed in a local source-equivalent environment using recreated minimal `credit_risk` and `correlated_defaults` helpers**, not a full clone of the published repository; Python compilation and CLI smoke passed. The demonstration generated hypothetical outputs only. The complete published revision and its new GitHub Actions suite are **not yet verified**. No historical default/recovery calibration, independent model review, regulatory approval or production certification. **Next:** inspect exact-revision hosted CI, fix failures, then implement borrower-level tail attribution with explicit loss additivity and concentration sensitivity before starting Project 19.

### Project 18 correlation-sensitivity — exact-revision CI acceptance (2026-11-10)

Verified [GitHub Actions run 42830422413](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42830422413) for commit [`d91f5bd7cab91ab560f120dac07c855481dfcecd`](https://github.com/sssamant21/python-financial-mathematics/commit/d91f5bd7cab91ab560f120dac07c855481dfcecd): the workflow completed **successfully**, and the `quant-labs` job's `Validate Project 18 credit expected loss and concentration` step passed. The committed workflow explicitly invokes `python -m unittest -v test_credit_risk.py test_correlated_defaults.py test_correlation_sensitivity.py`. Individual test counts and stdout were not independently extracted from the hosted logs; the earlier 10/10 source-equivalent local results are separate evidence. This establishes successful hosted execution of all three suites, **not** historical credit-default/recovery calibration, independent model validation, regulatory approval or production certification. **Next:** implement borrower-level tail-loss attribution with additivity checks, deterministic seed controls, and concentration sensitivity; update tutorial, tests, master TOC and workflow as appropriate, then verify exact-revision CI before starting Project 19.

### Project 18 borrower-level tail attribution (2026-11-10)

Added `tail_attribution.py` and `test_tail_attribution.py` with deterministic Gaussian one-factor scenario-tail contributions, top-k loss additivity, stable tie handling, borrower EAD redistribution and HHI sensitivity. **13/13 local tests passed** with compilation and a synthetic CLI smoke test using a locally reconstructed `credit_risk` helper; this is **not** complete exact published-revision execution. The new suite is configured in the dedicated quant CI workflow; its exact-revision hosted result is **pending**. No real-default calibration, independent model review, regulatory validation or production certification. **Next:** verify CI for this commit and resolve failures, then advance to Project 19 as a distinct lab.

### Project 18 tail attribution — exact-revision CI acceptance (2026-11-10)

Verified [GitHub Actions run 42850207586](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42850207586) for commit [`7547f67bb7095a0a67089ed93c46e8c4dfa4cc05`](https://github.com/sssamant21/python-financial-mathematics/commit/7547f67bb7095a0a67089ed93c46e8c4dfa4cc05). Run completed **successfully** at 2026-11-10 16:00:47 UTC. The `quant-labs` job and its `Validate Project 18 credit expected loss and concentration` step succeeded. The workflow at this exact SHA explicitly executes `python -m unittest -v test_credit_risk.py test_correlated_defaults.py test_correlation_sensitivity.py test_tail_attribution.py`. Hosted stdout and individual test counts were not independently retrieved; the earlier 13/13 local source-equivalent results are separate evidence. This confirms configured-suite hosted success, not historical credit-default/recovery calibration, independent model validation, regulatory approval, or production certification. **Next:** begin Project 19 as a distinct educational quant lab with deterministic synthetic fixtures, model assumptions, tests, and scoped CI; avoid broker/live trading and point-in-time bias.

### Project 19 initial publication (2026-11-10)

Added `19-liability-cashflow-matching/` with a beginner-friendly synthetic annual asset/liability schedule, present-value funding gaps, cumulative undiscounted cash-flow shortfalls, flat-rate sensitivity, deterministic unit tests and standard-library-only implementation. **Tests authored; local execution and exact-revision CI not yet verified in this run.** No market data, independent model review, or production certification. Next: verify the Project 19 CI suite on its exact SHA, then extend to predeclared synthetic bond candidate matching with feasibility diagnostics and rate stress.


### Project 19 exact-revision CI acceptance (2026-11-10)

Verified [GitHub Actions run 42871279651](https://github.com/sssamant21/python-financial-mathematics/actions/runs/42871279651) completed **successfully** for published commit `92e206ed9752b1c10f756bc92a9c0ce547489cb5` (2026-11-10 18:03–18:04 UTC). The hosted `quant-labs` job explicitly passed `python -m unittest -v test_cashflow_matching.py` and `python -m compileall -q cashflow_matching.py test_cashflow_matching.py` under the Project 19 step; all other configured quant-project steps also passed. Individual test counts were not extracted from logs; do not confuse successful job steps with independent model review. The educational synthetic fixture does not establish market calibration, realistic liability dynamics, operational suitability, or production certification. **Next:** extend Project 19 with constrained synthetic bond cash-flow matching, explicit infeasibility diagnostics, and interest-rate sensitivity tests, without modifying unrelated repository paths.
