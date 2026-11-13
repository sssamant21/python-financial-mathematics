"""Educational risk-neutral European call Monte Carlo with antithetic pairs."""
import argparse
import math
import random
from statistics import NormalDist


def validate(spot, strike, rate, dividend, volatility, years, pairs):
    values = (spot, strike, rate, dividend, volatility, years)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError('parameters must be finite real numbers')
    if spot <= 0 or strike <= 0 or years <= 0 or volatility <= 0:
        raise ValueError('spot, strike, years, and volatility must be positive')
    if not (-1 < rate < 1) or not (-1 < dividend < 1) or volatility > 3 or years > 100:
        raise ValueError('rate/dividend/volatility/horizon outside educational guardrails')
    if isinstance(pairs, bool) or not isinstance(pairs, int) or not 2 <= pairs <= 2_000_000:
        raise ValueError('pairs must be an integer from 2 to 2,000,000')


def black_scholes_call(spot, strike, rate, dividend, volatility, years):
    validate(spot, strike, rate, dividend, volatility, years, 2)
    scale = volatility * math.sqrt(years)
    d1 = (math.log(spot / strike) + (rate - dividend + 0.5 * volatility ** 2) * years) / scale
    d2 = d1 - scale
    cdf = NormalDist().cdf
    return spot * math.exp(-dividend * years) * cdf(d1) - strike * math.exp(-rate * years) * cdf(d2)


def estimate(spot=100., strike=100., rate=.03, dividend=0., volatility=.2, years=1., pairs=10000, seed=2026):
    validate(spot, strike, rate, dividend, volatility, years, pairs)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError('seed must be an integer')
    rng = random.Random(seed)
    drift = (rate - dividend - .5 * volatility ** 2) * years
    diffusion = volatility * math.sqrt(years)
    discount = math.exp(-rate * years)
    n = 0
    mean = m2 = 0.
    for _ in range(pairs):
        z = rng.gauss(0, 1)
        plus = max(spot * math.exp(drift + diffusion * z) - strike, 0.)
        minus = max(spot * math.exp(drift - diffusion * z) - strike, 0.)
        observation = discount * (plus + minus) / 2
        n += 1
        delta = observation - mean
        mean += delta / n
        m2 += delta * (observation - mean)
    se = math.sqrt(m2 / (n - 1) / n)
    benchmark = black_scholes_call(spot, strike, rate, dividend, volatility, years)
    return {'price': mean, 'standard_error': se, 'ci95_low': mean - 1.96 * se,
            'ci95_high': mean + 1.96 * se, 'black_scholes': benchmark,
            'error': mean - benchmark, 'pairs': n, 'paths': 2 * n}


def main():
    parser = argparse.ArgumentParser(description='Synthetic European call antithetic Monte Carlo')
    parser.add_argument('--pairs', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=2026)
    args = parser.parse_args()
    for key, value in estimate(pairs=args.pairs, seed=args.seed).items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()
