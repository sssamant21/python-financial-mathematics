# Project 05 — Walk-forward stability and market-regime stress

**Educational only.** Synthetic data by default; not a trading system or historical market claim.

## What this lab teaches

A long-only five-asset minimum-variance portfolio uses the **previous 52 weekly returns** to estimate covariance. Monthly rebalancing targets weights that sum to 100%, with no position above 40%. Portfolio weights drift naturally between rebalances. The lab measures forecast-volatility instability, turnover, modeled transaction costs, and compounded returns in 2020/2022 calendar windows.

The covariance estimator is `(1-alpha)*sample_cov + alpha*diag(sample_cov)`. Portfolio optimization minimizes `w.T @ cov @ w` under long-only and position-limit constraints. Weekly modeled net return is `(1-turnover*cost_bps/10000)*(1+gross_return)-1`. Forecast annual volatility is `sqrt(52*w.T @ cov @ w)`.

Six scenarios compare baseline (10 bps), zero cost, 25 bps, correlation halfway toward +1, doubled forecast volatility, and stronger 50% covariance diagonal shrinkage. Correlation and volatility shocks **only change forecast risk**, not realized returns or target weights. Shrinkage changes optimized weights and may change realized results.

The two named date windows are 2020-02-21–2020-06-26 and 2022-01-07–2022-12-30. When running the seeded synthetic fixture, these are **fictional shocks assigned to real calendar dates**, not actual COVID or 2022 inflation/rate market results.

## Windows PowerShell

From repository root:

```powershell
py -m pip install -r quant-projects/requirements.txt
cd quant-projects/05-regime-stress-stability
py -m pytest -q test_stress_lab.py
py stress_lab.py
```

No internet needed. To use an independently licensed adjusted-price dataset with sorted Friday-labeled dates and exact columns `Date,AAPL,JNJ,JPM,PG,NEE`:

```powershell
py stress_lab.py --prices C:\path\to\weekly_adjusted_prices.csv --output reports-real
```

The script generates `scenario_summary.csv`, `regime_windows.csv`, `weekly_results.csv`, `monthly_allocations.csv`, and `run_metadata.json` under the selected output directory. The default `reports/` folder is Git-ignored.

## Safety, interpretation, and limitations

Training uses only observations **strictly before** the scored week. Named regimes are ex-post reporting windows, not predictive features. Historical adjusted prices can be back-adjusted and are not necessarily point-in-time tradable. Five names are hindsight-selected; this study excludes taxes, market impact, bid-ask spreads, delistings, and execution slippage beyond the fixed bps assumption. Weekly drawdown misses intraday lows. Forecast-volatility standard deviation describes instability but is not a calibration test.

The local source development run had 7 tests passing after fixing a pandas date-index compatibility issue. The GitHub-published implementation and CI require separate confirmation; see [VALIDATION.md](VALIDATION.md).

Next: add forecast-versus-realized volatility calibration, alternative lookback lengths, historical-bootstrap shocks, and licensed point-in-time data provenance.
