"""Book 02 Section 16.8: residual-based calibration validation."""
import json
import math
from fractions import Fraction

TRAINING=((1.0,1050.0),(2.0,1100.0),(3.0,1150.0))
HOLDOUT=((4.0,1201.0),)

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric and not boolean")
    try:
        v=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def observations(rows):
    if not isinstance(rows,(list,tuple)) or not rows:
        raise ValueError("observations must be a nonempty sequence")
    clean=[]
    for row in rows:
        if not isinstance(row,(list,tuple)) or len(row)!=2:
            raise ValueError("each observation must have time and price")
        t,y=finite(row[0],"time"),finite(row[1],"price")
        if t<=0:
            raise ValueError("time must be positive")
        clean.append((t,y))
    return tuple(clean)

def price(rate,time):
    r,t=finite(rate,"rate"),finite(time,"time")
    if t<=0:
        raise ValueError("time must be positive")
    return finite(1000*(1+t*r),"model price")

def residuals(rate,rows):
    return tuple(finite(price(rate,t)-y,"residual")
                 for t,y in observations(rows))

def metrics(errors):
    if not isinstance(errors,(tuple,list)) or not errors:
        raise ValueError("errors must be a nonempty sequence")
    e=tuple(finite(v,"residual") for v in errors)
    n=len(e)
    exact=tuple(Fraction(v) for v in e)
    scale=max(abs(v) for v in e)
    # Normalize before squaring; the norm itself may exceed float range even
    # though the root-mean-square is finite. Means use exact represented sums
    # to preserve cancellation and avoid overflowing an intermediate total.
    rms=0.0 if scale==0 else scale*math.sqrt(math.fsum((v/scale)**2 for v in e)/n)
    return {"mae":finite(float(sum(map(abs,exact))/n),"mae"),
            "rmse":finite(rms,"rmse"),
            "bias":finite(float(sum(exact)/n),"bias"),
            "max_abs":scale}

def weighted_loss(rate,rows,weights):
    data=observations(rows)
    if not isinstance(weights,(list,tuple)) or len(weights)!=len(data):
        raise ValueError("weights must match observations")
    w=tuple(finite(v,"weight") for v in weights)
    if any(v<0 for v in w) or not any(v>0 for v in w):
        raise ValueError("weights must be nonnegative with positive total")
    e=residuals(rate,data)
    return finite(0.5*sum(a*b*b for a,b in zip(w,e)),"weighted loss")

def fit_rate(rows):
    data=observations(rows)
    denominator=sum((1000*t)**2 for t,_ in data)
    numerator=sum(1000*t*(y-1000) for t,y in data)
    if denominator<=0 or not math.isfinite(denominator):
        raise ValueError("invalid calibration sensitivity")
    return finite(numerator/denominator,"fitted rate")

def gradient(rate,rows):
    return finite(sum(1000*t*e for (t,_),e in
                      zip(observations(rows),residuals(rate,rows))),"gradient")

def curvature(rows):
    return finite(sum((1000*t)**2 for t,_ in observations(rows)),"curvature")

def assessment():
    rate=fit_rate(TRAINING)
    train_errors=residuals(rate,TRAINING)
    holdout_errors=residuals(rate,HOLDOUT)
    return {"fitted_rate":rate,
            "training_residuals":train_errors,
            "training_metrics":metrics(train_errors),
            "holdout_residuals":holdout_errors,
            "holdout_metrics":metrics(holdout_errors),
            "gradient":gradient(rate,TRAINING),
            "curvature":curvature(TRAINING),
            "weighted_loss":weighted_loss(rate,TRAINING,(1,2,1)),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
