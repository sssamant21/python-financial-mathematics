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

## Joint same-expiry quote interval feasibility (small synthetic grids)

The separate `joint_feasibility.py` asks a stronger question than the individual screens: **does one vector of theoretical European call prices simultaneously lie inside all bid/ask intervals and satisfy strike monotonicity, discounted vertical-spread bounds and discrete convexity?** For strikes \(K_i\), the constraints are \(b_i \le C_i \le a_i\), \(-D(K_{i+1}-K_i) \le C_{i+1}-C_i \le 0\), and nondecreasing neighboring secant slopes. Fourier–Motzkin variable elimination checks this finite system of linear inequalities. To bound worst-case combinatorial growth it rejects grids outside 3–5 strikes or more than 20,000 intermediate inequalities. Floating-point tolerances mean borderline cases require higher-precision independent review.

```sh
python -m unittest -v test_joint_feasibility.py
python -m compileall -q joint_feasibility.py test_joint_feasibility.py
python joint_feasibility.py
```

The five synthetic tests cover feasible point quotes, wide intervals, impossible monotonicity, a **jointly infeasible** grid whose separately screened inequalities can pass, and input guards. The implementation has no third-party dependencies (Python 3.11+). **Validation:** an earlier local source-equivalent prototype passed 5/5 tests, compilation and CLI smoke; the published source and its hosted CI remain **unverified**. This is not a full no-arbitrage option-surface certificate: it omits put-call parity, boundary/forward bounds, maturity coupling, trading costs and liquidity. It does not identify an executable trade.

## Boundary and scaling regression checkpoint

`test_boundary_scaling.py` adds five deterministic synthetic tests for exact convex boundaries, strict convexity violations, uniform strike/quote unit rescaling (0.1×, 1×, 100×), a small material convexity violation, and invalid tolerance inputs. Run `python -m unittest -v test_joint_feasibility.py test_boundary_scaling.py` from this directory. The dedicated workflow now invokes both suites. **New exact-source CI is pending; local execution was blocked by GitHub DNS resolution.** These checks do not establish numerical accuracy near the tolerance threshold, scale invariance for arbitrary magnitudes, or independent mathematical certification.

## Dimensionless tolerance checkpoint (2026-11-15)

The joint solver now divides strikes and bid/ask prices by one common positive scale before Fourier–Motzkin elimination. The public `tolerance` argument is interpreted in **normalized price units**, not dollars: for example `1e-9` is relative to the largest strike/ask scale. The mathematical inequalities are homogeneous under simultaneous rescaling of strike and option-price units; normalizing reduces sensitivity to quote currency units. This is a numerical policy, **not** an economically justified quote-error allowance. Extreme magnitudes, cancellation, the solver's fixed coefficient normalization, and near-zero constraints still need independent numerical assessment.

Run `python -m unittest -v test_joint_feasibility.py test_boundary_scaling.py test_normalized_tolerance.py` and `python -m compileall -q joint_feasibility.py test_normalized_tolerance.py`. The new suite uses synthetic 0.001×/1×/1000× unit changes for a strict convexity violation, an exact boundary, and feasible bid/ask intervals. **Exact published-revision tests and CI are pending; do not infer a pass from publication.**

## Irregular-grid Decimal reference checkpoint (2026-11-15)

`test_irregular_decimal_reference.py` independently checks **point quotes** (bid equals ask) using 70-digit `decimal.Decimal` arithmetic on irregular three- and five-strike grids. It compares exact secant-slope monotonicity, vertical-spread limits, and convexity with the Fourier–Motzkin classification, including common unit scaling. Run `python -m unittest -v test_irregular_decimal_reference.py` from this directory. The dedicated workflow includes this suite. **Tests have been authored, not yet verified passing on the published revision.** This is not an independent linear-programming oracle for interval quotes; near-zero elimination pivots and extreme strike spacing remain unverified. No live market data or production certification.

### Independent interval-feasibility reference

Run `python -m unittest -v test_interval_reference.py` from this directory. The standard-library `fractions.Fraction` oracle enumerates vertices of the bounded three-strike quote polytope instead of using Fourier–Motzkin elimination. Five deterministic tests compare both methods for point quotes, nonzero bid/ask intervals and irregular strikes. This is a small-grid cross-check, **not** proof of floating-point stability, five-strike correctness or production readiness. No market data is bundled.

## CI coverage correction (2026-11-16)

The dedicated workflow previously invoked only `test_surface.py` and `test_quote_intervals.py` in its Project 37 step. Earlier workflow success therefore **did not validate** the joint-feasibility, scaling, Decimal, or Fraction reference suites. The workflow has now been updated to run all seven test modules and compile their Python files. Until the new exact-source workflow completes, the expanded tests are **not CI-verified**. Run locally with:

```sh
python -m unittest -v test_surface.py test_quote_intervals.py test_joint_feasibility.py test_boundary_scaling.py test_normalized_tolerance.py test_irregular_decimal_reference.py test_interval_reference.py
python -m compileall -q surface.py quote_intervals.py joint_feasibility.py test_surface.py test_quote_intervals.py test_joint_feasibility.py test_boundary_scaling.py test_normalized_tolerance.py test_irregular_decimal_reference.py test_interval_reference.py
```

## Five-strike exact-rational interval reference (2026-11-16)

`test_five_interval_reference.py` independently enumerates vertices of a bounded five-dimensional bid/ask quote polytope using exact `fractions.Fraction` arithmetic and Gaussian elimination. It checks a feasible interval grid, an impossible monotonicity grid, and duplicate-strike rejection against `joint_feasibility.py`. The reference is intentionally exhaustive and only appropriate for small synthetic fixtures. Run `python -m unittest -v test_five_interval_reference.py` from this directory. **The local exact-arithmetic oracle alone was exercised on two fixtures (feasible=True, infeasible=False), and compilation passed; the combined solver/reference tests and exact-revision CI have not yet been verified.** Near-zero pivots, extreme strike spacing, independent review and licensed market-data validation remain outstanding.
