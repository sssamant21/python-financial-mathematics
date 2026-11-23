"""Synthetic Bayesian uncertainty for a single credit-rating transition row.

A Dirichlet prior and multinomial transition counts yield a Dirichlet posterior.
No market data, empirical calibration, or investment decisions.
"""
import argparse
import json
import math
import random

def posterior_alpha(counts, prior):
    if not isinstance(counts, (list, tuple)) or not isinstance(prior, (list, tuple)):
        raise ValueError("counts and prior must be sequences")
    if not 2 <= len(counts) <= 20 or len(prior) != len(counts):
        raise ValueError("matching 2..20 rating states required")
    if any(type(x) is not int or x < 0 or x > 10**9 for x in counts):
        raise ValueError("counts must be nonnegative integers")
    if any(isinstance(x, bool) or not isinstance(x, (int, float))
           or not math.isfinite(x) or not 0 < x <= 1e6 for x in prior):
        raise ValueError("prior concentrations must be finite and positive")
    return [float(c) + float(a) for c, a in zip(counts, prior)]

def summarize_default(counts, prior, default_index, draws=4000, seed=42):
    alpha = posterior_alpha(counts, prior)
    if type(default_index) is not int or not 0 <= default_index < len(alpha):
        raise ValueError("default_index outside rating states")
    if type(draws) is not int or not 100 <= draws <= 100000:
        raise ValueError("draws must be an integer in [100, 100000]")
    if type(seed) is not int or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an integer in [0, 2**32-1]")
    rng = random.Random(seed)
    a = alpha[default_index]
    b = sum(alpha) - a
    samples = []
    for _ in range(draws):
        x = rng.gammavariate(a, 1.0)
        y = rng.gammavariate(b, 1.0)
        total = x + y
        if not math.isfinite(total) or total <= 0:
            raise ArithmeticError("unstable gamma sampling")
        samples.append(x / total)
    samples.sort()
    return {
        "posterior_mean_default": a / sum(alpha),
        "credible_interval_95": [samples[int(0.025 * draws)], samples[min(draws - 1, int(0.975 * draws))]],
        "posterior_alpha": alpha,
        "draws": draws,
        "seed": seed,
        "observed_transitions": sum(counts),
        "interpretation": "Synthetic posterior uncertainty, not a frequentist coverage guarantee",
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counts", type=int, nargs="+", default=[920, 65, 15])
    parser.add_argument("--prior", type=float, nargs="+", default=[1.0, 1.0, 1.0])
    parser.add_argument("--default-index", type=int, default=2)
    parser.add_argument("--draws", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(summarize_default(args.counts, args.prior, args.default_index,
                                       args.draws, args.seed), indent=2))

if __name__ == "__main__":
    main()
