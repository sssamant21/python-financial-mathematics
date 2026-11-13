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
