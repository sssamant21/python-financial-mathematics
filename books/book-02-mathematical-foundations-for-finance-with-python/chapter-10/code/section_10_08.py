"""Section 10.8: discrete versus continuous payments."""
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def valid_horizon(T):
    t=finite(T,"horizon")
    if t<0:
        raise ValueError("horizon must be nonnegative")
    return t

def valid_count(n):
    if type(n) is not int or n<=0:
        raise ValueError("n must be a positive integer")
    return n

def continuous_pv(payment_rate,rate,horizon):
    c,r,t=finite(payment_rate,"payment_rate"),finite(rate,"rate"),valid_horizon(horizon)
    x=r*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    result=c*t if x==0 else c*t*(-math.expm1(-x))/x
    if not math.isfinite(result):
        raise ValueError("nonfinite PV")
    return result

def schedule_pv(payments,rate):
    r=finite(rate,"rate")
    terms=[]
    for payment in payments:
        if len(payment)!=2:
            raise ValueError("payment must be (time, amount)")
        t,amount=payment
        time=finite(t,"time")
        if time<0:
            raise ValueError("payment time must be nonnegative")
        value=finite(amount,"amount")*math.exp(-r*time)
        if not math.isfinite(value):
            raise ValueError("nonfinite discounted payment")
        terms.append(value)
    result=math.fsum(terms)
    if not math.isfinite(result):
        raise ValueError("nonfinite PV")
    return result

def equal_payment_pv(payment_rate,rate,horizon,n,timing="end"):
    c,r,t=finite(payment_rate,"payment_rate"),finite(rate,"rate"),valid_horizon(horizon)
    n=valid_count(n)
    if timing not in ("begin","mid","end"):
        raise ValueError("timing must be begin, mid, or end")
    if c==0 or t==0:
        return 0.0
    h=t/n
    x=r*h
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    if x==0:
        return c*t
    # Exact finite geometric sum, evaluated stably for small |x|.
    base=(-math.expm1(-r*t))/(-math.expm1(-x))
    offset={"begin":0.0,"mid":0.5,"end":1.0}[timing]
    result=c*h*base*math.exp(-x*offset)
    if not math.isfinite(result):
        raise ValueError("nonfinite PV")
    return result

def timing_ratio(rate,horizon,n,timing="end"):
    r,t=finite(rate,"rate"),valid_horizon(horizon)
    n=valid_count(n)
    if timing not in ("begin","mid","end"):
        raise ValueError("unknown timing")
    x=r*t/n
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    if x==0:
        return 1.0
    # x/(e^x-1) is stable via expm1; very small x remains well-conditioned.
    factor=x/math.expm1(x)
    shift={"begin":1.0,"mid":0.5,"end":0.0}[timing]
    result=factor*math.exp(x*shift)
    if not math.isfinite(result):
        raise ValueError("nonfinite ratio")
    return result

def comparison(payment_rate=1200,rate=0.06,horizon=2):
    c,r,t=finite(payment_rate,"payment_rate"),finite(rate,"rate"),valid_horizon(horizon)
    reference=continuous_pv(c,r,t)
    rows=[]
    for n in (2,8,24,730):
        row={"n":n,"payment_amount":c*t/n,"nominal_total":c*t}
        for timing in ("begin","mid","end"):
            value=equal_payment_pv(c,r,t,n,timing)
            row[timing+"_pv"]=value
            row[timing+"_difference"]=value-reference
        rows.append(row)
    return {"continuous_pv":reference,"scenarios":rows,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(comparison(),indent=2,allow_nan=False))
