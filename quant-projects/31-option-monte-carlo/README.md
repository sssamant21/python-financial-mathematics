# Project 31 — European Call Monte Carlo and Antithetic Variates

**Audience:** Beginner quantitative analysts and Python learners. **Data:** entirely synthetic; no downloads, accounts, broker connections, or market-data redistribution. **Python:** 3.11+ standard library; no third-party dependencies.

## Business question

How accurately can simulation value a hypothetical European call option, and how do we distinguish simulation uncertainty from model risk? This lab compares a seeded, risk-neutral geometric Brownian motion simulation against an independently implemented Black–Scholes closed-form price. The two methods share **the same model assumptions**, so numerical agreement is *not* market calibration or independent model certification.

## Mathematics

Under the assumed risk-neutral dynamics with continuously compounded risk-free rate `r`, continuous dividend yield `q`, volatility `sigma`, and time `T`:

`S_T = S_0 exp((r-q-sigma²/2)T + sigma sqrt(T) Z)` where `Z ~ N(0,1)`.

The European call value is `exp(-rT) E[max(S_T-K,0)]`. For every generated `Z`, also simulate `-Z`, discount each payoff, and average the **pair**. This is an *antithetic variate*: its covariance can reduce sampling noise, but the reduction is not guaranteed for every payoff or parameter choice. Treat each pair as one independent observation, not two independent samples.

The standard error is `sample_standard_deviation(pair_averages)/sqrt(number_of_pairs)`. The reported 95% normal-approximation interval is `estimate ± 1.96 × standard_error`. It describes **Monte Carlo sampling uncertainty conditional on this model**, not uncertainty about volatility, dividends, prices, or future returns.

For comparison, the Black–Scholes call formula is `S_0 exp(-qT) N(d1) - K exp(-rT) N(d2)`, with `d1=[ln(S_0/K)+(r-q+sigma²/2)T]/(sigma sqrt(T))` and `d2=d1-sigma sqrt(T)`.

## Reproduce

From this directory:

```bash
python monte_carlo.py --pairs 10000 --seed 2026
python -m unittest -v test_monte_carlo.py
python -m compileall -q monte_carlo.py test_monte_carlo.py
```

The defaults are hypothetical `S0=100`, `K=100`, `r=3%`, `q=0%`, `sigma=20%`, `T=1 year`. A known mathematical benchmark (`S0=K=100`, `r=5%`, `sigma=20%`, `T=1`, `q=0`) is approximately `10.4505835722` and is asserted in tests. The seeded convergence check uses a fixed absolute tolerance rather than claiming every random sample must contain the benchmark in its confidence interval.

## Validation and guardrails

The implementation checks finite parameters, strictly positive spot/strike/volatility/maturity, bounded educational parameter ranges, integer seeds, and 2–2,000,000 independent pairs. The RNG is local and seeded; no input files or trades are accepted. Tests cover the analytical benchmark, determinism, path accounting, interval arithmetic, a synthetic convergence tolerance, dividend sensitivity and invalid inputs. A CI run must execute the **published revision** before claiming hosted validation.

**Limitations:** European exercise only; constant rates, dividends and volatility; lognormal dynamics; no stochastic rates, jumps, transaction costs, volatility surface, or historical calibration. The closed-form comparison validates numerical implementation under shared assumptions, not real-world pricing accuracy. No historical market data, survivorship selection, look-ahead features, investment recommendations, independent review, or production certification.

**Next extension:** compare naive versus antithetic Monte Carlo using equal simulation budgets and repeated independent seeds, reporting empirical standard-error and coverage diagnostics without cherry-picking runs.
