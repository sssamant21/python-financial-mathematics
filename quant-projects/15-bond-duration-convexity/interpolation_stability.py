"""Compare hypothetical spot-curve interpolation and key-rate stress sensitivity."""
from __future__ import annotations
import math
from curve_portfolio import Bond, validate_curve, shift

def discount_factor(curve, year, method="rate_linear"):
    validate_curve(curve)
    if isinstance(year, bool) or not isinstance(year, int) or not 1 <= year <= curve[-1][0]:
        raise ValueError("year outside curve")
    if method not in ("rate_linear", "log_discount"):
        raise ValueError("unsupported interpolation")
    for t, r in curve:
        if t == year:
            return (1+r)**(-year)
    for (t0,r0),(t1,r1) in zip(curve[:-1],curve[1:]):
        if t0 < year < t1:
            alpha=(year-t0)/(t1-t0)
            if method=="rate_linear":
                return (1+r0+alpha*(r1-r0))**(-year)
            return math.exp((1-alpha)*(-t0*math.log1p(r0))+alpha*(-t1*math.log1p(r1)))
    raise ValueError("year outside curve")

def value(bonds, curve, method="rate_linear"):
    bonds=tuple(bonds)
    if not bonds or not all(isinstance(b,Bond) for b in bonds):
        raise ValueError("nonempty Bond portfolio required")
    validate_curve(curve)
    if method not in ("rate_linear","log_discount"):
        raise ValueError("unsupported interpolation")
    if any(b.years>curve[-1][0] for b in bonds):
        raise ValueError("maturity outside curve")
    total=sum(b.units*sum((b.face*b.coupon+(b.face if t==b.years else 0))*discount_factor(curve,t,method)
                          for t in range(1,b.years+1)) for b in bonds)
    if not math.isfinite(total) or total<=0:
        raise ValueError("portfolio value must be finite and positive")
    return total

def diagnostics(bonds, curve, shocks_bps, bump_bps=1.0):
    """Compare fixed methods, nodewise central-difference DV01 and exact stress."""
    if isinstance(bump_bps,bool) or not isinstance(bump_bps,(int,float)) or not math.isfinite(bump_bps) or not 0<bump_bps<=10:
        raise ValueError("bump must be in (0,10] bp")
    bonds=tuple(bonds)
    shifted=shift(curve,shocks_bps)
    result={}
    for method in ("rate_linear","log_discount"):
        base=value(bonds,curve,method)
        dv=[]
        for i in range(len(curve)):
            bumps=[0.0]*len(curve)
            bumps[i]=bump_bps
            up=value(bonds,shift(curve,bumps),method)
            bumps[i]=-bump_bps
            down=value(bonds,shift(curve,bumps),method)
            dv.append((down-up)/(2*bump_bps))
        exact=value(bonds,shifted,method)-base
        linear=-sum(x*y for x,y in zip(dv,shocks_bps))
        result[method]={"base":base,"dv01":tuple(dv),"exact_change":exact,
                        "linear_change":linear,"linear_error":linear-exact}
    result["base_difference"]=result["log_discount"]["base"]-result["rate_linear"]["base"]
    result["stress_difference"]=result["log_discount"]["exact_change"]-result["rate_linear"]["exact_change"]
    return result

def main():
    curve=((1,.035),(3,.04),(5,.043),(10,.047))
    bonds=(Bond(1000,.04,3,2),Bond(1000,.05,7),Bond(1000,.03,10))
    scenarios=(("parallel +100bp",(100,100,100,100)),("steepener",(-50,-25,25,100)),("flattener",(100,50,-25,-50)))
    for label, shocks in scenarios:
        d=diagnostics(bonds,curve,shocks)
        print(f'{label}: base difference={d["base_difference"]:.4f}, stress difference={d["stress_difference"]:.4f}')
        for method in ("rate_linear","log_discount"):
            x=d[method]
            print(f'  {method}: value={x["base"]:.4f} exact={x["exact_change"]:.4f} linear error={x["linear_error"]:.4f} sum DV01={sum(x["dv01"]):.5f}')

if __name__=="__main__":
    main()
