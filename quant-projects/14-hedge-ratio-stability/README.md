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

## Window and shrinkage sensitivity

Run `python sensitivity.py --seed 14` and `python -m pytest -q test_sensitivity.py`.
This second lab uses common held-out origins for 26/52/78-week training windows and
fixed 0/50/100% shrinkage of the sample asset–hedge covariance toward zero.
The estimator is `h = clip((1 - shrinkage) Cov(A,H) / Var(H), -2, 2)`.
Shrinking covariance toward zero is an explicit *hedge attenuation assumption*,
not a generally optimal covariance estimator. Each 13-week forward window is
non-overlapping; no forward returns enter ratio estimation. Variance reduction
is measured ex post against the unhedged asset, and early/late synthetic
regimes are descriptive, not estimated change points.

Do not select the best configuration on the same held-out blocks and call it
out-of-sample validated. The grid is a sensitivity exercise, not a nested
selection protocol. No bootstrap confidence coverage, margin ledger,
licensed 2020/2022 data, or independent review is claimed.

## Regime-specific block-bootstrap uncertainty (descriptive)

Run `python regime_uncertainty.py --seed 14` and `python -m pytest -q test_regime_uncertainty.py`.
For the **predeclared** 52-week, zero-shrinkage estimator, `block_intervals` resamples complete, non-overlapping 13-week held-out variance-reduction scores **within** each synthetic early/late regime. For regime `g`, its reported point estimate is the mean of block scores, `mean(VR[g, j])`; percentile limits come from seeded bootstrap resampling of whole block scores. At least three usable blocks per regime are required; otherwise results are marked insufficient, never silently fabricated. The intervals are descriptive sampling-sensitivity summaries, **not** calibrated future prediction intervals, proof of 95% coverage, or evidence of real 2020/2022 stress performance. Adjacent blocks may still be dependent, and the early/late label is known only in the synthetic generator. No parameter is selected on the held-out observations.
