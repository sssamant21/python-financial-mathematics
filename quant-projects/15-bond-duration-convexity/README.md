# Project 15 — Bond Duration, Convexity and Yield-Shock Stress

**Business question:** How much might a fixed-rate bond's theoretical value change when market yields rise or fall? This is an educational interest-rate risk lab, not a bond recommendation or trading system.

## Valuation and mathematics

For annual end-of-year coupons, face value `F`, coupon rate `c`, maturity `T` years, and a **flat annual yield** `y > -100%`:

`P(y) = sum[t=1..T] (F*c + F*1[t=T]) / (1+y)^t`.

Macaulay duration is the present-value-weighted average payment time. Modified duration is `Dmod = Dmac/(1+y)`. Convexity is `C = sum[t(t+1)*CF_t/(1+y)^(t+2)] / P`.

For a **predeclared** parallel yield shock `dy`, compare exact repricing `P(y+dy)/P(y)-1` with duration approximation `-Dmod*dy` and second-order approximation `-Dmod*dy + 0.5*C*dy^2`. One basis point (bp) is 0.0001 in yield units.

## Reproduce

Python 3.11+, standard library only for the model; install repository test dependencies using `python -m pip install -r quant-projects/requirements.txt` from repository root, then:

```bash
cd quant-projects/15-bond-duration-convexity
python bond_lab.py --face 1000 --coupon 0.04 --years 5 --yield-rate 0.05
python -m pytest -q test_bond_lab.py
```

The default scenario prices a **hypothetical** five-year 4% annual-coupon bond at 5% yield and applies fixed -200/-100/+100/+200 bp parallel shocks. No third-party data, security identifiers, live orders, or market forecasts are used.

## Guardrails and model validation

Tests verify par pricing, zero-coupon analytical duration, cash-flow timing, monotonic yield-price response, duration finite differences, convexity approximation, zero shock, and invalid inputs. The scenario grid is predeclared; no hindsight optimization or market-data selection occurs.

**Important limits:** Flat yield-to-maturity discounting is not a full spot-curve valuation. This lab excludes accrued interest, day count, coupon frequency other than annual, yield-curve twists, credit/spread risk, optionality, liquidity, taxes, defaults, financing, and settlement. Duration/convexity approximations deteriorate for large shocks and nonparallel changes. A negative shocked yield below -100% is rejected. All results are hypothetical, not historical 2020/2022 evidence.

**Acceptance:** Synthetic mathematical checks only. Published-revision CI, licensed historical validation, independent review, and production readiness must be verified separately. Not financial advice.

**Next exercise:** Extend to a multi-bond portfolio with key-rate shocks and curve steepening/flattening, and compare parallel-duration approximation with exact repricing.
