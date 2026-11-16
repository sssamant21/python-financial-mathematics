# Project 40 — Plain-vanilla interest-rate swap valuation

**Goal.** Understand the cash-flow and present-value mechanics of a spot-start, fixed-for-floating interest-rate swap using a hypothetical discount curve. This standard-library-only exercise is educational, not a market pricing or trading engine.

## Business and mathematical context

A borrower with floating-rate debt might examine a **pay-fixed/receive-floating** swap to understand fixed-rate exposure. A receiver of fixed payments takes the opposite sign. This exercise values both legs at time zero without exchanging notional.

With positive notional `N`, fixed coupon rate `K`, accrual fractions `a_i`, and discount factors `D_i` for payment dates `t_i`:

```text
A = sum_i(a_i * D_i)              # fixed-leg annuity
PV_fixed = N * K * A
PV_float = N * (1 - D_last)       # spot-start, single-curve telescoping
K_par = (1 - D_last) / A
PV_pay_fixed = PV_float - PV_fixed
PV_receive_fixed = -PV_pay_fixed
```

The floating-leg identity assumes `D(0)=1`, a swap starting **today**, the same curve for projecting and discounting floating coupons, matching payment periods, no spreads, and no principal exchange. Negative implied rates and discount factors above one are allowed. The implementation accepts explicitly supplied year fractions rather than silently choosing day-count conventions.

## Reproduce (Python 3.11–3.13, standard library only)

From this directory:

```bash
python -m unittest -v test_swap.py
python -m compileall -q swap.py test_swap.py
python swap.py
python swap.py --receive-fixed
```

The fixed four-period example uses half-year accruals and hypothetical discount factors `[0.98, 0.96, 0.94, 0.92]`. Its par fixed rate is approximately 4.210526%, and the pay-fixed value at 4% is +4,000 for 1,000,000 notional. These are synthetic calculations, not market observations.

## Validation, limits and guardrails

Seven deterministic tests check the par zero-PV identity, payer/receiver symmetry, independent coupon sum, fixed-rate direction, negative rates, input rejection, and a one-period cash-flow identity. Inputs must have matching nonempty schedules, positive finite accruals/discount factors and notional, and finite fixed rate. Extreme finite inputs producing nonfinite outputs are rejected. No market data, third-party redistribution, credentials, brokerage or live trades are involved.

**Not modeled:** multi-curve projection and collateral discounting, historical fixings, forward-starting swaps, reset/payment lags, holiday calendars, day-count conventions, stub periods, credit/funding adjustments, basis, bid/ask, counterparty exposure or calibration. No survivorship or look-ahead claims arise from the synthetic fixture; a real-data extension would need point-in-time provenance and release-date discipline. Local synthetic test success does **not** establish exact-published-revision CI acceptance, independent model review, or production certification.

**Next exercise:** validate an independently constructed period-by-period floating coupon schedule and sensitivity to curve bumps; compare the telescoping identity against explicitly projected forwards.

## Independent cash-flow reconciliation and curve sensitivity

The extension `test_curve_reconciliation.py` independently constructs each floating coupon using `F_i=(D_{i-1}/D_i-1)/a_i`, with `D_0=1`, then discounts it by `D_i`. The sum telescopes to `N(1-D_last)` only under the stated single-curve, spot-start assumptions. Six deterministic tests cover coupon-by-coupon reconciliation, negative forwards, uneven accruals, par valuation, and independent terminal/interior discount-factor bumps. An interior bump changes fixed-leg PV but leaves telescoping floating-leg PV unchanged; a terminal bump changes both. This is not a multi-curve or real-market sensitivity model.

Run from this folder:

```bash
python -m unittest -v test_swap.py test_curve_reconciliation.py
python -m compileall -q swap.py test_swap.py test_curve_reconciliation.py
```

Six extension tests passed locally against a source-equivalent copy of the published `swap.py` implementation on 2026-11-16; full exact-GitHub-source integration and hosted CI for the extension remain unverified. The extension uses only the Python standard library and synthetic inputs.

Two additional synthetic regression cases check linear notional scaling, pay/receive sign symmetry at a non-par strike, and rejection of finite inputs whose intermediate present values overflow. Run the same combined `unittest` command above (15 total test methods). The two added checks passed locally against a manually reconstructed, source-equivalent implementation on 2026-11-16; exact published-source and hosted execution of the expanded suite remain unverified.
