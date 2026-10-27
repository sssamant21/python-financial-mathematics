"""Book 02 Section 19.7: financial depletion, events and jump rules."""
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

def account(initial,rate,withdrawal,years):
    a,r,w,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal"),(years,"years")))
    if a<0 or w<0 or t<0:
        raise ValueError("initial, withdrawal, and years must be nonnegative")
    if r==0:
        return finite(a-w*t,"balance")
    exponent=r*t
    factor=t if exponent==0 else t*(math.expm1(exponent)/exponent)
    return finite(a*math.exp(exponent)-w*factor,"balance")

def depletion_time(initial,rate,withdrawal):
    a,r,w=(finite(v,n) for v,n in
           ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal")))
    if a<0 or w<0:
        raise ValueError("initial and withdrawal must be nonnegative")
    if a==0:
        return 0.0
    if w==0:
        return None
    if r==0:
        return a/w
    ratio=r*a/w
    if ratio==0:
        return finite(a/w,"depletion time")
    if ratio>=1:
        return None
    return finite(-math.log1p(-ratio)/r,"depletion time")

def linear_crossing(t0,t1,y0,y1):
    a,b,ya,yb=(finite(v,n) for v,n in
               ((t0,"t0"),(t1,"t1"),(y0,"y0"),(y1,"y1")))
    if b<=a or ya<=0 or yb>0:
        raise ValueError("requires a positive-to-nonpositive crossing on an increasing interval")
    return finite(a+(b-a)*ya/(ya-yb),"crossing time")

def simulate_jumps(initial,rate,withdrawal,horizon,jumps,stop_at_depletion=True):
    a,r,w,T=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal"),(horizon,"horizon")))
    if a<0 or w<0 or T<0 or type(stop_at_depletion) is not bool:
        raise ValueError("invalid simulation inputs")
    if not isinstance(jumps,(list,tuple)):
        raise TypeError("jumps must be a sequence")
    events=[]
    previous=-1.0
    for item in jumps:
        if not isinstance(item,(list,tuple)) or len(item)!=2:
            raise ValueError("jumps must be (time, amount) pairs")
        t,j=finite(item[0],"jump time"),finite(item[1],"jump amount")
        if t<0 or t>T or t<=previous:
            raise ValueError("jump times must be unique, increasing and within horizon")
        events.append((t,j))
        previous=t
    current_time=0.0
    # Policy: at t=0, apply scheduled jumps before checking depletion.
    for next_time,jump in events+[(T,0.0)]:
        dt=next_time-current_time
        if dt<0:
            raise ValueError("unordered events")
        if stop_at_depletion:
            crossing=depletion_time(a,r,w)
            if crossing is not None and crossing<dt:
                return {"status":"depleted","event_time":current_time+crossing,
                        "final_time":current_time+crossing,"final_balance":0.0}
        a=account(a,r,w,dt)
        current_time=next_time
        if stop_at_depletion and a<0:
            return {"status":"depleted","event_time":current_time,
                    "final_time":current_time,"final_balance":0.0}
        a=finite(a+jump,"post-jump balance")
        if stop_at_depletion and a<=0:
            return {"status":"depleted","event_time":current_time,
                    "final_time":current_time,"final_balance":0.0}
    return {"status":"completed","event_time":None,
            "final_time":T,"final_balance":a}

def assessment():
    return {"depletion_positive_rate":depletion_time(1000,0.04,100),
            "depletion_zero_rate":depletion_time(1000,0,100),
            "depletion_negative_rate":depletion_time(1000,-0.02,50),
            "no_depletion":depletion_time(1000,0.04,40),
            "jump_balance":simulate_jumps(1000,0.05,0,5,[(2,200)]),
            "terminal_depletion":simulate_jumps(1000,0.04,100,20,[]),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
