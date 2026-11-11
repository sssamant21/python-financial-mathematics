# Project 23 — Downside Risk, Sortino Ratio, and Omega Ratio

**Business question:** Two hypothetical portfolios can have the same average return but very different shortfall exposure. How do we describe losses below a predeclared minimum acceptable return (MAR), without treating upside volatility as downside risk?

This is a **synthetic, ex-post, educational** Python 3.11+ lab. No market downloads, broker connectivity, investment recommendations, or third-party datasets.

## Mathematics and conventions

For simple returns `r_t` and a **per-observation** target `m`, let `d_t = r_t - m` and `L_t = max(m-r_t, 0)`. With `n` observations:

- Downside deviation: `DD = sqrt(sum(L_t^2)/n)`. The denominator is **all n observations**, not only negative observations; this is the population lower-partial-moment convention.
- Arithmetic annualized excess: `A = P * mean(d_t)`, where `P` is periods per year.
- Annualized downside deviation: `DD_a = sqrt(P) * DD`.
- Sortino ratio: `A / DD_a` when `DD > 0`, otherwise `None`.
- Omega ratio: `sum(max(d_t, 0)) / sum(max(-d_t, 0))` when total shortfall is positive, otherwise `None`.
- Shortfall frequency: number of `r_t < m` divided by `n`.

**Important:** This is a chosen arithmetic annualization convention, not a compounded performance measure. Square-root scaling assumes a stability structure that may fail under serial dependence. Omega and Sortino are descriptive sample ratios, not estimates of future skill. A zero denominator is *undefined*, not infinite or guaranteed safe.

## Reproduce

From the repository root:

```bash
cd quant-projects/23-downside-risk-ratios
python -m unittest -v test_downside_risk.py
python -m compileall -q downside_risk.py test_downside_risk.py
python downside_risk.py
```

The implementation and tests use only the Python standard library. Project-wide dependencies are defined separately in `quant-projects/requirements.txt`; no additional package is required here.

## Exercise

Compare the same synthetic monthly returns at predeclared monthly targets of 0% and 0.5%, then examine trailing four-month windows. Report how target choice affects the downside deviation, Sortino, Omega, and shortfall frequency. The trailing values use only observations ending at their labeled index; **do not** interpret them as held-out forecasts.

## Guardrails and limitations

Require at least three finite simple returns (each >= -100%), a finite per-period target greater than -100%, integer annualization frequency 1–366, and trailing windows of at least three observations. Missing data, timestamp alignment, currency conventions, corporate actions, stale prices, sample selection, transaction costs, and nonstationarity require separate review. Do not optimize the target after inspecting outcomes or confuse a monthly MAR with an annual MAR. No look-ahead inputs are used by the implementation; this alone does not establish point-in-time validity for real data.

## Validation status

Ten deterministic synthetic `unittest` cases are authored, including exact numerical identities, zero downside, all-loss samples, target and frequency sensitivity, future-mutation isolation, and invalid-input rejection. **Hosted CI and exact published-source runtime execution remain unverified until observed.** Historical calibration, independent model review, and production certification are not claimed.
