"""Single-tenor synthetic quote CS01: recalibrate hazard after quote bumps.

Simplified interval-end CDS cash flows only; not ISDA-standard CS01.
"""
import math
from cds_risk import legs, pv


def _finite(value, name, lo, hi):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not lo <= value <= hi:
        raise ValueError(f"{name} must be finite and within [{lo}, {hi}]")
    return float(value)


def hazard_from_quote(quote_bp, recovery=0.4, frequency=4):
    """Invert the flat-hazard discrete-coupon par-spread identity exactly."""
    q = _finite(quote_bp, "quote_bp", 0, 100000) / 10000
    rec = _finite(recovery, "recovery", 0, 0.999999)
    if isinstance(frequency, bool) or not isinstance(frequency, int) or not 1 <= frequency <= 24:
        raise ValueError("frequency must be integer in [1,24]")
    h = frequency * math.log1p(q / ((1 - rec) * frequency))
    if h > 5:
        raise ValueError("implied hazard exceeds supported bound")
    return h


def quote_cs01(quote_bp=120, coupon_bp=100, bump_bp=1, notional=1_000_000,
               maturity=5, recovery=0.4, rate=0.02, frequency=4):
    """PV change for a +1bp market-quote shift (central difference where possible).

    bump_bp controls numerical difference spacing. The reported cs01 is scaled
    to a one-basis-point quote move, not a hazard-intensity bump.
    """
    quote = _finite(quote_bp, "quote_bp", 0, 100000)
    coupon = _finite(coupon_bp, "coupon_bp", 0, 10000) / 10000
    bump = _finite(bump_bp, "bump_bp", 0.001, 100)
    _finite(notional, "notional", 0.01, 1e12)
    # Validate all contract inputs even when quote is zero.
    legs(0, maturity=maturity, recovery=recovery, rate=rate, frequency=frequency)
    def value(q):
        h = hazard_from_quote(q, recovery, frequency)
        return pv(h, coupon, notional=notional, maturity=maturity,
                  recovery=recovery, rate=rate, frequency=frequency)
    base = value(quote)
    upper = value(quote + bump)
    if quote >= bump:
        lower = value(quote - bump)
        cs01 = (upper - lower) / (2 * bump)
        method = "central"
    else:
        cs01 = (upper - base) / bump
        method = "forward"
    return {"pv": base, "calibrated_hazard": hazard_from_quote(quote, recovery, frequency),
            "quote_cs01": cs01, "difference": method}


if __name__ == "__main__":
    for name, value in quote_cs01().items():
        print(f"{name}: {value}")
