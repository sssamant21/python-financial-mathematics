"""Covariance-aware equal-risk-contribution allocation; synthetic educational lab."""
import argparse
import numpy as np

def estimate_covariance(history, shrinkage=0.15):
    x = np.asarray(history, dtype=float)
    if x.ndim != 2 or x.shape[0] < 4 or x.shape[1] < 2 or not np.isfinite(x).all():
        raise ValueError("need finite history with >=4 rows and >=2 assets")
    if not np.isfinite(shrinkage) or not 0 <= shrinkage <= 1:
        raise ValueError("shrinkage must be in [0,1]")
    c = np.cov(x, rowvar=False, ddof=1)
    if np.any(np.diag(c) <= 1e-14):
        raise ValueError("zero-variance asset")
    c = (1-shrinkage)*c + shrinkage*np.diag(np.diag(c))
    if np.linalg.eigvalsh(c)[0] <= 1e-14:
        raise ValueError("covariance not positive definite")
    return c

def risk_contributions(weights, covariance):
    w, c = np.asarray(weights, float), np.asarray(covariance, float)
    if w.ndim != 1 or w.size < 2 or c.shape != (w.size, w.size):
        raise ValueError("dimension mismatch")
    if not np.isfinite(w).all() or np.any(w < 0) or not np.isclose(w.sum(), 1):
        raise ValueError("invalid weights")
    if not np.isfinite(c).all() or not np.allclose(c, c.T, atol=1e-12):
        raise ValueError("invalid covariance")
    v = float(w @ c @ w)
    if v <= 0:
        raise ValueError("nonpositive variance")
    return w * (c @ w) / v

def erc_weights(covariance, tolerance=1e-9, max_iter=20000):
    """Cyclic coordinate descent of 0.5*x'Cov*x - sum(log(x_i))."""
    c = np.asarray(covariance, float)
    if c.ndim != 2 or c.shape[0] < 2 or c.shape[0] != c.shape[1]:
        raise ValueError("covariance must be square")
    if not np.isfinite(c).all() or not np.allclose(c, c.T, atol=1e-12):
        raise ValueError("invalid covariance")
    if np.linalg.eigvalsh(c)[0] <= 1e-14:
        raise ValueError("covariance must be positive definite")
    if not np.isfinite(tolerance) or tolerance <= 0 or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("invalid solver controls")
    c = c / float(np.mean(np.diag(c)))
    x = 1 / np.sqrt(np.diag(c))
    for _ in range(max_iter):
        for i in range(x.size):
            a = c[i,i]
            b = float(c[i] @ x - a*x[i])
            x[i] = 2/(b + np.sqrt(b*b + 4*a)) if b >= 0 else (-b + np.sqrt(b*b + 4*a))/(2*a)
        w = x / x.sum()
        if np.max(np.abs(risk_contributions(w,c) - 1/x.size)) < tolerance:
            return w
    raise RuntimeError("ERC solver did not converge")

def walk_forward_stability(returns, lookback=52, horizon=13, shrinkage=0.15):
    r = np.asarray(returns, float)
    if r.ndim != 2 or r.shape[1] < 2 or not np.isfinite(r).all():
        raise ValueError("invalid returns")
    if not isinstance(lookback,int) or not isinstance(horizon,int) or lookback < 4 or horizon < 4 or r.shape[0] < lookback+horizon:
        raise ValueError("invalid windows")
    if np.any(r <= -1):
        raise ValueError("returns must exceed -100%")
    records = []
    for origin in range(lookback, r.shape[0]-horizon+1, horizon):
        train_cov = estimate_covariance(r[origin-lookback:origin], shrinkage)
        w = erc_weights(train_cov)
        train_rc = risk_contributions(w, train_cov)
        # Future observations are used only for ex-post scoring.
        heldout_cov = estimate_covariance(r[origin:origin+horizon], shrinkage)
        heldout_rc = risk_contributions(w, heldout_cov)
        records.append((origin, w.copy(), train_rc.copy(), heldout_rc.copy(),
                        float(np.max(np.abs(heldout_rc-1/w.size)))))
    return records

def demo(seed=13):
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(260,3))
    x = z @ np.array([[.014,.006,.002],[.002,.023,.005],[.003,.004,.019]])
    x[140:] = x[140:] @ np.array([[1.6,.2,0],[.1,1.2,0],[0,.15,1.5]])
    for origin,w,_,_,drift in walk_forward_stability(x):
        print(f"origin={origin} weights={np.round(w,3)} heldout_max_risk_budget_error={drift:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,default=13)
    demo(parser.parse_args().seed)
