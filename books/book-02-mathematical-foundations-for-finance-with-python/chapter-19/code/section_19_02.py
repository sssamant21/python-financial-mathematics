"""Book 02 Section 19.2: separable equations lab."""
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
    return finite(a*math.exp(r*t),"growth balance")

def variable_growth(initial,a,b,years):
    start,base,slope,t=(finite(v,n) for v,n in
                         ((initial,"initial"),(a,"a"),(b,"b"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    return finite(start*math.exp(base*t+0.5*slope*t*t),"variable growth balance")

def logistic(initial,rate,capacity,years):
    a,r,k,t=(finite(v,n) for v,n in
               ((initial,"initial"),(rate,"rate"),(capacity,"capacity"),(years,"years")))
    if a<0 or r<=0 or k<=0 or t<0:
        raise ValueError("invalid logistic inputs")
    if a==0:
        return 0.0
    q=(k/a)-1
    denominator=1+q*math.exp(-r*t)
    if denominator<=0:
        raise ValueError("logistic solution outside valid interval")
    return finite(k/denominator,"logistic balance")

def quadratic_growth(initial,rate,years):
    a,k,t=finite(initial,"initial"),finite(rate,"rate"),finite(years,"years")
    if a<=0 or k<=0 or t<0:
        raise ValueError("initial and rate must be positive; years nonnegative")
    singularity=1/(k*a)
    if t>=singularity:
        raise ValueError("at or beyond finite-time singularity")
    return finite(a/(1-k*a*t),"quadratic growth balance")

def proportional_withdrawals(initial,growth_rate,withdrawal_rate,years):
    a,r,w,t=(finite(v,n) for v,n in
              ((initial,"initial"),(growth_rate,"growth rate"),
               (withdrawal_rate,"withdrawal rate"),(years,"years")))
    if a<0 or w<0 or t<0:
        raise ValueError("invalid withdrawal inputs")
    return growth(a,r-w,t)

def assessment():
    return {"exponential_growth":growth(1000,0.04,3),
            "variable_growth":variable_growth(1000,0.03,0.002,5),
            "logistic":logistic(200,0.4,1000,5),
            "logistic_zero_equilibrium":logistic(0,0.4,1000,5),
            "quadratic_growth_before_singularity":quadratic_growth(100,0.001,5),
            "quadratic_singularity_time":10.0,
            "proportional_withdrawals":proportional_withdrawals(1000,0.04,0.06,5),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
