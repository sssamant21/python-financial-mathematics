# Project 29 — Credit Spread Duration and Scenario P&L

**Business question:** How sensitive is a hypothetical corporate-bond portfolio to changes in credit spreads, holding benchmark rates fixed? This complements Project 15's interest-rate duration and Project 18's expected credit loss, but does not estimate defaults or trade bonds.

## Mathematics

For position market value `V`, spread duration `D_s` (years), spread convexity `C_s` (years squared), and spread shock `Δs` in decimal yield units:

`ΔV ≈ V × (−D_s Δs + 0.5 C_s (Δs)^2)`.

One basis point (bp) = 0.0001. Portfolio scenario P&L is the sum of position P&Ls; loss is `−P&L`. The first-order spread DV01 is `V × D_s × 0.0001` (currency lost for a +1 bp shock). A positive spread widening generally hurts long credit exposure. This is an approximation, not a repricing engine. Convexity may be unreliable for callable, distressed, floating-rate, or otherwise nonlinear securities.

## Run locally

Python 3.11+; standard library only, with no third-party dependencies or data downloads:

```bash
cd quant-projects/29-credit-spread-stress
python -m unittest -v test_spread_stress.py
python -m compileall -q spread_stress.py test_spread_stress.py
python spread_stress.py
```

The CLI reports a deterministic two-position portfolio under predeclared +50, +100, and −50 bp parallel spread scenarios. All inputs are hypothetical.

## Validation and guardrails

Positions must have unique nonempty IDs, strictly positive finite market values, nonnegative finite spread durations and convexities. Shock magnitudes are limited to ±2,000 bp for this educational approximation; invalid, nonfinite, or duplicate inputs raise `ValueError`. Tests cover zero shocks, sign conventions, additive attribution, convexity, basis-point units, invalid inputs and deterministic scenarios. No optimization or live execution occurs.

**Model limitations:** This ignores default jumps, recovery, rating migration, liquidity, taxes, funding, rate/spread co-movement, and spread term structures. Scenario shocks are selected before evaluating results; no future market information is used. The model is not independently reviewed, historically calibrated, or production certified. Real market data, if added later, must be downloaded by authorized users with documented provider, licensing, observation dates and point-in-time availability.

**Next exercise:** Add issuer/sector-specific nonparallel shocks and concentration diagnostics, then independently check scenario P&L against a separate repricing implementation.
