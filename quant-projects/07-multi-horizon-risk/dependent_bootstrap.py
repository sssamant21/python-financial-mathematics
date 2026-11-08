"""Dependence-aware horizon-loss bootstrap; synthetic educational research only."""
import numpy as np


def bootstrap_horizon_losses(weekly_returns, horizon, block_length=4, draws=2000, seed=2026):
    """Circular moving-block bootstrap of historical weekly returns.

    Each synthetic path contains `horizon` consecutive resampled weekly returns.
    Blocks retain local ordering within the training sample, with circular wrap.
    Never pass returns from or after the forecast origin.
    """
    r = np.asarray(weekly_returns, dtype=float)
    if r.ndim != 1 or len(r) < 30 or not np.isfinite(r).all() or np.any(r <= -1):
        raise ValueError("Require at least 30 finite weekly simple returns greater than -1")
    if type(horizon) is not int or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    if type(block_length) is not int or not 1 <= block_length <= len(r):
        raise ValueError("block_length must be in [1, training sample size]")
    if type(draws) is not int or not 100 <= draws <= 100000:
        raise ValueError("draws must be an integer in [100, 100000]")
    if type(seed) is not int or not 0 <= seed < 2**64:
        raise ValueError("seed must be a nonnegative integer below 2**64")
    rng = np.random.default_rng(seed)
    blocks = (horizon + block_length - 1) // block_length
    starts = rng.integers(0, len(r), size=(draws, blocks))
    offsets = np.arange(block_length)
    indexes = ((starts[..., None] + offsets) % len(r)).reshape(draws, -1)[:, :horizon]
    return -np.expm1(np.log1p(r[indexes]).sum(axis=1))


def bootstrap_var_cvar(losses, alpha=0.05):
    """Return nonnegative empirical VaR and tail-mean CVaR, as fractions of capital."""
    x = np.asarray(losses, dtype=float)
    if x.ndim != 1 or len(x) < 100 or not np.isfinite(x).all():
        raise ValueError("Require at least 100 finite bootstrap losses")
    if not np.isfinite(alpha) or not 0 < alpha < 0.5:
        raise ValueError("alpha must be in (0, 0.5)")
    cutoff = float(np.quantile(x, 1 - alpha))
    return max(0.0, cutoff), max(0.0, float(x[x >= cutoff].mean()))
