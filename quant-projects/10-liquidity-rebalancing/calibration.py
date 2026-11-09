"""Training-only empirical ADV forecast intervals; synthetic educational diagnostics."""
import argparse
import json
import numpy as np
from adv_walkforward import evaluate


def calibrate(prices, volumes, trades, window=20, horizon=5,
              participation=0.1, alpha=0.1, min_history=3):
    """Prequential interval: only earlier completed forecast errors calibrate origin t.

    Ratio = realized_max_days / forecast_max_days. Upper multiplier uses
    conservative nearest-rank empirical quantile of past ratios. No interval
    is issued until min_history prior *completed* evaluation windows exist.
    """
    if (not np.isfinite(alpha) or not 0 < alpha < 1 or
            isinstance(min_history, bool) or not isinstance(min_history, int)
            or min_history < 2):
        raise ValueError("invalid alpha or min_history")
    rows = evaluate(prices, volumes, trades, window=window, horizon=horizon,
                    participation=participation, stress_factors=(1.0,))
    history = []
    result = []
    for row in rows:
        predicted = row["forecast_max_days"]
        actual = row["realized_max_days"]
        if predicted <= 0 or not np.isfinite(predicted) or not np.isfinite(actual):
            raise ValueError("positive finite trades and capacities required")
        # Every earlier evaluation ends no later than this origin.
        if len(history) >= min_history:
            ordered = np.sort(history)
            rank = min(len(ordered), int(np.ceil((len(ordered) + 1) * (1-alpha))))
            multiplier = float(ordered[rank - 1])
            upper = predicted * multiplier
            covered = bool(actual <= upper)
        else:
            multiplier, upper, covered = None, None, None
        result.append({"origin_index": row["origin_index"],
                       "test_end_exclusive": row["test_end_exclusive"],
                       "prior_completed_windows": len(history),
                       "forecast_max_days": predicted,
                       "realized_max_days": actual,
                       "upper_multiplier": multiplier,
                       "upper_capacity_days": upper,
                       "covered": covered})
        history.append(actual / predicted)
    return result


def demo():
    rng = np.random.default_rng(20261109)
    prices = np.full((160, 2), [100., 50.])
    volumes = rng.integers(8000, 12000, size=(160, 2)).astype(float)
    volumes[90:120] *= 0.35
    return calibrate(prices, volumes, [20000., -20000.])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alpha", type=float, default=0.1)
    args = parser.parse_args()
    # Demo data are seeded and synthetic; no third-party market data.
    rows = demo() if args.alpha == 0.1 else calibrate(
        np.full((160, 2), [100., 50.]),
        np.random.default_rng(20261109).integers(8000, 12000, size=(160, 2)),
        [20000., -20000.], alpha=args.alpha)
    evaluated = [r for r in rows if r["covered"] is not None]
    print(json.dumps({"origins": len(rows), "scored": len(evaluated),
                      "empirical_coverage": (sum(r["covered"] for r in evaluated) /
                                             len(evaluated) if evaluated else None),
                      "last": rows[-1]}, indent=2))
