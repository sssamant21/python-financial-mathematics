"""CDS accrued-on-default classroom sensitivity with exact flat-curve interval integration.

Premium paid at scheduled dates only if surviving; default accrual is paid
at the default time. Protection settles at default time in this extension.
All amounts are synthetic and per unit notional unless specified.
"""
import math
from cds import legs, _number

def accrued_legs(notional=1_000_000, hazard=0.02, recovery=0.4,
                 rate=0.03, years=5, payments_per_year=4):
    # Reuse baseline's complete bounds and aligned-tenor validation.
    baseline = legs(notional, hazard, recovery, rate, years, payments_per_year)
    n, h, rec, r, t = (_number(k, v) for k, v in
        (("notional", notional), ("hazard", hazard),
         ("recovery", recovery), ("rate", rate), ("years", years)))
    dt = 1.0 / payments_per_year
    count = round(t * payments_per_year)
    k = h + r
    # Integral over each period: int_0^dt u*h*exp(-k*u) du.
    # expm1 gives stable small-k behavior; series avoids cancellation.
    x = k * dt
    if abs(x) < 1e-4:
        integral = dt * dt * (0.5 - x / 3 + x*x / 8
                            - x*x*x / 30 + x*x*x*x / 144)
    else:
        integral = (-math.expm1(-x) - x * math.exp(-x)) / (k*k)
    accrual = h * integral * sum(math.exp(-k * i * dt) for i in range(count))
    scheduled = baseline["premium_annuity_per_notional"]
    # Continuous settlement of default protection, exact for flat curves.
    if abs(k) < 1e-12:
        default_pv = h * t
    else:
        default_pv = h * (-math.expm1(-k*t)) / k
    protection = n * (1-rec) * default_pv
    annuity = scheduled + accrual
    spread = (1-rec) * default_pv / annuity
    return {"scheduled_annuity_per_notional": scheduled,
            "accrual_annuity_per_notional": accrual,
            "total_annuity_per_notional": annuity,
            "protection_leg": protection, "par_spread": spread,
            "par_spread_bp": 10000*spread,
            "baseline_spread_bp": baseline["par_spread_bp"],
            "spread_change_bp": 10000*spread-baseline["par_spread_bp"]}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Synthetic CDS default-accrual sensitivity")
    parser.add_argument("--hazard", type=float, default=0.02)
    parser.add_argument("--recovery", type=float, default=0.4)
    args = parser.parse_args()
    print(accrued_legs(hazard=args.hazard, recovery=args.recovery))
