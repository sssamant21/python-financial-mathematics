"""Book 02 Section 16.1: objectives and decision variables."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def model_price(rate):
    r=finite(rate,"rate")
    return finite(1000*(1+2*r),"model price")

def residual(rate,target=1100):
    return finite(model_price(rate)-finite(target,"target"),"residual")

def loss(rate,target=1100):
    e=residual(rate,target)
    return finite(e*e,"squared residual")

def gradient(rate,target=1100):
    r=finite(rate,"rate")
    y=finite(target,"target")
    return finite(4000*(1000*(1+2*r)-y),"loss gradient")

def hessian():
    return 8_000_000.0

def analytic_minimizer(target=1100):
    y=finite(target,"target")
    return finite((y/1000-1)/2,"optimal rate")

def weighted_loss(parameters,targets,weights):
    if not all(isinstance(a,(list,tuple)) for a in (parameters,targets,weights)):
        raise TypeError("parameters, targets and weights must be sequences")
    if len(parameters)==0 or len(parameters)!=len(targets) or len(targets)!=len(weights):
        raise ValueError("sequences must be nonempty and have equal lengths")
    terms=[]
    for p,y,w in zip(parameters,targets,weights):
        e=residual(p,y)
        weight=finite(w,"weight")
        if weight<=0:
            raise ValueError("weights must be positive")
        terms.append(finite(weight*e*e,"weighted residual"))
    return finite(math.fsum(terms),"weighted loss")

def two_variable_objective(x,y,a,b):
    x,y,a,b=(finite(v,"quadratic input") for v in (x,y,a,b))
    return finite(2*(x-a)**2+3*(y-b)**2,"quadratic objective")

def assessment():
    optimum=analytic_minimizer()
    return {
        "decision_variable":"rate",
        "target":1100,
        "optimal_rate":optimum,
        "optimal_loss":loss(optimum),
        "loss_at_004":loss(0.04),
        "loss_at_006":loss(0.06),
        "gradient_at_optimum":gradient(optimum),
        "hessian":hessian(),
        "two_variable_optimum":(2.0,3.0),
        "two_variable_optimal_loss":two_variable_objective(2,3,2,3),
        "weighted_reference_loss":weighted_loss((0.04,0.06),(1100,1100),(1,2)),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
