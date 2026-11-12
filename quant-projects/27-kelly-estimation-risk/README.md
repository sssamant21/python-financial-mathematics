# Project 27 — Kelly Sizing and Estimation Risk

**Business question:** Why can a seemingly attractive positive-edge investment become dangerous when the probability of winning is estimated incorrectly?

This **synthetic-only**, standard-library Python 3.11+ exercise is about model risk, **not** recommended portfolio allocations or live trading. Assume a single independent binary payoff: each period an invested fraction `f` earns `+b` with probability `p`, or loses fraction `a` of the stake with probability `1-p`. Uninvested capital earns zero.

## Mathematics

Expected log growth is `G(f) = p log(1+b f) + (1-p) log(1-a f)`. Setting its derivative to zero gives the unconstrained fraction `f* = (p b - (1-p) a)/(a b)`. We clip it to a **predeclared long-only cap** in [0,1]. A full loss at `f=a=1` has log growth `-infinity` (ruin). No leverage, shorts, price data or transaction costs are modeled.

The key model-validation exercise holds the fraction chosen using estimated `p` fixed, then changes the **true** scenario probability. This avoids choosing allocations using the stressed outcomes. Stress probabilities are hypothetical, not confidence intervals or calibrated forecasts.

## Run

```bash
cd quant-projects/27-kelly-estimation-risk
python -m unittest -v test_kelly.py
python -m compileall -q kelly.py test_kelly.py
python kelly.py --probability 0.55 --cap 0.5
```

With symmetric +/-100% payoff on the invested fraction and estimated `p=0.55`, the illustrative fraction is 10%. At a true win probability of 45%, expected log growth of that **unchanged** position is negative. This shows why estimation error matters.

## Guardrails and limitations

Finite numeric inputs only; strict probability bounds; strictly positive win payoff and loss fraction; no more than 100% loss of invested stake; long-only allocation capped at 100%; reject invalid stress probabilities; report ruin as negative infinity. Real markets have fat tails, serial dependence, changing payoffs, slippage, taxes, and estimation uncertainty. This lab has no empirical calibration, independent review or production certification. Do not use it for investment decisions.

## Sample-size uncertainty extension

The optional `uncertainty.py` lab computes a **Wilson score interval** for an independently observed binary win count `w` among `n` trials. With `p_hat=w/n`, `z=1.96` and `d=1+z²/n`, its center is `(p_hat+z²/(2n))/d` and its radius is `z sqrt(p_hat(1-p_hat)/n+z²/(4n²))/d`. The lower and upper bounds are the center minus/plus the radius. Unlike a naive normal interval, the Wilson bounds stay within [0,1] for zero/all successes.

A **predeclared** conservative scenario plugs the lower bound into the existing capped long-only Kelly formula, then holds that fraction fixed across three hypothetical evaluation probabilities (0.45, 0.50, 0.55). For 55 wins in 100 synthetic independent trials, the approximate 95% Wilson interval is [0.452444, 0.643856]. The point-estimate fraction is 0.10; the lower-bound fraction is zero under symmetric payoffs. More observations with the same observed win rate generally narrow the interval.

```bash
cd quant-projects/27-kelly-estimation-risk
python -m unittest -v test_kelly.py test_uncertainty.py
python -m compileall -q kelly.py uncertainty.py test_kelly.py test_uncertainty.py
python uncertainty.py --wins 55 --trials 100
```

**Validation boundary:** The approximate 95% coverage assumes independent, identically distributed Bernoulli trials and a predeclared confidence level; it is not a posterior probability, a guarantee, a regime-robust bound, or a correction for data snooping. The scenarios are not out-of-sample market evidence. A zero conservative fraction means this simplified decision rule has no positive estimated edge at the lower bound, **not** that holding cash is generally optimal. No actual win observations, calibrated market probabilities, transaction costs, broker integration, independent review or production certification are supplied.
