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
