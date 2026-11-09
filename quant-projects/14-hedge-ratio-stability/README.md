# Project 14 — Minimum-Variance Hedge Ratios and Regime Drift

**Business question:** How much of a correlated hedge instrument would offset an asset's historical return variability, and how reliably does that relationship persist after a market-regime shift?

## Core mathematics

For asset return A and hedge-instrument return H, a linear hedge is `A - hH`. Minimizing historical variance gives

`h* = Cov(A,H) / Var(H)`.

The ratio is estimated using **only the 52 observations preceding** each decision origin, clipped to a predeclared absolute exposure limit of 2. The subsequent 13 observations are held out. A regime shift in the seeded synthetic data changes the underlying beta halfway through the sample. The lab reports held-out unhedged and hedged sample variance, hedge-ratio turnover, and a simple arithmetic net P&L proxy after one-way transaction costs.

A negative ratio represents a long hedge-instrument exposure, not a guaranteed hedge. The example permits signed hedge ratios but does **not** execute any orders. A hedge can increase risk when correlations shift.

## Reproduce

Python 3.11; install repository dependencies from the repository root:

```bash
python -m pip install -r quant-projects/requirements.txt
cd quant-projects/14-hedge-ratio-stability
python hedge_lab.py --seed 14
python -m pytest -q test_hedge_lab.py
```

The core implementation requires NumPy >=1.26,<3; tests use pytest >=8,<10. Data are generated in memory with a fixed seed; no market data are redistributed.

## Model validation and guardrails

Tests check analytic beta recovery, signed caps, constant-variance rejection, non-overlapping windows, future-data isolation, cost monotonicity, reproducibility, and invalid inputs. Costs are applied once at each hedge reset. **Arithmetic P&L is a teaching proxy, not a self-financing futures or securities ledger.** No margin, financing, contract multipliers, roll yield, execution timing, tax, corporate actions, basis risk, or hedge-instrument availability is modeled. Historical hedge ratios can be unstable, and the synthetic beta shift is not an observed 2020/2022 market episode.

**Acceptance:** Synthetic fixtures and tests only; licensed historical observations, actual release timestamps, exact-revision CI, independent model review, and production certification must be verified separately. Not financial advice.

**Next exercise:** Compare rolling hedge estimation windows and shrinkage against a no-hedge baseline using held-out regime-specific variance reduction and robust uncertainty intervals.
