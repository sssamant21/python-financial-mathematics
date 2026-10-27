"""Book 02 Section 18.5: multiple IRRs and cash-flow root scanning."""
import json
import math

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
    z=math.exp(-math.log1p(r))
    result=math.fsum(c*z**t for t,c in enumerate(values))
    return finite(result,"NPV")

def opposite(a,b):
    return (a<0<b) or (b<0<a)

def scan_brackets(flows,low=0.0,high=0.3,steps=30):
    values=validate_flows(flows)
    lo,hi=finite(low,"low"),finite(high,"high")
    if lo<=-1 or hi<=lo or type(steps) is not int or steps<1:
        raise ValueError("invalid scan interval or steps")
    xs=[lo+(hi-lo)*i/steps for i in range(steps+1)]
    ys=[npv(x,values) for x in xs]
    brackets=[]
    exact=[]
    for i,(x,y) in enumerate(zip(xs,ys)):
        if y==0:
            exact.append(x)
        if i and opposite(ys[i-1],y):
            brackets.append((xs[i-1],x))
    return {"brackets":brackets,"exact_grid_roots":exact,
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

def discover_roots(flows=CASH_FLOWS,low=0.0,high=0.3,steps=30):
    scanned=scan_brackets(flows,low,high,steps)
    candidates=list(scanned["exact_grid_roots"])
    candidates.extend(bisect_npv(flows,a,b) for a,b in scanned["brackets"])
    candidates.sort()
    distinct=[]
    for x in candidates:
        if not distinct or abs(x-distinct[-1])>1e-9:
            distinct.append(x)
    return {"roots":distinct,"scan":scanned,
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
