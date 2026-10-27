"""Book 02 Section 17.2: equality-constrained minimum-variance portfolio."""
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def variance(w1,w2):
    a,b=finite(w1,"w1"),finite(w2,"w2")
    return finite(0.04*a*a+0.02*a*b+0.09*b*b,"variance")

def optimal_portfolio(budget=1.0):
    b=finite(budget,"budget")
    w1,w2=(8/11)*b,(3/11)*b
    value=variance(w1,w2)
    multiplier=finite(-2*value/b,"multiplier") if b!=0 else 0.0
    return {"budget":b,"weights":(w1,w2),"variance":value,
            "multiplier":multiplier}

def residuals(w1,w2,multiplier,budget=1.0):
    a,c=finite(w1,"w1"),finite(w2,"w2")
    lam=finite(multiplier,"multiplier")
    b=finite(budget,"budget")
    return {"feasibility":finite(a+c-b,"feasibility"),
            "stationarity":(finite(2*(0.04*a+0.01*c)+lam,"stationarity1"),
                            finite(2*(0.01*a+0.09*c)+lam,"stationarity2"))}

def value_function(budget):
    b=finite(budget,"budget")
    return finite((7/220)*b*b,"optimal value")

def value_derivative(budget):
    b=finite(budget,"budget")
    return finite((7/110)*b,"value derivative")

def assessment():
    solution=optimal_portfolio()
    w1,w2=solution["weights"]
    return {"solution":solution,
            "residuals":residuals(w1,w2,solution["multiplier"]),
            "tangent_curvature":0.22,
            "value_derivative":value_derivative(1),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
