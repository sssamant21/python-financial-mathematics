"""Synthetic forward-rate diagnostics for zero-coupon curves; no market data."""
from math import isfinite, log
from interpolation import discount_factor, compare

def forward_rate(start, end, curve, method="log_discount"):
    """Continuously compounded forward rate over (start, end)."""
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not isfinite(x) for x in (start, end)) or start <= 0 or end <= start:
        raise ValueError("require finite 0 < start < end")
    first = discount_factor(start, curve, method)
    last = discount_factor(end, curve, method)
    if first <= 0 or last <= 0:
        raise ValueError("discount factors must be positive")
    return (log(first) - log(last)) / (end - start)

def forward_grid(curve, method="log_discount"):
    """Adjacent-node forwards; no extrapolation."""
    if not isinstance(curve, dict) or len(curve) < 2:
        raise ValueError("at least two nodes required")
    nodes = sorted(curve)
    return [(a, b, forward_rate(a, b, curve, method)) for a, b in zip(nodes, nodes[1:])]

def horizon_diagnostics(face, maturity, horizons, curve):
    """Predeclared holding-horizon sensitivity; not a return forecast."""
    if not isinstance(horizons, (tuple, list)) or not horizons or len(horizons) > 100:
        raise ValueError("require 1 to 100 horizons")
    if len(set(map(str, horizons))) != len(horizons):
        raise ValueError("duplicate horizons")
    rows = []
    for h in horizons:
        outcomes = compare(face, maturity, h, curve)
        rows.append({"horizon": h, "linear_spot_pnl": outcomes["linear_spot"]["pnl"],
                     "log_discount_pnl": outcomes["log_discount"]["pnl"],
                     "difference": outcomes["log_discount"]["pnl"] - outcomes["linear_spot"]["pnl"]})
    return rows

if __name__ == "__main__":
    c = {1.: .03, 2.: .035, 3.: .04, 5.: .045}
    print("Adjacent-node forwards:", forward_grid(c))
    print("Horizon sensitivity:", horizon_diagnostics(100., 3., [.25, .5, 1.], c))
