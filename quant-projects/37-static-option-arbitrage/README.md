# Project 37 — Static Option Quote Arbitrage Diagnostics

**Business question:** Can a set of European call quotes at one expiration violate elementary static no-arbitrage conditions before any implied-volatility model is fitted?

## Math and intuition

For strikes K1 < K2, a call price C(K) should be nonincreasing with strike, and its finite-difference slope must lie between -D and 0, where D=exp(-rT) is the discount factor. On any ordered (including uneven) strike grid, adjacent secant slopes must be nondecreasing: this is discrete convexity. Violations can indicate stale quotes, bad timestamps, or crossed markets, but mid-price violations do **not** establish an executable arbitrage after bid/ask spreads, transaction costs, financing, and liquidity.

The checks are **necessary, not sufficient** for a complete arbitrage-free option surface. They assume European calls with a shared expiration, consistent quote time, strike units, and discount convention. They do not validate calendar spreads, put-call parity, spot/forward bounds, dividends, early exercise, or market microstructure.

## Reproduce (Python 3.11+, standard library only)

```sh
cd quant-projects/37-static-option-arbitrage
python -m unittest -v test_surface.py
python -m compileall -q surface.py test_surface.py
python surface.py
```

The sample uses five invented strike/price pairs. The test suite covers a valid grid, increasing call price, nonconvex irregular strikes, an excessive vertical spread, and invalid inputs. All observations are synthetic, with no downloaded or redistributed market data and no broker connection.

## Guardrails and validation

Input arrays require at least three aligned observations, finite numeric values, strictly increasing positive strikes, nonnegative tolerance, and a positive bounded discount factor. A small absolute tolerance addresses floating-point noise but is **not** a market bid/ask allowance. No implied-volatility calibration or trade construction is performed.

Local authored-source validation: five unittest methods passed, Python compilation passed, and the sample CLI produced a valid synthetic grid. Hosted exact-revision CI, independent review, actual quote quality, and production readiness remain **unverified**.

**Next:** add calendar consistency and executable bid/ask-aware feasibility diagnostics, with a carefully defined forward/discount convention and independently checked fixtures.

## Bid/ask-aware necessary-condition extension

`quote_intervals.py` screens whether **every** choice of theoretical prices inside quoted bid/ask intervals violates strike monotonicity, the discounted vertical spread bound, or convexity on irregular strikes. A violation is a strong quote-quality warning; a pass **does not prove joint feasibility** because the tests check each inequality separately. It does not establish executable arbitrage after fees, latency, margin or liquidity. Quotes are invented, not real-market observations.

The separate calendar check compares earlier **bid** with later **ask**, each divided by its expiry discount factor. **Only use this screen when the European calls have identical strikes and the same forward level at both maturities**, with deterministic discounting and a martingale forward. It is not a general calendar-arbitrage test for equities with dividends or changing forwards. Bid/ask spreads, timestamps and exercise styles must be consistent.

```sh
python -m unittest -v test_surface.py test_quote_intervals.py
python -m compileall -q surface.py test_surface.py quote_intervals.py test_quote_intervals.py
python quote_intervals.py
```

Eight additional deterministic synthetic tests were authored; exact published-source CI and independent model review remain unverified. No external dependencies (Python 3.11+).
