"""Book 02 Section 17.8: independent two-asset KKT certificate."""
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

def verify(weights,lam,multipliers,cap=0.6,tolerance=1e-9):
    if not isinstance(weights,(tuple,list)) or len(weights)!=2:
        raise ValueError("two weights required")
    if not isinstance(multipliers,(tuple,list)) or len(multipliers)!=3:
        raise ValueError("three multipliers required")
    x,y=(finite(v,"weight") for v in weights)
    lam=finite(lam,"lambda")
    m=tuple(finite(v,"multiplier") for v in multipliers)
    u=finite(cap,"cap")
    tol=finite(tolerance,"tolerance")
    if tol<0 or not 0<=u<=1:
        raise ValueError("invalid cap or tolerance")
    objective=0.04*x*x+0.02*x*y+0.09*y*y
    grad=(0.08*x+0.02*y,0.02*x+0.18*y)
    equality=x+y-1
    inequalities=(-x,-y,x-u)
    stationarity=(grad[0]+lam-m[0]+m[2],grad[1]+lam-m[1])
    products=tuple(a*b for a,b in zip(m,inequalities))
    primal_violation=max(abs(equality),*(max(0,v) for v in inequalities))
    dual_violation=max(0,*(-v for v in m))
    stationarity_norm=max(abs(v) for v in stationarity)
    complementarity_norm=max(abs(v) for v in products)
    convex_hessian_certified=(0.08>0 and 0.08*0.18-0.02**2>0)
    passes=(primal_violation<=tol and dual_violation<=tol
            and stationarity_norm<=tol and complementarity_norm<=tol
            and convex_hessian_certified)
    return {"weights":(x,y),"objective":objective,
            "gradient":grad,"equality_residual":equality,
            "inequality_residuals":inequalities,
            "stationarity":stationarity,"complementarity":products,
            "primal_violation":primal_violation,
            "dual_violation":dual_violation,
            "stationarity_norm":stationarity_norm,
            "complementarity_norm":complementarity_norm,
            "convex_hessian_certified":convex_hessian_certified,
            "passes":passes}

def assessment():
    return {"valid":verify((0.6,0.4),-0.084,(0,0,0.028)),
            "cap_violation":verify((0.7,0.3),-0.084,(0,0,0.028)),
            "nonstationary":verify((0.5,0.5),0,(0,0,0)),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
