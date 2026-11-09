"""Synthetic annual forward-rate diagnostics for two spot interpolation conventions."""
from __future__ import annotations
import math
from interpolation_stability import discount_factor
from curve_portfolio import validate_curve, shift

METHODS = ("rate_linear", "log_discount")

def forward_table(curve, method="rate_linear"):
    """Annual effective one-year forwards implied by consecutive discount factors.

    Year one starts at DF(0)=1. Negative forwards are reported, not suppressed.
    """
    validate_curve(curve)
    if method not in METHODS:
        raise ValueError("unsupported interpolation")
    last = curve[-1][0]
    if isinstance(last, bool) or not isinstance(last, int) or last > 100:
        raise ValueError("integer terminal tenor <=100 required")
    previous = 1.0
    rows = []
    for year in range(1, last + 1):
        df = discount_factor(curve, year, method)
        if not math.isfinite(df) or df <= 0:
            raise ValueError("invalid discount factor")
        fwd = previous / df - 1.0
        if not math.isfinite(fwd):
            raise ValueError("nonfinite forward")
        rows.append((year, df, fwd))
        previous = df
    return tuple(rows)

def compare_forwards(curve, shocks_bps=None):
    """Compare predeclared methods and optionally the same fixed node shock."""
    validate_curve(curve)
    base = {m: forward_table(curve, m) for m in METHODS}
    result = {"base": base, "max_abs_forward_gap_bps": max(
        abs(a[2] - b[2]) * 10000 for a, b in zip(*[base[m] for m in METHODS]))}
    if shocks_bps is not None:
        shocked = shift(curve, shocks_bps)
        result["shocked"] = {m: forward_table(shocked, m) for m in METHODS}
    return result

def main():
    curve = ((1, .035), (3, .04), (5, .043), (10, .047))
    result = compare_forwards(curve, (100, 50, 0, -50))
    print(f"Hypothetical max interpolation forward gap: {result['max_abs_forward_gap_bps']:.3f} bp")
    for method in METHODS:
        forwards = [r[2] for r in result["base"][method]]
        shocked = [r[2] for r in result["shocked"][method]]
        print(f"{method}: min base forward={min(forwards):.5%}; min shocked forward={min(shocked):.5%}")

if __name__ == "__main__":
    main()
