"""Book 02 Section 19.5: Euler time stepping and diagnostics."""
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

def euler(f,initial,horizon,steps):
    y,t=finite(initial,"initial"),finite(horizon,"horizon")
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("horizon must be nonnegative; steps positive integer")
    h=t/steps
    for n in range(steps):
        slope=finite(f(n*h,y),"derivative")
        y=finite(y+h*slope,"Euler state")
    return {"final_state":y,"steps":steps,"step_size":h,"status":"completed"}

def exact_account(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if r==0:
        return finite(a+u*t,"balance")
    exponent=r*t
    factor=t if exponent==0 else t*(math.expm1(exponent)/exponent)
    return finite(a*math.exp(exponent)+u*factor,"balance")

def linear_amplification(rate,step):
    lam,h=finite(rate,"rate"),finite(step,"step")
    if h<=0:
        raise ValueError("step must be positive")
    return finite(1+h*lam,"amplification")

def stable_linear_decay(rate,step):
    lam=finite(rate,"rate")
    if lam>=0:
        raise ValueError("requires a negative decay rate")
    return abs(linear_amplification(lam,step))<1

def assessment():
    exact=exact_account(1000,0.05,0,2)
    simulations={}
    for n in (10,20,40):
        result=euler(lambda t,y:0.05*y,1000,2,n)
        result["absolute_error"]=abs(result["final_state"]-exact)
        simulations[str(n)]=result
    account_exact=exact_account(1000,0.04,200,5)
    return {"growth_reference":exact,"growth_euler":simulations,
            "account_reference":account_exact,
            "account_euler_40":euler(lambda t,y:0.04*y+200,1000,5,40),
            "decay_amplification_h025":linear_amplification(-2,0.25),
            "decay_amplification_h075":linear_amplification(-2,0.75),
            "decay_amplification_h125":linear_amplification(-2,1.25),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
