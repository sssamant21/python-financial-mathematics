# Quantitative Finance — Hands-on Python Projects

Forty-seven self-contained labs complement the financial-mathematics books without duplicating their manuscript chapters.

| Project | Topic | Data | Main script |
|---|---|---|---|
| [01](01-single-stock-monte-carlo/README.md) | Geometric Brownian Motion, simulation, 95% VaR | Hypothetical | `stock_monte_carlo.py` |
| [02](02-two-stock-correlation/README.md) | Correlated stocks, diversification, portfolio VaR | Hypothetical | `two_stock_monte_carlo.py` |
| [03](03-five-stock-optimization/README.md) | Correlation/covariance, efficient frontier, constrained optimization, GBM Monte Carlo | Hypothetical | `five_stock_quant_lab.py` |
| [04](04-historical-backtesting/README.md) | Real-stock prices, walk-forward optimization, drawdowns, ex-ante VaR breaches | Download-on-demand | `backtest.py` |
| [05](05-regime-stress-stability/README.md) | Walk-forward covariance stability, stress windows, transaction costs, forecast-risk shocks | Seeded synthetic / optional licensed input | `stress_lab.py` |

| [06](06-tail-risk-bootstrap/README.md) | Rolling historical and normal VaR, CVaR, bootstrap uncertainty and breach diagnostics | Seeded synthetic / licensed input | `tail_risk.py` |

| [07](07-multi-horizon-risk/README.md) | Horizon-aligned historical/parametric VaR/CVaR, dependent bootstrap forecasts, and non-overlapping forward outcomes | Seeded synthetic / optional licensed prices | `multi_horizon.py` |
| [08](08-risk-attribution/README.md) | Euler volatility risk contributions and parametric normal component VaR | Synthetic only | `risk_attribution.py` |

| [09](09-drawdown-recovery/README.md) | Path-dependent drawdown, recovery, and circular-block scenario analysis | Seeded synthetic | `drawdown.py` |

| [10](10-liquidity-rebalancing/README.md) | Liquidity-aware rebalancing, participation capacity, spread and impact stress | Deterministic synthetic | `liquidity.py` |
| [11](11-factor-exposure-stability/README.md) | Rolling factor exposures, ex-post held-out decomposition, and regime drift | Seeded synthetic | `factor_lab.py` |
| [12](12-volatility-targeting/README.md) | Lagged realized-volatility targeting, turnover and linear transaction-cost sensitivity | Seeded synthetic | `volatility_targeting.py` |
| [13](13-risk-parity/README.md) | Inverse-volatility and covariance-aware ERC, matched held-out cost/risk comparison | Seeded synthetic | `risk_parity.py` |
| [14](14-hedge-ratio-stability/README.md) | Rolling minimum-variance hedge ratios, beta regime drift and costs | Seeded synthetic | `hedge_lab.py` |
| [15](15-bond-duration-convexity/README.md) | Fixed-coupon bond valuation, duration, convexity, parallel and nonparallel spot-curve shocks, key-rate DV01 | Hypothetical | `bond_lab.py` |
| [16](16-option-payoff-stress/README.md) | European expiry payoffs, Black–Scholes theoretical pricing, put-call parity, finite-difference Greeks and volatility/maturity sensitivity | Hypothetical | `option_payoff.py`, `black_scholes.py` |

| [17](17-implied-volatility-validation/README.md) | Bounded European implied volatility and no-arbitrage quote validation | Hypothetical | `implied_vol.py` |
| [18](18-credit-loss-concentration/README.md) | One-year credit expected loss, EAD concentration and PD/LGD stress | Synthetic only | `credit_risk.py` |

| [19](19-liability-cashflow-matching/README.md) | Liability cash-flow timing, cumulative funding shortfalls and flat-rate PV sensitivity | Synthetic only | `cashflow_matching.py` |
| [20](20-retirement-sequence-risk/README.md) | Retirement sequence-of-returns risk, withdrawals, and shuffled-return sensitivity | Seeded synthetic | `sequence_risk.py` |
| [21](21-sector-performance-attribution/README.md) | Single-period Brinson–Fachler allocation, selection and interaction reconciliation | Synthetic only | `attribution.py` |
| [22](22-tracking-error-information-ratio/README.md) | Ex-post active risk, information ratio, and trailing-window diagnostics | Synthetic only | `tracking_error.py` |
| [23](23-downside-risk-ratios/README.md) | Downside deviation, Sortino/Omega ratios, MAR sensitivity and trailing diagnostics | Synthetic only | `downside_risk.py` |
| [24](24-portfolio-concentration/README.md) | Capital concentration, return drift, lagged-target rebalancing and cost sensitivity | Synthetic only | `concentration.py`, `rebalancing.py` |
| [25](25-high-water-mark-fees/README.md) | Net NAV accounting, high-water marks, monthly/annual crystallization and hard-hurdle sensitivity | Synthetic only | `fee_lab.py`, `crystallization.py` |
| [26](26-cashflow-performance/README.md) | Time-weighted vs money-weighted returns, external cash-flow timing, periodic IRR and dated XIRR guardrails | Synthetic only | `performance.py`, `dated_xirr.py` |
| [27](27-kelly-estimation-risk/README.md) | Binary-payoff Kelly log-growth, Wilson uncertainty bounds and sample-size sensitivity | Synthetic only | `kelly.py`, `uncertainty.py` |
| [28](28-implementation-shortfall/README.md) | Arrival-price shortfall, VWAP benchmark, schedule/participation/impact sensitivity and fees | Synthetic only | `execution.py`, `benchmarks.py`, `schedule_sensitivity.py` |
| [29](29-credit-spread-stress/README.md) | Credit spread duration/convexity, issuer/sector shocks, concentration, scenario P&L and independent cash-flow repricing and yield-convention consistency checks | Synthetic only | `spread_stress.py`, `issuer_sector.py`, `repricing_check.py`, `external_pricing_check.py` |

| [30](30-bond-carry-roll-down/README.md) | Zero-coupon carry/roll-down, nonparallel curve shocks and interpolation-method stability | Synthetic only | `carry_roll.py`, `sensitivity.py`, `interpolation.py` |

| [31](31-option-monte-carlo/README.md) | Risk-neutral European call Monte Carlo, antithetic pairs, equal-path-budget variance/coverage, predeclared strike/volatility and seed-count sensitivity and Black–Scholes benchmark | Seeded synthetic | `monte_carlo.py` |

| [32](32-binomial-option-exercise/README.md) | CRR European/American put tree, early exercise, convergence, recursive CRR and finite-difference PDE cross-checks | Hypothetical | `binomial.py` |

| [33](33-delta-hedging-error/README.md) | Discrete European-call delta hedging, turnover and transaction-cost sensitivity | Seeded synthetic | `hedge.py`, `sensitivity.py` |
| [34](34-implied-volatility/README.md) | Synthetic Black–Scholes implied volatility inversion, bid/ask spread and strike/maturity conditioning | Synthetic only | `iv.py`, `sensitivity.py` |

| [35](35-barrier-option-monte-carlo/README.md) | Discretely monitored up-and-out European call, antithetic Monte Carlo, matched monitoring and Brownian-bridge continuous survival, reflection-density analytical pricing and independent numerical quadrature | Seeded synthetic | `barrier.py`, `matched_convergence.py` |
| [36](36-asian-option-monte-carlo/README.md) | Discrete arithmetic-average Asian call with antithetic Monte Carlo, exact geometric-average benchmark and paired control variate | Seeded synthetic | `asian_option.py`, `geometric_control.py` |
| [37](37-static-option-arbitrage/README.md) | European call strike-grid, bid/ask interval and common-forward calendar necessary-condition diagnostics | Synthetic only | `surface.py`, `quote_intervals.py` |
| [38](38-put-call-parity/README.md) | European put–call parity with dividend/discount conventions and bid/ask consistency | Synthetic only | `parity.py` |
| [39](39-forward-rate-agreements/README.md) | Single-period forward-rate agreements, implied forwards, start-date settlement, PV identity and independent curve-sensitivity checks | Hypothetical only | `fra.py` |
| [40](40-interest-rate-swaps/README.md) | Spot-start fixed/floating interest-rate swaps, par coupon, coupon reconciliation, curve sensitivity, notional scaling and overflow guardrails | Hypothetical only | `swap.py` |
| [41](41-par-swap-curve-bootstrap/README.md) | Annual par-swap quote bootstrap, discount factors, implied forwards, cash-flow reconciliation and one-basis-point quote sensitivity | Hypothetical only | `curve.py` |
| [42](42-key-rate-curve-risk/README.md) | Key-rate PV01, curve-shape sensitivity, and parallel-bump reconciliation | Synthetic only | `key_rate.py` |
| [43](43-fx-forward-parity/README.md) | FX forward parity, funding-side bid/ask scenarios, hypothetical basis sensitivity and tiny-bump numerical stability (21 authored tests; exact-revision CI pending) | Synthetic only | `fx_forward.py`, `funding_basis.py` |

| [44](44-credit-default-swap-basics/README.md) | Synthetic CDS par spread, hazard/survival, recovery, discounted legs, accrued-on-default and numerical edge-case sensitivity | Synthetic only | `cds.py`, `accrued_default.py` |

| [45](45-cds-survival-curve-bootstrap/README.md) | Piecewise-constant CDS hazard calibration from synthetic par spreads, bounded bisection, infeasibility and boolean-input rejection | Synthetic only | `bootstrap.py` |

| [46](46-cds-credit-sensitivity/README.md) | Synthetic CDS protection-buyer PV, par spread, coupon DV01, finite-difference hazard sensitivity, single- and multi-tenor quote-recalibrated bucket CS01 and analytical regression checks | Synthetic only | `cds_risk.py`, `multi_tenor_cs01.py` |

| [47](47-credit-portfolio-tranche-loss/README.md) | Exact independent-default tranche loss, one-factor Gaussian correlated-default stress, Monte Carlo uncertainty and convergence/reconciliation diagnostics | Synthetic only | `tranche_loss.py`, `correlated_defaults.py` |

## Quick start (Windows PowerShell)

```powershell
py -m pip install -r quant-projects/requirements.txt
cd quant-projects/01-single-stock-monte-carlo
py stock_monte_carlo.py
py -m pytest -q
```

Then change folders for the other labs. Project 04 requires a fresh authorized historical price download:

```powershell
cd ../04-historical-backtesting
py -m pip install yfinance
py download_prices.py
py backtest.py
py -m pytest -q
```

**Important:** scripts and tests are educational. Hypothetical Monte Carlo output is not a market forecast. Historical comparisons are affected by the price provider, hindsight selection, trading frictions, and model assumptions. Project 04 deliberately excludes third-party historical prices from this public GitHub repository because upstream redistribution rights have not been verified. Archived study results are labeled by their 2020–2026 sample dates.

## Development and validation

Run `py -m pytest -q` inside Projects 01, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, and 13 (Project 02 runs as a self-contained script). Charts/CSVs generated by scripts are ignored by project-local `.gitignore` rules. Keep the work separate from `books/` and manuscript QA.

See [PROJECT-TRACKER.md](PROJECT-TRACKER.md) for scope, next exercises, and acceptance status.

Project 08 also includes `oos_covariance.py`, a synthetic walk-forward comparison of fixed covariance-shrinkage scenarios with non-overlapping forward variance scoring. Run `python -m pytest -q test_oos_covariance.py` from its directory; see the Project 08 README for model-validation limits.

Project 09 also provides `walkforward.py` for training-only rolling drawdown scenario scoring and non-overlapping held-out 26-week outcomes, with 2/4/8-week circular-block sensitivity. Run `python -m pytest -q test_walkforward.py` in its folder.

Project 10 also includes `adv_walkforward.py` and `test_adv_walkforward.py` for lagged rolling dollar-volume forecasts and non-overlapping held-out liquidity-shock scoring on synthetic data.

Project 10 includes `calibration.py` for prequential liquidity-capacity uncertainty diagnostics; run `python -m pytest -q test_calibration.py` in its folder.

Project 11 uses synthetic three-factor observations and rolling training-only regression. Run `python -m pytest -q test_factor_lab.py` in its directory.

Project 11 also includes `beta_diagnostics.py` for point-in-time release-lagged factor beta uncertainty and rolling drift; run `python -m pytest -q test_beta_diagnostics.py` in its folder.

Project 12 uses a lagged volatility estimator and seeded regime-shift returns; run `python -m pytest -q test_volatility_targeting.py` in its folder.

Project 12 also includes `calibration_walkforward.py` and `test_calibration_walkforward.py` for non-overlapping held-out volatility forecast errors and predeclared leverage/cost sensitivity. This is synthetic educational validation, not live-market calibration.

Project 13 uses training-only inverse-volatility allocation, capped long-only weights and 13-week non-overlapping synthetic evaluation. Run `python -m pytest -q test_risk_parity.py` in its directory.

Project 13 also includes `erc.py` and `test_erc.py` for covariance-aware equal-risk-contribution optimization and non-overlapping held-out risk-budget drift. Run `python -m pytest -q test_erc.py` from `13-risk-parity/`. This extension uses synthetic observations only.

Project 13 also includes `compare.py` and `test_compare.py` for matched uncapped long-only inverse-volatility versus ERC allocation, non-overlapping buy-and-hold blocks, drifted holdings, turnover and ex-post risk-budget comparison. Run `python -m pytest -q test_compare.py` from its folder.

Project 14 uses synthetic rolling hedge ratios and non-overlapping held-out variance scoring; run `python -m pytest -q test_hedge_lab.py` from its folder. Real-market validation and independent review are outstanding.

Project 14 also includes `sensitivity.py` and `test_sensitivity.py` for matched-origin 26/52/78-week hedge-window and fixed covariance-shrinkage sensitivity. This is synthetic ex-post evaluation, not a trading strategy.

Project 14 also includes `regime_uncertainty.py` and `test_regime_uncertainty.py` for seeded, descriptive block-bootstrap intervals on predeclared held-out hedge variance-reduction scores. Run `python -m pytest -q test_regime_uncertainty.py` from its directory. These intervals are not certified coverage estimates.

Project 15 provides annual-coupon bond valuation and predeclared parallel yield-shock stress; run `python -m pytest -q test_bond_lab.py` in its directory.

Project 15 also provides `curve_portfolio.py` and `test_curve_portfolio.py` for hypothetical multi-bond spot-curve key-rate DV01 and nonparallel scenario repricing.

Project 15 additionally includes `interpolation_stability.py` and `test_interpolation_stability.py` for a fixed rate-linear versus log-discount interpolation comparison, node DV01 aggregation, and parallel/nonparallel stress sensitivity. Run `python -m pytest -q test_interpolation_stability.py` in Project 15. Synthetic-only; independent review pending.

Project 15 also includes `forward_diagnostics.py` and `test_forward_diagnostics.py` for annual effective forward-rate consistency under the two predeclared spot-curve interpolation methods, using synthetic rates and a fixed curve shock.

Project 16 uses standard-library `unittest` for synthetic expiry payoffs and a separate European Black–Scholes theoretical valuation extension; run `python -m unittest -v test_option_payoff.py test_black_scholes.py` from `16-option-payoff-stress/`. Exact-revision CI and independent review remain unverified.

Project 16 additionally includes `sensitivity.py` and `test_sensitivity.py`, a deterministic synthetic Black–Scholes volatility/maturity grid with parity and edge-case guardrails. Run `python -m unittest -v test_sensitivity.py` in its directory. Exact published-revision CI is tracked separately.

Project 16 also includes `stability_diagnostics.py` and `test_stability_diagnostics.py` for analytical-versus-finite-difference Greeks under predeclared near-expiry and low-volatility synthetic scenarios. Run `python -m unittest -v test_stability_diagnostics.py` from Project 16. Exact-revision CI and independent review remain unverified.


Project 17 additionally includes `quote_validation.py` and `test_quote_validation.py` for European call/put bid-ask parity intervals, quote guardrails and synthetic implied-volatility ranges. Run `python -m unittest -v test_implied_vol.py test_quote_validation.py` from Project 17. CI and independent review must be checked on the exact revision.

Project 17 also includes `surface_checks.py` and `test_surface_checks.py` for synthetic European call cross-strike monotonicity, vertical spread and butterfly inequalities, and zero-dividend/nonnegative-rate calendar monotonicity. Run `python -m unittest -v test_surface_checks.py` from Project 17. These necessary conditions do not certify executable arbitrage absence.

Project 18 uses standard-library credit risk calculations and deterministic tests. Run `python -m unittest -v test_credit_risk.py` from `18-credit-loss-concentration/`.

Project 18 also provides `correlated_defaults.py` and `test_correlated_defaults.py` for seeded synthetic one-factor correlated borrower defaults, empirical loss-tail diagnostics and explicit analytical expected-loss comparison. Run `python -m unittest -v test_credit_risk.py test_correlated_defaults.py` from Project 18. No real-default calibration or independent model review is claimed.

Project 18 also includes `correlation_sensitivity.py` and `test_correlation_sensitivity.py` for predeclared latent asset-correlation scenarios and repeated-seed Monte Carlo dispersion. Run `python -m unittest -v test_correlation_sensitivity.py` from Project 18. Synthetic only; exact-revision CI and independent review tracked separately.

Project 18 also provides [borrower-level scenario-tail attribution](18-credit-loss-concentration/README.md) with additivity and EAD concentration sensitivity. Run `python -m unittest -v test_tail_attribution.py` in Project 18; synthetic only.

Project 19 uses standard-library cash-flow matching and synthetic discount-rate stress. Run `python -m unittest -v test_cashflow_matching.py` from `19-liability-cashflow-matching/`. Exact-revision CI and independent review remain unverified.

Project 19 also includes `constrained_matching.py` and `test_constrained_matching.py` for bounded integer-lot synthetic bond cash-flow matching, infeasibility diagnostics, and fixed-holdings parallel-rate PV stress. Run `python -m unittest -v test_constrained_matching.py` from Project 19.

Project 19 also includes `maturity_diagnostics.py` and `test_maturity_diagnostics.py` for synthetic fixed-holdings Macaulay duration-gap and rate-derivative diagnostics. Run `python -m unittest -v test_maturity_diagnostics.py` from its directory; exact published-revision CI and independent review are tracked separately.

Project 20 — [Retirement sequence-of-returns risk](20-retirement-sequence-risk/README.md): standard-library synthetic withdrawal timing, early/late loss ordering, seeded return permutations, and explicit ruin convention. Run `python -m unittest -v test_sequence_risk.py` in the Project 20 folder. Local standalone tests 10/10 passed; exact published CI and independent review unverified.

Project 20 uses standard-library `unittest` and seeded return permutations. Run `python -m unittest -v test_sequence_risk.py` and `python sequence_risk.py --draws 500 --seed 2026` from `20-retirement-sequence-risk/`. The permutation ruin fraction is not a calibrated retirement-failure probability.

Project 20 extension — [Funded-withdrawal and inflation sensitivity](20-retirement-sequence-risk/README.md): predeclared 3/5/7/9% withdrawal and 0/2/4% inflation grids, per-year funded/unfunded spending and nominal funding ratios. Run `python -m unittest -v test_withdrawal_sensitivity.py` and `python withdrawal_sensitivity.py` from the Project 20 folder. Synthetic only; hosted CI and independent review pending.

Project 21 uses standard-library synthetic one-period sector attribution with ten deterministic regression tests. Run `python -m unittest -v test_attribution.py` and `python attribution.py` from `21-sector-performance-attribution/`. Multi-period linking, real-market validation, and independent review are not established.

Project 21 also includes [two-period geometric linking](21-sector-performance-attribution/README.md) via `linked_attribution.py` and `test_linked_attribution.py`; run `python -m unittest -v test_linked_attribution.py` from Project 21. Synthetic only; hosted CI pending.

Project 22 uses standard-library tracking error and information ratio diagnostics. Run `python -m unittest -v test_tracking_error.py` and `python tracking_error.py` from `22-tracking-error-information-ratio/`. Synthetic only; exact-revision CI and independent review pending.

Project 22 extension: `sensitivity.py` and `test_sensitivity.py` compare predeclared synthetic benchmarks and monthly versus nonoverlapping quarterly compounded returns. Run `python -m unittest -v test_sensitivity.py` in its directory; hosted CI and independent review pending.

Project 23 uses Python standard-library synthetic returns. Run `python -m unittest -v test_downside_risk.py` and `python downside_risk.py` in `23-downside-risk-ratios/`. Undefined zero-shortfall ratios return `None`; no historical calibration or independent review is claimed.

Project 24 — [Portfolio concentration and diversification diagnostics](24-portfolio-concentration/README.md): HHI, effective holding count, Shannon entropy, synthetic post-return weight drift and one-way rebalancing turnover. Run `python -m unittest -v test_concentration.py` and `python concentration.py` from the project directory. Published-revision CI and independent review pending.

Project 24 extension: run `python -m unittest -v test_rebalancing.py` and `python rebalancing.py` from `24-portfolio-concentration/`. Targets are precommitted before period returns; historical validation and independent review are unverified.

Project 25 extension: run `python -m unittest -v test_crystallization.py` and `python crystallization.py` in `25-high-water-mark-fees/` for synthetic 1/3/6/12-month fee crystallization and hard-hurdle sensitivity. Local standalone 11/11 passed; exact published-revision CI and independent review are unverified.

Project 26: run `python -m unittest -v test_performance.py` and `python performance.py` from `26-cashflow-performance/`. Synthetic-only; exact published CI and independent review pending.

Project 27: run `python -m unittest -v test_kelly.py`, `python -m compileall -q kelly.py test_kelly.py`, and `python kelly.py` from `27-kelly-estimation-risk/`. This is an educational binary-payoff model, not investment guidance; hosted CI and independent review pending.

Project 27 extension: run `python -m unittest -v test_uncertainty.py` and `python uncertainty.py --wins 55 --trials 100` in `27-kelly-estimation-risk/`. Wilson intervals assume independent Bernoulli observations; all inputs and evaluation probabilities are hypothetical.

Project 28 provides offline synthetic execution-shortfall accounting; run `python -m unittest -v test_execution.py` and `python execution.py` from its directory. Hosted CI and independent review are tracked separately.

Project 28 schedule sensitivity: run `python -m unittest -v test_schedule_sensitivity.py` and `python schedule_sensitivity.py` in its folder. Synthetic-only; hosted CI and independent review tracked separately.

Project 29 uses standard-library Python only. Run `python -m unittest -v test_spread_stress.py` from `29-credit-spread-stress/`. Exact published-revision CI and independent review remain unverified.

Project 29 issuer/sector extension: run `python -m unittest -v test_issuer_sector.py` and `python issuer_sector.py` from `29-credit-spread-stress/`. This uses predeclared synthetic nonparallel shocks and capital HHI; exact published-revision CI and independent review are tracked separately.

Project 29 additionally includes `convention_check.py` and `test_convention_check.py` for nominal-periodic versus continuously compounded synthetic bond repricing. Run `python -m unittest -v test_convention_check.py` in Project 29. No external pricing-library validation is claimed.

Project 29 now includes [high-precision Decimal reference checks](29-credit-spread-stress/README.md#independent-high-precision-arithmetic-cross-check) for nominal-yield bond pricing. Run `python -m unittest -v test_decimal_reference.py` in its directory. This checks arithmetic consistency using synthetic cash flows; external library comparison and independent review remain pending.

Project 30 also provides [nonparallel curve and holding-horizon sensitivity](30-bond-carry-roll-down/README.md) via `sensitivity.py` and `test_sensitivity.py`; all fixtures are synthetic and require no external dependencies.

Project 30 interpolation diagnostics: run `python -m unittest -v test_interpolation.py` and `python interpolation.py` from `30-bond-carry-roll-down/`. Synthetic-only; exact-revision CI and independent review remain unverified.

Project 30 additionally includes `forward_diagnostics.py` and `test_forward_diagnostics.py` for synthetic implied forward-rate discount-ratio consistency and predeclared holding-horizon sensitivity. Run `python -m unittest -v test_forward_diagnostics.py` from Project 30. The forward rates are curve-implied quantities, not market forecasts. The dedicated quant-projects workflow now includes the forward-diagnostics tests, compilation and synthetic CLI; its exact-revision hosted result remains unverified.

Project 31: run `python -m unittest -v test_monte_carlo.py` and `python monte_carlo.py --pairs 10000 --seed 2026` from `31-option-monte-carlo/`. Python 3.11+ standard library only; no historical data or independent model certification.

Project 31's equal-budget follow-up: from `31-option-monte-carlo/`, run `python comparison.py --pairs 2000` and `python -m unittest -v test_comparison.py`. Eight fixed synthetic seeds provide descriptive—not certified—variance reduction and interval coverage.

Project 31 sensitivity extension: run `python -m unittest -v test_sensitivity.py` and `python sensitivity.py --pairs 500` in `31-option-monte-carlo/`. Uses fixed synthetic scenarios and eight predetermined seeds; exact-revision CI and independent review must be checked separately.

Project 31 seed-count stability: run `python -m unittest -v test_seed_stability.py` and `python seed_stability.py --pairs 500` in `31-option-monte-carlo/`. Nested 4/8/16 precommitted seeds are descriptive synthetic evidence, not validated coverage.

Project 32 convergence and exercise-boundary extension: run `python -m unittest -v test_diagnostics.py` and `python diagnostics.py --steps 100` from `32-binomial-option-exercise/`. Fixed 25/50/100/200/400-step European/Black–Scholes comparisons and discrete American put exercise nodes are synthetic diagnostics, not independent certification.

Project 32 also includes `independent_reference.py` and `test_independent_reference.py` for 30 predeclared small-tree, synthetic, separately implemented recursion comparisons. Run `python -m unittest -v test_independent_reference.py` in Project 32; this is not an external model benchmark.

Project 32 now also provides `pde_benchmark.py` and `test_pde_benchmark.py`: a synthetic explicit finite-difference Black–Scholes PDE benchmark with American exercise projection, stability rejection, and coarse-grid comparisons against CRR. Run `python -m unittest -v test_pde_benchmark.py` in Project 32. Local source-equivalent tests passed 6/6; exact-revision hosted CI and independent numerical review remain unverified.

Project 32 PDE grid sensitivity: run `python -m unittest -v test_grid_sensitivity.py` and `python grid_sensitivity.py` in `32-binomial-option-exercise/`. Three precommitted synthetic grids compare European prices against an analytic Black–Scholes put and report American early-exercise premium. This does not certify convergence or production accuracy.

Project 33: run `python -m unittest -v test_hedge.py` and `python hedge.py --paths 100` from `33-delta-hedging-error/`. Synthetic only; published-source CI and independent review pending.

Project 33 additionally provides `sensitivity.py` and `test_sensitivity.py` for predeclared nested path-count, paired transaction-cost, and volatility stress comparisons. Run `python -m unittest -v test_hedge.py test_sensitivity.py` from its folder. Monte Carlo intervals are model-conditional and do not validate market behavior.

Project 33 extension: [nested Brownian-path hedge-grid refinement](33-delta-hedging-error/README.md#nested-brownian-path-hedge-grid-refinement-synthetic) compares matched 13/26/52/104 hedge dates with fee and turnover diagnostics.

Project 35 matched-grid monitoring extension: `35-barrier-option-monte-carlo/monitoring.py` and `test_monitoring.py`; common Brownian paths across nested observation grids and an analytical vanilla Black–Scholes comparison. Run `python -m unittest -v test_monitoring.py` in that folder. Exact-source hosted CI and independent barrier benchmark pending.

Project 35 also includes `bridge.py` and `test_bridge.py` for conditional continuous-monitoring survival under GBM, matched discrete/continuous payoff bounds, and paired sampling-error diagnostics. Run `python -m unittest -v test_bridge.py` inside its folder. Independent barrier benchmark and historical calibration remain pending.

Project 35 also includes `convergence.py` for exploratory Brownian-bridge monitoring-grid sensitivity, with explicit non-matched-grid sampling caveats and synthetic tests. See [Project 35](35-barrier-option-monte-carlo/README.md).

Project 35 includes `matched_convergence.py` for nested common-Brownian-path grid diagnostics; run `python -m unittest -v test_matched_convergence.py` from its directory. Synthetic only; independent barrier benchmark pending.

Project 35 now includes `analytical.py` (reflection-density continuous-barrier benchmark) and `test_analytical.py`. Run `python -m unittest -v test_analytical.py` from its folder; exact-source CI and independent validation remain pending.

Project 36 numerical stress follow-up: `36-asian-option-monte-carlo/test_geometric_control.py` now includes deep-in-the-money and one-fixing limiting-case checks, seeded high-volatility finite-output stress, and input rejection. Run `python -m unittest -v test_geometric_control.py` from Project 36; newly added tests require exact-revision CI confirmation and independent model review.

Project 37: run `python -m unittest -v test_surface.py`, `python -m compileall -q surface.py test_surface.py`, and `python surface.py` in `37-static-option-arbitrage/`. Five local synthetic unittest methods passed; hosted CI and independent review remain unverified.

Project 37 bid/ask extension: run `python -m unittest -v test_surface.py test_quote_intervals.py` and `python quote_intervals.py` from `37-static-option-arbitrage/`. The calendar screen assumes a common forward at both expiries; passing is not a joint feasibility certificate.

Project 37 joint bid/ask feasibility extension: `37-static-option-arbitrage/joint_feasibility.py` checks simultaneous same-expiry monotonicity, discounted vertical-spread and convexity inequalities for 3–5 synthetic quotes using bounded Fourier–Motzkin elimination. Run `python -m unittest -v test_joint_feasibility.py` from Project 37. Authored tests and hosted exact-source CI remain unverified; this is not complete option-surface certification.

Project 37 boundary/scale diagnostics: run `python -m unittest -v test_joint_feasibility.py test_boundary_scaling.py` inside `37-static-option-arbitrage/`. The synthetic tests are configured in hosted CI; their new exact-revision outcome remains unverified.

Project 37 scale-aware tolerance follow-up: the joint solver now normalizes strikes and quote prices to a common unit before elimination. Run `python -m unittest -v test_joint_feasibility.py test_boundary_scaling.py test_normalized_tolerance.py` in `37-static-option-arbitrage/`. New exact-source CI and independent numerical review remain pending.

**Project 37 numerical reference:** `37-static-option-arbitrage/test_irregular_decimal_reference.py` compares irregular-grid point-quote classifications against an independent high-precision Decimal slope reference. Published-source CI and broader bid/ask interval reference validation remain pending.

Project 37 also includes `test_interval_reference.py`, an independent exact-rational three-strike bid/ask interval-feasibility cross-check. Run `python -m unittest -v test_interval_reference.py` from `37-static-option-arbitrage/`; exact published-source CI and independent numerical review are tracked separately.

Project 37 now also includes a five-strike exact-rational bid/ask interval oracle (`test_five_interval_reference.py`). Run `python -m unittest -v test_five_interval_reference.py` in its folder; hosted CI and independent numerical review must be checked on the exact revision.

**Project 37 five-strike numerical validation (2026-11-16):** Added two irregular-grid exact-rational cross-check fixtures for feasible and convexity-infeasible point quotes. See [Project 37](37-static-option-arbitrage/README.md). Exact published-source test execution and CI remain unverified.

Project 37 numerical-conditioning regression: `python -m unittest -v test_near_zero_pivots.py` from its folder compares four small-gap/near-flat synthetic quote grids against the independent exact-rational three-strike oracle. Hosted CI and independent review must be checked before treating these as accepted.

Project 38 additionally includes adjacent-binary64 quote-boundary regression cases in `test_decimal_reference.py`. The one-ULP checks illustrate strict numerical comparisons, not executable market arbitrage; consult its README and the tracker for validation limitations.

Project 40 also includes `test_curve_reconciliation.py`: independent period-by-period floating coupon projections, uneven-accrual and negative-rate scenarios, and terminal/interior discount-factor sensitivity. Run `python -m unittest -v test_swap.py test_curve_reconciliation.py` from its folder. The extension's exact-revision hosted CI remains unverified.

Project 42 off-grid extension: `42-key-rate-curve-risk/offgrid.py` adds piecewise-linear zero-rate interpolation, exact node gradients and finite-difference cross-checks for synthetic off-node payments. Run `python -m unittest -v test_key_rate.py test_offgrid.py` from Project 42. New tests require exact-revision execution/CI confirmation.

Project 43 funding/basis regression now includes an independent `expm1`-based 2-bp sensitivity identity with a negative synthetic basis (`test_funding_basis.py`); 19 total Project 43 tests are authored. Run `python -m unittest -v test_fx_forward.py test_funding_basis.py` from `43-fx-forward-parity/`. The new case's runtime and exact-revision CI remain unverified.


### Project 45 — CDS survival-curve bootstrap

[Project 45: Piecewise-constant default hazard curve calibration](45-cds-survival-curve-bootstrap/README.md) uses synthetic par CDS quotes, a bounded sequential bisection solver, explicit infeasibility rejection, and seven deterministic regression tests. Run `python -m unittest -v test_bootstrap.py` from the project directory. Local authored-source tests passed 7/7; exact-revision CI and independent model review remain unverified.

Project 45 additionally includes an independent two-period, piecewise-hazard coupon-PV reconciliation regression test. Run `python -m unittest -v test_bootstrap.py` in `45-cds-survival-curve-bootstrap/`; 14 tests are authored, but exact-revision execution and CI are not yet verified.

Project 46 update: [synthetic multi-tenor bucket-CS01 parallel-shock reconciliation](46-cds-credit-sensitivity/README.md) adds four independent derivative/finite-shock checks; execution and exact-revision CI remain unverified.

Project 46 bump-size convergence extension: [Project 46](46-cds-credit-sensitivity/README.md) adds `test_bump_convergence.py`, five synthetic finite-difference stability/boundary checks across 1, 0.1 and 0.01 bp quote bumps. Run `python -m unittest -v test_bump_convergence.py` from that directory. Newly authored checks and exact-revision hosted CI remain unverified.

Project 46 additionally includes an independent closed-form flat-hazard reference in `test_flat_curve_reference.py`. Run `python -m unittest -v test_flat_curve_reference.py` in `46-cds-credit-sensitivity/`; the four new synthetic tests require exact-revision CI confirmation and independent review.

Project 47 update: [credit portfolio tranche-loss Monte Carlo diagnostics](47-credit-portfolio-tranche-loss/README.md) now include a seeded pathwise loss-partition conservation test alongside convergence, correlation and bounded-loss checks. **21 synthetic tests authored; exact-revision CI remains unverified.** Run `python -m unittest -v test_tranche_loss.py test_correlated_defaults.py test_mc_diagnostics.py` from the Project 47 directory.
