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
