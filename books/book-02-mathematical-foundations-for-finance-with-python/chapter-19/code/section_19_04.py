"""Book 02 Section 19.4: equilibria and local stability."""
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

def classify_derivative(derivative):
    d=finite(derivative,"derivative")
    if d<0:
        return "locally_asymptotically_stable"
    if d>0:
        return "unstable"
    return "inconclusive"

def mean_reversion(initial,target,speed,years):
    a,target,k,t=(finite(v,n) for v,n in
                  ((initial,"initial"),(target,"target"),
                   (speed,"speed"),(years,"years")))
    if k<=0 or t<0:
        raise ValueError("speed must be positive and years nonnegative")
    return finite(target+(a-target)*math.exp(-k*t),"balance")

def half_life(speed):
    k=finite(speed,"speed")
    if k<=0:
        raise ValueError("speed must be positive")
    return math.log(2)/k

def account_equilibrium(rate,flow):
    r,u=finite(rate,"rate"),finite(flow,"flow")
    if r==0:
        return None if u!=0 else "all_states"
    return finite(-u/r,"equilibrium")

def logistic_equilibria(rate,capacity):
    r,k=finite(rate,"rate"),finite(capacity,"capacity")
    if r<=0 or k<=0:
        raise ValueError("rate and capacity must be positive")
    return [{"state":0.0,"derivative":r,"classification":classify_derivative(r)},
            {"state":k,"derivative":-r,
             "classification":classify_derivative(-r)}]

def logistic(initial,rate,capacity,years):
    a,r,k,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),
              (capacity,"capacity"),(years,"years")))
    if a<0 or r<=0 or k<=0 or t<0:
        raise ValueError("invalid logistic inputs")
    if a==0:
        return 0.0
    return finite(k/(1+(k/a-1)*math.exp(-r*t)),"logistic balance")

def phase_direction(value):
    x=finite(value,"velocity")
    return "right" if x>0 else ("left" if x<0 else "equilibrium")

def assessment():
    return {"mean_reverting_balance":mean_reversion(1200,1000,0.5,2),
            "mean_reversion_half_life":half_life(0.5),
            "withdrawal_threshold":account_equilibrium(0.04,-100),
            "withdrawal_threshold_classification":classify_derivative(0.04),
            "logistic_equilibria":logistic_equilibria(0.4,1000),
            "logistic_balance":logistic(200,0.4,1000,5),
            "cubic_derivative_test":classify_derivative(0),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
