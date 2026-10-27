"""Book 02 Section 16.7: scaling and deterministic local multistart."""
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

def raw_quadratic(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite(0.5*(1e6*(x-0.02)**2+(y-3)**2),"raw objective")

def scaled_quadratic(u,v):
    u,v=finite(u,"u"),finite(v,"v")
    return finite(0.5*(u*u+v*v),"scaled objective")

def to_scaled(x,y):
    return (finite(1000*(finite(x,"x")-0.02),"u"),
            finite(finite(y,"y")-3,"v"))

def to_raw(u,v):
    return (finite(0.02+finite(u,"u")/1000,"x"),
            finite(3+finite(v,"v"),"y"))

def double_well(x):
    x=finite(x,"x")
    return finite((x*x-1)**2+0.2*x,"double-well objective")

def double_well_gradient(x):
    x=finite(x,"x")
    return finite(4*x*(x*x-1)+0.2,"double-well gradient")

def local_descent(start,step=0.05,tolerance=1e-9,max_iterations=2000):
    x=finite(start,"start")
    alpha=finite(step,"step")
    tol=finite(tolerance,"tolerance")
    if alpha<=0 or tol<0:
        raise ValueError("step must be positive and tolerance nonnegative")
    if type(max_iterations) is not int or not 1<=max_iterations<=100000:
        raise ValueError("invalid iteration budget")
    status="max_iterations"
    for k in range(max_iterations+1):
        g=double_well_gradient(x)
        if abs(g)<=tol:
            status="gradient_tolerance"
            break
        if k==max_iterations:
            break
        trial=finite(x-alpha*g,"trial point")
        if double_well(trial)>double_well(x):
            status="no_descent"
            break
        x=trial
    return {"start":float(start),"x":x,"objective":double_well(x),
            "gradient":double_well_gradient(x),"iterations":k,
            "status":status,"runtime_certified":False}

def multistart(starts=(-1.5,-0.5,0.5,1.5)):
    if not isinstance(starts,(tuple,list)) or not starts:
        raise ValueError("starts must be a nonempty sequence")
    runs=[local_descent(s) for s in starts]
    successful=[run for run in runs if run["status"]=="gradient_tolerance"]
    best=min(successful,key=lambda run:run["objective"]) if successful else None
    return {"runs":runs,"best_observed":best,
            "global_optimality_certified":False}

def assessment():
    u,v=to_scaled(0.021,4)
    return {"raw_loss":raw_quadratic(0.021,4),
            "scaled_loss":scaled_quadratic(u,v),
            "scaled_parameters":(u,v),
            "round_trip":to_raw(u,v),
            "raw_condition_number":1_000_000,
            "scaled_condition_number":1,
            "multistart":multistart(),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
