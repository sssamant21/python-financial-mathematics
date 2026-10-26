"""Book 02 Section 15.8: level sets and sensitivity interpretation."""
import json
import math

def number(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def future_value(principal,rate,years):
    p=number(principal,"principal")
    r=number(rate,"rate")
    t=number(years,"years")
    if p<=0 or t<0:
        raise ValueError("principal must be positive and years nonnegative")
    try:
        return number(p*math.exp(r*t),"future value")
    except OverflowError as exc:
        raise ValueError("future value overflow") from exc

def iso_value_slope(rate,years):
    r=number(rate,"rate")
    t=number(years,"years")
    if r==0 or t<0:
        raise ValueError("rate must be nonzero and years nonnegative")
    return number(-t/r,"iso-value slope")

def exact_unchanged_value_time(rate,years,rate_shock):
    r=number(rate,"rate")
    t=number(years,"years")
    dr=number(rate_shock,"rate shock")
    if t<0 or r==0 or r+dr==0:
        raise ValueError("invalid maturity or zero rate")
    new_time=number(r*t/(r+dr),"adjusted maturity")
    if new_time<0:
        raise ValueError("adjusted maturity outside nonnegative domain")
    return new_time

def portfolio_variance(weight1,weight2):
    w1=number(weight1,"weight1")
    w2=number(weight2,"weight2")
    return number(0.04*w1*w1+0.02*w1*w2+0.09*w2*w2,"variance")

def portfolio_gradient(weight1,weight2):
    w1=number(weight1,"weight1")
    w2=number(weight2,"weight2")
    return (number(0.08*w1+0.02*w2,"gradient"),
            number(0.02*w1+0.18*w2,"gradient"))

def iso_variance_slope(weight1,weight2):
    gx,gy=portfolio_gradient(weight1,weight2)
    if gy==0:
        raise ValueError("vertical tangent or critical point")
    return number(-gx/gy,"iso-variance slope")

def fully_invested_derivative(weight1,weight2):
    w1=number(weight1,"weight1")
    w2=number(weight2,"weight2")
    if not math.isclose(w1+w2,1,rel_tol=0,abs_tol=1e-12):
        raise ValueError("weights must sum to one")
    gx,gy=portfolio_gradient(w1,w2)
    return number(gx-gy,"feasible variance derivative")

def assessment():
    r,t,dr=0.05,2.0,0.001
    base=future_value(1000,r,t)
    adjusted=exact_unchanged_value_time(r,t,dr)
    w1,w2=0.6,0.4
    return {
        "base_future_value":base,
        "iso_value_slope":iso_value_slope(r,t),
        "linear_time_adjustment":iso_value_slope(r,t)*dr,
        "exact_adjusted_maturity":adjusted,
        "exact_time_adjustment":adjusted-t,
        "revalued_future_value":future_value(1000,r+dr,adjusted),
        "portfolio_variance":portfolio_variance(w1,w2),
        "portfolio_gradient":portfolio_gradient(w1,w2),
        "unconstrained_iso_variance_slope":iso_variance_slope(w1,w2),
        "fully_invested_derivative":fully_invested_derivative(w1,w2),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
