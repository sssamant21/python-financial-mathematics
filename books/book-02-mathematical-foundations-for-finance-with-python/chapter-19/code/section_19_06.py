"""Book 02 Section 19.6: RK4 and adaptive step-doubling solver."""
import json
import math
from fractions import Fraction

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

def _rounded(value,name):
    try:
        return float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc

def rk4_step(f,t,y,h):
    t,y,h=finite(t,"time"),finite(y,"state"),finite(h,"step")
    if h<=0:
        raise ValueError("step must be positive")
    return _rk4_interval(f,t,y,Fraction(h))

def _rk4_interval(f,t,y,hf):
    tf,yf=map(Fraction,(t,y))
    k1=Fraction(finite(f(t,y),"k1"))
    midpoint=_rounded(tf+hf/2,"RK4 midpoint time")
    k2=Fraction(finite(f(midpoint,_rounded(yf+hf*k1/2,"RK4 second stage state")),"k2"))
    k3=Fraction(finite(f(midpoint,_rounded(yf+hf*k2/2,"RK4 third stage state")),"k3"))
    endpoint=_rounded(tf+hf,"RK4 endpoint time")
    k4=Fraction(finite(f(endpoint,_rounded(yf+hf*k3,"RK4 fourth stage state")),"k4"))
    return _rounded(yf+hf*(k1+2*k2+2*k3+k4)/6,"RK4 state")

def _step_factor(scale,error):
    if not error:
        return 5.0
    ratio=scale/error
    # Clamp before converting extreme ratios to float.
    if ratio<=Fraction(1,10000):
        return 0.2
    if ratio>=10000:
        return 5.0
    return max(0.2,min(5.0,0.9*float(ratio)**0.2))

def fixed_rk4(f,initial,horizon,steps):
    y,T=finite(initial,"initial"),finite(horizon,"horizon")
    if T<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid horizon or step count")
    if T==0:
        return {"final_state":y,"final_time":0.0,"steps":0,"evaluations":0,
                "status":"completed"}
    width=Fraction(T)/steps
    message="fixed RK4 grid has non-increasing endpoints"
    if width<Fraction(math.ulp(0.0)):
        raise ValueError(message)

    # Round each ideal endpoint, then integrate exactly the represented
    # interval between adjacent endpoints instead of repeating rounded T/n.
    def intervals():
        left=0.0
        for n in range(1,steps+1):
            right=float(n*width)
            yield left,right
            left=right

    # Reject the entire grid before calling the RHS, even for a collapse
    # near the end. Regenerate it so storage does not grow with steps.
    if any(right<=left for left,right in intervals()):
        raise ValueError(message)
    for left,right in intervals():
        y=_rk4_interval(f,left,y,Fraction(right)-Fraction(left))
    return {"final_state":y,"final_time":T,"steps":steps,
            "evaluations":4*steps,"status":"completed"}

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

def adaptive_rk4(f,initial,horizon,atol=1e-7,rtol=1e-9,
                 initial_step=None,max_attempts=10000,min_step=1e-12):
    y,T=finite(initial,"initial"),finite(horizon,"horizon")
    atol,rtol=finite(atol,"atol"),finite(rtol,"rtol")
    min_step=finite(min_step,"min_step")
    if T<0 or atol<=0 or rtol<0 or min_step<=0:
        raise ValueError("invalid horizon, tolerance, or minimum step")
    if type(max_attempts) is not int or max_attempts<1:
        raise ValueError("max_attempts must be a positive integer")
    if initial_step is None:
        h=T/10 if T else 0
    else:
        h=finite(initial_step,"initial_step")
        if h<=0:
            raise ValueError("initial_step must be positive")
    if T==0:
        return {"status":"completed","final_state":y,"final_time":0.0,
                "accepted_steps":0,"rejected_steps":0,"evaluations":0,
                "atol":atol,"rtol":rtol}
    t=0.0
    accepted=rejected=evaluations=0
    for _ in range(max_attempts):
        remaining=T-t
        if remaining<=0:
            break
        h=min(h,remaining)
        half_step=h/2
        if h<min_step or t+h==t or 2*half_step!=h:
            return {"status":"step_too_small","final_state":y,"final_time":t,
                    "accepted_steps":accepted,"rejected_steps":rejected,
                    "evaluations":evaluations,"atol":atol,"rtol":rtol}
        full=rk4_step(f,t,y,h)
        mid=rk4_step(f,t,y,half_step)
        half=rk4_step(f,t+half_step,mid,half_step)
        evaluations+=12
        error=abs(Fraction(half)-Fraction(full))/15
        scale=Fraction(atol)+Fraction(rtol)*Fraction(max(abs(y),abs(half)))
        if error<=scale:
            y=half
            t=min(T,t+h)
            accepted+=1
        else:
            rejected+=1
        factor=_step_factor(scale,error)
        h*=factor
    if t<T:
        status="attempt_budget_exhausted"
    else:
        status="completed"
    return {"status":status,"final_state":y,"final_time":t,
            "accepted_steps":accepted,"rejected_steps":rejected,
            "evaluations":evaluations,"atol":atol,"rtol":rtol}

def assessment():
    f=lambda t,y:0.05*y
    exact=exact_account(1000,0.05,0,2)
    fixed={}
    for n in (4,8,16):
        result=fixed_rk4(f,1000,2,n)
        result["absolute_error"]=abs(result["final_state"]-exact)
        fixed[str(n)]=result
    adaptive=adaptive_rk4(f,1000,2)
    adaptive["absolute_error"]=abs(adaptive["final_state"]-exact)
    return {"growth_reference":exact,"fixed_rk4":fixed,
            "adaptive_growth":adaptive,
            "account_reference":exact_account(1000,0.04,200,5),
            "adaptive_account":adaptive_rk4(lambda t,y:0.04*y+200,1000,5),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
