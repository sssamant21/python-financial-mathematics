"""Nested common-Brownian-path discrete/bridge up-and-out call diagnostics."""
import argparse
import math
import random
from bridge import bridge_survival

def matched_grid(steps=(12, 36, 84, 252), pairs=2000, seed=2026,
                 spot=100., strike=100., barrier=130., years=1.,
                 rate=0.02, vol=0.2):
    if (not isinstance(steps, (tuple, list)) or not 1 <= len(steps) <= 12
        or any(type(n) is not int or n < 1 or n > 10000 for n in steps)
        or len(set(steps)) != len(steps)):
        raise ValueError("unique positive monitoring counts required")
    grids = tuple(sorted(steps))
    fine = grids[-1]
    if any(fine % n for n in grids):
        raise ValueError("each grid must divide the finest grid")
    vals = (spot, strike, barrier, years, rate, vol)
    if (not all(math.isfinite(v) for v in vals)
        or min(spot, strike, barrier, years, vol) <= 0 or barrier <= spot
        or type(pairs) is not int or not 2 <= pairs <= 100000
        or type(seed) is not int or abs(rate*years) > 700
        or vol*math.sqrt(years/fine) > 10
        or abs((rate-0.5*vol*vol)*years/fine) > 700
        or pairs*fine > 2000000):
        raise ValueError("invalid or unsafe simulation budget/model")
    rng = random.Random(seed)
    dt = years/fine
    drift = (rate - vol*vol/2)*dt
    scale = vol*math.sqrt(dt)
    discount = math.exp(-rate*years)
    discrete = {n: [] for n in grids}
    continuous = {n: [] for n in grids}
    for _ in range(pairs):
        paths = [[spot], [spot]]
        for _ in range(fine):
            z = rng.gauss(0., 1.)
            for k, shock in enumerate((z, -z)):
                s = paths[k][-1] * math.exp(drift + scale*shock)
                if not math.isfinite(s) or s <= 0:
                    raise ValueError("path overflow/underflow")
                paths[k].append(s)
        for n in grids:
            stride = fine // n
            dvals, cvals = [], []
            for path in paths:
                endpoints = path[::stride]
                payoff = discount*max(endpoints[-1]-strike, 0.)
                alive = all(s < barrier for s in endpoints)
                survival = 1.
                for a, b in zip(endpoints, endpoints[1:]):
                    survival *= bridge_survival(a, b, barrier, vol, years/n)
                dvals.append(payoff * alive)
                cvals.append(payoff * survival)
            discrete[n].append(sum(dvals)/2)
            continuous[n].append(sum(cvals)/2)
    def summary(values):
        avg = sum(values)/pairs
        se = math.sqrt(sum((v-avg)**2 for v in values)/(pairs*(pairs-1)))
        return avg, se
    rows = []
    for n in grids:
        d, dse = summary(discrete[n])
        c, cse = summary(continuous[n])
        gap, gap_se = summary([a-b for a,b in zip(discrete[n],continuous[n])])
        rows.append(dict(steps=n, discrete_call=d, discrete_se=dse,
                         continuous_bridge_call=c, continuous_se=cse,
                         discretization_gap=gap, paired_gap_se=gap_se))
    return rows

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pairs", type=int, default=2000)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--steps", type=int, nargs="+", default=[12,36,84,252])
    a = p.parse_args()
    for row in matched_grid(tuple(a.steps), pairs=a.pairs, seed=a.seed):
        print(row)
