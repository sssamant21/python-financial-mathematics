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

## Correlated-default stress extension (one-factor Gaussian model)

**Business question:** Why can two credit portfolios with the same average default probability have very different senior-tranche losses? The shared systematic factor makes defaults cluster. For obligor `i`, draw independent standard normal `Z` and `epsilon_i`; default occurs when `sqrt(rho)*Z + sqrt(1-rho)*epsilon_i < Phi^{-1}(PD)`. The parameter `rho` is **latent asset correlation**, not directly observed default-event correlation. Each scenario draws a new shared `Z`; each obligor gets a fresh idiosyncratic shock. `rho=0` reproduces independent Bernoulli defaults in distribution.

```bash
cd quant-projects/47-credit-portfolio-tranche-loss
python correlated_defaults.py
python -m unittest -v test_tranche_loss.py test_correlated_defaults.py
python -m compileall -q tranche_loss.py correlated_defaults.py test_tranche_loss.py test_correlated_defaults.py
```

The output reports expected loss **per portfolio notional**, its Monte Carlo standard error `SE=s/sqrt(paths)`, an approximate clipped `mean +/- 1.96*SE` interval, and the **exact independent-default** benchmark. This interval describes simulation noise conditional on assumed parameters, **not** model uncertainty or a forecast interval. Compare senior-tranche outcomes across predeclared correlations (0, 0.25, 0.60); do not assume every tranche's loss increases monotonically with correlation. Use the same fixed seed for reproducibility; scenarios are not paired common-random-number estimators. Maximum workload is 5 million obligor-path draws; no external dependencies, live orders, or market downloads.

**Validation status:** Seven new tests passed locally against a source-equivalent temporary baseline shim, after correcting a floating-point equality assertion; the actual published integration and exact-revision GitHub Actions run remain **unverified**. The previously published nine baseline tests passed hosted CI. The Gaussian copula, constant PD/LGD, one-year horizon, homogeneous obligors, independent idiosyncratic shocks, normal-approximation CI, and absence of calibration are material limitations. This is not a market tranche-pricing model, investment advice, or production-certified code.
