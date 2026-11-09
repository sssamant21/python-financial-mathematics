"""Out-of-sample covariance forecasts using training-only observations."""
import numpy as np

def walk_forward_covariance(returns, weights, train=52, horizon=4, step=4, shrinkages=(0., .5, 1.)):
    """Return (origin, train_start, test_end, shrinkage, forecast_variance, realized_second_moment, squared_error)."""
    x = np.asarray(returns, dtype=float)
    w = np.asarray(weights, dtype=float)
    if x.ndim != 2 or x.shape[1] < 1 or not np.all(np.isfinite(x)):
        raise ValueError("returns must be a finite 2-D matrix")
    if w.shape != (x.shape[1],) or not np.all(np.isfinite(w)) or not np.isclose(w.sum(), 1):
        raise ValueError("weights must be finite, aligned, and sum to one")
    if not all(isinstance(v, int) and not isinstance(v, bool) for v in (train, horizon, step)) or train < 3 or horizon < 1 or step < horizon:
        raise ValueError("require train>=3, horizon>=1 and step>=horizon")
    if x.shape[0] < train + horizon:
        raise ValueError("insufficient observations")
    a = np.asarray(shrinkages, dtype=float)
    if a.ndim != 1 or not a.size or not np.all(np.isfinite(a)) or np.any((a < 0) | (a > 1)):
        raise ValueError("invalid shrinkage intensities")
    records = []
    for origin in range(train, x.shape[0] - horizon + 1, step):
        cov = np.atleast_2d(np.cov(x[origin-train:origin], rowvar=False, ddof=1))
        realized = float(np.mean((x[origin:origin+horizon] @ w)**2))
        for alpha in a:
            shrunk = (1-alpha)*cov + alpha*np.diag(np.diag(cov))
            forecast = float(w @ shrunk @ w)
            records.append((origin, origin-train, origin+horizon, float(alpha), forecast, realized, (forecast-realized)**2))
    return records

def summarize(records):
    """Compare fixed scenarios without selecting a winning parameter on test data."""
    if not records:
        raise ValueError("records cannot be empty")
    return {alpha: {"origins": sum(r[3] == alpha for r in records),
                    "variance_mse": float(np.mean([r[6] for r in records if r[3] == alpha]))}
            for alpha in sorted({r[3] for r in records})}

def example():
    rng = np.random.default_rng(20261109)
    x = rng.normal(size=(260, 1)) @ np.array([[.015, .010, -.005]]) + rng.normal(size=(260, 3)) * [.012, .011, .009]
    for alpha, result in summarize(walk_forward_covariance(x, [.5, .3, .2])).items():
        print(f"shrinkage={alpha:.1f} origins={result['origins']} variance_mse={result['variance_mse']:.10f}")

if __name__ == "__main__":
    example()
