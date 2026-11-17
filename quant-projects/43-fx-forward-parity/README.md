# Project 43 — FX forwards and covered-interest parity

**Business question:** Given an FX spot quote and domestic/foreign funding rates, what is the theoretical forward exchange rate, and what is the mark-to-market of an existing forward contract? This is a synthetic classroom valuation, **not** an executable arbitrage strategy.

## Conventions and mathematics

Let `S` be **domestic currency units per one foreign currency unit** (e.g., USD per EUR), `r_d` the domestic continuously compounded annual rate, `r_f` the foreign rate, and `T` the year fraction. In a frictionless world with matched collateral/funding assumptions, covered-interest parity gives:

`F = S exp[(r_d - r_f) T]`.

A contract **receiving N foreign units and paying K domestic units per foreign unit at T** has domestic present value

`V = N [S exp(-r_f T) - K exp(-r_d T)] = N exp(-r_d T)(F - K)`.

A newly agreed contract at `K=F` has zero theoretical initial value. A positive value is an asset to the receiving-foreign side. The simple bid/ask screen compares a forward bid/ask interval with spot-bid/ask-derived parity bounds under *identical illustrative rates*; it is **not** a tradable-arbitrage test because funding bid/ask, cross-currency basis, collateral, credit, taxes, settlement, capital and execution costs are excluded.

## Reproduce

Python 3.11–3.13; standard library only (no pip dependencies).

```bash
cd quant-projects/43-fx-forward-parity
python -m unittest -v test_fx_forward.py
python -m compileall -q fx_forward.py test_fx_forward.py
python fx_forward.py
python fx_forward.py --spot 1.2 --domestic-rate 0.05 --foreign-rate 0.03 --years 2
```

All inputs and nine regression tests are deterministic and synthetic. Tests cover closed-form parity, zero-rate spread, negative rates, discounted valuation reconciliation, notional/sign symmetry, bid/ask interval classification, and invalid-input rejection.

## Risk boundaries and model validation

Rates are continuously compounded and use a user-provided year fraction. The implementation rejects nonfinite, invalid, or unreasonably extreme inputs; it does not download quotes or place trades. A live market comparison would require **licensed** timestamped spot and forward bid/ask quotes, tenor-specific deposit/funding rates, cross-currency basis, calendar/day-count, collateral/CSA, settlement and credit assumptions. All inputs must be available as of the valuation timestamp to prevent look-ahead. There is no historical portfolio universe, so survivorship bias is not evaluated. Real-market calibration, exact-revision hosted CI, independent mathematical review and production readiness remain **unverified**.

**Next validation:** check funding-side bid/ask conventions and collateral basis sensitivity with separately sourced, appropriately licensed data. This lab is educational, not financial advice.
