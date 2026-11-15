# Project 36 — Arithmetic Asian Option Monte Carlo

**Business question:** How does an option whose payoff depends on an average stock price differ from a conventional European call? This is a synthetic educational pricing lab, not a quote or trading recommendation.

## Mathematics and interpretation

Under risk-neutral geometric Brownian motion, `S(t+dt) = S(t) exp((r - sigma²/2)dt + sigma sqrt(dt) Z)`, with independent standard-normal increments. With `n` equally spaced **post-initial** observations, define `A = (S(t1)+...+S(tn))/n`. A discretely monitored arithmetic-average Asian call pays `max(A-K,0)` at maturity, so its model price is `exp(-rT) E[max(A-K,0)]`.

The simulator generates antithetic Brownian increments `Z` and `-Z` and averages each pair's discounted payoffs. Standard error is computed across independent **pair means**, not correlated individual paths. A vanilla call is calculated from the same terminal paths for context; it is **not** a universal upper bound on the Asian call for every realized path. With one observation at maturity, the Asian payoff equals the vanilla payoff exactly on every path.

## Run (Python 3.11+, standard library only)

```sh
cd quant-projects/36-asian-option-monte-carlo
python -m unittest -v test_asian_option.py
python -m compileall -q asian_option.py test_asian_option.py
python asian_option.py --pairs 5000 --observations 12 --seed 2026
```

Try `--observations 1`, `12`, and `52` to explore averaging-frequency sensitivity. Changing observation count changes the contractual payoff, so it is **not** a convergence study for one fixed contract. Estimates are seeded and reproducible on the same Python implementation; they still have Monte Carlo sampling error.

## Guardrails and validation boundaries

Only finite positive spot, strike, maturity, and volatility are accepted; rates must be finite, and extreme exponents are rejected. Pair counts and monitoring counts are bounded. No downloaded data, historical calibration, dividends, stochastic volatility, volatility smile, jumps, liquidity, counterparty risk, broker access, or trading actions. The reported standard error is descriptive and does not prove coverage or pricing accuracy. Synthetic regression tests check reproducibility, a one-observation identity, zero payoff, finite results, and invalid inputs. Independent model review, exact-source hosted CI, and production suitability remain **unverified**.
