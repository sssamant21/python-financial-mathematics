"""Book 02 Section 16.9: deterministic calibration optimizer project."""
import json
import math
from fractions import Fraction
from section_16_08 import _rounded_calibration
from section_16_08 import metrics as checked_metrics

TRAIN=((1.0,1050.0),(2.0,1100.0),(3.0,1150.0))
HOLDOUT=((4.0,1201.0),)
STARTS=(-0.10,0.0,0.10)

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

def validate_rows(rows):
    if not isinstance(rows,(list,tuple)) or not rows:
        raise ValueError("observations must be nonempty")
    out=[]
    for row in rows:
        if not isinstance(row,(tuple,list)) or len(row)!=2:
            raise ValueError("observation requires time and price")
        t,y=finite(row[0],"time"),finite(row[1],"price")
        if t<=0:
            raise ValueError("time must be positive")
        out.append((t,y))
    return tuple(out)

def price(rate,time):
    r,t=finite(rate,"rate"),finite(time,"time")
    if t<=0:
        raise ValueError("time must be positive")
    return finite(1000*(1+t*r),"price")

def normalized_residuals(rate,rows=TRAIN):
    return tuple(finite((price(rate,t)-y)/1000,"normalized residual")
                 for t,y in validate_rows(rows))

def objective(rate,rows=TRAIN):
    e=normalized_residuals(rate,rows)
    return finite(0.5*sum(v*v for v in e),"objective")

def gradient(rate,rows=TRAIN):
    data=validate_rows(rows)
    e=normalized_residuals(rate,data)
    return _rounded_calibration(sum(Fraction(t)*Fraction(v) for (t,_),v in zip(data,e)),"gradient")

def curvature(rows=TRAIN):
    return _rounded_calibration(sum(Fraction(t)**2 for t,_ in validate_rows(rows)),"curvature")

def analytical_rate(rows=TRAIN):
    data=validate_rows(rows)
    denominator=sum(Fraction(t)**2 for t,_ in data)
    numerator=sum(Fraction(t)*(Fraction(y)-1000)/1000 for t,y in data)
    return _rounded_calibration(numerator/denominator,"analytical rate")

def optimize(start,method="gradient_descent",step=0.05,
             tolerance=1e-9,max_iterations=100):
    x=finite(start,"start")
    alpha=finite(step,"step")
    tol=finite(tolerance,"tolerance")
    if method not in ("gradient_descent","newton"):
        raise ValueError("unsupported method")
    if alpha<=0 or tol<0:
        raise ValueError("invalid step or tolerance")
    if type(max_iterations) is not int or not 1<=max_iterations<=100000:
        raise ValueError("invalid iteration budget")
    h=curvature()
    history=[]
    status="max_iterations"
    for k in range(max_iterations+1):
        g=gradient(x)
        f=objective(x)
        history.append({"iteration":k,"rate":x,"loss":f,"gradient":g})
        if abs(g)<=tol:
            status="gradient_tolerance"
            break
        if k==max_iterations:
            break
        direction=-alpha*g if method=="gradient_descent" else -g/h
        x=finite(x+direction,"updated rate")
    return {"method":method,"start":float(start),"rate":x,
            "loss":history[-1]["loss"],"gradient":history[-1]["gradient"],
            "iterations":len(history)-1,"status":status,
            "history":history,"runtime_certified":False}

def price_metrics(rate,rows):
    e=tuple(finite(price(rate,t)-y,"price residual")
            for t,y in validate_rows(rows))
    return {"residuals":e,**checked_metrics(e)}

def assessment():
    benchmark=analytical_rate()
    runs=[optimize(start,method) for method in
          ("gradient_descent","newton") for start in STARTS]
    for run in runs:
        candidate=run["rate"]
        run["training"]=price_metrics(candidate,TRAIN)
        run["holdout"]=price_metrics(candidate,HOLDOUT)
        run["recomputed_loss"]=objective(candidate,TRAIN)
        run["recomputed_gradient"]=gradient(candidate,TRAIN)
        run["provisional_acceptance"]=(
            run["status"]=="gradient_tolerance" and
            abs(candidate-benchmark)<=1e-8 and
            abs(run["gradient"])<=1e-8 and
            abs(run["recomputed_gradient"])<=1e-8 and
            run["training"]["mae"]<=1e-5 and
            run["training"]["rmse"]<=1e-5 and
            all(abs(residual+1)<=1e-5 for residual in run["holdout"]["residuals"]))
    train=price_metrics(benchmark,TRAIN)
    holdout=price_metrics(benchmark,HOLDOUT)
    accepted=all(run["provisional_acceptance"] for run in runs)
    accepted=accepted and train["mae"]<=1e-5 and train["rmse"]<=1e-5
    accepted=accepted and abs(holdout["residuals"][0]+1)<=1e-5
    return {"analytical_rate":benchmark,"curvature":curvature(),
            "runs":runs,"training":train,"holdout":holdout,
            "provisional_acceptance":accepted,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
