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

Rates are continuously compounded and use a user-provided year fraction. The implementation rejects nonfinite inputs, rates outside [-100%, +100%], tenors outside (0, 100] years, and extreme absolute rate-differential times tenor above 50; it does not download quotes or place trades. A live market comparison would require **licensed** timestamped spot and forward bid/ask quotes, tenor-specific deposit/funding rates, cross-currency basis, calendar/day-count, collateral/CSA, settlement and credit assumptions. All inputs must be available as of the valuation timestamp to prevent look-ahead. There is no historical portfolio universe, so survivorship bias is not evaluated. Real-market calibration, exact-revision hosted CI, independent mathematical review and production readiness remain **unverified**.

**Next validation:** check funding-side bid/ask conventions and collateral basis sensitivity with separately sourced, appropriately licensed data. This lab is educational, not financial advice.


## Extension — funding-side asymmetry and basis sensitivity (synthetic)

`funding_basis.py` adds a conservative **illustrative interval** rather than an executable arbitrage bound. With spot bid/ask `S_b/S_a`, domestic lending/borrowing rates `d_l/d_b`, foreign lending/borrowing rates `f_l/f_b`, and explicitly assumed additive basis-premium scenarios `b_l/b_h`:

`F_low = S_b exp[(d_l - f_b + b_l)T]` and
`F_high = S_a exp[(d_b - f_l + b_h)T]`.

The direction of the rates reflects conservative financing assumptions. The basis parameter is **not** a market-calibrated cross-currency basis swap quote. Funding, collateral, FX swaps and credit conventions differ across real markets; these endpoints are scenario illustrations only. No arbitrage conclusion should be drawn from a disjoint market quote.

For `F(b)=S exp[(r_d-r_f+b)T]`, the analytical sensitivity is `dF/db = T F`. The code reports a finite one-basis-point shift alongside the derivative to check numerical consistency.

```bash
cd quant-projects/43-fx-forward-parity
python -m unittest -v test_fx_forward.py test_funding_basis.py
python -m compileall -q fx_forward.py funding_basis.py test_fx_forward.py test_funding_basis.py
python funding_basis.py
```

Nine additional deterministic regression cases check zero-spread parity, interval widening, basis shocks, analytical derivatives, bounded inputs and overflow. Standard library only, Python 3.11–3.13. **The extension tests have been authored but not yet executed on the published revision; hosted CI and independent review remain unverified.** A real-market study needs licensed timestamped two-sided quotes and consistent funding/collateral terms before any empirical comparison.

### Exponent-boundary regression checkpoint (2026-11-17)

Added a deterministic test for basis-adjusted exponent guardrails: an in-range positive basis bump must remain finite, while a scenario exceeding the classroom exponent limit must raise `ValueError`. The combined Project 43 suite now contains **20 authored tests** (9 base, 11 funding/basis). The existing dedicated CI workflow invokes both test modules, but this newly published test has **not been executed on its exact revision**; CI outcome, independent review, and licensed-market validation remain unverified.

### Tiny-bump numerical stability (2026-11-17)

`basis_sensitivity` now computes the positive basis-bump difference as `F * expm1(bump_bp * 1e-4 * T)` rather than subtracting nearly equal forward levels. It still checks the bumped exponent against the existing ±50 classroom limit. A new deterministic regression test covers a `1e-8` basis-point bump against the analytical `expm1` identity. **21 Project 43 tests are now authored (9 base, 12 funding/basis); the new exact-revision hosted CI result is pending.** The arithmetic identity was checked separately with local Python, but the repository test suite was not executed locally because GitHub DNS resolution failed. Licensed-market calibration, independent review, and production certification remain unverified.
