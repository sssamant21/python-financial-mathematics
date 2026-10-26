"""Book 02 Section 15.1: functions of several variables."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        converted=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(converted):
        raise ValueError(f"{name} must be finite")
    return converted

def account_value(principal,annual_rate,years):
    p=finite(principal,"principal")
    r=finite(annual_rate,"annual rate")
    t=finite(years,"years")
    if p<0 or t<0:
        raise ValueError("principal and years must be nonnegative")
    try:
        result=p*math.exp(r*t)
    except OverflowError as exc:
        raise ValueError("account value overflow") from exc
    return finite(result,"account value")

def present_value(cash_flow,annual_rate,years):
    f=finite(cash_flow,"cash flow")
    r=finite(annual_rate,"annual rate")
    t=finite(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    try:
        result=f*math.exp(-r*t)
    except OverflowError as exc:
        raise ValueError("present value overflow") from exc
    return finite(result,"present value")

def rate_for_target(principal,target,years):
    p=finite(principal,"principal")
    c=finite(target,"target")
    t=finite(years,"years")
    if p<=0 or c<=0 or t<=0:
        raise ValueError("principal, target, and years must be positive")
    return finite(math.log(c/p)/t,"recovered rate")

def assessment():
    rates=(0.0,0.05,0.10)
    horizons=(1.0,2.0)
    return {
        "reference_value":account_value(1000,0.05,2),
        "higher_rate_value":account_value(1000,0.06,2),
        "scenario_difference":account_value(1000,0.06,2)-account_value(1000,0.05,2),
        "reference_present_value":present_value(1000,0.05,2),
        "scenario_grid":tuple(tuple(account_value(1000,r,t) for t in horizons)
                              for r in rates),
        "recovered_rate":rate_for_target(1000,1000*math.exp(0.1),2),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
