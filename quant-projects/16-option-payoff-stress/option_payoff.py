"""Educational European option expiry payoff and bounded scenario stress; no pricing model."""
from __future__ import annotations
import argparse
import math

def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)

def leg(kind, strike, premium, quantity=1):
    if kind not in ("call", "put"):
        raise ValueError("kind must be call or put")
    strike, premium, quantity = (finite(strike, "strike"), finite(premium, "premium"), finite(quantity, "quantity"))
    if strike <= 0 or premium < 0 or quantity == 0 or abs(quantity) > 1000:
        raise ValueError("invalid strike, premium or quantity")
    return (kind, strike, premium, quantity)

def payoff_at_expiry(legs, spot):
    """Net expiry P&L per underlying unit; positive quantity is long."""
    spot = finite(spot, "spot")
    if spot < 0:
        raise ValueError("spot cannot be negative")
    if not legs or len(legs) > 20:
        raise ValueError("one to twenty option legs required")
    total = 0.0
    for kind, strike, premium, quantity in legs:
        kind, strike, premium, quantity = leg(kind, strike, premium, quantity)
        intrinsic = max(spot - strike, 0.0) if kind == "call" else max(strike - spot, 0.0)
        total += quantity * (intrinsic - premium)
    if not math.isfinite(total):
        raise ValueError("nonfinite payoff")
    return total

def stress_table(legs, spots):
    if not spots or len(spots) > 1001:
        raise ValueError("one to 1001 spot scenarios required")
    return tuple((finite(s, "spot"), payoff_at_expiry(legs, s)) for s in spots)

def main():
    parser = argparse.ArgumentParser(description="Synthetic option expiry P&L; not a trade recommendation")
    parser.add_argument("--strike", type=float, default=100.0)
    parser.add_argument("--premium", type=float, default=6.0)
    args = parser.parse_args()
    example = (leg("call", args.strike, args.premium),)
    for spot, pnl in stress_table(example, (60, 80, 90, 100, 110, 120, 140)):
        print(f"expiry_spot={spot:.2f} net_pnl={pnl:.2f}")
    print("Hypothetical expiry-only results; excludes fees, funding and early exercise.")

if __name__ == "__main__":
    main()
