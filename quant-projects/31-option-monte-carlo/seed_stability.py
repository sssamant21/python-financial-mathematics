"""Predeclared seed-count sensitivity; descriptive Monte Carlo diagnostics only."""
import argparse
import math
from comparison import compare

SEEDS = (11, 23, 37, 53, 71, 89, 101, 131, 149, 167, 181, 199, 223, 241, 263, 281)
COUNTS = (4, 8, 16)


def study(pairs=500, seeds=SEEDS, counts=COUNTS):
    """Nested, fixed seed prefixes; no post-hoc seed selection."""
    if isinstance(pairs, bool) or not isinstance(pairs, int) or not 2 <= pairs <= 100000:
        raise ValueError("pairs must be an integer in [2, 100000]")
    if not isinstance(seeds, (tuple, list)) or not 2 <= len(seeds) <= 100:
        raise ValueError("provide 2 to 100 distinct seeds")
    if any(isinstance(s, bool) or not isinstance(s, int) for s in seeds) or len(set(seeds)) != len(seeds):
        raise ValueError("seeds must be distinct integers")
    if not isinstance(counts, (tuple, list)) or not counts or len(counts) > 10:
        raise ValueError("provide 1 to 10 seed counts")
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 2 or n > len(seeds) for n in counts):
        raise ValueError("counts must be integers between 2 and the number of seeds")
    if sorted(set(counts)) != list(counts):
        raise ValueError("counts must be distinct and increasing")
    rows = []
    for count in counts:
        r = compare(pairs=pairs, seeds=tuple(seeds[:count]))
        rows.append({"seed_count": count, "variance_ratio": r["empirical_variance_ratio"],
                     "naive_coverage": r["naive_coverage_fraction"],
                     "antithetic_coverage": r["antithetic_coverage_fraction"],
                     "naive_variance": r["naive_empirical_variance"],
                     "antithetic_variance": r["antithetic_empirical_variance"]})
    return {"pairs": pairs, "paths_per_estimator_per_seed": 2 * pairs, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description="Synthetic predeclared seed-count sensitivity")
    parser.add_argument("--pairs", type=int, default=500)
    args = parser.parse_args()
    for row in study(pairs=args.pairs)["rows"]:
        print(row)


if __name__ == "__main__":
    main()
