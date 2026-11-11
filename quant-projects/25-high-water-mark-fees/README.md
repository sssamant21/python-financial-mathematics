# Project 25 — High-Water-Mark Performance Fee Accounting

**Business question:** How do management fees, performance fees and a high-water mark affect an investor's net asset value after losses and recoveries?

This is a **synthetic-only, educational** Python 3.11+ lab. It uses only the standard library, no external prices, credentials, broker connections or investment recommendations.

## Mathematical convention

At period start, let net NAV be \(N_{t-1}\), gross simple return \(r_t\), annual management rate \(m\), fee periods per year \(k\), performance fee fraction \(p\), and prior net high-water mark \(H_{t-1}\).

1. Pre-fee NAV: \(G_t=N_{t-1}(1+r_t)\).
2. Management fee: \(M_t=\min(G_t,N_{t-1}m/k)\), so it cannot exceed remaining NAV.
3. After-management NAV: \(A_t=G_t-M_t\).
4. Performance fee: \(F_t=p\max(0,A_t-H_{t-1})\).
5. Ending net NAV: \(N_t=A_t-F_t\); updated high-water mark: \(H_t=\max(H_{t-1},N_t)\).

**Important:** This lab crystallizes performance fees **every period**, uses a net-of-fee HWM, has **no hurdle rate**, and does not reset the HWM. Actual fund contracts may use different fee bases, crystallization dates, equalization, subscriptions, redemptions, tax and loss-carryforward rules. The model is not a fund NAV accounting system.

## Reproduce

From the repository root:

```bash
cd quant-projects/25-high-water-mark-fees
python -m unittest -v test_fee_lab.py
python -m compileall -q fee_lab.py test_fee_lab.py
python fee_lab.py
```

The CLI uses four hypothetical period returns (+10%, -15%, +12%, +8%) and zero management fee to make the HWM effect visible. The first period charges a 2.000 performance fee on a starting NAV of 100; after the drawdown, no further performance fee is charged until net NAV exceeds the previous 108 HWM. The last period incurs approximately 0.608 in performance fees. These are invented observations, not historical performance.

## Validation and limitations

Ten deterministic `unittest` cases, compilation and the CLI demonstration passed in an isolated local run on 2026-11-11. **Exact published-revision hosted CI, independent model review and production certification remain unverified.** Tests cover first gains, drawdowns, recovery, fee order, zero returns, total loss, invalid input and determinism.

Inputs require a nonempty list or tuple of finite numeric simple returns (each at least -100%), positive finite initial NAV, valid fee rates, and a positive integer period frequency. Boolean inputs, oversized histories and nonfinite NAV are rejected. There is no market-data download or redistribution, no point-in-time asset universe, no future-data-driven strategy and no trading execution.

**Next extension:** compare monthly versus annual crystallization and introduce a clearly specified hurdle convention, with reconciliation tests.
