"""Book 02 Section 19.1: differential models and initial conditions."""
import json
import math
from fractions import Fraction

from section_19_02 import _scaled_exponential
from section_19_08 import _continuous_balance, _euler_balance

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
    return _scaled_exponential(a,Fraction(r)*Fraction(t),reject_underflow=False)

def account(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if t==0:
        return a
    return _continuous_balance(a,r,u,t,reject_underflow=False)

def continuous_from_effective(rate):
    r=finite(rate,"effective rate")
    if r<=-1:
        raise ValueError("effective rate must exceed -1")
    return math.log1p(r)

def effective_from_continuous(rate):
    r=finite(rate,"continuous rate")
    try:
        effective=math.expm1(r)
    except OverflowError as exc:
        raise ValueError("effective rate outside floating-point range") from exc
    if effective<=-1:
        raise ValueError("effective rate rounds to the excluded endpoint -1")
    return effective

def euler_account(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid time or step count")
    return _euler_balance(a,r,u,t,steps,reject_underflow=False)

def assessment():
    exact=growth(1000,0.05,2)
    euler={n:euler_account(1000,0.05,0,2,n) for n in (10,20,40)}
    return {"growth_2_years":exact,
            **{f"growth_euler_{n}":value for n,value in euler.items()},
            **{f"growth_euler_absolute_error_{n}":abs(value-exact)
               for n,value in euler.items()},
            "account_with_flow":account(1000,0.04,200,5),
            "zero_rate_account":account(1000,0,200,5),
            "depletion_years":10,
            "annual_effective_equivalent":effective_from_continuous(0.05),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
