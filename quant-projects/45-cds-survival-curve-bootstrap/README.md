# Project 45 — Synthetic CDS survival-curve bootstrapping

**Business question:** Given synthetic CDS par spreads at several maturities, what nonnegative piecewise-constant default hazard rates reproduce those quotes?

## Mathematical model
Survival probability is \(Q(t)=\exp[-\int_0^t h(u)du]\). Each maturity introduces one new hazard segment. For quarterly payment times \(t_i\), the **simplified interval-end settlement** premium annuity is \(A=\sum_i \Delta t_i e^{-rt_i}Q(t_i)\), and the protection leg per unit notional is \(P=(1-R)\sum_i e^{-rt_i}[Q(t_{i-1})-Q(t_i)]\). The par running spread is \(s=P/A\). Solve each new segment's hazard with bracketed bisection, keeping earlier segments fixed.

This builds on Project 44 but solves an **inverse curve calibration problem** rather than pricing a single flat-hazard CDS. The simplified settlement convention excludes accrued premium on default, standard coupons/upfronts, calendars, ISDA conventions, counterparty risk and market calibration. A nonnegative solution may not exist for arbitrary quotes; reject infeasible inputs rather than inventing negative hazards. `max_hazard` must be finite and strictly positive (units: annualized intensity); zero-quote inputs still undergo contract validation, and an empty hazard curve is rejected.

## Reproduce (Python 3.11–3.13, standard library only)

```bash
cd quant-projects/45-cds-survival-curve-bootstrap
python bootstrap.py
python -m unittest -v test_bootstrap.py
python -m compileall -q bootstrap.py test_bootstrap.py
```

The CLI generates its own three-tenor synthetic quotes from known hazards, then recovers the original curve. No downloads, broker access, credentials, or trading actions.

## Validation and limitations
Eleven deterministic synthetic tests cover exact curve recovery, zero spreads, piecewise survival, infeasible quotes, invalid inputs, recovery sensitivity, coupon-grid alignment, nonfinite/nonpositive maximum hazard bounds, empty survival curves and invalid contract settings even for zero quotes. The original seven authored-source tests passed **7/7** locally on 2026-11-18, with compilation and CLI smoke checks. Four additional regression methods were published later; **the expanded eleven-test suite has not been executed locally or verified in hosted CI**. A network-isolated checkout attempt failed because `raw.githubusercontent.com` could not be resolved. Independent mathematical review is **unverified**. This is not a market-standard CDS curve bootstrap or production certification.

For later empirical study, source licensed point-in-time spreads, conventions, recovery assumptions and discount curves; pin observation timestamps, retain provenance, and avoid survivorship selection. Do not redistribute third-party quotes.
