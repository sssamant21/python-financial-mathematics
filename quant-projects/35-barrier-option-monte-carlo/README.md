# Project 35 — Discretely Monitored Barrier Option Monte Carlo

**Business question:** How does a European call's theoretical value change when it expires worthless if the underlying touches an upper barrier on an observation date?

## Model and mathematics

Under risk-neutral geometric Brownian motion, each synthetic observation advances by
`S(t+dt) = S(t) exp((r - sigma²/2)dt + sigma sqrt(dt) Z)`.
For an **up-and-out call**, the discounted payoff is
`exp(-rT) max(S(T)-K,0) 1{S(t_j)<H for every monitored date}`.
Here `H>S(0)` and monitoring is **discrete** (not continuous); touching the barrier knocks out the option. Antithetic normal pairs `Z,-Z` share the same seed and provide a paired Monte Carlo estimator. The reported standard error uses the **pair means** as independent observations, not the two correlated paths separately.

## Reproduce

Requires Python 3.11+; standard library only. From this folder:

```sh
python -m unittest -v test_barrier.py
python -m compileall -q barrier.py test_barrier.py
python barrier.py --pairs 5000 --steps 52 --seed 2026
```

Compare `--steps 12` and `--steps 252` using identical seeds, while recognizing the different monitoring dates and that no continuous-monitoring correction is applied. The paired vanilla call is a pathwise upper benchmark. Results are seeded **synthetic educational estimates**, not quoted market prices or trading advice.

## Guardrails and limitations

Inputs must be finite, with positive spot/strike/maturity/volatility, barrier above initial spot, at least two antithetic pairs and one monitoring step. Exponentially unsafe rate and per-step volatility values are rejected. No broker access, external data, dividends, volatility smile, jump risk, transaction costs, early exercise, or live trading. The sample standard error is descriptive and does not establish calibrated confidence interval coverage. Further numerical benchmarking, continuous barrier correction, exact published-source CI and independent model review remain outstanding.


## Matched-grid monitoring-frequency lab

Run `python -m unittest -v test_monitoring.py`, `python -m compileall -q monitoring.py test_monitoring.py`, and `python monitoring.py --pairs 2000 --seed 2026`. Python 3.11+ standard library only.

The new `monitoring.py` simulates **one common fine Brownian grid** and reuses exactly the same antithetic price paths for 12, 36, 84 and 252 observation dates. Each coarse grid is a subset of the finer grid. For each simulated path, adding barrier checks cannot increase an up-and-out payoff, so the estimated prices must be non-increasing as monitoring becomes more frequent. This *pathwise* comparison avoids confusing a change in random samples with a monitoring effect.

The independent European vanilla-call Black–Scholes formula is `S0 Φ(d1) - K exp(-rT) Φ(d2)`, with `d1=[ln(S0/K)+(r+σ²/2)T]/(σ√T)` and `d2=d1-σ√T`. The experiment reports its analytical value, the Monte Carlo vanilla estimate, and their difference. The vanilla check **does not validate barrier pricing**; it checks a shared underlying simulation component. The standard errors use independent *antithetic pair means*, not individual correlated paths.

Only divisible, nested monitoring grids are accepted; all grids share the maturity observation. Inputs are bounded and checked for finite values. This is a **discrete-monitoring** experiment, not a continuously monitored barrier option. No dividends, smile, jumps, historical calibration, market quotes, live trading or independent barrier benchmark are included. CI exact-source execution and independent review remain unverified until confirmed.

## Brownian-bridge continuous-monitoring estimator

Run `python -m unittest -v test_bridge.py`, `python -m compileall -q bridge.py test_bridge.py`, and `python bridge.py --pairs 2000 --steps 52 --seed 2026`. Python 3.11+ standard library only; no downloaded prices.

For two GBM endpoints below upper barrier H, conditional no-hit probability is
`1 - exp[-2 ln(H/S_start) ln(H/S_end)/(sigma² dt)]`; any endpoint at or above H has survival zero. Multiplying segment survival probabilities and terminal discounted call payoffs gives a Brownian-bridge conditional-expectation estimate of **continuous** knockout under idealized constant-volatility GBM. The discrete estimator checks only simulated endpoints using the **same paths**. Pathwise, continuous bridge-weighted payoff cannot exceed the discretely monitored payoff, which cannot exceed vanilla payoff. The reported gap and paired standard error use antithetic-pair means; the bridge estimate integrates out within-step crossings rather than simulating crossing indicators.

This conditional formula is a model-based numerical reference, **not** an independent externally implemented analytical barrier-price benchmark. Results depend on GBM, zero dividends, idealized continuous monitoring and finite Monte Carlo sampling. The paired standard error does not establish calibrated coverage; historical calibration, independent model review and exact published-revision CI remain unverified.
