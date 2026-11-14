"""Exploratory grid sensitivity for Brownian-bridge barrier pricing (synthetic GBM)."""
import argparse
import math
from bridge import compare_bridge

def convergence_table(steps=(12, 52, 252), pairs=2000, seed=2026, **model):
    if (not isinstance(steps, (tuple, list)) or not steps or len(steps)>12
        or any(type(n) is not int or n<1 or n>10000 for n in steps)
        or len(set(steps)) != len(steps)):
        raise ValueError("unique positive monitoring counts required (at most 12)")
    rows = []
    for n in sorted(steps):
        r = compare_bridge(steps=n, pairs=pairs, seed=seed, **model)
        rows.append({"steps":n, "continuous_bridge_call":r["continuous_bridge_call"],
                     "continuous_se":r["continuous_se"],
                     "discrete_call":r["discrete_call"],
                     "discrete_se":r["discrete_se"],
                     "discretization_gap":r["discretization_gap"],
                     "paired_gap_se":r["paired_gap_se"]})
    # Separate grid simulations reuse a seed but are NOT matched Brownian paths.
    # Consequently, do not interpret between-grid differences as paired tests.
    return rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--steps", type=int, nargs="+", default=[12,52,252])
    args = parser.parse_args()
    for row in convergence_table(tuple(args.steps), pairs=args.pairs, seed=args.seed):
        print(row)
