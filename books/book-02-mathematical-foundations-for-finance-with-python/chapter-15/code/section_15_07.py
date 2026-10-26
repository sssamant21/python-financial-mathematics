"""Book 02 Section 15.7: multivariable Taylor scenario approximations."""
import json
import math

def number(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside floating-point range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def inputs(amount,rate,years):
    a=number(amount,"amount")
    r=number(rate,"rate")
    t=number(years,"years")
    if a<0 or t<0:
        raise ValueError("amount and years must be nonnegative")
    return a,r,t

def valuation(amount,rate,years,discount=False):
    a,r,t=inputs(amount,rate,years)
    sign=-1 if discount else 1
    try:
        return number(a*math.exp(sign*r*t),"valuation")
    except OverflowError as exc:
        raise ValueError("valuation overflow") from exc

def taylor_changes(amount,rate,years,rate_shock,time_shock,discount=False):
    a,r,t=inputs(amount,rate,years)
    dr=number(rate_shock,"rate shock")
    dt=number(time_shock,"time shock")
    if t+dt<0:
        raise ValueError("shocked maturity must be nonnegative")
    sign=-1 if discount else 1
    base=valuation(a,r,t,discount)
    shocked=valuation(a,r+dr,t+dt,discount)
    linear=number(sign*base*(t*dr+r*dt),"first order")
    quadratic=number(base*(0.5*t*t*dr*dr+
                           (r*t+sign)*dr*dt+
                           0.5*r*r*dt*dt),"quadratic correction")
    second=number(linear+quadratic,"second order")
    exact=number(shocked-base,"exact change")
    return {"base":base,"shocked":shocked,
            "first_order_change":linear,
            "quadratic_correction":quadratic,
            "second_order_change":second,
            "exact_change":exact,
            "first_order_error":number(linear-exact,"first order error"),
            "second_order_error":number(second-exact,"second order error")}

def polynomial(x,y):
    x=number(x,"x")
    y=number(y,"y")
    return number(x*x+3*x*y+2*y*y,"polynomial")

def assessment():
    return {
        "polynomial_base":polynomial(1,2),
        "polynomial_first_order_change":-1.4,
        "polynomial_second_order_change":-1.37,
        "polynomial_exact_change":number(polynomial(1.1,1.8)-polynomial(1,2),
                                         "polynomial change"),
        "future_value":taylor_changes(1000,0.05,2,0.01,0.5),
        "present_value":taylor_changes(1000,0.05,2,0.01,0.5,discount=True),
        "runtime_certified":False,
        "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
