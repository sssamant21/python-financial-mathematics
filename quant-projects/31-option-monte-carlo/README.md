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

## Equal-budget variance-reduction experiment

The follow-up `comparison.py` compares **4,000 discounted payoff paths per method** by default: naive Monte Carlo uses 4,000 independent normals, while antithetic Monte Carlo uses 2,000 independent normals paired with their negatives. Each antithetic pair counts as **one** independent observation when estimating its standard error. Both estimators target the same Black–Scholes value under the same risk-neutral assumptions.

For each of eight **predeclared** independent seeds, we compute each method's estimate, standard error, and whether its nominal 95% normal interval covers the analytical benchmark. We report the sample variance of the eight replicate estimates, their naive-to-antithetic ratio, and observed interval coverage. The ratio measures this fixture's empirical variance reduction, **not a guarantee**; coverage from only eight seeds is especially noisy and must not be interpreted as calibrated 95% coverage. The naive and antithetic estimators share some draws for paired comparisons, but their per-method path budgets match.

```bash
python comparison.py --pairs 2000
python -m unittest -v test_comparison.py
python -m compileall -q comparison.py test_comparison.py
```

The synthetic local fixture produced a naive-to-antithetic empirical variance ratio of approximately 1.538 across eight seeds. This result is conditional on the fixed model, seeds and parameters; it is not a forecast, a confidence guarantee, or an independently reviewed model. Larger predeclared seed grids, alternative strikes and stress cases are future exercises.

## Predeclared strike and volatility sensitivity

Run `python sensitivity.py --pairs 500` and `python -m unittest -v test_sensitivity.py`. This offline standard-library experiment evaluates strikes 80/100/120 and annual volatilities 10%/20%/40% with eight predetermined seeds. Both estimators use exactly `2 * pairs` discounted paths per seed; antithetic paths are correlated within each pair, so each pair counts as one independent observation. The independent Black–Scholes formula provides a same-assumptions numerical benchmark, not market validation. Output includes across-seed variance ratios and observed nominal 95% coverage fractions; small seed counts make those fractions unreliable as coverage estimates. No scenarios or seeds are selected based on outcomes. Extreme parameters are rejected by the underlying pricing guardrails. Results are hypothetical, not investment advice. No real-market calibration, independent model review or production certification has been performed.

**Next:** verify exact-revision CI for all Project 31 modules, then investigate larger precommitted seed grids and numerical stability without fitting to selected results.
