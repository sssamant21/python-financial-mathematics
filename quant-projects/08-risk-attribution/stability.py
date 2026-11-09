"""Finite-difference risk gradient and covariance-shrinkage sensitivity lab."""
from __future__ import annotations
import numpy as np
from risk_attribution import contributions


def sample_covariance(returns):
    """Sample covariance per observation period; annualize explicitly outside."""
    x = np.asarray(returns, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 1 or not np.all(np.isfinite(x)):
        raise ValueError("returns must be a finite 2-D array with at least two rows")
    return np.atleast_2d(np.cov(x, rowvar=False, ddof=1))


def shrink_to_diagonal(covariance, intensity):
    """Convex PSD-preserving shrinkage, with no fitted intensity claim."""
    c = np.asarray(covariance, dtype=float)
    if c.ndim != 2 or c.shape[0] == 0 or c.shape[0] != c.shape[1] or not np.all(np.isfinite(c)):
        raise ValueError("covariance must be a finite square matrix")
    if not np.allclose(c, c.T, atol=1e-12, rtol=1e-10) or np.linalg.eigvalsh(c).min() < -1e-10:
        raise ValueError("covariance must be symmetric positive semidefinite")
    if not np.isfinite(intensity) or not 0 <= intensity <= 1:
        raise ValueError("intensity must be between zero and one")
    return (1-intensity)*c + intensity*np.diag(np.diag(c))


def finite_difference_marginal(weights, covariance, step=1e-5):
    """Unconstrained central-difference gradient; do NOT renormalize perturbed weights."""
    w = np.asarray(weights, dtype=float)
    c = np.asarray(covariance, dtype=float)
    contributions(w, c)  # validate full portfolio and PSD assumptions
    if not np.isfinite(step) or step <= 0:
        raise ValueError("step must be finite and positive")
    out = np.empty(w.size)
    for i in range(w.size):
        shift = np.zeros_like(w)
        shift[i] = step
        positive = float((w+shift) @ c @ (w+shift))
        negative = float((w-shift) @ c @ (w-shift))
        if min(positive, negative) <= 0:
            raise ValueError("step too large for positive perturbed risk")
        out[i] = (np.sqrt(positive)-np.sqrt(negative))/(2*step)
    return out


def example():
    rng = np.random.default_rng(20261108)
    common = rng.normal(size=(120, 1))
    noise = rng.normal(size=(120, 3))
    monthly_returns = common @ np.array([[.014, .009, -.004]]) + noise * [.012, .010, .008]
    w = np.array([.5, .3, .2])
    annual_cov = sample_covariance(monthly_returns)*12
    for intensity in (0., .5, 1.):
        c = shrink_to_diagonal(annual_cov, intensity)
        vol, marginal, component = contributions(w, c)
        finite_difference = finite_difference_marginal(w, c)
        print(f"shrinkage={intensity:.1f} annual_vol={vol:.6f} "
              f"component_sum={component.sum():.6f} "
              f"max_gradient_error={np.max(np.abs(marginal-finite_difference)):.3g}")


if __name__ == "__main__":
    example()
