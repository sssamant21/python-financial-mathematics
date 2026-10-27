"""Book 02 Section 19.3: linear first-order financial equations."""
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

def account(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if r==0:
        return finite(a+u*t,"balance")
    exponent=r*t
    factor=t if exponent==0 else t*(math.expm1(exponent)/exponent)
    return finite(a*math.exp(exponent)+u*factor,"balance")

def depletion_time(initial,rate,withdrawal):
    a,r,w=(finite(v,n) for v,n in
           ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal")))
    if a<=0 or r<0 or w<=0:
        raise ValueError("requires positive balance and withdrawal, nonnegative rate")
    if r==0:
        return a/w
    if w<=r*a:
        return None
    ratio=r*a/w
    if ratio==0:
        return finite(a/w,"depletion time")
    return finite(-math.log1p(-ratio)/r,"depletion time")

def variable_rate_no_flow(initial,base,slope,years):
    a,r,b,t=(finite(v,n) for v,n in
             ((initial,"initial"),(base,"base"),(slope,"slope"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    return finite(a*math.exp(r*t+0.5*b*t*t),"balance")

def piecewise_account(initial,rate,segments):
    a=finite(initial,"initial")
    r=finite(rate,"rate")
    if not isinstance(segments,(tuple,list)):
        raise TypeError("segments must be a sequence")
    for segment in segments:
        if not isinstance(segment,(tuple,list)) or len(segment)!=2:
            raise ValueError("each segment requires (flow, years)")
        flow,years=segment
        a=account(a,r,flow,years)
    return a

def euler_account(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid years or step count")
    h=t/steps
    for _ in range(steps):
        a=finite(a+h*(r*a+u),"Euler balance")
    return a

def assessment():
    exact=account(1000,0.04,200,5)
    return {"constant_flow_balance":exact,
            "zero_rate_balance":account(1000,0,200,5),
            "small_rate_balance":account(1000,1e-8,200,5),
            "depletion_time":depletion_time(1000,0.04,100),
            "time_varying_rate_balance":variable_rate_no_flow(1000,0.03,0.002,5),
            "piecewise_balance":piecewise_account(1000,0.04,[(100,2),(200,3)]),
            "euler_10":euler_account(1000,0.04,200,5,10),
            "euler_20":euler_account(1000,0.04,200,5,20),
            "euler_40":euler_account(1000,0.04,200,5,40),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
