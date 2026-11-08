# Project 07 — Multi-Horizon Portfolio Risk

**Goal:** Learn why one-week, four-week, and thirteen-week downside risk cannot be compared without aligning both the forecast and realized outcome to the **same holding period**.

## Model and interpretation

Three hypothetical assets (TECH, BANK, HEALTH) form a **40% / 30% / 30%** portfolio, rebalanced to target weights weekly without modeled transaction costs. Weekly simple portfolio return is the weighted sum of asset simple returns. To compound over h weeks, calculate the sum of `log(1+r)` and transform back using `expm1`. Horizon loss is `1 - product(1+r_week)`.

At each forecast origin t, use only the preceding 104 weekly returns `[t-104,t)`. Historical horizon loss is estimated from all *overlapping h-week windows entirely within that training history*. Historical 95% VaR is the 95th percentile of those losses, floored at zero. Historical CVaR is the mean of losses at or beyond that empirical cutoff. Normal parametric VaR assumes iid weekly **log returns**, with mean `h*mu` and standard deviation `sqrt(h)*sigma`, transformed to a simple-return loss. Both estimates are proportions of initial capital, **not dollars**.

Actual forward losses are evaluated over `[t,t+h)`, with **non-overlapping scored horizons** spaced h weeks apart. This avoids counting overlapping outcomes as independent breaches, though overlapping training windows and changing regimes still induce dependence. For h=13, the default synthetic fixture yields only 19 scored periods: this is insufficient for confident 95% tail calibration. The normal square-root scaling is not reliable under serial dependence, volatility clustering, or heavy tails.

## Run on Windows PowerShell

From repository root:

```powershell
py -m pip install -r quant-projects/requirements.txt
cd quant-projects/07-multi-horizon-risk
py -m pytest -q test_multi_horizon.py
py multi_horizon.py
```

Outputs (ignored by Git): `reports/horizon_1_weeks.csv`, `reports/horizon_4_weeks.csv`, `reports/horizon_13_weeks.csv`, `reports/summary.csv`, and `reports/metadata.json`.

To supply independently licensed weekly **price levels** (not returns), use a CSV with `Date,TECH,BANK,HEALTH` in strictly increasing **consecutive Fridays**:

```powershell
py multi_horizon.py --prices C:\\data\\licensed_weekly_prices.csv --lookback 104 --horizons 1 4 13 --output reports-real
```

Missing weeks, nonpositive prices, bad dates, invalid weights, insufficient lookback, and incomplete forward horizons are rejected rather than silently filled.

## Synthetic fixture validation

Local development prototype (NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, pytest 9.0.2): **12/12 tests passed**, and the CLI produced 255 one-week, 63 four-week, and 19 thirteen-week scored periods. This GitHub-published implementation was streamlined from that prototype; **exact published-revision CI remains unverified**. No third-party market prices are bundled. The 2019+ date labels of the seeded fictional shocks are **not evidence of actual market events**.

## Research guardrails and next work

- Fixed weights are selected for demonstration, not optimized with hindsight; weekly constant-mix rebalancing is assumed without spreads, slippage, taxes or turnover costs.
- If using real prices, verify corporate actions, delistings, point-in-time availability, instrument selection, and redistribution rights; do not commit proprietary price files.
- VaR is **not** a maximum loss, CVaR tail estimates are noisy, and breach rates alone do not certify calibration.
- Next: dependent-return bootstrap for horizon losses, overlapping-vs-nonoverlapping uncertainty, risk aggregation under dynamic weights, and a formal point-in-time provenance checklist.


## Extension — dependence-aware moving-block bootstrap

`dependent_bootstrap.py` adds a **circular moving-block bootstrap** for horizon loss. Unlike iid weekly resampling, it retains within-block ordering, providing a simple sensitivity check when weekly returns exhibit short-run dependence. This is **not** a calibrated conditional volatility model and does not solve long-memory, regime change, or tail-data scarcity. Circular wrap is a modeling choice that can create artificial boundary adjacency.

Run from this project folder:

```powershell
py -m pytest -q test_dependent_bootstrap.py
py -c "import numpy as np; from dependent_bootstrap import bootstrap_horizon_losses, bootstrap_var_cvar; r=np.random.default_rng(7).normal(0,.02,104); print(bootstrap_var_cvar(bootstrap_horizon_losses(r,4,block_length=4,draws=2000,seed=2026)))"
```

For each walk-forward origin, pass **only the training-period** weekly portfolio returns into `bootstrap_horizon_losses`; never use the current or future outcome to estimate the forecast. Compare block lengths 1, 4, 8 and 13, document sensitivity, and do not treat bootstrap draws as independent market observations. The existing `multi_horizon.py` CLI does **not yet** integrate this optional helper into its forecast CSVs; the extension is a separately runnable research exercise.

Local isolated validation of this helper and its tests: `python -m pytest -q` in a disposable working directory with NumPy/pytest available, **10 passed** (2026-11-08). Published-revision CI, external price provenance, independent validation, and production certification remain unverified.

### Point-in-time market data checklist

Before using real data, record source/provider and license, acquisition timestamp (UTC), exact requested and returned date ranges, timezone, adjusted vs unadjusted price convention, dividends/splits/corporate actions, ticker changes and delistings, survivorship-selection policy, missing-week treatment, asset weights and decision timestamp, and SHA-256 of the private input CSV. Keep restricted raw data out of Git. Verify each forecast uses data actually available at its origin, not merely earlier timestamps in a revised dataset.
