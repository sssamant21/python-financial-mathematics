"""Equal-path-budget naive versus antithetic European-call Monte Carlo diagnostics."""
import argparse
import math
import random
from statistics import mean, stdev
from monte_carlo import black_scholes_call, validate


def compare(pairs=2000, seeds=(11, 23, 37, 53, 71, 89, 101, 131), spot=100., strike=100., rate=.03, dividend=0., volatility=.2, years=1.):
    """Use 2*pairs paths per estimator per seed; intervals use independent units."""
    validate(spot, strike, rate, dividend, volatility, years, pairs)
    if not isinstance(seeds, (tuple, list)) or len(seeds) < 2 or len(seeds) > 100:
        raise ValueError('provide 2 to 100 distinct integer seeds')
    if any(isinstance(s, bool) or not isinstance(s, int) for s in seeds) or len(set(seeds)) != len(seeds):
        raise ValueError('seeds must be distinct integers')
    truth = black_scholes_call(spot, strike, rate, dividend, volatility, years)
    drift = (rate - dividend - .5 * volatility ** 2) * years
    scale = volatility * math.sqrt(years)
    discount = math.exp(-rate * years)
    records = []
    for seed in seeds:
        rng = random.Random(seed)
        naive = []
        anti = []
        for _ in range(pairs):
            z1 = rng.gauss(0, 1)
            z2 = rng.gauss(0, 1)
            def payoff(z):
                return discount * max(spot * math.exp(drift + scale * z) - strike, 0.)
            naive.extend((payoff(z1), payoff(z2)))
            anti.append((payoff(z1) + payoff(-z1)) / 2)
        n_mean, a_mean = mean(naive), mean(anti)
        n_se = stdev(naive) / math.sqrt(2 * pairs)
        a_se = stdev(anti) / math.sqrt(pairs)
        records.append({'seed': seed, 'naive_price': n_mean, 'antithetic_price': a_mean,
                        'naive_se': n_se, 'antithetic_se': a_se,
                        'naive_covers': abs(n_mean - truth) <= 1.96 * n_se,
                        'antithetic_covers': abs(a_mean - truth) <= 1.96 * a_se})
    naive_var = stdev([r['naive_price'] for r in records]) ** 2
    anti_var = stdev([r['antithetic_price'] for r in records]) ** 2
    return {'benchmark': truth, 'pairs': pairs, 'paths_per_estimator': 2 * pairs,
            'seeds': len(seeds), 'naive_empirical_variance': naive_var,
            'antithetic_empirical_variance': anti_var,
            'empirical_variance_ratio': naive_var / anti_var if anti_var > 0 else None,
            'naive_coverage_fraction': mean(r['naive_covers'] for r in records),
            'antithetic_coverage_fraction': mean(r['antithetic_covers'] for r in records),
            'records': records}


def main():
    parser = argparse.ArgumentParser(description='Synthetic equal-budget Monte Carlo comparison')
    parser.add_argument('--pairs', type=int, default=2000)
    args = parser.parse_args()
    result = compare(pairs=args.pairs)
    for key, value in result.items():
        if key != 'records':
            print(f'{key}: {value}')


if __name__ == '__main__':
    main()
