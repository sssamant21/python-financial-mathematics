"""Repeated independent-seed precision diagnostics for a fixed synthetic tilt grid.

No tilt is selected on test outcomes; all reported comparisons are descriptive.
"""
import argparse
import math
import statistics

from rare_event import estimate, validate


def repeated_precision(n=30, p=0.02, threshold=5, tilts=(0.08, 0.17, 0.35),
                       paths=1000, repetitions=12, seed=500):
    if type(repetitions) is not int or not 3 <= repetitions <= 100:
        raise ValueError("repetitions must be an integer from 3 to 100")
    if type(seed) is not int or not 0 <= seed <= 2**32 - repetitions:
        raise ValueError("seed range exceeds 32-bit limit")
    if type(tilts) not in (tuple, list) or not 1 <= len(tilts) <= 12:
        raise ValueError("provide 1 to 12 fixed tilts")
    if any(type(q) not in (int, float) or not math.isfinite(q) for q in tilts):
        raise ValueError("tilts must be finite numbers")
    if len(set(tilts)) != len(tilts):
        raise ValueError("tilts must be distinct")
    if paths * repetitions * len(tilts) * n > 120_000_000:
        raise ValueError("simulation budget exceeds 120 million Bernoulli draws")
    for q in tilts:
        validate(n, p, threshold, q, paths)
    results = []
    for q in tilts:
        plain, tilted, reported = [], [], []
        for i in range(repetitions):
            result = estimate(n, p, threshold, q, paths, seed + i)
            plain.append(result["plain"])
            tilted.append(result["importance"])
            reported.append(result["importance_se"])
        plain_sd = statistics.stdev(plain)
        tilted_sd = statistics.stdev(tilted)
        results.append({
            "q": q, "exact": result["exact"],
            "plain_mean": statistics.fmean(plain),
            "importance_mean": statistics.fmean(tilted),
            "plain_empirical_sd": plain_sd,
            "importance_empirical_sd": tilted_sd,
            "importance_mean_reported_se": statistics.fmean(reported),
            "variance_ratio": (plain_sd / tilted_sd)**2 if tilted_sd > 0 else None,
            "repetitions": repetitions,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--p", type=float, default=0.02)
    parser.add_argument("--threshold", type=int, default=5)
    parser.add_argument("--tilts", type=float, nargs="+", default=[0.08, 0.17, 0.35])
    parser.add_argument("--paths", type=int, default=1000)
    parser.add_argument("--repetitions", type=int, default=12)
    parser.add_argument("--seed", type=int, default=500)
    args = parser.parse_args()
    try:
        for row in repeated_precision(**vars(args)):
            print(" ".join(f"{k}={v:.8g}" if isinstance(v, float) else f"{k}={v}"
                           for k, v in row.items()))
    except (ValueError, OverflowError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
