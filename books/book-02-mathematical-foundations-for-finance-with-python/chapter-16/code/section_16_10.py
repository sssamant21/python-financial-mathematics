"""Book 02 Section 16.10: chapter-wide applied optimization lab."""
import json
import math
from fractions import Fraction
from section_16_08 import _rounded_calibration
from section_16_08 import metrics as checked_metrics

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
    return _rounded_calibration(sum(Fraction(v)**2 for v in residuals(rate,data))/2_000_000,"loss")

def gradient(rate,rows=TRAIN):
    data=validate(rows)
    return _rounded_calibration(sum(Fraction(t)*Fraction(v)/1000 for (t,_),v in zip(data,residuals(rate,data))),"gradient")

def hessian(rows=TRAIN):
    return _rounded_calibration(sum(Fraction(t)**2 for t,_ in validate(rows)),"hessian")

def analytical_rate(rows=TRAIN):
    data=validate(rows)
    denominator=sum(Fraction(t)**2 for t,_ in data)
    numerator=sum(Fraction(t)*(Fraction(y)-1000)/1000 for t,y in data)
    return _rounded_calibration(numerator/denominator,"analytical rate")

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
    return checked_metrics(errors)

def portfolio_variance(w1,w2):
    x,y=finite(w1,"w1"),finite(w2,"w2")
    return finite(0.04*x*x+0.02*x*y+0.09*y*y,"portfolio variance")

def exercise_objectives():
    """Compute the exact exercise scopes, separate from the aggregate model."""
    from section_16_05 import gradient_descent,quadratic_loss,quadratic_gradient
    from section_16_06 import newton_solve
    single=((2.0,1100.0),)
    stationary=analytical_rate(single)
    shifted_loss=lambda x:quadratic_loss(x,a=1.0,b=3.0)
    shifted_gradient=lambda x:quadratic_gradient(x,a=1.0,b=3.0)
    return {
        "single_observation":{
            "rows":single,"stationary_rate":stationary,
            "curvature":hessian(single),
            "stationary_loss":loss(stationary,single),
            "stationary_gradient":gradient(stationary,single),
            "evaluations":[{"rate":r,"loss":loss(r,single),
                            "gradient":gradient(r,single)}
                           for r in (-0.125,0.0,0.125,0.25)],
        },
        "shifted_quadratic":{
            "curvature":1.0,"center":3.0,
            "gradient_descent":[{
                "step":step,"result":gradient_descent(
                    0.0,shifted_loss,shifted_gradient,step=step,
                    tolerance=0.0,max_iterations=2)}
                for step in (0.5,1.0,2.0,3.0)],
            "newton":newton_solve(0.0,shifted_gradient,lambda x:1.0,
                                  tolerance=0.0,max_iterations=1),
        },
        "three_observation_curvature":hessian(),
    }

def assessment():
    reference=analytical_rate()
    runs=[solve(start,method) for method in ("newton","gradient_descent")
          for start in (-0.1,0.0,0.1)]
    limits={"rate_abs":1e-8,"gradient_abs":1e-8,"loss_consistency_abs":1e-12,
            "training_mae":1e-5,"training_rmse":1e-5,"holdout_max_abs":1.01}
    for run in runs:
        candidate=finite(run["rate"],"candidate rate")
        train_errors=residuals(candidate,TRAIN)
        holdout_errors=residuals(candidate,HOLDOUT)
        run["training_residuals"]=train_errors
        run["holdout_residuals"]=holdout_errors
        run["training_metrics"]=metrics(train_errors)
        run["holdout_metrics"]=metrics(holdout_errors)
        run["recomputed_loss"]=loss(candidate,TRAIN)
        run["recomputed_gradient"]=gradient(candidate,TRAIN)
        reported_gradient=finite(run["gradient"],"reported gradient")
        reported_loss=finite(run["loss"],"reported loss")
        run["acceptance_checks"]={
            "status":run["status"]=="gradient_tolerance",
            "rate_error":abs(candidate-reference)<=limits["rate_abs"],
            "solver_gradient":abs(reported_gradient)<=limits["gradient_abs"],
            "recomputed_gradient":abs(run["recomputed_gradient"])<=limits["gradient_abs"],
            "reported_loss_consistency":abs(reported_loss-run["recomputed_loss"])<=limits["loss_consistency_abs"],
            "training_mae":run["training_metrics"]["mae"]<=limits["training_mae"],
            "training_rmse":run["training_metrics"]["rmse"]<=limits["training_rmse"],
            "holdout_max_abs":run["holdout_metrics"]["max_abs"]<=limits["holdout_max_abs"],
        }
        run["provisional_acceptance"]=all(run["acceptance_checks"].values())
    return {"analytical_rate":reference,"gradient_at_reference":gradient(reference),
            "hessian":hessian(),"runs":runs,
            "exercise_objectives":exercise_objectives(),
            "acceptance_limits":limits,
            "acceptance_scope":"synthetic_numerical_only",
            "provisional_acceptance":all(run["provisional_acceptance"] for run in runs),
            "benchmark_metric_rate":reference,
            "training_metrics":metrics(residuals(reference,TRAIN)),
            "holdout_metrics":metrics(residuals(reference,HOLDOUT)),
            "portfolio_variance":portfolio_variance(0.6,0.4),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
