"""Synthetic rolling factor exposure diagnostics; educational, no trading."""
import argparse
import json
import numpy as np


def rolling_exposures(factors, returns, window=60, horizon=20, ridge=0.0):
    """Fit intercept + factor loadings on [t-window,t), score [t,t+horizon)."""
    x = np.asarray(factors, dtype=float)
    y = np.asarray(returns, dtype=float)
    if x.ndim != 2 or y.ndim != 1 or len(x) != len(y) or not 1 <= x.shape[1] <= 20:
        raise ValueError('expected aligned 2D factors and 1D portfolio returns')
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError('nonfinite data')
    if isinstance(window, bool) or isinstance(horizon, bool) or not isinstance(window, int) or not isinstance(horizon, int) or window < x.shape[1] + 5 or horizon < 1 or len(y) < window + horizon:
        raise ValueError('invalid window or horizon')
    if not np.isfinite(ridge) or ridge < 0:
        raise ValueError('ridge must be finite and nonnegative')
    out = []
    for t in range(window, len(y) - horizon + 1, horizon):
        train = np.column_stack([np.ones(window), x[t-window:t]])
        target = y[t-window:t]
        if ridge == 0:
            if np.linalg.matrix_rank(train) < train.shape[1]:
                raise ValueError('rank-deficient training factors; use positive ridge')
            coef = np.linalg.lstsq(train, target, rcond=None)[0]
        else:
            penalty = np.diag([0.0] + [ridge] * x.shape[1])
            coef = np.linalg.solve(train.T @ train + penalty, train.T @ target)
        predictions = coef[0] + x[t:t+horizon] @ coef[1:]
        realized = y[t:t+horizon]
        out.append({'origin_index': t, 'test_end_exclusive': t+horizon,
                    'intercept': float(coef[0]), 'betas': coef[1:].tolist(),
                    'heldout_mse': float(np.mean((realized-predictions)**2)),
                    'heldout_mean_residual': float(np.mean(realized-predictions))})
    return out


def synthetic(seed=20261109, n=320):
    rng = np.random.default_rng(seed)
    factors = rng.normal(0, .01, (n, 3))
    betas = np.tile([1.1, .4, -.3], (n, 1))
    betas[n//2:, 0] = 1.7
    returns = .0002 + np.sum(factors * betas, axis=1) + rng.normal(0, .003, n)
    return factors, returns


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed', type=int, default=20261109)
    p.add_argument('--window', type=int, default=80)
    p.add_argument('--horizon', type=int, default=20)
    a = p.parse_args()
    rows = rolling_exposures(*synthetic(seed=a.seed), window=a.window, horizon=a.horizon)
    print(json.dumps({'origins': len(rows), 'first': rows[0], 'last': rows[-1],
                      'mean_heldout_mse': float(np.mean([r['heldout_mse'] for r in rows]))}, indent=2))
