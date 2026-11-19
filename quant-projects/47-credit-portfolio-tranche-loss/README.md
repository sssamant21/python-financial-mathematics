# Project 47 — Credit portfolio tranche loss (independent defaults)

**Business question:** How is a portfolio's expected credit loss allocated across junior, mezzanine, and senior loss layers? This is a synthetic educational exercise, not a tradable CDO valuation.

## Model and mathematics

Assume `n` equally weighted obligors, independent one-year Bernoulli defaults with identical probability `p`, and constant loss-given-default `LGD`. The default count `K ~ Binomial(n,p)`; total portfolio loss as a fraction of original portfolio notional is `L = LGD*K/n`. For attachment `A` and detachment `D`, the loss allocated to a tranche per unit **portfolio** notional is `min(max(L-A,0),D-A)`. Expected tranche loss is the sum of this payoff times the binomial probability over `K=0,...,n`. Divide by `D-A` to express it as a fraction of the tranche's own notional.

The sum of losses across a non-overlapping partition from 0 to 100% must equal `p*LGD`. This is a useful independent accounting identity. The implementation evaluates binomial probabilities around the mode to avoid underflow in the tails.

## Reproduce (Python 3.11–3.13, no dependencies)

```bash
cd quant-projects/47-credit-portfolio-tranche-loss
python tranche_loss.py
python -m unittest -v test_tranche_loss.py
python -m compileall -q tranche_loss.py test_tranche_loss.py
```

The CLI uses invented assumptions and prints expected loss in portfolio-notional and tranche-notional units. The tests include exact one-name and boundary cases, expected-loss conservation across layers, monotonicity, and malformed-input rejection. No broker, API, external data, secrets, or downloaded market prices.

## Model validation and limitations

This is **not** a credit-correlation, copula, tranche-pricing, discounting, recovery-timing, or CDS-convention model. Independent defaults strongly understate clustered-loss possibilities; homogeneous exposure, fixed LGD, and a single period are additional material limitations. No survival or selection bias is inferred from synthetic data. To study empirical portfolios, source authorized point-in-time constituents, defaults and recoveries with observation dates and licenses; never commit third-party raw datasets.

**Validation:** Nine deterministic tests authored. Exact published-revision CI, independent review, market calibration, and production certification remain unverified until separately confirmed.
