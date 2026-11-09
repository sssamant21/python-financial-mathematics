"""Point-in-time factor beta uncertainty and drift diagnostics (synthetic research only)."""
import argparse
import json
import numpy as np
from factor_lab import synthetic


def beta_diagnostics(factors, returns, window=80, horizon=20, release_lag=2,
                     ridge=0.0, draws=200, seed=20261109):
    """At origin t, train only on indices < t-release_lag; score no future observations.

    Residual bootstrap conditions on the historical factor design. Intervals quantify
    estimation noise, not factor-model misspecification or regime-break uncertainty.
    """
    x = np.asarray(factors, dtype=float)
    y = np.asarray(returns, dtype=float)
    if x.ndim != 2 or y.ndim != 1 or x.shape[0] != len(y) or not 1 <= x.shape[1] <= 20:
        raise ValueError("aligned 2D factors and 1D returns required")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("nonfinite input")
    if any(isinstance(v, bool) or not isinstance(v, (int, np.integer)) for v in
           (window, horizon, release_lag, draws, seed)):
        raise ValueError("integer settings required")
    if window < x.shape[1] + 6 or horizon < 1 or release_lag < 0 or draws < 20:
        raise ValueError("invalid window, horizon, release lag or draws")
    if not np.isfinite(ridge) or ridge < 0:
        raise ValueError("invalid ridge")
    if len(y) < window + release_lag + horizon:
        raise ValueError("insufficient history")
    rng = np.random.default_rng(seed)
    rows = []
    previous = None
    for t in range(window + release_lag, len(y) - horizon + 1, horizon):
        end = t - release_lag
        start = end - window
        design = np.column_stack((np.ones(window), x[start:end]))
        observed = y[start:end]
        if ridge == 0 and np.linalg.matrix_rank(design) < design.shape[1]:
            raise ValueError("rank-deficient factors: choose positive ridge")
        penalty = np.diag([0.0] + [ridge] * x.shape[1])
        gram = design.T @ design + penalty
        coefficients = np.linalg.solve(gram, design.T @ observed)
        residual = observed - design @ coefficients
        centered = residual - residual.mean()
        simulated = np.empty((draws, x.shape[1]))
        fitted = design @ coefficients
        for j in range(draws):
            boot_y = fitted + rng.choice(centered, size=window, replace=True)
            simulated[j] = np.linalg.solve(gram, design.T @ boot_y)[1:]
        lower, upper = np.quantile(simulated, [.025, .975], axis=0)
        beta = coefficients[1:]
        rows.append({
            "origin_index": int(t), "training_start": int(start),
            "training_end_exclusive": int(end), "release_lag": int(release_lag),
            "test_end_exclusive": int(t + horizon),
            "betas": beta.tolist(), "bootstrap_lower": lower.tolist(),
            "bootstrap_upper": upper.tolist(),
            "beta_drift_l2": None if previous is None else float(np.linalg.norm(beta - previous))
        })
        previous = beta
    return rows


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=20261109)
    p.add_argument("--release-lag", type=int, default=2)
    p.add_argument("--ridge", type=float, default=0.0)
    a = p.parse_args()
    rows = beta_diagnostics(*synthetic(seed=a.seed), release_lag=a.release_lag,
                            ridge=a.ridge, seed=a.seed)
    print(json.dumps({"origins": len(rows), "first": rows[0], "last": rows[-1]}, indent=2))
