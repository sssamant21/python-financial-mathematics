"""Synthetic continuous-zero-rate interpolation diagnostics; no extrapolation."""
from math import exp, log, isfinite
from carry_roll import price

def discount_factor(tenor, curve, method="linear_spot"):
    """Interpolate either zero yields or log discount factors between observed nodes."""
    if method not in ("linear_spot", "log_discount"):
        raise ValueError("unknown interpolation method")
    if isinstance(tenor, bool) or not isinstance(tenor, (int, float)) or not isfinite(tenor) or tenor <= 0:
        raise ValueError("tenor must be positive finite")
    if not isinstance(curve, dict) or len(curve) < 2:
        raise ValueError("at least two curve nodes required")
    # Reuse base pricing validation, including bounds and no extrapolation.
    nodes = sorted(curve)
    for t in nodes:
        price(1.0, t, curve)
    if tenor < nodes[0] or tenor > nodes[-1]:
        raise ValueError("extrapolation prohibited")
    if method == "linear_spot":
        return price(1.0, tenor, curve)
    if tenor in curve:
        return exp(-curve[tenor] * tenor)
    for a, b in zip(nodes, nodes[1:]):
        if a < tenor < b:
            weight = (tenor - a) / (b - a)
            log_df = (1 - weight) * (-curve[a] * a) + weight * (-curve[b] * b)
            return exp(log_df)
    raise ValueError("invalid tenor")

def compare(face, maturity, holding_years, curve):
    """Matched-horizon frozen-curve decomposition under both interpolation rules."""
    if isinstance(face, bool) or not isinstance(face, (int, float)) or not isfinite(face) or face <= 0:
        raise ValueError("face must be positive finite")
    if isinstance(holding_years, bool) or not isinstance(holding_years, (int, float)) or not isfinite(holding_years) or not 0 < holding_years < maturity:
        raise ValueError("holding period must be within bond life")
    remaining = maturity - holding_years
    rows = {}
    for method in ("linear_spot", "log_discount"):
        initial = face * discount_factor(maturity, curve, method)
        rolled = face * discount_factor(remaining, curve, method)
        initial_rate = -log(initial / face) / maturity
        carry_price = face * exp(-initial_rate * remaining)
        rows[method] = {"start": initial, "rolled": rolled,
                        "carry": carry_price - initial,
                        "roll_down": rolled - carry_price,
                        "pnl": rolled - initial}
    return rows

if __name__ == "__main__":
    curve = {1.: .03, 2.: .035, 3.: .04, 5.: .045}
    for method, result in compare(100., 3., .5, curve).items():
        print(method, result)
