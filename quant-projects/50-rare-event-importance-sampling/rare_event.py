"""Educational Bernoulli portfolio rare-event importance sampling; no market data."""
import argparse
import math
import random
import statistics


def validate(n, p, threshold, q, paths):
    if type(n) is not int or not 1 <= n <= 200:
        raise ValueError('n must be an integer from 1 to 200')
    if type(threshold) is not int or not 1 <= threshold <= n:
        raise ValueError('threshold must be an integer from 1 to n')
    if any(type(x) not in (int, float) or not math.isfinite(x) or not 0 < x < 1 for x in (p, q)):
        raise ValueError('p and q must be finite probabilities strictly between 0 and 1')
    if type(paths) is not int or not 100 <= paths <= 200000:
        raise ValueError('paths must be an integer from 100 to 200000')


def exact_tail(n, p, threshold):
    validate(n, p, threshold, p, 100)
    return sum(math.comb(n, k) * p**k * (1-p)**(n-k) for k in range(threshold, n+1))


def estimate(n=30, p=.02, threshold=5, q=.17, paths=20000, seed=50):
    validate(n, p, threshold, q, paths)
    if type(seed) is not int or not 0 <= seed <= 2**32-1:
        raise ValueError('seed must be a nonnegative 32-bit integer')
    rng = random.Random(seed)
    plain = []
    tilted = []
    for _ in range(paths):
        k_plain = sum(rng.random() < p for _ in range(n))
        k_tilt = sum(rng.random() < q for _ in range(n))
        plain.append(float(k_plain >= threshold))
        likelihood = (p/q)**k_tilt * ((1-p)/(1-q))**(n-k_tilt)
        tilted.append(likelihood if k_tilt >= threshold else 0.0)
    return {'exact': exact_tail(n,p,threshold),
            'plain': statistics.fmean(plain),
            'importance': statistics.fmean(tilted),
            'plain_se': statistics.stdev(plain)/math.sqrt(paths),
            'importance_se': statistics.stdev(tilted)/math.sqrt(paths)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, default=30)
    parser.add_argument('--p', type=float, default=.02)
    parser.add_argument('--threshold', type=int, default=5)
    parser.add_argument('--q', type=float, default=.17)
    parser.add_argument('--paths', type=int, default=20000)
    parser.add_argument('--seed', type=int, default=50)
    args = parser.parse_args()
    try:
        for key, value in estimate(**vars(args)).items():
            print(f'{key}={value:.8g}')
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
