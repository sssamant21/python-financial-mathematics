"""Seeded borrower-level tail-loss attribution (synthetic, standard library)."""
import math
import random
from statistics import NormalDist
from credit_risk import Exposure, summarize

def attribute(exposures, *, asset_correlation=0.2, scenarios=10000, seed=42, quantile=0.99):
    """Top-k scenario contributions sum to tail mean; ties use scenario order."""
    book = tuple(exposures)
    baseline = summarize(book)
    if isinstance(asset_correlation, bool) or not isinstance(asset_correlation, (int, float)) or not math.isfinite(asset_correlation) or not 0 <= asset_correlation < 1:
        raise ValueError('asset_correlation must be finite in [0,1)')
    if isinstance(scenarios, bool) or not isinstance(scenarios, int) or not 100 <= scenarios <= 100000:
        raise ValueError('scenarios must be an integer in [100,100000]')
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError('seed must be an integer')
    if isinstance(quantile, bool) or not isinstance(quantile, (int, float)) or not math.isfinite(quantile) or not 0 < quantile < 1:
        raise ValueError('quantile must be finite in (0,1)')
    if len(book) > 1000 or scenarios * len(book) > 2000000:
        raise ValueError('simulation workload exceeds guardrail')
    rng = random.Random(seed)
    a, b = math.sqrt(asset_correlation), math.sqrt(1 - asset_correlation)
    norm = NormalDist()
    thresholds = [norm.inv_cdf(x.pd) if 0 < x.pd < 1 else (-math.inf if x.pd == 0 else math.inf) for x in book]
    severities = [x.ead * x.lgd for x in book]
    outcomes = []
    for scenario in range(scenarios):
        z = rng.gauss(0, 1)
        parts = tuple(sev if a*z + b*rng.gauss(0, 1) < t else 0.0 for t, sev in zip(thresholds, severities))
        outcomes.append((math.fsum(parts), scenario, parts))
    ordered = sorted(outcomes, key=lambda row: (-row[0], row[1]))
    k = max(1, scenarios - math.ceil(quantile * scenarios) + 1)
    selected = ordered[:k]
    contributions = {x.name: math.fsum(row[2][i] for row in selected)/k for i, x in enumerate(book)}
    return {'analytical_expected_loss': baseline['expected_loss'],
            'loss_var': ordered[k-1][0],
            'tail_average_loss': math.fsum(row[0] for row in selected)/k,
            'tail_contributions': contributions, 'tail_count': k,
            'scenarios': scenarios, 'quantile': quantile,
            'ead_hhi': baseline['ead_hhi'], 'asset_correlation': asset_correlation}

def concentration_comparison(exposures, *, transfer_fraction=0.2, **kwargs):
    """Transfer EAD from largest to smallest borrower, preserving total EAD."""
    book = tuple(exposures)
    base = summarize(book)
    if len(book) < 2:
        raise ValueError('at least two borrowers required')
    if isinstance(transfer_fraction, bool) or not isinstance(transfer_fraction, (int, float)) or not math.isfinite(transfer_fraction) or not 0 < transfer_fraction < 1:
        raise ValueError('transfer_fraction must be in (0,1)')
    largest = max(range(len(book)), key=lambda i: book[i].ead)
    smallest = min(range(len(book)), key=lambda i: book[i].ead)
    if largest == smallest or book[largest].ead == book[smallest].ead:
        raise ValueError('book needs unequal EAD to transfer')
    transfer = min(book[largest].ead * transfer_fraction, (book[largest].ead - book[smallest].ead)/2)
    modified = list(book)
    for i, delta in ((largest, -transfer), (smallest, transfer)):
        x = book[i]
        modified[i] = Exposure(x.name, x.ead + delta, x.pd, x.lgd)
    return {'baseline': attribute(book, **kwargs),
            'redistributed': attribute(modified, **kwargs),
            'transfer_ead': transfer, 'total_ead': base['total_ead']}

if __name__ == '__main__':
    book = (Exposure('A', 1000000, .01, .45), Exposure('B', 500000, .03, .60), Exposure('C', 250000, .06, .50))
    print(concentration_comparison(book, scenarios=2000))
