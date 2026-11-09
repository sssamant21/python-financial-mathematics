"""Educational variance-based portfolio risk attribution, with synthetic inputs."""
from __future__ import annotations
import argparse
import numpy as np


def contributions(weights, covariance):
    """Return volatility, marginal and component volatility contributions.

    Covariance is annualized; contributions sum to portfolio annualized volatility.
    Negative contributions are possible for hedging positions.
    """
    w = np.asarray(weights, dtype=float)
    c = np.asarray(covariance, dtype=float)
    if w.ndim != 1 or not w.size or not np.all(np.isfinite(w)):
        raise ValueError('weights must be a finite nonempty vector')
    if c.shape != (w.size, w.size) or not np.all(np.isfinite(c)):
        raise ValueError('covariance shape/values invalid')
    if not np.allclose(c, c.T, atol=1e-12, rtol=1e-10):
        raise ValueError('covariance must be symmetric')
    if np.linalg.eigvalsh(c).min() < -1e-10:
        raise ValueError('covariance must be positive semidefinite')
    if not np.isclose(w.sum(), 1.0, atol=1e-9):
        raise ValueError('weights must sum to one')
    var = float(w @ c @ w)
    if var <= 1e-14:
        raise ValueError('portfolio volatility must be positive')
    vol = float(np.sqrt(var))
    marginal = c @ w / vol
    component = w * marginal
    return vol, marginal, component


def normal_var_contributions(weights, covariance, z=1.6448536269514722, horizon=1):
    """Zero-mean normal loss VaR Euler contributions, iid period assumption."""
    if not np.isfinite(z) or z <= 0 or not isinstance(horizon, int) or horizon < 1:
        raise ValueError('z must be positive and horizon a positive integer')
    vol, marginal, component = contributions(weights, covariance)
    factor = float(z * np.sqrt(horizon))
    return factor * vol, factor * marginal, factor * component


def example():
    w = np.array([0.5, 0.3, 0.2])
    annual_vol = np.array([0.20, 0.15, 0.10])
    corr = np.array([[1, .4, .1], [.4, 1, .2], [.1, .2, 1]])
    cov = np.outer(annual_vol, annual_vol) * corr
    vol, _, components = contributions(w, cov)
    print(f'annual volatility: {vol:.6f}')
    for label, value in zip(('Technology', 'Bank', 'Utilities'), components):
        print(f'{label} component volatility: {value:.6f} ({value/vol:.1%})')
    print(f'component sum: {components.sum():.6f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    example()
