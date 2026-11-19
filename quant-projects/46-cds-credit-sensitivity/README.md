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

The original seven deterministic tests passed locally on source-equivalent code on 2026-11-18. The subsequently expanded 13-test `test_cds_risk.py` suite passed on GitHub Actions [run 44387307924](https://github.com/sssamant21/python-financial-mathematics/actions/runs/44387307924), commit `2eaec784`; Python compilation and synthetic CLI also passed in that job. This **does not verify** the newer eight-test `test_quote_cs01.py` extension or the combined 21-test suite at the latest revision. Licensed-market calibration and independent mathematical review remain unverified. No production certification or financial recommendation is implied. For future empirical studies, obtain authorized point-in-time CDS quotes, document convention versions, timestamp observations, and do not redistribute unlicensed quotes.

## Analytical and boundary regression extension (2026-11-18)

Four additional standard-library tests cover the closed-form flat-hazard par spread `s=(1-recovery)*frequency*expm1(hazard/frequency)` across nine synthetic cases, linear notional scaling of PV and sensitivities, rejection of a hazard bump beyond the supported upper bound, and the explicit forward difference at zero hazard. Run `python -m unittest -v test_cds_risk.py` from this directory. The four checks passed in a local source-equivalent standalone execution; **the expanded 11-test suite and exact published GitHub Actions revision have not yet been verified**. This discrete-coupon identity does not establish ISDA pricing equivalence, quote-based CS01, or independent model validation.

## Single-tenor quote-based CS01 extension (2026-11-18)

`quote_cs01.py` recalibrates a **flat hazard rate from a single synthetic par CDS quote** using the exact discrete-coupon identity `spread=(1-recovery)*frequency*expm1(hazard/frequency)`. It bumps the **quoted spread**, recalibrates the hazard, and reprices a fixed-coupon protection-buyer contract. `quote_cs01` is the PV change per **+1 bp quoted spread**, estimated with a central difference (one-sided near zero). This is different from `hazard01`, which directly bumps default intensity. The exercise assumes the same recovery, discount rate, maturity and coupon grid for calibration and valuation; it is not a multi-tenor curve or ISDA-standard market CS01.

```bash
python -m unittest -v test_cds_risk.py test_quote_cs01.py
python -m compileall -q cds_risk.py quote_cs01.py test_cds_risk.py test_quote_cs01.py
python quote_cs01.py
```

Eight new deterministic tests cover quote/par calibration, at-par PV, quote sensitivity, independent repricing, zero-quote forward differences, notional scaling, near-zero handling, and invalid-input guardrails. **The new suite and exact-revision hosted CI have not yet been verified**; previous 13/13 results apply only to the older baseline revision. No external data, independent mathematical review, or production certification.

## Multi-tenor quote-recalibrated bucket CS01 (2026-11-19)

`multi_tenor_cs01.py` extends the simplified quarterly-coupon CDS model to a **piecewise-constant hazard curve** calibrated sequentially from synthetic 1-, 3-, and 5-year par quotes. Each bucket CS01 bumps one quote, recalibrates **all** hazard segments, and reprices the unchanged protection-buyer contract. `parallel_sum` sums bucket derivatives; it is a first-order parallel-shift approximation, not an exact finite-shock P&L. Zero quotes use forward differences. Infeasible bumped curves raise an error rather than silently using negative hazards.

The premium leg is `A = Σ D(t_i)Q(t_i)/f`, protection leg `P = (1-R)Σ D(t_i)(Q(t_{i-1})-Q(t_i))`, and PV `N(P-cA)`. No ISDA calendars, accrued-on-default, upfronts, credit-risk discounting or real-market data are modeled. The bisection tolerance is educational, and numerical derivative stability should be assessed across multiple bump sizes.

```bash
cd quant-projects/46-cds-credit-sensitivity
python multi_tenor_cs01.py
python -m unittest -v test_multi_tenor_cs01.py
python -m compileall -q multi_tenor_cs01.py test_multi_tenor_cs01.py
```

Seven synthetic unittest methods are authored for quote reproduction, bucket aggregation, scaling, one-sided zero quotes, infeasibility and malformed inputs. **Execution and exact-revision hosted CI are not verified** for this extension. The previous hosted evidence applies only to earlier revisions. Independent mathematical review, licensed-market validation, and production certification remain outstanding.
