"""Predeclared tilt sensitivity for the synthetic independent-default model.

Uses a separate deterministic seed per tilt; diagnostics are descriptive, not
an optimizer or proof of unbiasedness for a finite simulation.
"""
import argparse
import math
import random
import statistics

from rare_event import exact_tail, validate


def diagnose(n=30, p=0.02, threshold=5, tilts=(0.08, 0.17, 0.35),
             paths=5000, seed=50):
    if type(seed) is not int or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be a nonnegative 32-bit integer")
    if not isinstance(tilts, (tuple, list)) or not 1 <= len(tilts) <= 12:
        raise ValueError("provide 1 to 12 fixed tilts")
    if len(set(tilts)) != len(tilts):
        raise ValueError("tilts must be distinct")
    exact = exact_tail(n, p, threshold)
    rows = []
    for index, q in enumerate(tilts):
        validate(n, p, threshold, q, paths)
        rng = random.Random(seed + index)
        logp = math.log(p)
        logq = math.log(q)
        log1p = math.log1p(-p)
        log1q = math.log1p(-q)
        weighted = []
        weights = []
        hits = 0
        for _ in range(paths):
            k = sum(rng.random() < q for _ in range(n))
            weight = math.exp(k * (logp - logq) +
                              (n-k) * (log1p - log1q))
            weights.append(weight)
            hit = k >= threshold
            hits += hit
            weighted.append(weight if hit else 0.0)
        estimate = statistics.fmean(weighted)
        se = statistics.stdev(weighted) / math.sqrt(paths)
        sumw = math.fsum(weights)
        ess = sumw * sumw / math.fsum(w*w for w in weights)
        rows.append({"q": q, "estimate": estimate, "se": se,
                     "exact": exact, "absolute_error": abs(estimate-exact),
                     "event_hits": hits, "ess": ess,
                     "ess_fraction": ess / paths,
                     "weight_mean": sumw / paths})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--p", type=float, default=0.02)
    parser.add_argument("--threshold", type=int, default=5)
    parser.add_argument("--tilts", type=float, nargs="+", default=[0.08, 0.17, 0.35])
    parser.add_argument("--paths", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=50)
    args = parser.parse_args()
    try:
        for row in diagnose(**vars(args)):
            print(" ".join(f"{key}={value:.8g}" if isinstance(value, float)
                           else f"{key}={value}" for key, value in row.items()))
    except (ValueError, OverflowError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
