"""Hypothetical annual spot-curve portfolio valuation and key-rate DV01."""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Bond:
    face: float
    coupon: float
    years: int
    units: float = 1.0

    def __post_init__(self):
        if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in (self.face, self.coupon, self.units)):
            raise ValueError("face, coupon, units must be finite")
        if self.face <= 0 or self.coupon < 0 or self.units < 0 or isinstance(self.years, bool) or not isinstance(self.years, int) or self.years < 1:
            raise ValueError("invalid bond definition")

def validate_curve(curve):
    if not isinstance(curve, (tuple, list)) or len(curve) < 2:
        raise ValueError("at least two nodes required")
    previous = 0
    for t, r in curve:
        if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or t <= previous:
            raise ValueError("tenors must increase")
        if isinstance(r, bool) or not isinstance(r, (int, float)) or not math.isfinite(r) or r <= -1:
            raise ValueError("rates must be finite and above -100%")
        previous = t
    if curve[0][0] != 1:
        raise ValueError("first tenor must be 1 year")

def spot(curve, year):
    validate_curve(curve)
    if isinstance(year, bool) or not isinstance(year, int) or year < 1 or year > curve[-1][0]:
        raise ValueError("cash flow outside curve")
    for (t0, r0), (t1, r1) in zip(curve[:-1], curve[1:]):
        if t0 <= year <= t1:
            return r0 + (r1-r0)*(year-t0)/(t1-t0)
    raise ValueError("cash flow outside curve")

def bond_value(bond, curve):
    validate_curve(curve)
    if bond.years > curve[-1][0]:
        raise ValueError("curve does not cover maturity")
    return bond.units * sum((bond.face*bond.coupon + (bond.face if t == bond.years else 0)) /
                            (1+spot(curve,t))**t for t in range(1,bond.years+1))

def portfolio_value(bonds, curve):
    bonds = tuple(bonds)
    if not bonds or not all(isinstance(b, Bond) for b in bonds):
        raise ValueError("nonempty Bond portfolio required")
    total = sum(bond_value(b, curve) for b in bonds)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("portfolio value must be positive and finite")
    return total

def shift(curve, shocks_bps):
    validate_curve(curve)
    if len(shocks_bps) != len(curve):
        raise ValueError("one shock per knot required")
    out = []
    for (t,r), bp in zip(curve, shocks_bps):
        if isinstance(bp, bool) or not isinstance(bp, (int,float)) or not math.isfinite(bp):
            raise ValueError("invalid shock")
        s = r + bp/10000
        if s <= -1:
            raise ValueError("shocked rate must exceed -100%")
        out.append((t,s))
    return tuple(out)

def key_rate_dv01(bonds, curve, bump_bps=1.0):
    """Central-difference dollar price decline per +1bp bump at each node."""
    if isinstance(bump_bps, bool) or not isinstance(bump_bps, (int,float)) or not math.isfinite(bump_bps) or not 0 < bump_bps <= 10:
        raise ValueError("bump must be in (0,10] bp")
    base = portfolio_value(bonds, curve)
    dv = []
    for i in range(len(curve)):
        bumps = [0.0]*len(curve)
        bumps[i] = bump_bps
        up = portfolio_value(bonds, shift(curve, bumps))
        bumps[i] = -bump_bps
        down = portfolio_value(bonds, shift(curve, bumps))
        dv.append((down-up)/(2*bump_bps))
    return base, tuple(dv)

def scenario(bonds, curve, shocks_bps):
    base, dv = key_rate_dv01(bonds, curve)
    exact = portfolio_value(bonds, shift(curve, shocks_bps))-base
    linear = -sum(d*s for d,s in zip(dv, shocks_bps))
    return {"base_value":base, "exact_change":exact, "linear_change":linear,
            "approximation_error":linear-exact, "exact_return":exact/base}

def main():
    curve = ((1,.035),(3,.04),(5,.043),(10,.047))
    bonds = (Bond(1000,.04,3,2),Bond(1000,.05,7),Bond(1000,.03,10))
    base,dv = key_rate_dv01(bonds,curve)
    print(f"Hypothetical portfolio value: {base:.2f}; key-rate DV01: {tuple(round(x,4) for x in dv)}")
    for label,bumps in {"parallel +100bp":(100,100,100,100),
                        "steepener":(-50,-25,25,100),
                        "flattener":(100,50,-25,-50)}.items():
        result = scenario(bonds,curve,bumps)
        print(f"{label}: exact={result['exact_change']:+.2f}, linear={result['linear_change']:+.2f}, error={result['approximation_error']:+.2f}")

if __name__ == "__main__":
    main()
