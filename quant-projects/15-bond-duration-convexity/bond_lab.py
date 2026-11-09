"""Educational fixed-rate bond valuation and parallel yield-shock stress (annual coupons)."""
from __future__ import annotations
import argparse
import math


def cashflows(face: float, coupon_rate: float, years: int):
    """End-of-year fixed coupon payments; principal repaid at maturity."""
    for value in (face, coupon_rate):
        if not math.isfinite(value):
            raise ValueError("Inputs must be finite")
    if face <= 0 or coupon_rate < 0 or years < 1 or isinstance(years, bool) or not isinstance(years, int):
        raise ValueError("face>0, coupon_rate>=0, and integer years>=1 required")
    return [(t, face * coupon_rate + (face if t == years else 0.0)) for t in range(1, years + 1)]


def price(face: float, coupon_rate: float, years: int, ytm: float) -> float:
    if not math.isfinite(ytm) or ytm <= -1:
        raise ValueError("annual yield must be finite and greater than -100%")
    return sum(cf / (1 + ytm) ** t for t, cf in cashflows(face, coupon_rate, years))


def sensitivities(face: float, coupon_rate: float, years: int, ytm: float):
    p = price(face, coupon_rate, years, ytm)
    flows = cashflows(face, coupon_rate, years)
    macaulay = sum(t * cf / (1 + ytm) ** t for t, cf in flows) / p
    modified = macaulay / (1 + ytm)
    convexity = sum(t * (t + 1) * cf / (1 + ytm) ** (t + 2) for t, cf in flows) / p
    return {"price": p, "macaulay_duration": macaulay, "modified_duration": modified, "convexity": convexity}


def shock_table(face: float, coupon_rate: float, years: int, ytm: float, shocks_bps=(-200, -100, 100, 200)):
    base = sensitivities(face, coupon_rate, years, ytm)
    rows = []
    for bps in shocks_bps:
        if isinstance(bps, bool) or not isinstance(bps, (int, float)) or not math.isfinite(bps):
            raise ValueError("shocks must be finite basis-point numbers")
        dy = bps / 10000
        shocked = price(face, coupon_rate, years, ytm + dy)
        exact = shocked / base["price"] - 1
        linear = -base["modified_duration"] * dy
        quadratic = linear + 0.5 * base["convexity"] * dy * dy
        rows.append({"shock_bps": bps, "exact_return": exact, "duration_return": linear,
                     "duration_convexity_return": quadratic, "approximation_error": quadratic - exact})
    return base, rows


def main():
    parser = argparse.ArgumentParser(description="Synthetic fixed-coupon bond yield-shock stress")
    parser.add_argument("--face", type=float, default=1000.0)
    parser.add_argument("--coupon", type=float, default=0.04)
    parser.add_argument("--years", type=int, default=5)
    parser.add_argument("--yield-rate", type=float, default=0.05)
    args = parser.parse_args()
    base, rows = shock_table(args.face, args.coupon, args.years, args.yield_rate)
    print("Bond price: {:.4f}; modified duration: {:.4f}; convexity: {:.4f}".format(
        base["price"], base["modified_duration"], base["convexity"]))
    for row in rows:
        print("{:+5.0f} bp | exact={:+.4%} | duration={:+.4%} | duration+convexity={:+.4%}".format(
            row["shock_bps"], row["exact_return"], row["duration_return"], row["duration_convexity_return"]))


if __name__ == "__main__":
    main()
