"""Synthetic fixed-income carry and roll-down: annual zero-coupon spot curve."""
from math import exp, isfinite

def _rate(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not isfinite(x) or not (-0.5 < x < 1):
        raise ValueError("rates must be finite decimals between -0.5 and 1")
    return float(x)

def price(face, maturity, curve):
    """Continuous-compounding zero-coupon price with linear spot interpolation."""
    if isinstance(face, bool) or not isinstance(face, (int, float)) or not isfinite(face) or face <= 0:
        raise ValueError("face must be positive finite")
    if isinstance(maturity, bool) or not isinstance(maturity, (int, float)) or not isfinite(maturity) or maturity <= 0:
        raise ValueError("maturity must be positive finite")
    if not isinstance(curve, dict) or len(curve) < 2:
        raise ValueError("at least two curve nodes required")
    nodes = sorted(curve.items())
    if any(isinstance(t, bool) or not isinstance(t, (int, float)) or not isfinite(t) or t <= 0 for t, _ in nodes):
        raise ValueError("positive finite tenors required")
    if len({float(t) for t, _ in nodes}) != len(nodes):
        raise ValueError("duplicate tenor")
    for _, r in nodes: _rate(r)
    if maturity < nodes[0][0] or maturity > nodes[-1][0]:
        raise ValueError("maturity outside observed curve; extrapolation prohibited")
    for t, r in nodes:
        if maturity == t: return float(face) * exp(-_rate(r) * maturity)
    for (a, ra), (b, rb) in zip(nodes, nodes[1:]):
        if a < maturity < b:
            rate = ra + (rb - ra) * (maturity - a) / (b - a)
            return float(face) * exp(-rate * maturity)
    raise ValueError("invalid curve")

def carry_roll(face, maturity, holding_years, curve, shocked_curve=None):
    """Frozen-curve roll-down versus unchanged-tenor yield, plus scenario P&L."""
    if isinstance(holding_years, bool) or not isinstance(holding_years, (int, float)) or not isfinite(holding_years) or holding_years <= 0 or holding_years >= maturity:
        raise ValueError("holding years must be strictly between zero and maturity")
    start = price(face, maturity, curve)
    remaining = maturity - holding_years
    rolled = price(face, remaining, curve)
    initial_yield = -__import__("math").log(start / face) / maturity
    unchanged_tenor = face * exp(-initial_yield * remaining)
    stressed = price(face, remaining, shocked_curve if shocked_curve is not None else curve)
    return {"start": start, "rolled": rolled, "unchanged_tenor": unchanged_tenor,
            "carry": unchanged_tenor - start, "roll_down": rolled - unchanged_tenor,
            "scenario_pnl": stressed - start, "curve_shock_effect": stressed - rolled}

if __name__ == "__main__":
    c = {1.0: .03, 2.0: .035, 3.0: .04, 5.0: .045}
    print(carry_roll(100.0, 3.0, 1.0, c))
