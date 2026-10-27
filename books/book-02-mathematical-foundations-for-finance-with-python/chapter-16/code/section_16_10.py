"""Book 02 Section 16.10: chapter-wide applied optimization lab."""
import json
import math

TRAIN=((1.0,1050.0),(2.0,1100.0),(3.0,1150.0))
HOLDOUT=((4.0,1201.0),)

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric and not boolean")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def model_price(rate,time):
    r,t=finite(rate,"rate"),finite(time,"time")
    if t<=0:
        raise ValueError("time must be positive")
    return finite(1000*(1+t*r),"price")

def validate(rows):
    if not isinstance(rows,(tuple,list)) or not rows:
        raise ValueError("nonempty observations required")
    out=[]
    for row in rows:
        if not isinstance(row,(tuple,list)) or len(row)!=2:
            raise ValueError("observation must contain time and price")
        t,p=finite(row[0],"time"),finite(row[1],"observed price")
        if t<=0:
            raise ValueError("time must be positive")
        out.append((t,p))
    return tuple(out)

def residuals(rate,rows):
    return tuple(finite(model_price(rate,t)-p,"residual") for t,p in validate(rows))

def loss(rate,rows=TRAIN):
    data=validate(rows)
    return finite(0.5*sum((v/1000)**2 for v in residuals(rate,data)),"loss")

def gradient(rate,rows=TRAIN):
    data=validate(rows)
    return finite(sum(t*v/1000 for (t,_),v in zip(data,residuals(rate,data))),"gradient")

def hessian(rows=TRAIN):
    return finite(sum(t*t for t,_ in validate(rows)),"hessian")

def analytical_rate(rows=TRAIN):
    data=validate(rows)
    return finite(sum(t*(p-1000)/1000 for t,p in data)/hessian(data),"rate")

def solve(start,method="newton",step=0.05,tol=1e-9,max_iterations=100):
    x=finite(start,"start")
    alpha=finite(step,"step")
    tolerance=finite(tol,"tolerance")
    if method not in ("newton","gradient_descent"):
        raise ValueError("unsupported method")
    if alpha<=0 or tolerance<0 or type(max_iterations) is not int or not 1<=max_iterations<=100000:
        raise ValueError("invalid solver controls")
    status="max_iterations"
    for k in range(max_iterations+1):
        g=gradient(x)
        if abs(g)<=tolerance:
            status="gradient_tolerance"
            break
        if k==max_iterations:
            break
        direction=-g/hessian() if method=="newton" else -alpha*g
        x=finite(x+direction,"updated rate")
    return {"method":method,"start":float(start),"rate":x,"loss":loss(x),
            "gradient":gradient(x),"iterations":k,"status":status}

def metrics(errors):
    if not isinstance(errors,(tuple,list)) or not errors:
        raise ValueError("nonempty residuals required")
    e=tuple(finite(v,"residual") for v in errors)
    return {"mae":sum(abs(v) for v in e)/len(e),
            "rmse":math.sqrt(sum(v*v for v in e)/len(e)),
            "bias":sum(e)/len(e),"max_abs":max(abs(v) for v in e)}

def portfolio_variance(w1,w2):
    x,y=finite(w1,"w1"),finite(w2,"w2")
    return finite(0.04*x*x+0.02*x*y+0.09*y*y,"portfolio variance")

def assessment():
    reference=analytical_rate()
    runs=[solve(start,method) for method in ("newton","gradient_descent")
          for start in (-0.1,0.0,0.1)]
    return {"analytical_rate":reference,"gradient_at_reference":gradient(reference),
            "hessian":hessian(),"runs":runs,
            "training_metrics":metrics(residuals(reference,TRAIN)),
            "holdout_metrics":metrics(residuals(reference,HOLDOUT)),
            "portfolio_variance":portfolio_variance(0.6,0.4),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
