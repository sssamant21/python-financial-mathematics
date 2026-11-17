"""Synthetic FX forward no-arbitrage *illustration* with funding sides and basis.

Quote: domestic currency per foreign unit. No executable trade inference.
"""
from __future__ import annotations
import math
from fx_forward import _finite, fair_forward


def funding_interval(spot_bid, spot_ask, domestic_lend, domestic_borrow,
                     foreign_lend, foreign_borrow, years,
                     basis_low=0.0, basis_high=0.0):
    """Conservative synthetic interval [spot_bid*exp((d_l-f_b+b_l)T),
    spot_ask*exp((d_b-f_l+b_h)T)].

    Basis is an explicitly assumed additive annualized forward-premium spread,
    NOT a calibrated cross-currency swap basis or a funding arbitrage model.
    """
    vals = [_finite(name, x) for name, x in zip(
        ("spot_bid", "spot_ask", "domestic_lend", "domestic_borrow",
         "foreign_lend", "foreign_borrow", "years", "basis_low", "basis_high"),
        (spot_bid, spot_ask, domestic_lend, domestic_borrow,
         foreign_lend, foreign_borrow, years, basis_low, basis_high))]
    sb, sa, dl, db, fl, fb, t, bl, bh = vals
    if not (0 < sb <= sa <= 1_000_000):
        raise ValueError("spot quotes must be positive, bounded and ordered")
    if not (0 < t <= 100):
        raise ValueError("years outside (0,100]")
    if not (-1 <= dl <= db <= 1 and -1 <= fl <= fb <= 1):
        raise ValueError("funding lend/borrow rates must be bounded and ordered")
    if not (-1 <= bl <= bh <= 1):
        raise ValueError("basis scenarios must be bounded and ordered")
    low = fair_forward(sb, dl + 0.0, fb - bl, t) if -1 <= fb-bl <= 1 else _exp_bound(sb, (dl-fb+bl)*t)
    high = fair_forward(sa, db + 0.0, fl - bh, t) if -1 <= fl-bh <= 1 else _exp_bound(sa, (db-fl+bh)*t)
    if low > high:
        raise ValueError("invalid interval ordering")
    return low, high


def _exp_bound(spot, exponent):
    if abs(exponent) > 50:
        raise ValueError("rate differential times tenor exceeds classroom bound")
    value = spot * math.exp(exponent)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("nonfinite forward")
    return value


def basis_sensitivity(spot, domestic_rate, foreign_rate, years, basis=0.0,
                      bump_bp=1.0):
    """Forward, analytic dF/db, exact bumped difference for positive basis bump."""
    b = _finite("basis", basis)
    bump = _finite("bump_bp", bump_bp)
    if not (-1 <= b <= 1 and 0 < bump <= 100):
        raise ValueError("basis or bump out of range")
    # Use direct bounded exponent to avoid treating adjusted rates as standalone funding quotes.
    s = _finite("spot", spot)
    rd = _finite("domestic_rate", domestic_rate)
    rf = _finite("foreign_rate", foreign_rate)
    t = _finite("years", years)
    if not (0 < s <= 1_000_000 and -1 <= rd <= 1 and -1 <= rf <= 1 and 0 < t <= 100):
        raise ValueError("invalid base inputs")
    exponent = (rd-rf+b)*t
    delta = bump * 1e-4
    base = _exp_bound(s, exponent)
    shifted = _exp_bound(s, exponent + delta*t)
    return {"forward": base, "d_forward_d_basis": t*base,
            "bump_bp": bump, "bumped_change": shifted-base}


if __name__ == "__main__":
    lo, hi = funding_interval(1.099, 1.101, .03, .05, .01, .03, 1)
    print(f"synthetic funding interval: [{lo:.8f}, {hi:.8f}]")
    print(basis_sensitivity(1.10, .04, .02, 1))
