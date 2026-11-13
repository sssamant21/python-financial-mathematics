# Project 32 — Binomial Option Pricing and Early Exercise

**Goal:** Understand why an American put can be worth more than a European put. This offline, standard-library Python lab uses a Cox–Ross–Rubinstein (CRR) recombining tree with hypothetical parameters only. No broker connections, live trades, or market data.

## Business context and mathematics

A **European put** may be exercised only at maturity; an **American put** may be exercised at any tree date. Each step lasts `dt=T/N`, with up factor `u=exp(sigma sqrt(dt))`, down factor `d=1/u`, and risk-neutral probability `p=[exp((r-q)dt)-d]/(u-d)`. The no-arbitrage tree requires `0 <= p <= 1`; otherwise the script raises an error rather than silently clipping.

At maturity, payoff is `max(K-S,0)`. Working backward, continuation value is `exp(-r dt)[p V_up+(1-p)V_down]`. For American puts the node value is the maximum of continuation and immediate exercise `max(K-S,0)`; European puts use continuation only. This model assumes constant volatility, continuously compounded rates and dividends, discrete exercise opportunities, and frictionless markets. It is **not** a market forecast.

## Reproduce

From `quant-projects/32-binomial-option-exercise/`:

```bash
python binomial.py --steps 200
python binomial.py --steps 400 --spot 90 --strike 100 --volatility 0.3
python -m unittest -v test_binomial.py
python -m compileall -q binomial.py test_binomial.py
```

No extra dependencies are required (Python 3.11). Tests check one-step pricing against direct algebra, the American/European inequality, immediate exercise, an independent Black–Scholes European put benchmark, volatility monotonicity, and invalid inputs. The Black–Scholes benchmark is approximately **5.5735260223** for `S=K=100, r=5%, sigma=20%, q=0, T=1`. Finite-tree convergence oscillates with step parity; a 400-step tolerance is deliberately nonzero.

## Guardrails and validation limits

The tree is limited to 2,000 steps, positive finite spot/strike/volatility/maturity, and bounded educational rate/dividend inputs. Memory usage is O(N); runtime is O(N²). A positive early-exercise premium is possible but not guaranteed. Deterministic tests establish numerical consistency under the stated assumptions, **not** historical calibration, independent model validation, real-market arbitrage freedom, or production certification. CI status must be checked against the exact commit.

**Next extension:** predeclared step-count convergence and early-exercise boundary diagnostics, with comparisons to independently implemented numerical benchmarks.

## Tree-step convergence and early-exercise boundary diagnostics

Run `python -m unittest -v test_diagnostics.py` and `python diagnostics.py --steps 100` from this folder. The fixed tree-step grid 25, 50, 100, 200, 400 compares European CRR put values with an independently evaluated closed-form Black–Scholes put reference (5.5735260223 for S=K=100, r=5%, sigma=20%, q=0, T=1). CRR error can oscillate with odd/even step parity; **do not assume monotonic convergence**. American puts may be worth more than European puts because their holder can exercise before maturity. At each discrete pre-expiry layer, the diagnostic reports the highest in-the-money spot node at which immediate exercise is at least as valuable as discounted continuation. A missing boundary means no eligible node in that layer, not that exercise is impossible at other times. The lattice boundary is discrete and grid-dependent, not an independently validated continuous-time boundary. The code reuses the existing pricer's finite-value, risk-neutral probability and 2,000-step guards. Standard-library Python 3.11 only, no downloads, no broker operations, no historical calibration, and no production certification. Exact-source hosted CI and independent American-option numerical review must be checked separately.

## Independent implementation cross-check (small trees)

`independent_reference.py` uses a separately coded, **top-down memoized**
recursion rather than the primary engine's in-place backward induction. It
compares 3 precommitted hypothetical parameter sets × 5 tree sizes
(1, 2, 5, 10, 20) × European/American exercise = **30 comparisons**.
This is an implementation cross-check under the **same CRR model**, not an
independent pricing model, a market calibration, or an external QuantLib
American-option benchmark. The 24-step cap keeps the reference intentionally
small. Deep-in-the-money immediate-exercise and American ≥ European checks
supplement the price comparisons. Exercise-boundary shape across dates is
not independently certified.

```bash
cd quant-projects/32-binomial-option-exercise
python -m unittest -v test_independent_reference.py
python independent_reference.py
python -m compileall -q independent_reference.py test_independent_reference.py
```

Python 3.11 standard library only; no additional dependencies or downloaded
market data. Check the exact published revision's CI separately. Independent
finite-difference/PDE or QuantLib American-option comparisons remain future work.

## Independent finite-difference PDE benchmark (synthetic)

`pde_benchmark.py` solves the Black–Scholes put PDE backward on a uniform **spot** grid using explicit time stepping, an upwind first derivative, and an American exercise projection `max(continuation, K-S)` at each time layer. Unlike `independent_reference.py`, this is a **different numerical discretization** from CRR. It remains within the same constant-volatility Black–Scholes assumptions and is **not** an external audited reference. The lower boundary is `K` for American puts and `K exp(-r tau)` for European puts; the upper boundary is zero. Coefficient negativity rejects unstable grids rather than silently returning prices. The default PDE grid can be expensive; the documented quick run uses 100 spot intervals and 10,000 time intervals. Spatial truncation, interpolation, upwind bias, and exercise-grid approximation explain why comparisons use nonzero absolute tolerances (0.20 European, 0.25 American) against a 400-step CRR tree; these are **educational smoke tolerances, not independently established error bounds**.

```bash
cd quant-projects/32-binomial-option-exercise
python -m unittest -v test_pde_benchmark.py
python pde_benchmark.py --spot-steps 100 --time-steps 10000
python -m compileall -q pde_benchmark.py test_pde_benchmark.py
```

The six synthetic tests compare European and American values with CRR, exercise premium, deep-in-the-money exercise and rejected invalid/unstable grids. No downloaded market data, external dependencies, trading, or production certification. Local validation passed 6/6 on an equivalent locally reconstructed CRR helper; **full exact-revision repository CI is unverified**. Next: verify hosted CI and perform predeclared grid-refinement/error sensitivity before Project 33.

## Predeclared PDE grid-refinement sensitivity

`grid_sensitivity.py` compares three **fixed synthetic grids** (40×2,000, 60×5,000 and 80×9,000 spot×time intervals) against the analytic zero-dividend Black–Scholes European put (S=K=100, r=5%, volatility=20%, T=1). It also reports American put value and early-exercise premium on each grid. The grid choices are fixed before evaluation; error need **not** decrease monotonically because interpolation, upwind bias and time/space discretization interact. The analytic benchmark applies to European puts only; American results have no closed-form reference here. These are descriptive educational checks, not convergence-rate or production accuracy certification.

```bash
cd quant-projects/32-binomial-option-exercise
python -m unittest -v test_grid_sensitivity.py
python -m compileall -q grid_sensitivity.py test_grid_sensitivity.py
python grid_sensitivity.py
```

Six deterministic synthetic test methods cover the analytic reference, grid order, finite prices, exercise premium, coarse error and invalid inputs. Standard-library Python 3.11; no market-data download. Exact-revision hosted CI and independent model review must be verified separately.
