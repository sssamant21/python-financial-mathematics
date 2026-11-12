"""Deterministic zero-coupon bond horizon and nonparallel curve stress grid."""
from math import isfinite
from carry_roll import carry_roll

def shock_curve(curve, node_shocks):
    """Add tenor-specific decimal yield shocks without mutating inputs."""
    if not isinstance(curve, dict) or not isinstance(node_shocks, dict) or set(curve) != set(node_shocks):
        raise ValueError("shocks must have exactly the curve's tenor nodes")
    shocked = {}
    for tenor, yield_rate in curve.items():
        shock = node_shocks[tenor]
        if isinstance(shock, bool) or not isinstance(shock, (int, float)) or not isfinite(shock) or abs(shock) > 0.2:
            raise ValueError("shock must be finite, numeric and within +/- 2000 bps")
        shocked[tenor] = yield_rate + shock
    return shocked

def sensitivity_grid(face, maturity, horizons, curve, scenarios):
    """Evaluate predeclared shocks for each horizon; no future data or trading."""
    if not isinstance(horizons, (list, tuple)) or not horizons:
        raise ValueError("nonempty horizon sequence required")
    if not isinstance(scenarios, dict) or not scenarios:
        raise ValueError("nonempty scenario mapping required")
    if any(not isinstance(name, str) or not name.strip() for name in scenarios):
        raise ValueError("scenario names must be nonempty strings")
    if len(set(horizons)) != len(horizons):
        raise ValueError("horizons must be unique")
    output = []
    for horizon in horizons:
        for name, shocks in scenarios.items():
            shocked = shock_curve(curve, shocks)
            result = carry_roll(face, maturity, horizon, curve, shocked)
            output.append({"horizon_years": horizon, "scenario": name, **result})
    return output

if __name__ == "__main__":
    curve = {1.: .03, 2.: .035, 3.: .04, 5.: .045}
    scenarios = {"bear_steepener": {1.: .002, 2.: .005, 3.: .01, 5.: .015},
                 "bull_flattener": {1.: -.01, 2.: -.008, 3.: -.005, 5.: -.002}}
    for row in sensitivity_grid(100, 3, [0.5, 1.0], curve, scenarios):
        print(f"{row['scenario']:>15} h={row['horizon_years']:.1f} P&L={row['scenario_pnl']:+.6f} "
              f"carry={row['carry']:+.6f} roll={row['roll_down']:+.6f} shock={row['curve_shock_effect']:+.6f}")
