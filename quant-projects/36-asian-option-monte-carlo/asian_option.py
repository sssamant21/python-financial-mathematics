"""Synthetic arithmetic-average Asian call Monte Carlo (Python 3.11+, stdlib)."""
import argparse
import math
import random
from statistics import mean, stdev


def price_asian_call(spot=100.0, strike=100.0, rate=0.03, volatility=0.2,
                     maturity=1.0, observations=12, pairs=5000, seed=2026):
    """Risk-neutral discrete arithmetic average of post-initial observation prices."""
    values = (spot, strike, rate, volatility, maturity)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("parameters must be finite")
    if spot <= 0 or strike <= 0 or maturity <= 0 or volatility <= 0:
        raise ValueError("spot, strike, maturity and volatility must be positive")
    if not isinstance(observations, int) or isinstance(observations, bool) or not 1 <= observations <= 1000:
        raise ValueError("observations must be an integer from 1 to 1000")
    if not isinstance(pairs, int) or isinstance(pairs, bool) or not 2 <= pairs <= 1_000_000:
        raise ValueError("pairs must be an integer from 2 to 1000000")
    if abs(rate * maturity) > 50 or volatility * math.sqrt(maturity / observations) > 3:
        raise ValueError("unsafe exponent range")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be an integer")
    rng = random.Random(seed)
    dt = maturity / observations
    drift = (rate - 0.5 * volatility ** 2) * dt
    diffusion = volatility * math.sqrt(dt)
    discount = math.exp(-rate * maturity)
    pair_means = []
    vanilla_means = []
    for _ in range(pairs):
        prices = [spot, spot]
        totals = [0.0, 0.0]
        for _ in range(observations):
            z = rng.gauss(0, 1)
            for j, sign in enumerate((1, -1)):
                prices[j] *= math.exp(drift + sign * diffusion * z)
                totals[j] += prices[j]
        asian = [discount * max(total / observations - strike, 0.0) for total in totals]
        vanilla = [discount * max(p - strike, 0.0) for p in prices]
        pair_means.append(sum(asian) / 2)
        vanilla_means.append(sum(vanilla) / 2)
    estimate = mean(pair_means)
    stderr = stdev(pair_means) / math.sqrt(pairs)
    return {"asian_price": estimate, "standard_error": stderr,
            "vanilla_price": mean(vanilla_means), "pairs": pairs,
            "observations": observations, "seed": seed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=int, default=5000)
    parser.add_argument("--observations", type=int, default=12)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    for key, value in price_asian_call(pairs=args.pairs, observations=args.observations, seed=args.seed).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
