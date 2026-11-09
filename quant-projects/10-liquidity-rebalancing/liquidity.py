"""Synthetic liquidity-aware rebalancing exercise (not a trading model)."""
import argparse
import json
import numpy as np


def estimate(holdings, target_weights, prices, daily_volume, equity,
             participation=0.1, spread_bps=5.0, impact_bps=15.0,
             stress_volume_factor=1.0):
    h, w, p, v = (np.asarray(x, dtype=float) for x in
                  (holdings, target_weights, prices, daily_volume))
    arrays = (h, w, p, v)
    if any(a.ndim != 1 for a in arrays) or len(h) < 2 or any(len(a) != len(h) for a in arrays):
        raise ValueError("expected equal-length 1D arrays with >=2 assets")
    if not all(np.isfinite(a).all() for a in arrays) or not all(np.isfinite(x) for x in
            (equity, participation, spread_bps, impact_bps, stress_volume_factor)):
        raise ValueError("nonfinite input")
    if (h < 0).any() or (w < 0).any() or (p <= 0).any() or (v <= 0).any():
        raise ValueError("invalid holdings, weights, prices or volumes")
    if equity <= 0 or not np.isclose(h.sum(), equity, rtol=1e-8, atol=1e-6):
        raise ValueError("holdings must sum to equity")
    if not np.isclose(w.sum(), 1, atol=1e-9):
        raise ValueError("weights must sum to one")
    if not 0 < participation <= 1 or not 0 < stress_volume_factor <= 1 or min(spread_bps, impact_bps) < 0:
        raise ValueError("invalid capacity or costs")
    trade = equity * w - h
    capacity = p * v * participation * stress_volume_factor
    days = np.abs(trade) / capacity
    fraction = np.abs(trade) / (p * v * stress_volume_factor)
    cost = np.abs(trade) * (spread_bps / 20000 + impact_bps / 10000 * np.sqrt(fraction))
    return {"trade_dollars": trade.tolist(), "execution_days": days.tolist(),
            "estimated_cost_dollars": float(cost.sum()),
            "turnover_fraction": float(np.abs(trade).sum() / (2 * equity)),
            "max_execution_days": float(days.max()),
            "cost_bps_of_equity": float(cost.sum() / equity * 10000)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume-factor", type=float, default=1.0)
    parser.add_argument("--participation", type=float, default=0.1)
    args = parser.parse_args()
    print(json.dumps(estimate([60000, 40000], [.4, .6], [100, 50],
                              [10000, 20000], 100000,
                              participation=args.participation,
                              stress_volume_factor=args.volume_factor), indent=2))
