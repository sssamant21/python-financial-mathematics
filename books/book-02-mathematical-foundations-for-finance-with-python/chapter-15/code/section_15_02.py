"""Book 02 Section 15.2: partial derivatives of simple financial models."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def inputs(amount,annual_rate,years):
    a=finite(amount,"amount")
    r=finite(annual_rate,"annual rate")
    t=finite(years,"years")
    if a<0 or t<0:
        raise ValueError("amount and years must be nonnegative")
    return a,r,t

def future_value(amount,annual_rate,years):
    a,r,t=inputs(amount,annual_rate,years)
    try:
        return finite(a*math.exp(r*t),"future value")
    except OverflowError as exc:
        raise ValueError("future value overflow") from exc

def present_value(amount,annual_rate,years):
    a,r,t=inputs(amount,annual_rate,years)
    try:
        return finite(a*math.exp(-r*t),"present value")
    except OverflowError as exc:
        raise ValueError("present value overflow") from exc

def future_partials(amount,annual_rate,years):
    a,r,t=inputs(amount,annual_rate,years)
    value=future_value(a,r,t)
    return {"principal":finite(math.exp(r*t),"principal partial"),
            "rate":finite(t*value,"rate partial"),
            "time":finite(r*value,"time partial")}

def present_partials(amount,annual_rate,years):
    a,r,t=inputs(amount,annual_rate,years)
    value=present_value(a,r,t)
    return {"cash_flow":finite(math.exp(-r*t),"cash flow partial"),
            "rate":finite(-t*value,"rate partial"),
            "time":finite(-r*value,"time partial")}

def centered_rate_difference(fn,amount,annual_rate,years,step=1e-5):
    h=finite(step,"step")
    if h<=0:
        raise ValueError("step must be positive")
    r=finite(annual_rate,"annual rate")
    return finite((fn(amount,r+h,years)-fn(amount,r-h,years))/(2*h),
                  "centered rate difference")

def assessment():
    amount,rate,years=1000.0,0.05,2.0
    fv=future_value(amount,rate,years)
    fv_higher=future_value(amount,rate+0.01,years)
    return {"future_value":fv,"future_partials":future_partials(amount,rate,years),
            "present_value":present_value(amount,rate,years),
            "present_partials":present_partials(amount,rate,years),
            "first_order_rate_change":future_partials(amount,rate,years)["rate"]*0.01,
            "exact_rate_change":fv_higher-fv,
            "centered_future_rate_derivative":
                centered_rate_difference(future_value,amount,rate,years),
            "centered_present_rate_derivative":
                centered_rate_difference(present_value,amount,rate,years),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
