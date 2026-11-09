"""Synthetic, point-in-time minimum-variance hedge-ratio lab (no trading)."""
import argparse
import numpy as np

def hedge_ratio(asset_history, hedge_history, max_abs=2.0):
    """Minimize Var(asset - h*hedge) using observations known at origin."""
    a = np.asarray(asset_history, dtype=float)
    b = np.asarray(hedge_history, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or a.shape != b.shape or a.size < 8:
        raise ValueError("matching 1D histories with >=8 observations required")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("histories must be finite")
    if not np.isfinite(max_abs) or max_abs <= 0 or max_abs > 10:
        raise ValueError("invalid hedge limit")
    variance = float(np.var(b, ddof=1))
    if variance <= 1e-14:
        raise ValueError("hedge instrument has near-zero variance")
    raw = float(np.cov(a, b, ddof=1)[0, 1] / variance)
    return float(np.clip(raw, -max_abs, max_abs))

def walk_forward(asset, hedge, lookback=52, horizon=13, cost_bps=10, max_abs=2.0):
    """Non-overlapping held-out hedge evaluation; cash flows are simplified."""
    a, b = np.asarray(asset, float), np.asarray(hedge, float)
    if a.ndim != 1 or b.shape != a.shape or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("matching finite 1D return arrays required")
    if np.any(a <= -1) or np.any(b <= -1):
        raise ValueError("simple returns must exceed -100%")
    if type(lookback) is not int or type(horizon) is not int or lookback < 8 or horizon < 2:
        raise ValueError("invalid windows")
    if a.size < lookback + horizon:
        raise ValueError("insufficient history")
    if not np.isfinite(cost_bps) or not 0 <= cost_bps <= 1000:
        raise ValueError("cost must be between 0 and 1000 bps")
    rows = []
    previous = 0.0
    for origin in range(lookback, a.size - horizon + 1, horizon):
        h = hedge_ratio(a[origin-lookback:origin], b[origin-lookback:origin], max_abs)
        future_a, future_b = a[origin:origin+horizon], b[origin:origin+horizon]
        hedged = future_a - h * future_b
        turnover = abs(h - previous)
        # Costs charged once at origin; period arithmetic P&L is a stylized linear hedge.
        net = float(np.sum(hedged) - turnover * cost_bps / 10000)
        rows.append({"origin": origin, "ratio": h, "turnover": turnover,
                     "unhedged_variance": float(np.var(future_a, ddof=1)),
                     "hedged_variance": float(np.var(hedged, ddof=1)),
                     "net_arithmetic_pnl": net})
        previous = h
    return rows

def synthetic(seed=14, n=260):
    rng = np.random.default_rng(seed)
    market = rng.normal(0, .015, n)
    noise = rng.normal(0, .008, n)
    beta = np.where(np.arange(n) < n//2, 1.4, .6)
    return beta*market + noise, market

def demo(seed=14):
    a, b = synthetic(seed)
    for r in walk_forward(a, b):
        print(f"origin={r['origin']} hedge={r['ratio']:.3f} "
              f"variance={r['hedged_variance']:.7f} net_pnl={r['net_arithmetic_pnl']:.5f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=14)
    demo(parser.parse_args().seed)
