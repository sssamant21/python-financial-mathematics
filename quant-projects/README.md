# Quantitative Finance — Hands-on Python Projects

Twenty-nine self-contained labs complement the financial-mathematics books without duplicating their manuscript chapters.

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
| [29](29-credit-spread-stress/README.md) | Credit spread duration/convexity, issuer/sector shocks, concentration, scenario P&L and independent cash-flow repricing and yield-convention consistency checks | Synthetic only | `spread_stress.py`, `issuer_sector.py`, `repricing_check.py` |

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
