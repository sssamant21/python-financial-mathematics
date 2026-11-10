# Project 17 — Implied Volatility and Option Quote Validation

Recover the Black–Scholes–Merton volatility consistent with a **hypothetical** European option quote. Implied volatility is a model input inferred from a quote, **not** a forecast of realized volatility.

## Financial and mathematical context

With continuous dividend yield q and continuously compounded rate r, define discounted spot A = S exp(-qT) and discounted strike B = K exp(-rT). European call prices must satisfy max(0,A-B) ≤ C ≤ A; European puts must satisfy max(0,B-A) ≤ P ≤ B. The implementation requires strictly interior quotes to avoid nonunique or limiting-volatility solutions.

Bisection solves Black–Scholes(vol) = quote within the predeclared interval [0.000001, 3], at most 150 iterations, with an absolute **price residual** tolerance of 1e-8. It refuses quotes outside the no-arbitrage bounds or the solver bracket and raises on nonconvergence rather than inventing a root.

## Reproduce (Python 3.11+, no third-party dependencies)

```bash
cd quant-projects/17-implied-volatility-validation
python implied_vol.py
python implied_vol.py --kind put --quote 5.573526022256971
python -m unittest -v test_implied_vol.py
```

Default call assumptions: hypothetical spot 100, strike 100, maturity 1 year, rate 5%, dividend 0%, quote 10.450583572185565. Expected inferred volatility approximately 20%. The tests use synthetic prices and cover call/put inversion, dividends, bounds, invalid quotes, missing brackets and nonconvergence.

## Model validation and limitations

European exercise only; constant rate, dividend yield and volatility, lognormal underlying, frictionless markets. No American exercise, stale bid/ask quote handling, surface arbitrage, actual option chains, broker integrations or live trades. No third-party market data are redistributed. Passing synthetic tests does not establish historical calibration, independent review, or production certification. Educational research, not investment advice.


## Synthetic bid/ask and put-call parity extension

For European calls and puts with matching strike and expiry, define F = S exp(-qT) - K exp(-rT). A feasible bid/ask market must satisfy **call bid − put ask ≤ F ≤ call ask − put bid**. Each quote must also respect its discounted no-arbitrage bounds, be nonnegative, and have an uncrossed spread. The extension returns implied-volatility intervals only if all four quotes are strictly interior and individually bracketed by the bounded solver. This is a necessary consistency screen, **not** a sufficient absence-of-arbitrage proof (execution costs, early exercise, stale/asynchronous quotes, and calendar/strike constraints are excluded).

```bash
cd quant-projects/17-implied-volatility-validation
python quote_validation.py
python -m unittest -v test_implied_vol.py test_quote_validation.py
```

The example uses deterministic synthetic option quotes around a 20% Black–Scholes model, not observed prices. The model does not fetch, store or redistribute market data. Missing independent review and real bid/ask provenance remain **unverified**.
