"""Book 02 Section 18.6: interpolation and extrapolation lab."""
import json
import math

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

def nodes(xs,ys):
    if not isinstance(xs,(tuple,list)) or not isinstance(ys,(tuple,list)):
        raise TypeError("nodes must be lists or tuples")
    if len(xs)!=len(ys) or len(xs)<2:
        raise ValueError("at least two paired knots required")
    x=tuple(finite(v,"x") for v in xs)
    y=tuple(finite(v,"y") for v in ys)
    if any(a>=b for a,b in zip(x,x[1:])):
        raise ValueError("knots must be strictly increasing")
    return x,y

def piecewise_linear(xs,ys,query,allow_extrapolation=False):
    x,y=nodes(xs,ys)
    q=finite(query,"query")
    if not allow_extrapolation and not x[0]<=q<=x[-1]:
        raise ValueError("extrapolation disabled")
    if q<=x[0]:
        i=0
    elif q>=x[-1]:
        i=len(x)-2
    else:
        i=next(j for j in range(len(x)-1) if x[j]<=q<=x[j+1])
    t=(q-x[i])/(x[i+1]-x[i])
    return y[i]+t*(y[i+1]-y[i])

def lagrange(xs,ys,query):
    x,y=nodes(xs,ys)
    q=finite(query,"query")
    total=0.0
    for i,yi in enumerate(y):
        basis=1.0
        for j,xj in enumerate(x):
            if i!=j:
                basis*=(q-xj)/(x[i]-xj)
        total+=yi*basis
    return finite(total,"polynomial result")

def discount_factor(rate,years):
    r,t=finite(rate,"rate"),finite(years,"years")
    if r<=-1 or t<0:
        raise ValueError("rate must exceed -1 and maturity must be nonnegative")
    return math.exp(-t*math.log1p(r))

def financial_comparison():
    t=(1.0,3.0)
    rates=(0.04,0.05)
    d1=discount_factor(rates[0],t[0])
    d3=discount_factor(rates[1],t[1])
    rate_mid=piecewise_linear(t,rates,2.0)
    d_rate=discount_factor(rate_mid,2.0)
    d_linear=piecewise_linear(t,(d1,d3),2.0)
    d_log=math.exp(piecewise_linear(t,(math.log(d1),math.log(d3)),2.0))
    return {"rate_midpoint":rate_mid,"discount_from_rate":d_rate,
            "discount_linear":d_linear,"discount_log_linear":d_log,
            "discount_endpoints":(d1,d3)}

def assessment():
    return {"financial":financial_comparison(),
            "quadratic_interpolated":lagrange((0,1,2),(1,2,5),1.5),
            "linear_midpoint":piecewise_linear((1,3),(0.04,0.05),2),
            "extrapolated_rate":piecewise_linear((1,3),(0.04,0.05),4,True),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
