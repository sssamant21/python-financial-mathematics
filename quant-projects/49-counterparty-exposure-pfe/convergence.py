"""Independent-seed synthetic Brownian EPE convergence; educational only."""
import argparse
import math
from statistics import mean, stdev
from diagnostics import brownian_epe
from exposure import simulate

def convergence(*, path_counts=(200, 800, 3200), seeds=(11, 23, 37, 49, 71),
                notional=1000., volatility=.2, year=2, threshold=0.):
    """Between-seed SE measures mean-of-independent-runs variability, not CVA/PFE risk."""
    counts, seed_values = tuple(path_counts), tuple(seeds)
    if not counts or any(type(n) is not int or not 100 <= n <= 200000 for n in counts):
        raise ValueError("path_counts must be integers in 100..200000")
    if tuple(sorted(set(counts))) != counts:
        raise ValueError("path_counts must be unique and increasing")
    if len(seed_values) < 2 or len(set(seed_values)) != len(seed_values) or any(type(s) is not int for s in seed_values):
        raise ValueError("at least two distinct integer seeds required")
    target = brownian_epe(notional=notional, volatility=volatility, year=year, threshold=threshold)
    if len(seed_values) * sum(counts) * year > 3_000_000:
        raise ValueError("simulation budget exceeded")
    rows = []
    for n in counts:
        estimates = [simulate(notional=notional, volatility=volatility, years=year,
                              paths=n, threshold=threshold, seed=s)[-1]["epe"]
                     for s in seed_values]
        avg = mean(estimates)
        rows.append(dict(paths=n, seeds=len(estimates), mean_epe=avg,
                         between_seed_se=stdev(estimates)/math.sqrt(len(estimates)),
                         analytical_epe=target, absolute_error=abs(avg-target)))
    return rows

def main():
    parser = argparse.ArgumentParser(description="Synthetic multi-seed Brownian EPE convergence")
    parser.add_argument("--paths", nargs="+", type=int, default=[200, 800, 3200])
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 23, 37, 49, 71])
    args = parser.parse_args()
    keys = ("paths", "seeds", "mean_epe", "between_seed_se", "analytical_epe", "absolute_error")
    print(",".join(keys))
    for row in convergence(path_counts=args.paths, seeds=args.seeds):
        print(",".join(str(row[k]) for k in keys))

if __name__ == "__main__":
    main()
