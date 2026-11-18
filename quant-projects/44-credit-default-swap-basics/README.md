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


## Accrued-on-default extension (synthetic)

The optional `accrued_default.py` adds continuous default-time protection settlement and accrued running premium from the previous coupon date to default. With \(k=r+h\), each interval contributes \(h\int_0^{\Delta}u\exp[-k(t_{i-1}+u)]du\) to the accrued annuity. The par spread divides continuous-settlement protection PV by the sum of scheduled-survival and accrued premium annuities. The identity \(s=h(1-R)\) holds for a **continuous premium stream**, but is **not exact** here: scheduled coupons are paid only on survival at discrete payment dates. The independent numerical check therefore integrates default-time protection and accrual by midpoint quadrature, while retaining the discrete scheduled coupon sum. The implementation uses `expm1` and a near-zero series to limit cancellation.

```bash
python accrued_default.py
python accrued_default.py --hazard 0.05 --recovery 0.25
python -m unittest -v test_cds.py test_accrued_default.py
python -m compileall -q cds.py accrued_default.py test_cds.py test_accrued_default.py
```

The extension's nine deterministic test methods cover independent midpoint quadrature, protection-leg reconciliation, recovery, zero hazard, notional invariance, accrued annuity, baseline comparison and input rejection. All 19 baseline-plus-extension tests passed in [hosted run 44234866544](https://github.com/sssamant21/python-financial-mathematics/actions/runs/44234866544) at commit `4184fbf` (the log reports `Ran 19 tests` and `OK`); compilation and synthetic CLI checks also passed. This does not certify market conventions. An earlier test incorrectly asserted the continuous-premium identity for discrete scheduled coupons; it has been replaced by an independent quadrature comparison. The model is still not an ISDA-convention pricer; real CDS curves, accrual calendars, quote conventions, upfront amounts, licensed market data and independent model review remain outside scope.

## Validation and limits

No historical market observations or third-party data are distributed. For empirical work, obtain appropriately licensed point-in-time CDS quotes, risk-free curves, recovery assumptions, and obligor reference-entity information with timestamps. Compare at a pinned valuation date, record quote conventions, and avoid selecting surviving issuers after the fact. A flat hazard/recovery model is insufficient for production valuation or risk. **The corrected 19-test combined suite passed in hosted run 44234866544 at commit 4184fbf. This documentation update has not itself been validated in exact-revision CI. Independent mathematical review and market calibration remain unverified.**
