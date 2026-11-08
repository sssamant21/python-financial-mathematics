# Project 02 — Two-stock Monte Carlo and correlation

**Goal:** Understand how a technology-stock and a bank-stock portfolio's risk changes as their daily return-shock correlation varies.

- Two illustrative $100 stocks, 60/40 starting weights ($10,000 total).
- Technology annual GBM drift/volatility: 10%/30%.
- Banking annual GBM drift/volatility: 6%/18%.
- Compare correlations -0.20, +0.25, +0.90 using **the same random shocks**.
- 252 trading days, 10,000 paths, reproducible seed 42.
- Evaluate one-year 95% VaR, 5th/95th percentiles, loss probability, and initial portfolio volatility.

Run from this folder after installing `../requirements.txt`:
```powershell
py two_stock_monte_carlo.py
```
The script writes `two_stock_monte_carlo_results.csv` and two PNG charts to this folder. This is a hypothetical buy-and-hold experiment; weights drift after inception, and VaR is not a maximum-loss bound.
