"""Book 02 Section 15.3: total differentials and the chain rule."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def future_value(principal,annual_rate,years):
    p=finite(principal,"principal")
    r=finite(annual_rate,"annual rate")
    t=finite(years,"years")
    if p<0 or t<0:
        raise ValueError("principal and years must be nonnegative")
    try:
        return finite(p*math.exp(r*t),"future value")
    except OverflowError as exc:
        raise ValueError("future value overflow") from exc

def total_differential(principal,annual_rate,years,d_principal,d_rate,d_years):
    p=finite(principal,"principal")
    r=finite(annual_rate,"annual rate")
    t=finite(years,"years")
    dp=finite(d_principal,"principal increment")
    dr=finite(d_rate,"rate increment")
    dt=finite(d_years,"time increment")
    base=future_value(p,r,t)
    return finite(math.fsum((math.exp(r*t)*dp,t*base*dr,r*base*dt)),
                  "total differential")

def scenario_change(principal,annual_rate,years,d_principal,d_rate,d_years):
    p=finite(principal,"principal")
    r=finite(annual_rate,"annual rate")
    t=finite(years,"years")
    dp=finite(d_principal,"principal increment")
    dr=finite(d_rate,"rate increment")
    dt=finite(d_years,"time increment")
    return finite(future_value(p+dp,r+dr,t+dt)-future_value(p,r,t),
                  "exact scenario change")

def polynomial_value(x,y):
    x=finite(x,"x")
    y=finite(y,"y")
    return finite(x*x*y+3*y*y,"polynomial value")

def polynomial_differential(x,y,dx,dy):
    x=finite(x,"x")
    y=finite(y,"y")
    dx=finite(dx,"dx")
    dy=finite(dy,"dy")
    return finite(2*x*y*dx+(x*x+6*y)*dy,"polynomial differential")

def assessment():
    args=(1000,0.05,2,100,0.01,0.5)
    approximate=total_differential(*args)
    exact=scenario_change(*args)
    return {
        "base_value":future_value(1000,0.05,2),
        "shocked_value":future_value(1100,0.06,2.5),
        "total_differential":approximate,
        "exact_scenario_change":exact,
        "path_derivative_at_zero":approximate,
        "linearization_error_exact_minus_approximate":exact-approximate,
        "polynomial_differential":polynomial_differential(2,1,0.1,-0.05),
        "polynomial_exact_change":
            polynomial_value(2.1,0.95)-polynomial_value(2,1),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
