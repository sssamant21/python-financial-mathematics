"""Educational lagged volatility-targeting backtest on synthetic returns only."""
import argparse
import json
import math
import numpy as np


def run_strategy(returns, window=20, target_vol=0.12, max_leverage=1.5,
                 cost_bps=10.0, periods_per_year=252):
    """Weight at t uses returns strictly before t; costs charge weight changes."""
    r = np.asarray(returns, dtype=float)
    if r.ndim != 1 or not np.isfinite(r).all() or len(r) < window + 2:
        raise ValueError("finite 1D returns with sufficient history required")
    if isinstance(window, bool) or not isinstance(window, (int, np.integer)) or window < 3:
        raise ValueError("window must be an integer >= 3")
    if not isinstance(periods_per_year, int) or isinstance(periods_per_year, bool) or periods_per_year < 2:
        raise ValueError("invalid annualization")
    if not all(math.isfinite(float(v)) for v in (target_vol, max_leverage, cost_bps)):
        raise ValueError("nonfinite settings")
    if target_vol <= 0 or max_leverage <= 0 or cost_bps < 0:
        raise ValueError("invalid target, leverage, or cost")
    if np.any(r <= -1):
        raise ValueError("simple returns cannot be <= -100%")
    rows = []
    prev_weight = 0.0
    for t in range(window, len(r)):
        sigma = float(np.std(r[t-window:t], ddof=1) * np.sqrt(periods_per_year))
        weight = min(max_leverage, target_vol / sigma) if sigma > 0 else 0.0
        turnover = abs(weight - prev_weight)
        fee = turnover * cost_bps / 10000.0
        gross = weight * float(r[t])
        net = gross - fee
        rows.append({"index": t, "training_end_exclusive": t,
                     "forecast_vol": sigma, "weight": weight,
                     "turnover": turnover, "cost": fee,
                     "gross_return": gross, "net_return": net})
        prev_weight = weight
    return rows


def synthetic(seed=20261109, n=360):
    if isinstance(n, bool) or not isinstance(n, int) or n < 30:
        raise ValueError("n must be >= 30")
    rng = np.random.default_rng(seed)
    return np.r_[rng.normal(0.0002, 0.006, n // 2),
                 rng.normal(-0.0001, 0.018, n - n // 2)]


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=20261109)
    p.add_argument("--window", type=int, default=20)
    p.add_argument("--target-vol", type=float, default=0.12)
    p.add_argument("--cost-bps", type=float, default=10.0)
    a = p.parse_args()
    rows = run_strategy(synthetic(seed=a.seed), window=a.window,
                        target_vol=a.target_vol, cost_bps=a.cost_bps)
    print(json.dumps({"observations": len(rows),
                      "mean_turnover": float(np.mean([z["turnover"] for z in rows])),
                      "total_cost_fraction": float(sum(z["cost"] for z in rows)),
                      "first": rows[0], "last": rows[-1]}, indent=2))
