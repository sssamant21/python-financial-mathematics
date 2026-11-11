"""Educational portfolio concentration diagnostics; no trading or market data."""
import math


def diagnostics(weights):
    """Return HHI, effective count, Shannon entropy, and normalized entropy."""
    values = list(weights)
    if len(values) < 2:
        raise ValueError('at least two assets required')
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0 for x in values):
        raise ValueError('weights must be finite nonnegative numbers')
    if not math.isclose(math.fsum(values), 1.0, rel_tol=0, abs_tol=1e-9):
        raise ValueError('weights must sum to one')
    hhi = math.fsum(x * x for x in values)
    entropy = -math.fsum(x * math.log(x) for x in values if x > 0)
    return {'hhi': hhi, 'effective_n': 1.0 / hhi,
            'entropy': entropy, 'normalized_entropy': entropy / math.log(len(values)),
            'largest_weight': max(values)}


def turnover(before, after):
    """One-way turnover between two fully invested long-only weight vectors."""
    a, b = list(before), list(after)
    diagnostics(a)
    diagnostics(b)
    if len(a) != len(b):
        raise ValueError('weight vectors must have equal lengths')
    return 0.5 * math.fsum(abs(x - y) for x, y in zip(a, b))


def drift(weights, returns):
    """Post-return weights before any rebalance, with simple returns >= -100%."""
    w, r = list(weights), list(returns)
    diagnostics(w)
    if len(w) != len(r):
        raise ValueError('weight and return lengths differ')
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < -1 for x in r):
        raise ValueError('returns must be finite simple returns >= -1')
    wealth = [x * (1 + y) for x, y in zip(w, r)]
    total = math.fsum(wealth)
    if total <= 0:
        raise ValueError('portfolio fully depleted')
    return [x / total for x in wealth]


if __name__ == '__main__':
    target = [0.25] * 4
    realized = [0.20, -0.10, 0.05, 0.0]
    after = drift(target, realized)
    print('Target:', diagnostics(target))
    print('After synthetic returns:', diagnostics(after))
    print('One-way rebalance turnover:', round(turnover(after, target), 6))
