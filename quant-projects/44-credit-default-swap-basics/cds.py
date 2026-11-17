"""Synthetic discrete-time CDS premium and protection legs; no market data or trading."""
import argparse
import math

def _number(name, x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"{name} must be finite numeric")
    return float(x)

def legs(notional=1_000_000, hazard=0.02, recovery=0.4, rate=0.03, years=5, payments_per_year=4):
    """Approximate scheduled premium and default protection using interval-end settlement.

    Flat continuous hazard h, risk-free rate r; survival exp(-h*t).
    Premium accrual on default and upfront payments are excluded.
    """
    n, h, rec, r, t = (_number(k,v) for k,v in
        (("notional",notional),("hazard",hazard),("recovery",recovery),("rate",rate),("years",years)))
    if not (0 < n <= 1e12 and 0 <= h <= 2 and 0 <= rec <= 1 and -0.1 <= r <= 1 and 0 < t <= 30):
        raise ValueError("inputs outside educational bounds")
    if isinstance(payments_per_year,bool) or not isinstance(payments_per_year,int) or payments_per_year not in (1,2,4,12):
        raise ValueError("payments_per_year must be 1,2,4,12")
    steps = t * payments_per_year
    if abs(steps-round(steps)) > 1e-9:
        raise ValueError("tenor must align with payment frequency")
    count = round(steps)
    dt = 1/payments_per_year
    premium_annuity = 0.0
    protection_unit = 0.0
    prev_survival = 1.0
    for i in range(1,count+1):
        time = i*dt
        survival = math.exp(-h*time)
        discount = math.exp(-r*time)
        premium_annuity += dt*discount*survival
        protection_unit += discount*(prev_survival-survival)
        prev_survival = survival
    protection = n*(1-rec)*protection_unit
    par_spread = (1-rec)*protection_unit/premium_annuity
    return {"premium_annuity_per_notional":premium_annuity,
            "protection_leg":protection, "par_spread":par_spread,
            "par_spread_bp":par_spread*10000,
            "terminal_survival":prev_survival}

def main():
    parser=argparse.ArgumentParser(description="Synthetic CDS par-spread classroom lab")
    parser.add_argument("--hazard",type=float,default=0.02)
    parser.add_argument("--recovery",type=float,default=0.4)
    args=parser.parse_args()
    print(legs(hazard=args.hazard,recovery=args.recovery))

if __name__=="__main__":
    main()
