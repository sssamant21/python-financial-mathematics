"""Seeded one-factor Gaussian credit default simulation (educational, stdlib)."""
import math
import random
from statistics import NormalDist
from credit_risk import Exposure, summarize

_NORMAL = NormalDist()

def simulate(exposures, *, asset_correlation=0.2, scenarios=10000, seed=42, quantile=0.99):
    """Return empirical loss VaR/ES and simulated mean, without market calibration.

    Conditional defaults use sqrt(rho)*systematic + sqrt(1-rho)*idiosyncratic.
    rho is a common latent-factor loading squared, NOT pairwise default correlation.
    """
    exposures = tuple(exposures)
    baseline = summarize(exposures)
    if isinstance(asset_correlation, bool) or not isinstance(asset_correlation, (int, float)) or not math.isfinite(asset_correlation) or not 0 <= asset_correlation < 1:
        raise ValueError('asset_correlation must be finite in [0,1)')
    if isinstance(scenarios, bool) or not isinstance(scenarios, int) or not 100 <= scenarios <= 1000000:
        raise ValueError('scenarios must be an integer in [100, 1000000]')
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError('seed must be an integer')
    if isinstance(quantile, bool) or not isinstance(quantile, (int, float)) or not math.isfinite(quantile) or not 0 < quantile < 1:
        raise ValueError('quantile must be finite in (0,1)')
    rng = random.Random(seed)
    thresholds = [_NORMAL.inv_cdf(x.pd) if 0 < x.pd < 1 else (-math.inf if x.pd == 0 else math.inf) for x in exposures]
    severities = [x.ead * x.lgd for x in exposures]
    a, b = math.sqrt(asset_correlation), math.sqrt(1 - asset_correlation)
    losses = []
    for _ in range(scenarios):
        z = rng.gauss(0, 1)
        loss = sum(severity for threshold, severity in zip(thresholds, severities)
                   if a*z + b*rng.gauss(0, 1) < threshold)
        losses.append(loss)
    losses.sort()
    index = math.ceil(quantile * scenarios) - 1
    var = losses[index]
    tail = losses[index:]
    return {'analytical_expected_loss': baseline['expected_loss'],
            'simulated_mean_loss': math.fsum(losses)/scenarios,
            'loss_var': var, 'loss_expected_shortfall': math.fsum(tail)/len(tail),
            'unexpected_loss_var': var - baseline['expected_loss'],
            'scenarios': scenarios, 'asset_correlation': asset_correlation, 'quantile': quantile}

if __name__ == '__main__':
    book = (Exposure('A', 1_000_000, .01, .45), Exposure('B', 500_000, .03, .60), Exposure('C', 250_000, .06, .50))
    print(simulate(book))
