# Project 01 — Single-stock Monte Carlo (beginner)

**Question:** If a hypothetical stock starts at $100, what one-year outcomes could occur under constant-return/volatility assumptions?

Inputs: 8% annual GBM drift, 20% annual volatility, 252 trading days, 10,000 paths, seed 42.

The model uses `S[t+1]=S[t]*exp((mu-0.5*sigma**2)/252+sigma*Z/sqrt(252))`. It is a simplified *scenario model*, not a prediction or guarantee.

Run from this folder, after `py -m pip install -r ../requirements.txt`:
```powershell
py stock_monte_carlo.py
py -m pytest -q
```

Outputs under `reports/`: a one-row CSV summary, 30 sample paths with average path, and one-year ending-price histogram. Compare the 5th percentile, median, 95th percentile, loss probability, VaR, and tail-average loss (CVaR). Try changing the assumed drift and volatility.
