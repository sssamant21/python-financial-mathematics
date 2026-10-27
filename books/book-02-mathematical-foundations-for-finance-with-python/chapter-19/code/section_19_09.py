"""Book 02 Section 19.9: continuous account and depletion simulator."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def transition(balance,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((balance,"balance"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if r==0:
        return finite(a+u*t,"balance")
    return finite(a*math.exp(r*t)+u*math.expm1(r*t)/r,"balance")

def depletion_time(balance,rate,flow):
    a,r,u=finite(balance,"balance"),finite(rate,"rate"),finite(flow,"flow")
    if a<0:
        raise ValueError("balance must be nonnegative")
    if a==0:
        return 0.0
    if u>=0:
        return None
    w=-u
    if r==0:
        return a/w
    ratio=r*a/w
    if ratio>=1:
        return None
    return finite(-math.log1p(-ratio)/r,"depletion time")

def simulate(initial,rate,flow,horizon,jumps=()):
    a,r,u,T=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(horizon,"horizon")))
    if a<0 or T<0:
        raise ValueError("initial and horizon must be nonnegative")
    if not isinstance(jumps,(list,tuple)):
        raise TypeError("jumps must be a sequence")
    scheduled=[]
    previous=-1.0
    for event in jumps:
        if not isinstance(event,(tuple,list)) or len(event)!=2:
            raise ValueError("each jump must be (time, amount)")
        t,j=finite(event[0],"jump time"),finite(event[1],"jump amount")
        if t<0 or t>T or t<=previous:
            raise ValueError("jump times must be unique, increasing, within horizon")
        scheduled.append((t,j))
        previous=t
    time=0.0
    log=[]
    applied=0
    # Explicit policy: jumps at t=0 are applied before initial depletion.
    if scheduled and scheduled[0][0]==0:
        j=scheduled.pop(0)[1]
        a=finite(a+j,"post-jump balance")
        applied+=1
        log.append({"type":"jump","time":0.0,"amount":j,"balance":a})
    if a<=0:
        log.append({"type":"depletion","time":0.0})
        return _result("depleted",0,0,0.0,len(jumps),applied,log)
    for event_time,jump in scheduled+[(T,0.0)]:
        dt=event_time-time
        crossing=depletion_time(a,r,u)
        # Depletion takes precedence when simultaneous with a scheduled jump.
        if crossing is not None and crossing<=dt:
            event_at=time+crossing
            log.append({"type":"depletion","time":event_at})
            return _result("depleted",event_at,0.0,event_at,
                           len(jumps),applied,log)
        a=transition(a,r,u,dt)
        time=event_time
        if a<=0:
            log.append({"type":"depletion","time":time})
            return _result("depleted",time,0.0,time,len(jumps),applied,log)
        if (event_time,jump)!=(T,0.0) or (scheduled and scheduled[-1]==(T,0.0)):
            # All explicit events are processed before the final sentinel.
            pass
        if jump!=0.0 or (event_time,jump) in scheduled:
            a=finite(a+jump,"post-jump balance")
            applied+=1
            log.append({"type":"jump","time":time,"amount":jump,"balance":a})
            if a<=0:
                log.append({"type":"depletion","time":time})
                return _result("depleted",time,0.0,time,len(jumps),applied,log)
    return _result("completed",T,a,None,len(jumps),applied,log)

def _result(status,time,balance,event_time,scheduled,applied,events):
    return {"status":status,"final_time":time,"final_balance":balance,
            "depletion_time":event_time,"scheduled_jumps":scheduled,
            "applied_jumps":applied,"events":events,
            "units":{"time":"years","balance":"currency",
                     "rate":"inverse_years","flow":"currency_per_year"},
            "runtime_certified":False,"independent_review_completed":False}

def assessment():
    return {"growth":simulate(1000,0.04,0,5),
            "contributions":simulate(1000,0.04,200,5),
            "depletion":simulate(1000,0.04,-100,20),
            "scheduled_deposit":simulate(1000,0.05,0,5,[(2,200)]),
            "late_deposit":simulate(100,0,-50,5,[(3,1000)]),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
