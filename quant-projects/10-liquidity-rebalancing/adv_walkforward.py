"""Lagged ADV and non-overlapping held-out liquidity-capacity diagnostics."""
import argparse
import json
import numpy as np


def evaluate(prices, volumes, trade_dollars, window=20, horizon=5,
             participation=0.1, stress_factors=(1.0, 0.5, 0.25)):
    """Origin t uses [t-window,t); outcome uses [t,t+horizon)."""
    p, v, q = (np.asarray(a, dtype=float) for a in (prices, volumes, trade_dollars))
    if (p.ndim != 2 or v.shape != p.shape or q.ndim != 1 or
            p.shape[1] < 2 or q.shape[0] != p.shape[1] or
            isinstance(window, bool) or isinstance(horizon, bool) or
            not isinstance(window, (int, np.integer)) or
            not isinstance(horizon, (int, np.integer)) or
            window < 2 or horizon < 1 or p.shape[0] < window + horizon):
        raise ValueError("invalid dimensions or window/horizon")
    f = np.asarray(stress_factors, dtype=float)
    if (f.ndim != 1 or len(f) == 0 or not np.isfinite(f).all() or
            (f <= 0).any() or (f > 1).any() or
            not np.isfinite(participation) or not 0 < participation <= 1 or
            not np.isfinite(q).all() or not np.isfinite(p).all() or
            not np.isfinite(v).all() or (p <= 0).any() or (v <= 0).any()):
        raise ValueError("invalid market data, trade, or stress inputs")
    dv = p * v
    rows = []
    for t in range(window, len(p) - horizon + 1, horizon):
        adv = dv[t-window:t].mean(axis=0)
        realized = dv[t:t+horizon].mean(axis=0)
        for factor in f:
            predicted_days = np.abs(q) / (participation * adv * factor)
            realized_days = np.abs(q) / (participation * realized)
            rows.append({"origin_index": int(t), "train_end_exclusive": int(t),
                         "test_end_exclusive": int(t+horizon),
                         "stress_factor": float(factor),
                         "forecast_adv_dollars": adv.tolist(),
                         "realized_adv_dollars": realized.tolist(),
                         "forecast_max_days": float(predicted_days.max()),
                         "realized_max_days": float(realized_days.max()),
                         "underestimated_capacity_days": bool(realized_days.max() > predicted_days.max())})
    return rows


def demo(window=20, horizon=5):
    rng = np.random.default_rng(20261109)
    prices = np.full((85, 2), [100., 50.])
    volumes = rng.integers(8000, 12000, size=(85, 2)).astype(float)
    volumes[60:] *= 0.35
    return evaluate(prices, volumes, [20000, -20000], window, horizon)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, default=20)
    parser.add_argument("--horizon", type=int, default=5)
    args = parser.parse_args()
    result = demo(args.window, args.horizon)
    print(json.dumps({"rows": len(result), "first": result[0], "last": result[-1]}, indent=2))
