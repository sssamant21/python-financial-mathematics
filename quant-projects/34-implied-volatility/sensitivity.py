"""Predeclared synthetic quote-spread, strike and maturity diagnostics."""
import argparse
import math
from iv import implied_vol, price


def vega(spot, strike, years, rate, sigma):
    """Black-Scholes price derivative with respect to annual volatility."""
    if not all(math.isfinite(v) for v in (spot, strike, years, rate, sigma)) or min(spot, strike, years, sigma) <= 0:
        raise ValueError("positive finite spot, strike, maturity and volatility required")
    d1 = (math.log(spot / strike) + (rate + sigma * sigma / 2) * years) / (sigma * math.sqrt(years))
    return spot * math.sqrt(years) * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)


def quote_interval(spot, strike, years, rate, sigma, half_spread=0.05, kind="call"):
    """Invert a synthetic bid/ask interval, rejecting impossible or clipped quotes."""
    if not math.isfinite(half_spread) or half_spread <= 0:
        raise ValueError("positive finite half spread required")
    mid = price(spot, strike, years, rate, sigma, kind)
    bid, ask = mid - half_spread, mid + half_spread
    if bid < 0:
        raise ValueError("negative synthetic bid; narrow spread or choose another contract")
    low = implied_vol(bid, spot, strike, years, rate, kind)
    high = implied_vol(ask, spot, strike, years, rate, kind)
    sensitivity = vega(spot, strike, years, rate, sigma)
    return {"strike": strike, "years": years, "mid": mid, "bid": bid, "ask": ask,
            "iv_bid": low, "iv_ask": high, "iv_width": high - low,
            "vega": sensitivity, "linear_width": 2 * half_spread / sensitivity if sensitivity > 0 else math.inf}


def grid(spot=100, rate=0.02, sigma=0.25, half_spread=0.05, kind="call"):
    """Fixed, disclosed grid; invalid quotes are flagged, never silently clipped."""
    if kind not in ("call", "put"):
        raise ValueError("kind must be call or put")
    rows = []
    for years in (0.05, 0.25, 1.0):
        for strike in (90.0, 100.0, 110.0):
            try:
                rows.append({"status": "ok", **quote_interval(spot, strike, years, rate, sigma, half_spread, kind)})
            except (ValueError, RuntimeError) as exc:
                rows.append({"status": "unavailable", "strike": strike, "years": years, "reason": str(exc)})
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic IV spread and conditioning grid")
    parser.add_argument("--spread", type=float, default=0.05, help="half bid/ask spread in premium units")
    args = parser.parse_args()
    for row in grid(half_spread=args.spread):
        if row["status"] == "ok":
            print(f"T={row['years']:.2f} K={row['strike']:.0f} IV_width={row['iv_width']:.6f} vega={row['vega']:.6f} linear_width={row['linear_width']:.6f}")
        else:
            print(f"T={row['years']:.2f} K={row['strike']:.0f} unavailable: {row['reason']}")
