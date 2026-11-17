# Project 44 — Credit default swap (CDS) par spread, synthetic fundamentals

**Business question:** What annual premium rate approximately balances a CDS protection buyer's expected premium payments and default-contingent protection?

## Model and conventions

Use a flat continuously compounded risk-free rate `r`, constant default hazard `h`, recovery fraction `R`, and quarterly scheduled premiums. Survival through time `t` is `Q(t)=exp(-h*t)`. On a payment grid `t_i` with interval `dt`:

- Premium annuity per unit notional: `A = sum(dt * exp(-r*t_i) * Q(t_i))`.
- Protection present value: `P = N*(1-R)*sum(exp(-r*t_i)*(Q(t_(i-1))-Q(t_i)))`.
- Par running spread: `s = P/(N*A)`; multiply by 10,000 for basis points.

This is a **discrete interval-end default-settlement approximation**, not a standard CDS market pricer. It omits accrued premium on default, standard coupons/upfronts, settlement calendars, curve bootstrapping, counterparty risk, and market conventions. It is not a trade or investment recommendation.

## Run

Python 3.11–3.13, standard library only; no dependencies, credentials, downloads or market data.

```bash
cd quant-projects/44-credit-default-swap-basics
python cds.py
python cds.py --hazard 0.05 --recovery 0.25
python -m unittest -v test_cds.py
python -m compileall -q cds.py test_cds.py
```

The ten deterministic synthetic tests cover zero hazard, full recovery, monotonic hazard/recovery responses, notional scaling, survival and leg reconciliation, low-hazard approximation, payment frequency and invalid inputs.

## Validation and limits

No historical market observations or third-party data are distributed. For empirical work, obtain appropriately licensed point-in-time CDS quotes, risk-free curves, recovery assumptions, and obligor reference-entity information with timestamps. Compare at a pinned valuation date, record quote conventions, and avoid selecting surviving issuers after the fact. A flat hazard/recovery model is insufficient for production valuation or risk. **Runtime tests, exact-revision CI, independent mathematical review and market calibration remain unverified until executed and inspected.**
