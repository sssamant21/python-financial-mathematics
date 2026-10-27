"""Book 02 Section 17.1: feasible sets and portfolio constraints."""
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        value=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value

def variance(w1,w2):
    a,b=finite(w1,"w1"),finite(w2,"w2")
    return finite(0.04*a*a+0.02*a*b+0.09*b*b,"variance")

def feasibility(w1,w2,cap1=1.0,cap2=1.0,tolerance=1e-10):
    a,b=finite(w1,"w1"),finite(w2,"w2")
    u,v=finite(cap1,"cap1"),finite(cap2,"cap2")
    tol=finite(tolerance,"tolerance")
    if not 0<=u<=1 or not 0<=v<=1 or tol<0:
        raise ValueError("caps must be in [0,1] and tolerance nonnegative")
    equality=a+b-1
    inequalities={"w1_lower":-a,"w2_lower":-b,
                  "w1_cap":a-u,"w2_cap":b-v}
    violation=max([0.0]+[max(0.0,g) for g in inequalities.values()])
    return {"weights":[a,b],"equality_residual":equality,
            "inequality_residuals":inequalities,
            "maximum_inequality_violation":violation,
            "feasible":abs(equality)<=tol and violation<=tol,
            "active_inequalities":[name for name,g in inequalities.items()
                                   if abs(g)<=tol],
            "variance":variance(a,b)}

def minimum_variance_full_investment(cap1=1.0,cap2=1.0):
    u,v=finite(cap1,"cap1"),finite(cap2,"cap2")
    if not 0<=u<=1 or not 0<=v<=1:
        raise ValueError("caps must be in [0,1]")
    lower=max(0.0,1.0-v)
    upper=min(1.0,u)
    if lower>upper:
        raise ValueError("infeasible full-investment caps")
    unconstrained_on_line=8/11
    a=min(upper,max(lower,unconstrained_on_line))
    return {"w1":a,"w2":1-a,"variance":variance(a,1-a),
            "feasibility":feasibility(a,1-a,u,v)}

def assessment():
    return {"full_investment":minimum_variance_full_investment(),
            "capped":minimum_variance_full_investment(0.6,1),
            "example":feasibility(0.6,0.4,0.6,1),
            "infeasible_example":feasibility(0.8,0.2,0.6,1),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
