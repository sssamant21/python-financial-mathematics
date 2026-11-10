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

## Cross-strike and calendar consistency (synthetic)

For same-expiry European calls, price must be nonincreasing and convex in strike. A vertical call spread cannot exceed the discounted strike gap: `0 <= C(K1)-C(K2) <= exp(-rT)(K2-K1)` for `K1<K2`. For three strikes `K0<K1<K2`, convexity requires `C(K1) <= w C(K0)+(1-w) C(K2)`, where `w=(K2-K1)/(K2-K0)`. The bid/ask screen flags only *unavoidable* violations, using the most favorable bid/ask combination, and separately checks discounted European price bounds.

For the same strike and underlying, European call prices must be nondecreasing in maturity **only when dividends are zero and the continuously compounded risk-free rate is nonnegative**. The calendar function refuses other assumptions instead of incorrectly applying the rule.

```bash
cd quant-projects/17-implied-volatility-validation
python surface_checks.py
python -m unittest -v test_surface_checks.py
```

The CLI constructs hypothetical Black–Scholes quotes with a 0.02-wide bid/ask spread. Twelve deterministic regression tests cover consistent surfaces, vertical/butterfly/calendar violations, crossed quotes, invalid coordinates, nonfinite values and unsupported assumptions. These are **necessary checks, not sufficient proof** of executable arbitrage or an arbitrage-free surface: spreads may not be simultaneously executable, and sparse grids, stale/asynchronous quotes, fees, American exercise, financing and stock borrow are excluded. Synthetic tests are not market calibration or independent model validation.
