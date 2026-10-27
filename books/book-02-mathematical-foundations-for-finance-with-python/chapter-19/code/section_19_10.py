"""Book 02 Section 19.10: cumulative Chapter 19 analytical and numerical lab."""
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

def classify_equilibrium(derivative):
    d=finite(derivative,"derivative")
    return ("asymptotically_stable" if d<0 else
            "unstable" if d>0 else "inconclusive")

def euler(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid years or step count")
    h=t/steps
    for _ in range(steps):
        a=finite(a+h*(r*a+u),"Euler balance")
    return a

def rk4(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid years or step count")
    h=t/steps
    for _ in range(steps):
        k1=r*a+u
        k2=r*(a+h*k1/2)+u
        k3=r*(a+h*k2/2)+u
        k4=r*(a+h*k3)+u
        a=finite(a+h*(k1+2*k2+2*k3+k4)/6,"RK4 balance")
    return a

def depletion_time(initial,rate,withdrawal):
    a,r,w=(finite(v,n) for v,n in
           ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal")))
    if a<0 or w<0:
        raise ValueError("balance and withdrawal must be nonnegative")
    if a==0:
        return 0.0
    if w==0:
        return None
    if r==0:
        return a/w
    ratio=r*a/w
    if ratio>=1:
        return None
    if ratio==0:
        return finite(a/w,"depletion time")
    return finite(-math.log1p(-ratio)/r,"depletion time")

def deposit_at(initial,rate,deposit,deposit_year,horizon):
    a,r,j,tj,T=(finite(v,n) for v,n in
                ((initial,"initial"),(rate,"rate"),(deposit,"deposit"),
                 (deposit_year,"deposit_year"),(horizon,"horizon")))
    if not (0<=tj<=T):
        raise ValueError("deposit time must be within horizon")
    return exact_account(exact_account(a,r,0,tj)+j,r,0,T-tj)

def assessment():
    exact=exact_account(1000,0.05,0,2)
    comparisons={}
    for n in (10,20,40):
        e=euler(1000,0.05,0,2,n)
        k=rk4(1000,0.05,0,2,n)
        comparisons[str(n)]={"euler":e,"rk4":k,
                             "euler_absolute_error":abs(e-exact),
                             "rk4_absolute_error":abs(k-exact)}
    return {"exact_growth":exact,"convergence":comparisons,
            "contributions":exact_account(1000,0.04,200,5),
            "withdrawal_equilibrium":2500.0,
            "withdrawal_equilibrium_classification":classify_equilibrium(0.04),
            "mean_reversion_half_life":math.log(2)/0.5,
            "depletion_time":depletion_time(1000,0.04,100),
            "deposit_at_year_two":deposit_at(1000,0.05,200,2,5),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
