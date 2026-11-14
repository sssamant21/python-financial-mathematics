"""Educational discrete-monitoring up-and-out European call Monte Carlo."""
import argparse
import math
import random


def simulate(spot=100.0, strike=100.0, barrier=130.0, years=1.0,
             rate=0.02, vol=0.2, steps=52, pairs=5000, seed=2026):
    values = (spot, strike, barrier, years, rate, vol)
    if (not all(math.isfinite(v) for v in values) or min(spot, strike, years) <= 0
            or barrier <= spot or vol <= 0 or type(steps) is not int or steps < 1
            or type(pairs) is not int or pairs < 2 or type(seed) is not int
            or abs(rate * years) > 700 or vol * math.sqrt(years / steps) > 10):
        raise ValueError('invalid or numerically unsafe simulation inputs')
    rng = random.Random(seed)
    dt = years / steps
    drift = (rate - 0.5 * vol * vol) * dt
    diffusion = vol * math.sqrt(dt)
    discounted = []
    vanilla = []
    knocked = 0
    for _ in range(pairs):
        a = b = spot
        alive_a = alive_b = True
        for _ in range(steps):
            z = rng.gauss(0, 1)
            a *= math.exp(drift + diffusion * z)
            b *= math.exp(drift - diffusion * z)
            alive_a = alive_a and a < barrier
            alive_b = alive_b and b < barrier
        pa = max(a - strike, 0.0)
        pb = max(b - strike, 0.0)
        vanilla.append(math.exp(-rate * years) * (pa + pb) / 2)
        discounted.append(math.exp(-rate * years) * (pa * alive_a + pb * alive_b) / 2)
        knocked += (not alive_a) + (not alive_b)
    mean = sum(discounted) / pairs
    variance = sum((v - mean) ** 2 for v in discounted) / (pairs - 1)
    return {'barrier_call': mean, 'vanilla_call': sum(vanilla) / pairs,
            'standard_error': math.sqrt(variance / pairs),
            'knockout_fraction': knocked / (2 * pairs), 'pairs': pairs}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pairs', type=int, default=5000)
    parser.add_argument('--steps', type=int, default=52)
    parser.add_argument('--seed', type=int, default=2026)
    args = parser.parse_args()
    print(simulate(pairs=args.pairs, steps=args.steps, seed=args.seed))
