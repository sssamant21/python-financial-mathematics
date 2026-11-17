# Project 41 — Bootstrapping an annual discount curve from par swap rates

**Goal:** Convert hypothetical annual-pay par swap quotes into discount factors, reprice the quotes, and inspect one-year implied forwards. This is a deliberately simplified, single-curve, spot-start educational model; it is **not** a market curve builder.

## Business context and math

A par fixed-for-floating swap has zero value at inception. For maturity year `n`, annual accrual fractions of 1, and discount factors `D_i`, the par fixed rate `S_n` satisfies:

```text
S_n * (D_1 + ... + D_n) = 1 - D_n
D_n = (1 - S_n * sum(D_i, i=1..n-1)) / (1 + S_n)
F_(n-1,n) = D_(n-1) / D_n - 1; D_0 = 1
```

The sequential recurrence uses only quotes up to each maturity, so there is no future-market-data leakage. A negative interest rate may produce a discount factor above 1; do not reject that solely because it exceeds 1. Reject nonpositive discount factors and nonfinite arithmetic. The model does **not** impose monotonic discount factors.

## Reproduce

Python 3.11–3.13, **standard library only**, no installation or external datasets:

```bash
cd quant-projects/41-par-swap-curve-bootstrap
python -m unittest -v test_curve.py
python -m compileall -q curve.py test_curve.py
python curve.py
python curve.py --rates 0.02 0.025 0.03
```

The default synthetic 3%, 3.5%, 4% par quotes produce approximately 0.970874, 0.933352, 0.888299 annual discount factors. These are mathematical examples, not observed market quotes.

## Model validation and limitations

Seven deterministic tests check flat-curve closed-form values, input quote repricing, discount/forward consistency, negative-rate handling, invalid inputs, and discount-factor validation. Local tests and compilation were executed successfully on 2026-11-16 against a locally prepared copy; **exact published-revision CI and independent review remain unverified**.

This bootstrap assumes one quote for each consecutive annual maturity, no stubs, fixed annual accrual of one, start today, single-curve projection/discounting, no spreads or notional exchange. It omits day-count rules, calendars, coupon dates, deposits/OIS instruments, interpolation, collateral, multi-curve projection, bid/ask, quote uncertainty, and curve arbitrage diagnostics. A production curve requires instrument conventions, point-in-time sourced quotes, robust calibration and independent validation. No trading advice or broker connectivity is included.

**Next exercise:** verify the expanded tests on exact published-source GitHub Actions CI, then examine realistic instrument conventions before Project 42.

## Independent cash-flow reconciliation and quote sensitivity

For unit notional and one-year periods, the discounted floating coupon in period `i` is `D_i * F_(i-1,i) = D_(i-1) - D_i`. Summing the coupons telescopes to `1 - D_n`, independently of the fixed-leg par-rate formula. The fixed leg is `S_n * sum(D_i)`; the difference should be zero for every quoted maturity. Negative coupons are possible when forwards are negative.

A one-basis-point quote bump is `0.0001` in decimal-rate units. Bump **one par quote at a time**, rebuild the entire curve, and check that each bumped quote reprices. Earlier discount factors must be invariant to later quote changes (triangular bootstrap). This is a numerical quote-sensitivity exercise, **not** a calibrated market DV01: conventions, hedging instruments, multi-curve discounting and real quotes are absent.

```bash
cd quant-projects/41-par-swap-curve-bootstrap
python -m unittest -v test_curve.py test_reconciliation.py
python -m compileall -q curve.py test_curve.py test_reconciliation.py
python curve.py --rates 0.02 0.035 0.04 0.037
```

The six new tests use deterministic hypothetical quotes and require no third-party dependencies. The original seven tests remain unchanged. **Execution and exact-revision hosted CI of the expanded 13-test suite are pending verification**; independent model review and market calibration are unverified.
