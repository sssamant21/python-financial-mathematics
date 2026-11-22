"""Section 10.7: composite numerical quadrature (standard library)."""
import json
import math
from fractions import Fraction

MAX_PANELS=100000  # Declared educational work/memory budget, not an optimal bound.

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, not bool")
    try:
        v=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def integrate(f,a,b,n,method):
    if not callable(f):
        raise TypeError("f must be callable")
    a,b=finite(a,"a"),finite(b,"b")
    if type(n) is not int:
        raise TypeError("n must be an integer, excluding bool")
    if n<=0:
        raise ValueError("n must be a positive integer")
    if method not in ("midpoint","trapezoid","simpson"):
        raise ValueError("unknown quadrature method")
    if method=="simpson" and n%2:
        raise ValueError("Simpson requires even n")
    if n>MAX_PANELS:
        raise ValueError("panel count exceeds supported budget")
    if a==b:
        return 0.0
    lower=Fraction.from_float(a)
    step=(Fraction.from_float(b)-lower)/n
    grid=[float(lower+i*step) for i in range(n+1)]
    increasing=a<b
    if any((x>=y if increasing else x<=y) for x,y in zip(grid,grid[1:])):
        raise ValueError("quadrature grid collapses in float representation")
    midpoints=None
    if method=="midpoint":
        midpoints=[float(lower+Fraction(2*i+1,2)*step) for i in range(n)]
        if any(not min(x,y)<z<max(x,y)
               for x,y,z in zip(grid,grid[1:],midpoints)):
            raise ValueError("midpoint rounds outside its cell interior")
    def value(t):
        return finite(f(t),"integrand")
    # Complete weighted sum and scale use exact represented binary floats.
    # Intermediate overflow/underflow must not discard a reportable result.
    def exact_value(t):
        return Fraction.from_float(value(t))
    if method=="midpoint":
        total=sum((exact_value(t) for t in midpoints),Fraction(0))
        exact_result=step*total
    elif method=="trapezoid":
        total=(exact_value(a)+exact_value(b))/2
        total+=sum((exact_value(t) for t in grid[1:-1]),Fraction(0))
        exact_result=step*total
    else:
        total=exact_value(a)+exact_value(b)
        total+=sum(((4 if i%2 else 2)*exact_value(t)
                    for i,t in enumerate(grid[1:-1],1)),Fraction(0))
        exact_result=step*total/3
    try:
        result=float(exact_result)
    except OverflowError as exc:
        raise ValueError("integral outside float range") from exc
    if not math.isfinite(result) or (exact_result and result==0):
        raise ValueError("integral outside float range")
    return result

def refinement(f,a,b,method,counts):
    p=4 if method=="simpson" else 2
    rows=[]
    previous=None
    for n in counts:
        result=integrate(f,a,b,n,method)
        row={"n":n,"estimate":result}
        if previous is not None:
            old_n,old_value=previous
            if n==2*old_n:
                row["estimated_fine_error"]=abs(result-old_value)/(2**p-1)
        rows.append(row)
        previous=(n,result)
    return rows

def finance_integrand(t):
    return (1000+100*t)*math.exp(-0.03*t-0.0025*t*t)

def assessment():
    methods={}
    for method in ("midpoint","trapezoid","simpson"):
        methods[method]=refinement(finance_integrand,0,4,method,[8,16,32,64,128])
    return {"model":"linear continuous payments, deterministic time-varying discount",
            "horizon_years":4,"methods":methods,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
