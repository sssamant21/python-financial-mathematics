"""Section 10.7: composite numerical quadrature (standard library)."""
import json
import math

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
    if a==b:
        return 0.0
    h=(b-a)/n
    if not math.isfinite(h) or h==0:
        raise ValueError("invalid step width")
    def value(t):
        return finite(f(t),"integrand")
    if method=="midpoint":
        terms=[value(a+(i+0.5)*h) for i in range(n)]
        result=h*math.fsum(terms)
    elif method=="trapezoid":
        terms=[0.5*value(a),0.5*value(b)]
        terms.extend(value(a+i*h) for i in range(1,n))
        result=h*math.fsum(terms)
    else:
        terms=[value(a),value(b)]
        terms.extend((4 if i%2 else 2)*value(a+i*h) for i in range(1,n))
        result=(h/3)*math.fsum(terms)
    if not math.isfinite(result):
        raise ValueError("nonfinite integral")
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
