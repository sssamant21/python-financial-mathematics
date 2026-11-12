# Project 30 — Zero-Coupon Bond Carry and Roll-Down

**Question:** How much of a hypothetical bond's one-year mark-to-market change comes from passage of time versus moving down a fixed yield curve?

This educational exercise uses a **zero-coupon bond**, continuously compounded annual spot yields, and linear interpolation of spot yields. It deliberately excludes coupon accrual, default, bid/ask spreads, financing, reinvestment, taxes, calendars, and trading.

## Mathematics and business interpretation

A zero-coupon bond paying face value `F` in `T` years has present value `P(T)=F exp(-z(T)T)`, where `z(T)` is the annual continuously compounded spot rate. After holding `h` years, the remaining maturity is `T-h`.

- **Carry:** `F exp(-z(T)(T-h)) - P(T)`. This holds the original maturity's yield constant while time passes.
- **Roll-down:** `F exp(-z(T-h)(T-h)) - F exp(-z(T)(T-h))`. This assumes the **entire curve stays frozen** and the bond moves to a shorter tenor.
- **Curve shock effect:** Reprice at remaining maturity under a predeclared shocked curve, less frozen-curve repricing.

These components sum to scenario P&L. They are **accounting scenario decompositions**, not independently forecast returns or guaranteed profit. The curve shock is applied after the holding period; this is not a path simulation. No information from future periods is used.

## Reproduce (Python 3.11+, standard library only)

```bash
cd quant-projects/30-bond-carry-roll-down
python -m unittest -v test_carry_roll.py
python -m compileall -q carry_roll.py test_carry_roll.py
python carry_roll.py
```

All data are synthetic, with spot nodes at 1, 2, 3 and 5 years. There is no network download or dependency installation. Tests check exact node prices, interpolation, reconciliation, flat-curve behavior, upward yield shocks, invalid inputs and input immutability. Extrapolation beyond observed tenors is rejected, as are nonfinite rates, invalid maturities and zero/negative face values.

**Evidence boundary:** No actual 2020/2022 market episode, licensed data, independent bond model review, exact-revision hosted CI, or production certification is established by this initial implementation. The scenario is not investment advice. Next: add nonparallel curve-shock and holding-horizon sensitivity with independently calculated synthetic benchmarks.

## Nonparallel curve and horizon sensitivity extension (2026-11-12)

Run `python -m unittest -v test_sensitivity.py` and `python sensitivity.py` from this directory. The standard-library-only extension applies a **predeclared vector of absolute spot-yield shocks** at each tenor and linearly interpolates the resulting shocked curve. A bear steepener raises long-tenor yields more than short-tenor yields; a bull flattener lowers short-tenor yields more than long-tenor yields. Evaluate 0.5-year and 1-year holding horizons for the same three-year zero-coupon bond. All curves and dates are hypothetical.

For each scenario, **scenario P&L = carry + frozen-curve roll-down + curve-shock effect**, with all terms in face-value currency units. An interpolated 2.5-year remaining maturity under a +100 bp shock at the two-year node and zero shock at three years receives +50 bp; its independently calculated stressed price is `100 * exp(-0.0425 * 2.5)`. The test checks that benchmark, reconciliation, input immutability, invalid nodes and extreme/nonfinite shocks.

This is a terminal-horizon **static scenario**, not a realized path, forward-rate-implied forecast, or a claim of tradable carry. Shock sizes are capped at 2000 bps per node; shocked spot yields must satisfy the base pricing guardrails. Extrapolation remains prohibited. No market data, external model validation, transaction costs, or production certification is claimed. Eight extension tests passed on a locally reconstructed base helper; exact GitHub source and hosted CI are pending.

## Interpolation-method stability (2026-11-12)

Run `python -m unittest -v test_interpolation.py` and `python interpolation.py`. This standard-library extension compares **linear continuously compounded spot yields** with **linear log-discount factors** between the same predeclared synthetic 1/2/3/5-year nodes. At observed nodes both methods give `D(t)=exp(-z(t)t)`; between nodes, log-discount interpolation uses `log D(t)=(1-w)log D(a)+w log D(b)`. Thus both methods reproduce the observed discount factors, but their implied intermediate prices and frozen-curve roll-down can differ. The 2.5-year log-discount benchmark is the geometric mean of the two- and three-year discount factors.

The extension checks positive discount factors, exact-node consistency, arithmetic P&L reconciliation, immutability and invalid input rejection. **Positive discount factors alone do not prove nonnegative forward rates or arbitrage-free market calibration.** Holding-period comparisons are static hypothetical scenarios, not ex-ante trading signals. No market data, external validation, or independent review. Authored tests require exact-revision CI verification; local GitHub cloning was blocked by DNS.
