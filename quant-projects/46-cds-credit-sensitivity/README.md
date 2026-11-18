# Project 46 — Synthetic CDS present value and credit sensitivity

**Business question:** How does a protection buyer's simplified CDS value change when assumed default intensity, recovery, or the contractual coupon changes? This lab extends Project 45 from curve calibration to *position risk*, using a flat synthetic hazard assumption and no external market data.

## Math and conventions

For annualized hazard `h`, flat continuously compounded discount rate `r`, coupon frequency `f`, and payment dates `t_i=i/f`, survival is `Q(t)=exp(-h*t)` and discount factor `D(t)=exp(-r*t)`. The premium annuity per unit notional is `A=sum D(t_i)*Q(t_i)/f`. The protection leg is `P=(1-recovery)*sum D(t_i)*(Q(t_{i-1})-Q(t_i))`. The **protection-buyer** value is `N*(P-coupon*A)`, and the par spread is `P/A`. These calculations use interval-end default settlement, omit accrued-on-default premium, and are **not** market-standard ISDA CDS valuation.

A one-basis-point *contract coupon* increase changes protection-buyer PV by exactly `-N*A*0.0001` when the hazard curve is held fixed. The separately reported `hazard01` is a central finite-difference change for a one-basis-point increase in **annual hazard intensity** (forward difference at zero). It is **not** market-quote CS01: a quote-based CS01 would require repricing and recalibrating a curve from bumped market quotes.

## Run (Python 3.11–3.13; standard library only)

```bash
cd quant-projects/46-cds-credit-sensitivity
python cds_risk.py
python -m unittest -v test_cds_risk.py
python -m compileall -q cds_risk.py test_cds_risk.py
```

The CLI prints synthetic PV, par spread in basis points, coupon DV01 and hazard01. No provider data, trading integration, downloads, credentials, or nonstandard packages are required. Input validation rejects booleans, nonfinite inputs, nonpositive notional, invalid recovery, and coupon-grid misalignment. Notional is capped at one trillion, hazard at 5/year; a bump crossing the upper hazard bound is rejected.

## Validation evidence and limitations

Seven deterministic tests **passed locally on 2026-11-18** (`python -m unittest -q`), together with Python compilation and a CLI smoke test on source-equivalent code. Tests check zero par PV, zero-hazard protection, exact coupon DV01, hazard sensitivity direction, boundary finite differences, recovery monotonicity, and invalid-input rejection. **Exact published-revision GitHub Actions, licensed-market calibration, and independent mathematical review are unverified.** No production certification or financial recommendation is implied. For future empirical studies, obtain authorized point-in-time CDS quotes, document convention versions, timestamp observations, and do not redistribute unlicensed quotes.

## Analytical and boundary regression extension (2026-11-18)

Four additional standard-library tests cover the closed-form flat-hazard par spread `s=(1-recovery)*frequency*expm1(hazard/frequency)` across nine synthetic cases, linear notional scaling of PV and sensitivities, rejection of a hazard bump beyond the supported upper bound, and the explicit forward difference at zero hazard. Run `python -m unittest -v test_cds_risk.py` from this directory. The four checks passed in a local source-equivalent standalone execution; **the expanded 11-test suite and exact published GitHub Actions revision have not yet been verified**. This discrete-coupon identity does not establish ISDA pricing equivalence, quote-based CS01, or independent model validation.
