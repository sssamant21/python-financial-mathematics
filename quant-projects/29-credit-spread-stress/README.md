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

## Issuer and sector nonparallel spread stress

The `issuer_sector.py` extension separates a **sector-wide shock** from an **issuer-specific incremental shock**. For each bond, the total shock in basis points is `sector_bps + issuer_bps`; the existing second-order spread-duration approximation is applied at the position level. P&L is reconciled across position, issuer, and sector groupings. Capital concentration is measured using the Herfindahl–Hirschman index (HHI): `sum(group_market_value / total_market_value)^2`; 1 means all exposure is in one group. HHI describes **market-value concentration**, not default correlation or risk capital. An issuer may hold multiple positions, but each position ID must be unique.

**Synthetic business example:** Two technology bonds from issuer A ($1m and $0.5m) and one energy bond from issuer B ($0.5m). Predeclare Tech +100 bp, Energy +50 bp, and an additional issuer A +25 bp. The combined Tech/A shock is +125 bp. The synthetic issuer HHI is 0.625; the scenario P&L is approximately −$71,921.88. This is not a historical stress episode or investment advice.

```bash
cd quant-projects/29-credit-spread-stress
python -m unittest -v test_spread_stress.py test_issuer_sector.py
python -m compileall -q spread_stress.py issuer_sector.py test_spread_stress.py test_issuer_sector.py
python issuer_sector.py
```

The new tests cover parallel-shock parity with the original model, additive issuer shocks, P&L reconciliation, concentration, invalid inputs and ±2,000 bp limits on both individual and **combined** shocks. No external dependencies or third-party market data are needed. Synthetic-only tests cannot establish historical spread calibration, issuer/sector taxonomy correctness, correlation stability, nonlinear bond repricing accuracy, independent review or production certification. Next: independently compare approximation P&L against a bond-pricing reference and study spread-duration breakdown under large shocks.

## Independent fixed-cash-flow repricing check

The `repricing_check.py` extension validates the *mathematical approximation* against independently discounted deterministic cash flows. For cash flow `CF_t` at time `t` and continuously compounded benchmark rate `r` plus credit spread `s`, the benchmark is `P(s) = sum(CF_t × exp(-(r+s)t))`. Cash-flow-weighted spread duration and convexity are `D = sum(t × PV(CF_t))/P` and `C = sum(t² × PV(CF_t))/P`. Compare the second-order estimate `P(-DΔs + CΔs²/2)` to direct repricing `P(s+Δs)-P(s)`. Both use the same contractual cash flows but distinct numerical evaluation paths; this is a consistency check, **not independent external model review**.

```bash
cd quant-projects/29-credit-spread-stress
python -m unittest -v test_repricing_check.py
python -m compileall -q repricing_check.py test_repricing_check.py
python repricing_check.py
```

For a synthetic five-year annual 5% coupon bond with 105 paid in year five, benchmark yield 3% and spread 1.5%, the illustrative +100 bp spread shock produces approximately −4.518249 by second-order approximation versus −4.520045 by direct repricing, or +0.1765 bp of base price approximation error. At +500 bp the error rises to about +21.0208 bp of base price. These figures are synthetic, not observed bond prices. Tests include zero shock, direction, single-payment analytical duration, small/large shock error and invalid-input guards. This method assumes fixed positive cash flows, continuously compounded flat rates and spreads, no default, no calls/prepayments, no market liquidity changes and no time-varying spread curve. Historical calibration and independent model validation remain unverified.
