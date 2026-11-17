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

**Next exercise:** independently reconcile period cash flows and test sensitivity to individual par quotes, then add a dedicated hosted CI step.
