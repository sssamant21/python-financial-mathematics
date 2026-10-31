"""Book 02 Section 18.5: multiple IRRs and cash-flow root scanning."""
import json
import math
from fractions import Fraction

CASH_FLOWS=(-100.0,230.0,-132.0)

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def validate_flows(flows):
    if not isinstance(flows,(tuple,list)) or len(flows)<2:
        raise ValueError("at least two cash-flow periods required")
    values=tuple(finite(x,"cash flow") for x in flows)
    if not any(x!=0 for x in values):
        raise ValueError("all-zero cash flows do not define a unique IRR")
    return values

def npv(rate,flows=CASH_FLOWS):
    r=finite(rate,"rate")
    values=validate_flows(flows)
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return _periodic_value(r,values)

def periodic_npv(rate,flows):
    """Valuation API: nonempty finite cash flows, including zero/single flows."""
    r=finite(rate,"rate")
    if r<=-1 or not isinstance(flows,(tuple,list)) or not flows:
        raise ValueError("invalid rate or cash flows")
    values=tuple(finite(c,"cash flow") for c in flows)
    return _periodic_value(r,values)

def _periodic_value(r,values):
    # Integer periods make NPV a rational polynomial for represented inputs.
    # Round only the complete Horner result, so cancellation cannot invent
    # exact grid roots in a closely spaced or repeated-root example.
    z=1/(1+Fraction(r))
    exact=Fraction(0)
    for cash_flow in reversed(values):
        exact=exact*z+Fraction(cash_flow)
    try:
        result=float(exact)
    except OverflowError as exc:
        raise ValueError("NPV outside floating-point range") from exc
    if exact and result==0:
        raise ValueError("nonzero NPV underflows floating-point range")
    return finite(result,"NPV")

def opposite(a,b):
    return (a<0<b) or (b<0<a)

def scan_brackets(flows,low=0.0,high=0.3,steps=30):
    values=validate_flows(flows)
    lo,hi=finite(low,"low"),finite(high,"high")
    if lo<=-1 or hi<=lo or type(steps) is not int or steps<1:
        raise ValueError("invalid scan interval or steps")
    # Form each finite endpoint interpolation before final float rounding;
    # width*i can overflow even when every requested grid point is finite.
    lower=Fraction(lo);span=Fraction(hi)-lower
    xs=[float(lower+span*Fraction(i,steps)) for i in range(steps+1)]
    if any(a>=b for a,b in zip(xs,xs[1:])):
        raise ValueError("scan grid collapses in floating-point representation")
    ys=[npv(x,values) for x in xs]
    brackets=[]
    exact=[]
    for i,(x,y) in enumerate(zip(xs,ys)):
        if y==0:
            exact.append(x)
        if i and opposite(ys[i-1],y):
            brackets.append((xs[i-1],x))
    return {"brackets":brackets,"exact_grid_roots":exact,
            "grid":xs,"npv_values":ys,
            "exhaustive":False,"grid_steps":steps}

def bisect_npv(flows,a,b,width_tol=1e-12,max_iter=200):
    values=validate_flows(flows)
    lo,hi=finite(a,"lower"),finite(b,"upper")
    tol=finite(width_tol,"width_tol")
    if lo<=-1 or hi<=lo or tol<=0 or type(max_iter) is not int or max_iter<1:
        raise ValueError("invalid bracket or solver controls")
    flo,fhi=npv(lo,values),npv(hi,values)
    if flo==0:
        return lo
    if fhi==0:
        return hi
    if not opposite(flo,fhi):
        raise ValueError("no sign change")
    for _ in range(max_iter):
        mid=lo+(hi-lo)/2
        if mid==lo or mid==hi:
            raise ArithmeticError("floating-point stagnation")
        fm=npv(mid,values)
        if fm==0 or hi-lo<=tol:
            return mid
        if opposite(flo,fm):
            hi,fhi=mid,fm
        else:
            lo,flo=mid,fm
    raise ArithmeticError("maximum iterations reached")

def discover_roots(flows=CASH_FLOWS,low=0.0,high=0.3,steps=30,dedup_tol=1e-9):
    tolerance=finite(dedup_tol,"dedup_tol")
    if tolerance<0:
        raise ValueError("dedup_tol must be nonnegative")
    scanned=scan_brackets(flows,low,high,steps)
    candidates=list(scanned["exact_grid_roots"])
    candidates.extend(bisect_npv(flows,a,b) for a,b in scanned["brackets"])
    candidates.sort()
    distinct=[]
    for x in candidates:
        if not distinct or abs(Fraction(x)-Fraction(distinct[-1]))>Fraction(tolerance):
            distinct.append(x)
    return {"roots":distinct,"candidate_roots":candidates,"scan":scanned,
            "deduplication":{"absolute_rate_tolerance":tolerance,
                             "comparison":"exact represented-float distance to last retained candidate; strictly greater retains",
                             "merged_count":len(candidates)-len(distinct)},
            "completeness_certified":False}

def assessment():
    roots=discover_roots()
    return {"cash_flows":CASH_FLOWS,"discovered":roots,
            "analytical_roots":(0.1,0.2),
            "npv_at_15_percent":npv(0.15),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
