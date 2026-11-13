"""Predeclared synthetic strike/volatility sensitivity for equal-budget Monte Carlo."""
import argparse
import math
from comparison import compare

SEEDS = (11, 23, 37, 53, 71, 89, 101, 131)
STRIKES = (80., 100., 120.)
VOLATILITIES = (.1, .2, .4)


def grid(pairs=500, seeds=SEEDS, strikes=STRIKES, volatilities=VOLATILITIES):
    """Return scenario metrics without ex-post seed or scenario selection."""
    for name, values in (('strikes', strikes), ('volatilities', volatilities)):
        if not isinstance(values, (tuple, list)) or not 1 <= len(values) <= 10:
            raise ValueError(f'{name} must contain 1 to 10 values')
        if any(isinstance(x, bool) or not isinstance(x, (int, float))
               or not math.isfinite(x) or x <= 0 for x in values):
            raise ValueError(f'{name} must contain positive finite numbers')
        if len(set(values)) != len(values):
            raise ValueError(f'{name} must be distinct')
    rows = []
    for strike in strikes:
        for volatility in volatilities:
            r = compare(pairs=pairs, seeds=seeds, strike=strike, volatility=volatility)
            rows.append({'strike': strike, 'volatility': volatility,
                         'benchmark': r['benchmark'],
                         'variance_ratio': r['empirical_variance_ratio'],
                         'naive_coverage': r['naive_coverage_fraction'],
                         'antithetic_coverage': r['antithetic_coverage_fraction'],
                         'naive_variance': r['naive_empirical_variance'],
                         'antithetic_variance': r['antithetic_empirical_variance']})
    return {'pairs': pairs, 'paths_per_method': 2 * pairs,
            'seed_count': len(seeds), 'rows': rows}


def main():
    parser = argparse.ArgumentParser(description='Synthetic option Monte Carlo sensitivity')
    parser.add_argument('--pairs', type=int, default=500)
    args = parser.parse_args()
    r = grid(pairs=args.pairs)
    print('strike volatility benchmark variance_ratio naive_coverage antithetic_coverage')
    for row in r['rows']:
        print(f"{row['strike']:.0f} {row['volatility']:.2f} {row['benchmark']:.6f} "
              f"{row['variance_ratio']} {row['naive_coverage']:.3f} {row['antithetic_coverage']:.3f}")


if __name__ == '__main__':
    main()
