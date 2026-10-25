"""Section 10.6: improper integrals and infinite horizons."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def inputs(payment,growth,discount):
    c=finite(payment,"payment")
    g=finite(growth,"growth")
    r=finite(discount,"discount")
    delta=r-g
    if not math.isfinite(delta):
        raise ValueError("nonfinite net decay")
    return c,delta

def finite_horizon_pv(payment,growth,discount,horizon):
    c,d=inputs(payment,growth,discount)
    t=finite(horizon,"horizon")
    if t<0:
        raise ValueError("horizon must be nonnegative")
    if c==0 or t==0:
        return 0.0
    x=-d*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    result=c*t if d==0 else c*(-math.expm1(x))/d
    if not math.isfinite(result):
        raise ValueError("nonfinite PV")
    return result

def perpetuity_pv(payment,growth,discount):
    c,d=inputs(payment,growth,discount)
    if c==0:
        return 0.0
    if d<=0:
        raise ValueError("nonzero exponential perpetuity diverges: require discount > growth")
    result=c/d
    if not math.isfinite(result):
        raise ValueError("nonfinite perpetuity")
    return result

def tail_value(payment,growth,discount,horizon):
    c,d=inputs(payment,growth,discount)
    t=finite(horizon,"horizon")
    if t<0:
        raise ValueError("horizon must be nonnegative")
    if c==0:
        return 0.0
    if d<=0:
        raise ValueError("tail requires a convergent perpetuity")
    result=(c/d)*math.exp(-d*t)
    if not math.isfinite(result):
        raise ValueError("nonfinite tail")
    return result

def horizon_for_tail_fraction(growth,discount,fraction):
    _,d=inputs(1.0,growth,discount)
    f=finite(fraction,"fraction")
    if d<=0:
        raise ValueError("require discount > growth")
    if not 0<f<1:
        raise ValueError("fraction must be between 0 and 1")
    result=-math.log(f)/d
    if not math.isfinite(result):
        raise ValueError("nonfinite target horizon")
    return result

def p_integral_from_one(p):
    power=finite(p,"p")
    if power<=1:
        raise ValueError("integral diverges for p <= 1")
    return 1/(power-1)

def assessment():
    rows=[]
    for growth in (0,0.02,0.04,0.049,0.05):
        converges=growth<0.05
        row={"growth":growth,"discount":0.05,"converges":converges,
             "finite_horizons":{str(t):finite_horizon_pv(1000,growth,0.05,t)
                                for t in (10,30,100)}}
        if converges:
            row["perpetuity"]=perpetuity_pv(1000,growth,0.05)
            row["tail_at_100"]=tail_value(1000,growth,0.05,100)
            row["one_percent_tail_horizon"]=horizon_for_tail_fraction(growth,0.05,0.01)
        rows.append(row)
    return {"scenarios":rows,"runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
