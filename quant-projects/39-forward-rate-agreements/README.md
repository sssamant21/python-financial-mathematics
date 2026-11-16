# Project 39 — Forward Rate Agreements (FRA): discount factors, settlement and PV

**Purpose.** Learn how a fixed-versus-floating forward rate agreement converts a discount curve into a forward interest rate and a hypothetical present value. This is a small **standard-library-only** pricing lab, not a trading or production valuation engine.

## Business context and conventions

A corporate treasurer may want to understand sensitivity to a future borrowing rate. A receive-floating/pay-fixed FRA increases in value when the implied future floating rate rises relative to the agreed fixed rate. The opposite position has the opposite sign. The toy model assumes one future accrual period, deterministic discount factors, and an internally consistent curve.

Let `D(t1)` and `D(t2)` be time-zero discount factors, with `t2 > t1`, and let `a > 0` be the specified accrual year fraction. Under simple-compounding conventions:

```text
F = (D(t1) / D(t2) - 1) / a
settlement_at_t1 = N * a * (F - K) / (1 + F*a)
PV_at_t0 = settlement_at_t1 * D(t1)
         = N * (D(t1) - D(t2) * (1 + K*a))
```

Here `N` is positive notional, `K` is the agreed simple fixed rate, and `F` is the curve-implied forward. The settlement convention is **at the start of the accrual period**. Negative implied forward rates are permitted; discount factors must remain positive. A `--pay-floating` position flips the sign. This is not a quote for any specific market FRA tenor or day-count convention.

## Reproduce (Python 3.11–3.13; no third-party packages)

From this directory:

```bash
python -m unittest -v test_fra.py test_curve_sensitivity.py
python -m compileall -q fra.py test_fra.py test_curve_sensitivity.py
python fra.py --notional 1000000 --strike 0.04 --df-start 0.98 --df-end 0.96 --accrual 0.5
python fra.py --pay-floating
```

The default synthetic curve implies `F = (0.98/0.96 - 1)/0.5 ≈ 4.1667%`. At a 4% strike the receive-floating PV is positive. These values are **hypothetical**, not observed market rates.

## Validation and guardrails

Seven deterministic `unittest` methods check an independent algebraic PV identity, fair-strike zero PV, payer/receiver symmetry, strike direction, negative-rate handling, input validation and forward-ratio arithmetic. Invalid nonfinite/zero notional, accrual, or discount factors raise `ValueError`. The model does not infer accrual conventions from dates or calibrate discount curves. It also omits bid/ask, collateral/CSA discounting, credit/funding adjustments, payment delays, compounding differences, fixing calendars, day-count conventions, curve construction, market data and liquidity. **Passing synthetic tests is not independent model validation or production certification.**

No third-party market data, broker APIs, credentials or trading actions are used. The exact published-source CI and independent review must be verified separately.

## Independent curve-sensitivity exercise

`test_curve_sensitivity.py` adds five synthetic tests: a 60-digit `Decimal` PV reference grid, central finite-difference sensitivities to both discount factors and the fixed strike, payer/receiver sign symmetry, an equivalent end-of-period discounted cash-flow identity, and a negative-forward fair-strike case. For a receive-floating FRA, the algebraic PV is `N * (D1 - D2 * (1 + K*a))`; therefore `dPV/dD1 = N`, `dPV/dD2 = -N*(1+K*a)`, and `dPV/dK = -N*a*D2`. These are *partial* derivatives holding other inputs fixed, not a calibrated yield-curve parallel shift or key-rate DV01. The end-period cash flow is compared only as a mathematical equivalent under the same single-curve assumptions; real start-date fixing and payment conventions can differ. These checks do not cover live curves, CSA, basis, market conventions or independent certification.
