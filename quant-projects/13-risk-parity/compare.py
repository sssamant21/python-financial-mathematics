"""Synthetic-only point-in-time inverse-volatility versus ERC comparison."""
import argparse
import numpy as np
from erc import estimate_covariance, erc_weights, risk_contributions
from risk_parity import weights_from_history

def compare(returns, lookback=52, horizon=13, cost_bps=10, shrinkage=0.15):
    """Matched uncapped long-only portfolios, held as shares through each block."""
    r = np.asarray(returns, dtype=float)
    if r.ndim != 2 or r.shape[1] < 2 or not np.isfinite(r).all():
        raise ValueError("returns must be finite 2D with at least two assets")
    if not isinstance(lookback, int) or isinstance(lookback, bool) or lookback < 4:
        raise ValueError("lookback must be an integer >=4")
    if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon < 4:
        raise ValueError("horizon must be an integer >=4")
    if r.shape[0] < lookback + horizon or np.any(r <= -1):
        raise ValueError("insufficient history or return <= -100%")
    if not np.isfinite(cost_bps) or not 0 <= cost_bps <= 1000:
        raise ValueError("cost_bps must be between 0 and 1000")
    if not np.isfinite(shrinkage) or not 0 <= shrinkage <= 1:
        raise ValueError("shrinkage must be between 0 and 1")
    state = {name: {"wealth": 1., "previous": np.zeros(r.shape[1])}
             for name in ("inverse_vol", "erc")}
    rows = []
    for origin in range(lookback, r.shape[0]-horizon+1, horizon):
        train = r[origin-lookback:origin]
        cov = estimate_covariance(train, shrinkage)
        targets = {"inverse_vol": weights_from_history(train, cap=1.),
                   "erc": erc_weights(cov)}
        future = r[origin:origin+horizon]
        growth = np.prod(1 + future, axis=0)
        heldout_cov = estimate_covariance(future, shrinkage)
        for name, w in targets.items():
            s = state[name]
            turnover = float(np.abs(w-s["previous"]).sum())
            fee = turnover * cost_bps / 10000
            gross_factor = float(w @ growth)
            s["wealth"] *= (1-fee) * gross_factor
            s["previous"] = w * growth / gross_factor
            heldout_rc = risk_contributions(w, heldout_cov)
            rows.append({"origin": origin, "method": name,
                         "weights": w.copy(), "turnover": turnover,
                         "gross_return": gross_factor-1,
                         "net_return": (1-fee)*gross_factor-1,
                         "wealth": s["wealth"],
                         "heldout_max_rc_error": float(np.max(np.abs(heldout_rc-1/w.size)))})
    return rows

def synthetic(seed=13):
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(260,3))
    r = z @ np.array([[.012,.004,.001],[.002,.022,.005],[.003,.004,.017]])
    r[140:] = r[140:] @ np.array([[1.5,.2,0],[.1,1.2,0],[0,.1,1.7]])
    return r

def demo(seed=13):
    for row in compare(synthetic(seed)):
        print(f"origin={row['origin']} method={row['method']} wealth={row['wealth']:.5f} "
              f"turnover={row['turnover']:.3f} heldout_rc_error={row['heldout_max_rc_error']:.4f}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=13)
    demo(p.parse_args().seed)
