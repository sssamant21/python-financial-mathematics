"""Book 02 Section 19.1: differential models and initial conditions."""
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

def growth(initial,rate,years):
    a,r,t=finite(initial,"initial"),finite(rate,"rate"),finite(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    return finite(a*math.exp(r*t),"balance")

def account(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if r==0:
        return finite(a+u*t,"balance")
    return finite(a*math.exp(r*t)+u*math.expm1(r*t)/r,"balance")

def continuous_from_effective(rate):
    r=finite(rate,"effective rate")
    if r<=-1:
        raise ValueError("effective rate must exceed -1")
    return math.log1p(r)

def effective_from_continuous(rate):
    return finite(math.expm1(finite(rate,"continuous rate")),"effective rate")

def euler_account(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid time or step count")
    h=t/steps
    for _ in range(steps):
        a=finite(a+h*(r*a+u),"Euler balance")
    return a

def assessment():
    exact=growth(1000,0.05,2)
    return {"growth_2_years":exact,
            "growth_euler_10":euler_account(1000,0.05,0,2,10),
            "growth_euler_20":euler_account(1000,0.05,0,2,20),
            "growth_euler_40":euler_account(1000,0.05,0,2,40),
            "account_with_flow":account(1000,0.04,200,5),
            "zero_rate_account":account(1000,0,200,5),
            "depletion_years":10,
            "annual_effective_equivalent":effective_from_continuous(0.05),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
