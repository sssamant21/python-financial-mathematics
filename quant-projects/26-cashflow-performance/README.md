# Project 26 — Time-Weighted vs Money-Weighted Returns

**Business question:** How can a portfolio manager's investment performance differ from an investor's experience when cash is deposited or withdrawn?

This Python 3.11+ standard-library-only lab uses **hypothetical data**. No market download, brokerage connection, trade, or investment advice.

## Timing and mathematics

For period i, starting NAV is V(i-1), external cash contribution C(i) occurs **at period start**, and ending NAV is V(i). Positive C is a deposit; negative C is a withdrawal. The period growth factor is g(i) = V(i) / (V(i-1) + C(i)). The cumulative **time-weighted return** (TWR) is product(g(i)) - 1. This strips out external cash flows under the stated valuation convention.

For **money-weighted return** (MWR), define investor cash flows at integer period boundaries: at t=0, -V(0)-C(1); at t=i for 1<=i<n, -C(i+1); and at t=n, +V(n). Solve sum(CF(t)/(1+r)^t)=0 for periodic r > -1. The lab uses bounded bisection, returning `None` for intermediate withdrawals that could produce multiple roots. MWR is **per period** while TWR is **cumulative**, so they must not be compared directly without aligning horizons (e.g., compound periodic MWR for n periods).

## Reproduce

```bash
cd quant-projects/26-cashflow-performance
python -m unittest -v test_performance.py
python -m compileall -q performance.py test_performance.py
python performance.py
```

Synthetic two-period example: start NAV 100; first-period ending NAV 120 (+20%); contribute 100 at the start of period two; second-period ending NAV 198 (-10%). Cumulative TWR = +8%; periodic MWR approximately -0.6682%, implying a two-period money-weighted return of approximately -1.332%. The larger capital allocation experienced the loss, despite positive time-weighted performance.

## Guardrails and limits

Reject nonfinite/boolean values, nonpositive post-flow capital, zero or negative ending NAV, mismatched histories, and more than 10,000 periods. Return `None` instead of guessing an IRR when intermediate investor withdrawals occur or a finite bracket cannot be established. The restricted cash-flow pattern is a deliberate educational simplification; real IRR/XIRR tools must handle multiple roots, irregular dates, taxes, fees, stale valuations, and intra-period flows. No point-in-time data or historical return claims are made.

Ten deterministic local tests, compilation, and synthetic CLI passed on 2026-11-11 against prepared source. **Exact published-revision hosted CI, independent review, and production certification remain unverified** until independently checked.

## Dated XIRR extension

For irregular dates, periodic IRR is not annualized by assuming equal spacing. Dated XIRR solves the investor-perspective discounted cash-flow equation:

`0 = sum(CF_i / (1+r)^((date_i-date_0)/365))`.

The implementation uses an equivalent terminal-value equation with bounded bisection, strict ISO date ordering, a fixed 365-day annualization convention, and a restricted uniquely rooted cash-flow pattern (initial investment, additional contributions, final liquidation). Intermediate withdrawals/distributions are deliberately suppressed as `None`, rather than guessing a root. It is not a general commercial XIRR solver.

```bash
cd quant-projects/26-cashflow-performance
python -m unittest -v test_performance.py test_dated_xirr.py
python -m compileall -q performance.py dated_xirr.py test_performance.py test_dated_xirr.py
python dated_xirr.py
```

A synthetic 2024-01-01 / 2024-07-01 / 2025-01-01 contribution example (`[-100,-50,170]`) yields approximately **16.0552% annualized XIRR**. Holding dates and terminal value fixed while shifting the additional deposit earlier versus later changes XIRR. The dates are invented fixture dates, **not market observations**. The 11 extension tests passed locally against a functionally equivalent prepared implementation on 2026-11-11, alongside compilation and CLI; exact GitHub revision hosted CI and independent review remain unverified.
