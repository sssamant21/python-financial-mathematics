# Quant Finance Project 4 — Historical Portfolio Backtesting and Risk Validation

**Scope:** educational five-stock portfolio backtesting with adjusted historical prices, rolling covariance estimation, long-only constrained optimization, weekly Value-at-Risk backtesting, monthly rebalancing, and transaction costs. This is not investment advice, a validated trading system, or a point-in-time institutional data pipeline.

## Data and provenance

The bundled `weekly_adjusted_prices.csv` is an **educational derived snapshot**: weekly last-observed adjusted-close values, **rounded to cents**, for **AAPL, JNJ, JPM, PG, and NEE**, January 4, 2019 through May 29, 2026. It was derived from the public `data/clean/master_prices.csv` in the GitHub repository [S-Gijbile-19/AlphaPulse-Investment-Risk-Monitor](https://github.com/S-Gijbile-19/AlphaPulse-Investment-Risk-Monitor/blob/main/data/clean/master_prices.csv), read during this session. The repository's source values are stated as adjusted closes. The last original repository observation inspected was June 2, 2026; the last incomplete calendar week is excluded. The bundled sample should not be represented as current November 2026 market data. Verify the upstream provider's license and redistribution terms before distributing this beyond personal study. For analysis requiring current data, use your own authorized vendor feed.

**Known limitations:** stock selection with hindsight and survivorship bias, historical adjusted-price back-adjustments, weekly sampling missing intraday/daily drawdown extremes, estimation error, covariance/mean instability, the approximation of rebalance execution at period starts, fixed 3% annual risk-free rate, incomplete trading-impact and tax modeling, and normal VaR's weak performance in fat-tailed periods. The 16% forecast volatility constraint can be infeasible, and even when feasible does not cap future realized volatility. Transaction costs are a rough 10 bps times traded notional divided by portfolio value, including an initial purchase, and do not include bid-ask spreads, market impact, or taxes.

## Setup on Windows / PowerShell

```powershell
py -m pip install -r requirements.txt
py backtest.py
py -m pytest -q
```

Files are produced under `reports/`: equity curves, drawdowns, weekly VaR exception chart, allocation history, detailed weekly time series, monthly target weights, and a portfolio-risk summary CSV.

## Methodology

- **Train**: previous 52 weekly returns. All forecasts at week `t` use **only weeks strictly before t**.
- **Test**: January 10, 2020 through May 29, 2026, 334 non-overlapping weekly observed returns.
- **Rebalance**: at the start of the first observed week of each calendar month. The portfolio weights drift naturally within months. Weekly return is close-to-close on adjusted data, so actual tradable execution may differ from this approximation.
- **Strategies**: equal-weight 20% each; minimum annualized portfolio variance; maximum expected excess return / volatility (Sharpe); and maximum estimated annual return subject to a 16% *estimated* volatility limit. All constrained to `[0, 40%]` per name and weights summing to 100%.
- **Estimation**: annualized arithmetic weekly sample mean (`×52`) and annualized covariance (`×52`), with 20% diagonal shrinkage for stability.
- **Risk**: ex ante **one-week 5th-percentile normal forecast** using only past 52 weekly returns, compared with the subsequent realized **gross** weekly portfolio return. Breaches count as violations of the forecast quantile. The Kupiec likelihood-ratio p-value tests only unconditional exception coverage, not independence, conditional calibration, or tail-severity.
- **Performance**: growth of $100,000 after estimated transaction cost, CAGR, annualized weekly-return volatility, maximum observed *weekly* drawdown, historical 95% weekly loss VaR, turnover, and Sharpe versus fixed 3% risk-free.
- **Risk-cap exception**: if the 16% forecast-volatility constraint is infeasible, use the minimum-volatility weights and record an infeasible rebalance, instead of falsely certifying compliance.

## Optional: refresh from Yahoo Finance using yfinance

This step needs internet and the provider may rate-limit requests or revise adjusted prices. The available sample and dated reported results will no longer match exactly.

```powershell
py -m pip install yfinance
py download_prices.py --start 2019-01-01 --output weekly_adjusted_prices_refreshed.csv
py backtest.py --prices weekly_adjusted_prices_refreshed.csv --output refreshed_reports
```

`yfinance.download(..., auto_adjust=True)` requests split/dividend-adjusted OHLC; its `end` parameter is exclusive (see the [official yfinance documentation](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html)). Inspect provider metadata and any missing observations before use. To reproduce a truly historical live strategy, use point-in-time membership, data availability timestamps, and tradable execution prices rather than retrospective adjusted-close levels.

## Exercises

1. Change the 40% cap to 25%; check feasible solutions and return impact.
2. Change covariance shrinkage from 20% to 50% and compare drawdown and VaR violations.
3. Vary trading cost from 0 to 25 bps and compare turnover.
4. Use a 104-week training window rather than 52 weeks, keeping strictly out-of-sample execution.
5. Compare weekly normal VaR against a rolling historical-quantile VaR; evaluate breaches without using future returns.

## What constitutes a valid result?

A successful Python run is a **research backtest**, not proof of forecast accuracy or an actionable trade recommendation. In particular, (a) higher out-of-sample CAGR does not prove persistent strategy superiority, (b) backtests on a five-stock hindsight-selected universe have survivorship/selection bias, (c) a p-value above 0.05 is not evidence that risk is 'certified', and (d) a p-value below 0.05 is a warning of calibration mismatch under the test assumptions.

**Public repository note:** Historical adjusted-price CSV is intentionally not included. Start with `py download_prices.py` after installing optional `yfinance`. See [DATA-PROVENANCE.md](DATA-PROVENANCE.md).
