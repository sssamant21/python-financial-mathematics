"""Book 02 Section 17.4: active-set regimes and complementarity."""
import json
import math
from fractions import Fraction

TRANSITION=8/11

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def variance(w1,w2):
    x,y=finite(w1,"w1"),finite(w2,"w2")
    return finite(0.04*x*x+0.02*x*y+0.09*y*y,"variance")

def optimal_portfolio(cap):
    u=finite(cap,"cap")
    if not 0<=u<=1:
        raise ValueError("cap must lie in [0,1]")
    exact_cap=Fraction(u)
    exact_x=min(exact_cap,Fraction(8,11))
    x,y=float(exact_x),float(1-exact_x)
    # Decimal-model rational dual formulas avoid subtracting near-equal
    # rounded gradient components at the cap transition.
    lam=float((8*exact_x-9)/50)
    mu=float(max(Fraction(0),(8-11*exact_x)/50))
    exact_regime=("degenerate_endpoint" if exact_cap==0 else
                  "binding" if exact_cap<Fraction(8,11) else "inactive")
    if u==0:
        regime="degenerate_endpoint"
    elif u<TRANSITION:
        regime="binding"
    elif u==TRANSITION:
        regime="weakly_active_transition"
    else:
        regime="inactive"
    return {"cap":u,"weights":(x,y),"variance":variance(x,y),
            "lambda":lam,"multipliers":(0.0,0.0,mu),"regime":regime,
            "exact_model_regime":exact_regime,
            "model_cap_active":exact_cap==exact_x,
            "model_cap_slack":float(exact_cap-exact_x),
            "regime_basis":"rounded_transition_display"}

def kkt_report(solution,tolerance=1e-9):
    tol=finite(tolerance,"tolerance")
    if tol<0:
        raise ValueError("tolerance must be nonnegative")
    x,y=solution["weights"]
    u=solution["cap"]
    lam=solution["lambda"]
    m=solution["multipliers"]
    g=(-x,-y,x-u)
    stationarity=(2*(0.04*x+0.01*y)+lam-m[0]+m[2],
                  2*(0.01*x+0.09*y)+lam-m[1])
    products=tuple(a*b for a,b in zip(m,g))
    equality=x+y-1
    return {"equality_residual":equality,"inequalities":g,
            "stationarity":stationarity,"complementarity":products,
            "active":[i for i,v in enumerate(g) if abs(v)<=tol],
            "passes":abs(equality)<=tol and all(v<=tol for v in g)
            and all(v>=-tol for v in m)
            and all(abs(v)<=tol for v in stationarity)
            and all(abs(v)<=tol for v in products)}

def value_function(cap):
    return optimal_portfolio(cap)["variance"]

def shadow_price(cap):
    return optimal_portfolio(cap)["multipliers"][2]

def assessment():
    cases=[]
    for u in (0.0,0.6,TRANSITION,0.9):
        s=optimal_portfolio(u)
        cases.append({"solution":s,"kkt":kkt_report(s)})
    return {"transition":TRANSITION,"cases":cases,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
