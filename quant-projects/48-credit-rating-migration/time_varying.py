"""Time-varying synthetic credit migration; no market calibration."""
import math
from migration import STATES, BASE, STRESS, validate

def path_distributions(start='B', matrices=(BASE, BASE, BASE)):
    """Initial and annual state distributions; matrix t applies in year t."""
    if start not in STATES:
        raise ValueError('unknown initial rating')
    if not isinstance(matrices, (tuple, list)) or not 1 <= len(matrices) <= 50:
        raise ValueError('supply 1..50 annual matrices')
    probabilities = [float(s == start) for s in STATES]
    path = [dict(zip(STATES, probabilities))]
    for matrix in matrices:
        validate(matrix)
        probabilities = [sum(probabilities[i] * matrix[i][j] for i in range(4)) for j in range(4)]
        path.append(dict(zip(STATES, probabilities)))
    return path

def annual_default_increments(start='B', matrices=(BASE, BASE, BASE)):
    """Unconditional default mass newly accumulated in each year."""
    path = path_distributions(start, matrices)
    return [max(0.0, path[t]['D'] - path[t-1]['D']) for t in range(1, len(path))]

def scenario_summary(start='B', matrices=(BASE, BASE, BASE), lgd=0.6):
    if isinstance(lgd, bool) or not isinstance(lgd, (int, float)) or not math.isfinite(lgd) or not 0 <= lgd <= 1:
        raise ValueError('LGD must be finite in [0,1]')
    increments = annual_default_increments(start, matrices)
    return {'annual_default_mass': increments,
            'cumulative_pd': sum(increments),
            'cumulative_el_per_notional': sum(increments) * lgd}

if __name__ == '__main__':
    for name, matrices in [('baseline', (BASE, BASE, BASE)),
                           ('one-year shock', (BASE, STRESS, BASE)),
                           ('persistent stress', (STRESS, STRESS, STRESS))]:
        result = scenario_summary('B', matrices)
        print(f"{name}: PD={result['cumulative_pd']:.4%}; EL/notional={result['cumulative_el_per_notional']:.4%}")
