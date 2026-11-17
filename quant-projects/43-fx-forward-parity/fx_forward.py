"""Synthetic FX forward pricing under continuous-compounding conventions.

Domestic currency is quote currency per one unit of foreign currency.
No market feeds, trading instructions or broker connectivity.
"""
from __future__ import annotations
import argparse
import math


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _inputs(spot: float, domestic_rate: float, foreign_rate: float, years: float):
    s = _finite("spot", spot)
    rd = _finite("domestic_rate", domestic_rate)
    rf = _finite("foreign_rate", foreign_rate)
    t = _finite("years", years)
    if not (0 < s <= 1_000_000):
        raise ValueError("spot must be positive and bounded")
    if not (-1 <= rd <= 1 and -1 <= rf <= 1):
        raise ValueError("rates must lie between -100% and +100%")
    if not (0 < t <= 100):
        raise ValueError("years must lie in (0, 100]")
    return s, rd, rf, t


def fair_forward(spot: float, domestic_rate: float, foreign_rate: float, years: float) -> float:
    """Domestic/foreign forward F = S exp((rd-rf) T)."""
    s, rd, rf, t = _inputs(spot, domestic_rate, foreign_rate, years)
    exponent = (rd - rf) * t
    # Guard extreme synthetic combinations even when exp() remains finite.
    # Such values are not useful for a classroom parity comparison.
    if abs(exponent) > 50:
        raise ValueError("rate differential times tenor exceeds classroom bound")
    result = s * math.exp(exponent)
    if not math.isfinite(result) or result <= 0:
        raise ValueError("forward is nonfinite or underflowed")
    return result


def forward_value(
    spot: float, domestic_rate: float, foreign_rate: float, years: float,
    delivery_rate: float, foreign_notional: float = 1.0
) -> float:
    """Domestic PV of receiving foreign notional and paying K domestic per unit."""
    s, rd, rf, t = _inputs(spot, domestic_rate, foreign_rate, years)
    k = _finite("delivery_rate", delivery_rate)
    n = _finite("foreign_notional", foreign_notional)
    if k <= 0 or abs(n) > 1_000_000_000:
        raise ValueError("delivery_rate must be positive and notional bounded")
    pv = n * (s * math.exp(-rf * t) - k * math.exp(-rd * t))
    if not math.isfinite(pv):
        raise ValueError("nonfinite forward present value")
    return pv


def quote_spread_screen(
    spot_bid: float, spot_ask: float, domestic_rate: float,
    foreign_rate: float, years: float, forward_bid: float, forward_ask: float
) -> dict[str, float | bool]:
    """Illustrative screen only: deterministic single mid-rate curves, no costs."""
    sb = _finite("spot_bid", spot_bid)
    sa = _finite("spot_ask", spot_ask)
    fb = _finite("forward_bid", forward_bid)
    fa = _finite("forward_ask", forward_ask)
    if not (0 < sb <= sa and 0 < fb <= fa):
        raise ValueError("bid/ask must be positive and ordered")
    low = fair_forward(sb, domestic_rate, foreign_rate, years)
    high = fair_forward(sa, domestic_rate, foreign_rate, years)
    return {"parity_low": low, "parity_high": high,
            "forward_bid": fb, "forward_ask": fa,
            "disjoint": fa < low or fb > high}


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic FX covered-interest-parity lab")
    parser.add_argument("--spot", type=float, default=1.10)
    parser.add_argument("--domestic-rate", type=float, default=0.04)
    parser.add_argument("--foreign-rate", type=float, default=0.02)
    parser.add_argument("--years", type=float, default=1.0)
    args = parser.parse_args()
    f = fair_forward(args.spot, args.domestic_rate, args.foreign_rate, args.years)
    print(f"synthetic fair forward (domestic/foreign): {f:.8f}")
    print(f"new at-market contract PV: {forward_value(args.spot, args.domestic_rate, args.foreign_rate, args.years, f):.10f}")


if __name__ == "__main__":
    main()
