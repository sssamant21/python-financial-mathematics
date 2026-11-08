# Project 06 — Historical vs Normal VaR, CVaR, and Bootstrap Uncertainty

**Purpose:** Compare one-week downside-risk estimates without looking ahead. Educational research only, not investment advice or a trading system.

## Fundamentals

For weekly simple return `r`, define loss `L=-r`. The 95% one-week **historical VaR** is `max(0, -quantile(r, 0.05))` from the previous 52 weekly observations. **Normal parametric VaR** is `max(0, -(mean(r)+stdev(r)*Phi^-1(0.05)))`. Historical **CVaR / expected shortfall** here is the negative mean of observed returns at or below the empirical 5th-percentile cutoff. Outputs are fractions of invested capital, not USD.

**Bootstrap interval:** draw 500 independent-with-replacement samples from the training window, recompute historical VaR for each, and take the 2.5th/97.5th percentiles. This quantifies *sampling uncertainty in the VaR estimator* under an iid assumption. It is **not** a prediction interval for next week's loss and does not guarantee coverage during regime changes. IID resampling ignores serial dependence and volatility clustering.

The backtest compares each actual next-week loss against its prior-week forecast using `loss > VaR`. The exact binomial p-value compares breach counts with a nominal 5% rate, but assumes independent trials. Rolling windows and clustered volatility can violate this assumption, so treat the result as a diagnostic, not certification. CVaR with 52 observations is particularly noisy (about 2–3 tail observations).

## Run — Windows PowerShell

From repository root:

```powershell
py -m pip install -r quant-projects/requirements.txt
cd quant-projects/06-tail-risk-bootstrap
py -m pytest -q test_tail_risk.py
py tail_risk.py
```

By default, the lab generates **synthetic**, seeded weekly returns and fictional volatility shocks. Outputs are `reports/weekly_tail_risk.csv`, `reports/breach_summary.csv`, and `reports/metadata.json` (Git-ignored). No internet is needed.

For a legally obtained local CSV with `Date,Return` (weekly *simple decimal returns*, not prices; -0.02 means -2%):

```powershell
py tail_risk.py --returns C:\data\licensed_weekly_returns.csv --lookback 52 --bootstrap 500 --seed 42
```

Do not publish third-party market data without redistribution rights. Historical series may be revised/back-adjusted and contain survivorship or hindsight-selection bias. Record vendor, as-of timestamp, and selection rules for real studies.

## Safeguards and limitations

- Week t is scored using only returns `[t-52,t)`; its own return is excluded from the forecast.
- No live broker APIs, credentials, production data, or trading decisions.
- Normal VaR may miss skewness, heavy tails, and clustered volatility. Historical VaR may underestimate unprecedented losses.
- The bootstrap is reproducible but overlapping rolling estimates are not independent.
- VaR is floored at zero for reporting, affecting coverage in low-risk or positive-return regimes.
- Synthetic dates labeled 2019–2023 are **not historical evidence** about the 2020 or 2022 crises.

## Validation

On 2026-11-08, the prepared Python source was run locally using NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0 and pytest 9.0.2: **7/7 tests passed**. An end-to-end synthetic run with 100 bootstrap resamples produced 208 scored weeks: historical VaR 18 breaches, normal VaR 12 breaches. These are synthetic outcomes, not investment returns. Exact published-revision CI and independent review remain pending.

Next: dependent-return block bootstrap, horizon-aligned multiweek VaR, conditional coverage, and licensed point-in-time market-data provenance.
