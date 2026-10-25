"""Section 9.7: kinks, one-sided derivatives, and payoff scenarios."""
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def call_payoff(spot,strike):
    s,k=finite(spot,"spot"),finite(strike,"strike")
    if s<0 or k<=0:
        raise ValueError("spot must be nonnegative and strike positive")
    return max(s-k,0.0)

def put_payoff(spot,strike):
    s,k=finite(spot,"spot"),finite(strike,"strike")
    if s<0 or k<=0:
        raise ValueError("spot must be nonnegative and strike positive")
    return max(k-s,0.0)

def call_slopes(spot,strike):
    s,k=finite(spot,"spot"),finite(strike,"strike")
    call_payoff(s,k)
    if s<k:
        return {"left":0.0,"right":0.0,"differentiable":True}
    if s>k:
        return {"left":1.0,"right":1.0,"differentiable":True}
    return {"left":0.0,"right":1.0,"differentiable":False}

def put_slopes(spot,strike):
    s,k=finite(spot,"spot"),finite(strike,"strike")
    put_payoff(s,k)
    if s<k:
        return {"left":-1.0,"right":-1.0,"differentiable":True}
    if s>k:
        return {"left":0.0,"right":0.0,"differentiable":True}
    return {"left":-1.0,"right":0.0,"differentiable":False}

def capped_floored_payment(rate,notional,floor,cap):
    r,n,a,c=(finite(v,name) for v,name in
             ((rate,"rate"),(notional,"notional"),(floor,"floor"),(cap,"cap")))
    if n<=0 or a>=c:
        raise ValueError("notional must be positive and floor less than cap")
    return n*min(max(r,a),c)

def cap_floor_slopes(rate,notional,floor,cap):
    r,n,a,c=(finite(v,name) for v,name in
             ((rate,"rate"),(notional,"notional"),(floor,"floor"),(cap,"cap")))
    capped_floored_payment(r,n,a,c)
    if r<a or r>c:
        left=right=0.0
    elif a<r<c:
        left=right=n
    elif r==a:
        left,right=0.0,n
    else:
        left,right=n,0.0
    return {"left":left,"right":right,"differentiable":left==right}

def difference_report(function,point,step):
    if not callable(function):
        raise TypeError("function must be callable")
    x,h=finite(point,"point"),finite(step,"step")
    if h<=0 or x-h==x or x+h==x:
        raise ValueError("step must be positive and representable")
    f0=finite(function(x),"f(point)")
    fm=finite(function(x-h),"f(point-step)")
    fp=finite(function(x+h),"f(point+step)")
    left=(f0-fm)/h
    right=(fp-f0)/h
    return {"left_difference":left,"right_difference":right,
            "centered_difference":(fp-fm)/(2*h)}

def call_scenario(spot,strike,shock,rate=0,years=0):
    s,k,h,r,t=(finite(v,name) for v,name in
               ((spot,"spot"),(strike,"strike"),(shock,"shock"),
                (rate,"rate"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    base=call_payoff(s,k)
    changed=call_payoff(s+h,k)
    factor=math.exp(-r*t)
    if not math.isfinite(factor):
        raise ValueError("nonfinite discount factor")
    return {"baseline_value":factor*base,"shocked_value":factor*changed,
            "exact_change":factor*(changed-base),
            "left_slope":factor*call_slopes(s,k)["left"],
            "right_slope":factor*call_slopes(s,k)["right"],
            "differentiable":call_slopes(s,k)["differentiable"]}

if __name__=="__main__":
    import json
    result={
        "call_at_strike":call_slopes(100,100),
        "put_at_strike":put_slopes(100,100),
        "finite_differences":difference_report(lambda x:call_payoff(x,100),100,2),
        "call_up":call_scenario(100,100,2,0.04,2),
        "call_down":call_scenario(100,100,-2,0.04,2),
        "cap_at_threshold":cap_floor_slopes(0.05,1000,0.02,0.05)}
    print(json.dumps(result,indent=2,allow_nan=False))
