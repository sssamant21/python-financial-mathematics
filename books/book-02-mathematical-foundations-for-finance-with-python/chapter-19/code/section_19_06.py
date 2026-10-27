"""Book 02 Section 19.6: RK4 and adaptive step-doubling solver."""
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

def rk4_step(f,t,y,h):
    t,y,h=finite(t,"time"),finite(y,"state"),finite(h,"step")
    if h<=0:
        raise ValueError("step must be positive")
    k1=finite(f(t,y),"k1")
    k2=finite(f(t+h/2,y+h*k1/2),"k2")
    k3=finite(f(t+h/2,y+h*k2/2),"k3")
    k4=finite(f(t+h,y+h*k3),"k4")
    return finite(y+h*(k1+2*k2+2*k3+k4)/6,"RK4 state")

def fixed_rk4(f,initial,horizon,steps):
    y,T=finite(initial,"initial"),finite(horizon,"horizon")
    if T<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid horizon or step count")
    h=T/steps
    if T==0:
        return {"final_state":y,"final_time":0.0,"steps":0,"evaluations":0,
                "status":"completed"}
    for n in range(steps):
        y=rk4_step(f,n*h,y,h)
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
        if h<min_step or t+h==t:
            return {"status":"step_too_small","final_state":y,"final_time":t,
                    "accepted_steps":accepted,"rejected_steps":rejected,
                    "evaluations":evaluations,"atol":atol,"rtol":rtol}
        full=rk4_step(f,t,y,h)
        mid=rk4_step(f,t,y,h/2)
        half=rk4_step(f,t+h/2,mid,h/2)
        evaluations+=12
        error=abs(half-full)/15
        scale=atol+rtol*max(abs(y),abs(half))
        if error<=scale:
            y=half
            t=min(T,t+h)
            accepted+=1
        else:
            rejected+=1
        factor=5.0 if error==0 else max(0.2,min(5.0,0.9*(scale/error)**0.2))
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
