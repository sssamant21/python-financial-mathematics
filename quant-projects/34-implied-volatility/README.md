# Project 34 — Implied Volatility and Option Quote Validation

**Business question:** What annualized volatility makes the Black–Scholes model reproduce a European option premium? Implied volatility is a model-implied parameter, not a forecast or trading recommendation.

## Mathematics

For a non-dividend-paying stock, the call price is `C = S N(d1) - K exp(-rT) N(d2)`, where `d1 = [ln(S/K) + (r + sigma²/2)T]/(sigma sqrt(T))` and `d2 = d1 - sigma sqrt(T)`. Put price follows `P = C - S + K exp(-rT)`. Bisection inverts the premium over volatility from zero to a configured maximum of 500% annualized. At zero volatility the option has a discounted deterministic payoff. Quotes outside the finite pricing bracket are rejected. Near expiry or deep in/out of the money, inversion can be ill-conditioned.

## Reproduce

Python 3.11+; **standard library only** (no pip dependencies, network access, market quotes or broker integrations).

```bash
cd quant-projects/34-implied-volatility
python -m unittest -v test_iv.py
python -m compileall -q iv.py test_iv.py
python iv.py --spot 100 --strike 105 --years 1 --rate 0.02 --vol 0.25 --kind call
```

The CLI generates a **synthetic** model premium from the given volatility and recovers the volatility from that premium. Seven deterministic tests check call/put roundtrips, put–call parity, zero-volatility boundary, monotonicity, invalid quotes and inputs, and explicit nonconvergence. Roundtrip tests are *internal numerical consistency*, not independent market/model validation.

## Limitations and next step

Assumes European exercise, no dividends, constant rate and volatility, frictionless continuous markets and exact option quotes. Does not model bid/ask, stale quotes, American exercise, dividends, volatility smile, jumps or corporate actions. No real market data are downloaded or redistributed. Do not infer a profitable strategy or production readiness. Independent model review, exact-revision CI and market calibration are unverified.

Next: predetermined synthetic quote-spread, maturity and strike grids; quantify implied-volatility sensitivity and near-expiry numerical conditioning. For eventual licensed data, record provider, exact observation timestamps, contract identifiers, underlying adjustment and dividend/rate assumptions.

## Synthetic bid/ask, strike and maturity sensitivity

The fixed grid uses **S=100, r=2%, annual volatility=25%, strike K in {90,100,110}, maturity T in {0.05,0.25,1} years**, and a hypothetical premium half-spread of 0.05 currency units. It is a numerical-conditioning exercise, **not observed bid/ask market data**. For each contract, invert both sides of the quote interval and report the annual-volatility width. The analytical Black–Scholes vega is `S sqrt(T) phi(d1)`; for a narrow quote interval, `IV_ask - IV_bid ≈ (ask - bid)/vega`. Small vega can make implied volatility unstable, and the approximation need not hold for wide spreads. Unattainable/negative bids are marked unavailable rather than clipped.

```bash
cd quant-projects/34-implied-volatility
python -m unittest -v test_iv.py test_sensitivity.py
python -m compileall -q iv.py sensitivity.py test_iv.py test_sensitivity.py
python sensitivity.py --spread 0.05
```

The eight added deterministic methods cover finite-difference vega, quote ordering, spread widening, put/call symmetry, reproducibility, invalid inputs, unavailable quote flags, and the local linear approximation. All results are synthetic, with no dividends, quote timestamps, American options, exchange fees or real-world liquidity assumptions. Local equivalent-source testing is not exact-published-source acceptance; GitHub Actions and independent model review must be checked separately.
