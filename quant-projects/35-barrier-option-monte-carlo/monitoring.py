"""Matched-grid discrete up-and-out Monte Carlo and vanilla BS benchmark."""
import argparse
import math
import random


def black_scholes_call(spot, strike, years, rate, vol):
    if not all(math.isfinite(x) for x in (spot, strike, years, rate, vol)) or min(spot, strike, years, vol) <= 0 or abs(rate * years) > 700:
        raise ValueError('invalid Black-Scholes inputs')
    d1 = (math.log(spot / strike) + (rate + vol * vol / 2) * years) / (vol * math.sqrt(years))
    d2 = d1 - vol * math.sqrt(years)
    cdf = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))
    return spot * cdf(d1) - strike * math.exp(-rate * years) * cdf(d2)


def matched_monitoring(spot=100.0, strike=100.0, barrier=130.0, years=1.0,
                       rate=0.02, vol=0.2, fine_steps=252, monitoring=(12, 36, 84, 252),
                       pairs=2000, seed=2026):
    values = (spot, strike, barrier, years, rate, vol)
    if (not all(math.isfinite(v) for v in values) or min(spot, strike, years, vol) <= 0
            or barrier <= spot or abs(rate * years) > 700
            or type(fine_steps) is not int or not 1 <= fine_steps <= 10000
            or type(pairs) is not int or not 2 <= pairs <= 1000000
            or type(seed) is not int or not isinstance(monitoring, (tuple, list)) or not monitoring
            or any(type(n) is not int or n < 1 or fine_steps % n for n in monitoring)
            or len(set(monitoring)) != len(monitoring)
            or vol * math.sqrt(years / fine_steps) > 10
            or abs((rate - vol * vol / 2) * years / fine_steps) > 700):
        raise ValueError('invalid or non-nested monitoring grid')
    grids = tuple(sorted(monitoring))
    rng = random.Random(seed)
    dt = years / fine_steps
    drift = (rate - vol * vol / 2) * dt
    scale = vol * math.sqrt(dt)
    discount = math.exp(-rate * years)
    sums = {n: [] for n in grids}
    knockouts = {n: 0 for n in grids}
    vanilla = []
    for _ in range(pairs):
        paths = [spot, spot]
        alive = {n: [True, True] for n in grids}
        for step in range(1, fine_steps + 1):
            z = rng.gauss(0, 1)
            paths[0] *= math.exp(drift + scale * z)
            paths[1] *= math.exp(drift - scale * z)
            for n in grids:
                if step % (fine_steps // n) == 0:
                    for k in range(2):
                        alive[n][k] = alive[n][k] and paths[k] < barrier
        payoffs = [max(p - strike, 0.0) for p in paths]
        vanilla.append(discount * sum(payoffs) / 2)
        for n in grids:
            sums[n].append(discount * sum(payoffs[k] * alive[n][k] for k in range(2)) / 2)
            knockouts[n] += sum(not x for x in alive[n])
    vmean = sum(vanilla) / pairs
    results = []
    for n in grids:
        xs = sums[n]
        mean = sum(xs) / pairs
        se = math.sqrt(sum((x - mean) ** 2 for x in xs) / (pairs * (pairs - 1)))
        results.append({'steps': n, 'barrier_call': mean, 'standard_error': se,
                        'knockout_fraction': knockouts[n] / (2 * pairs)})
    bs = black_scholes_call(spot, strike, years, rate, vol)
    vse = math.sqrt(sum((x - vmean) ** 2 for x in vanilla) / (pairs * (pairs - 1)))
    return {'grids': results, 'vanilla_mc': vmean, 'vanilla_standard_error': vse,
            'vanilla_bs': bs, 'vanilla_mc_minus_bs': vmean - bs, 'pairs': pairs}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pairs', type=int, default=2000)
    p.add_argument('--seed', type=int, default=2026)
    args = p.parse_args()
    print(matched_monitoring(pairs=args.pairs, seed=args.seed))
