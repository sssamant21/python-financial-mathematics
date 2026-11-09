"""Training-only walk-forward realized volatility calibration on synthetic returns."""
import argparse
import json
import math
import numpy as np
from volatility_targeting import run_strategy, synthetic


def evaluate(returns, window=20, horizon=20, target_vol=0.12,
             max_leverage=1.5, cost_bps=10.0, periods_per_year=252):
    """Disjoint forward windows; only past returns determine exposure at each origin.

    Forecast annualized portfolio volatility = exposure * trailing asset volatility.
    Realized annualized portfolio volatility uses forward *gross* strategy returns;
    net return and cost are reported separately, not treated as volatility forecasts.
    """
    r = np.asarray(returns, dtype=float)
    if isinstance(horizon, bool) or not isinstance(horizon, (int, np.integer)) or horizon < 2:
        raise ValueError("horizon must be an integer >= 2")
    rows = run_strategy(r, window=window, target_vol=target_vol,
                        max_leverage=max_leverage, cost_bps=cost_bps,
                        periods_per_year=periods_per_year)
    result = []
    for start in range(window, len(r) - horizon + 1, horizon):
        # One decision at origin, fixed exposure for the full held-out horizon.
        sigma = float(np.std(r[start-window:start], ddof=1) * math.sqrt(periods_per_year))
        weight = min(max_leverage, target_vol / sigma) if sigma > 0 else 0.0
        forward = r[start:start+horizon]
        realized = float(np.std(weight * forward, ddof=1) * math.sqrt(periods_per_year))
        forecast = weight * sigma
        # First rebalance from cash; each origin's previous exposure is known.
        prev = result[-1]["weight"] if result else 0.0
        turnover = abs(weight-prev)
        fee = turnover * cost_bps / 10000.0
        result.append({"origin": start, "train_end_exclusive": start,
                       "test_end_exclusive": start+horizon,
                       "weight": float(weight), "forecast_vol": float(forecast),
                       "realized_vol": realized, "absolute_error": abs(realized-forecast),
                       "turnover": float(turnover), "entry_cost": float(fee),
                       "heldout_gross_return": float(np.prod(1+weight*forward)-1)})
    return result


def sensitivity(returns, leverage_caps=(1.0, 1.5), costs_bps=(0.0, 10.0, 25.0),
                **kwargs):
    """Fixed predeclared scenarios, not optimized using held-out performance."""
    if not leverage_caps or not costs_bps:
        raise ValueError("nonempty scenario grids required")
    out = []
    for cap in leverage_caps:
        for cost in costs_bps:
            rows = evaluate(returns, max_leverage=cap, cost_bps=cost, **kwargs)
            if not rows:
                raise ValueError("insufficient data for held-out evaluation")
            out.append({"max_leverage": float(cap), "cost_bps": float(cost),
                        "windows": len(rows),
                        "mean_abs_vol_error": float(np.mean([x["absolute_error"] for x in rows])),
                        "total_entry_cost_fraction": float(sum(x["entry_cost"] for x in rows))})
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=20261109)
    p.add_argument("--window", type=int, default=20)
    p.add_argument("--horizon", type=int, default=20)
    a = p.parse_args()
    print(json.dumps(sensitivity(synthetic(seed=a.seed), window=a.window,
                                 horizon=a.horizon), indent=2))
