"""Brownian-bridge conditional-survival estimate for synthetic GBM up-and-out calls."""
import argparse
import math
import random

def bridge_survival(start, end, barrier, vol, dt):
    if not all(math.isfinite(x) for x in (start, end, barrier, vol, dt)) or min(start, end, barrier, vol, dt) <= 0:
        raise ValueError("positive finite bridge inputs required")
    if start >= barrier or end >= barrier:
        return 0.0
    exponent = -2 * math.log(barrier/start) * math.log(barrier/end) / (vol*vol*dt)
    return -math.expm1(exponent)

def compare_bridge(spot=100., strike=100., barrier=130., years=1., rate=0.02,
                   vol=0.2, steps=52, pairs=2000, seed=2026):
    vals = (spot, strike, barrier, years, rate, vol)
    if (not all(math.isfinite(x) for x in vals) or min(spot, strike, barrier, years, vol) <= 0
        or barrier <= spot or abs(rate*years) > 700 or type(steps) is not int
        or not 1 <= steps <= 10000 or type(pairs) is not int or not 2 <= pairs <= 100000
        or type(seed) is not int or vol*math.sqrt(years/steps) > 10
        or abs((rate-0.5*vol*vol)*years/steps) > 700):
        raise ValueError("invalid or numerically unsafe simulation inputs")
    dt = years/steps
    drift = (rate-0.5*vol*vol)*dt
    scale = vol*math.sqrt(dt)
    discount = math.exp(-rate*years)
    rng = random.Random(seed)
    discrete, continuous, vanilla = [], [], []
    for _ in range(pairs):
        s = [spot, spot]
        survival = [1., 1.]
        alive = [True, True]
        for _ in range(steps):
            z = rng.gauss(0., 1.)
            for k, shock in enumerate((z, -z)):
                previous = s[k]
                s[k] *= math.exp(drift+scale*shock)
                if not math.isfinite(s[k]) or s[k] <= 0:
                    raise ValueError("numerical path overflow/underflow")
                alive[k] = alive[k] and s[k] < barrier
                survival[k] *= bridge_survival(previous, s[k], barrier, vol, dt)
        payoffs = [discount*max(x-strike, 0.) for x in s]
        vanilla.append(sum(payoffs)/2)
        discrete.append(sum(payoffs[k]*alive[k] for k in range(2))/2)
        continuous.append(sum(payoffs[k]*survival[k] for k in range(2))/2)
    def stats(xs):
        mean = sum(xs)/pairs
        se = math.sqrt(sum((x-mean)**2 for x in xs)/(pairs*(pairs-1)))
        return mean, se
    d, dse = stats(discrete)
    c, cse = stats(continuous)
    v, vse = stats(vanilla)
    gap, gap_se = stats([a-b for a,b in zip(discrete, continuous)])
    return dict(discrete_call=d, continuous_bridge_call=c, vanilla_call=v,
                discrete_se=dse, continuous_se=cse, vanilla_se=vse,
                discretization_gap=gap, paired_gap_se=gap_se, pairs=pairs, steps=steps)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pairs", type=int, default=2000)
    p.add_argument("--steps", type=int, default=52)
    p.add_argument("--seed", type=int, default=2026)
    a = p.parse_args()
    print(compare_bridge(pairs=a.pairs, steps=a.steps, seed=a.seed))
