"""Educational, synthetic-only walk-forward inverse-volatility allocation."""
import argparse
import numpy as np

def weights_from_history(history, floor=1e-6, cap=0.7):
    x = np.asarray(history, dtype=float)
    if x.ndim != 2 or x.shape[0] < 3 or x.shape[1] < 2 or not np.isfinite(x).all():
        raise ValueError("history must be finite 2D with >=3 rows and >=2 assets")
    if not (0 < floor < 1 and 1/x.shape[1] <= cap <= 1):
        raise ValueError("invalid floor or infeasible cap")
    vol = np.std(x, axis=0, ddof=1)
    raw = 1 / np.maximum(vol, floor)
    # Capped simplex projection by iterative water filling.
    w = np.zeros(x.shape[1])
    free = np.ones(x.shape[1], dtype=bool)
    remaining = 1.0
    while free.any():
        candidate = remaining * raw[free] / raw[free].sum()
        exceed = candidate > cap + 1e-12
        if not exceed.any():
            w[free] = candidate
            break
        ids = np.where(free)[0]
        w[ids[exceed]] = cap
        remaining -= cap * int(exceed.sum())
        free[ids[exceed]] = False
    return w

def walk_forward(returns, lookback=52, horizon=13, cost_bps=10, cap=0.7):
    x = np.asarray(returns, dtype=float)
    if x.ndim != 2 or x.shape[1] < 2 or x.shape[0] < lookback + horizon or not np.isfinite(x).all():
        raise ValueError("insufficient finite 2D returns")
    if lookback < 3 or horizon < 1 or not (0 <= cost_bps <= 1000):
        raise ValueError("invalid window or transaction cost")
    if np.any(x <= -1):
        raise ValueError("returns must exceed -100%")
    previous = np.zeros(x.shape[1])
    records = []
    for origin in range(lookback, x.shape[0] - horizon + 1, horizon):
        w = weights_from_history(x[origin-lookback:origin], cap=cap)
        turnover = float(np.abs(w - previous).sum())
        # Buy-and-hold through each held-out block; no future-informed rebalancing.
        gross = float(np.prod(1 + x[origin:origin+horizon] @ w) - 1)
        net = (1 + gross) * (1 - turnover * cost_bps / 10000) - 1
        records.append((origin, gross, net, turnover, *w))
        # Approximate end-of-window drift from cumulative asset returns.
        asset_growth = np.prod(1 + x[origin:origin+horizon], axis=0)
        drift = w * asset_growth
        previous = drift / drift.sum()
    return np.array(records)

def demo(seed=13):
    rng = np.random.default_rng(seed)
    x = rng.normal(0.001, [0.012, 0.025, 0.018], size=(260, 3))
    x[140:] *= [2.0, 1.2, 1.8]
    result = walk_forward(x)
    for row in result:
        print(f"origin={int(row[0])} gross={row[1]:+.4f} net={row[2]:+.4f} turnover={row[3]:.3f}")
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=13)
    demo(p.parse_args().seed)
