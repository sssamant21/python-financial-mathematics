"""Book 02 Section 17.10: Chapter 17 exercise and applied-problem lab."""
import json
import math

SIGMA=((0.04,0.01),(0.01,0.09))
TRANSITION=8/11

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

def portfolio(cap):
    u=finite(cap,"cap")
    if not 0<=u<=1:
        raise ValueError("cap must lie in [0,1]")
    x=min(u,TRANSITION)
    y=1-x
    grad=(0.08*x+0.02*y,0.02*x+0.18*y)
    lam=-grad[1]
    mu=max(0,grad[1]-grad[0]) if x>=u else 0.0
    g=(-x,-y,x-u)
    stat=(grad[0]+lam+mu,grad[1]+lam)
    objective=0.04*x*x+0.02*x*y+0.09*y*y
    return {"cap":u,"weights":(x,y),"variance":objective,
            "lambda":lam,"multipliers":(0.0,0.0,mu),
            "inequalities":g,"stationarity":stat,
            "complementarity":(0.0,0.0,mu*g[2]),
            "feasible":abs(x+y-1)<1e-9 and all(v<=1e-9 for v in g)}

def two_sided(cap1,cap2):
    a,b=finite(cap1,"cap1"),finite(cap2,"cap2")
    if not 0<=a<=1 or not 0<=b<=1 or a+b<1:
        raise ValueError("infeasible caps")
    lo=max(0,1-b)
    hi=min(1,a)
    x=min(hi,max(lo,TRANSITION))
    y=1-x
    return {"interval":(lo,hi),"weights":(x,y),
            "variance":0.04*x*x+0.02*x*y+0.09*y*y}

def linear_program_reference():
    vertices=((0,0),(5,0),(2,6),(0,8))
    scores=tuple(5*x+4*y for x,y in vertices)
    dual=(3,1)
    return {"vertices":vertices,"scores":scores,
            "optimal_point":vertices[scores.index(max(scores))],
            "primal_value":max(scores),
            "dual_multipliers":dual,
            "dual_value":8*dual[0]+10*dual[1]}

def financial_reference():
    x,y=0.6,0.4
    current=(0.5,0.5)
    capital=1000000
    gross=capital*(abs(x-current[0])+abs(y-current[1]))
    return {"expected_return":0.08*x+0.05*y,
            "gross_turnover":gross/capital,
            "gross_traded_notional":gross,
            "modeled_cost":gross*10/10000}

def assessment():
    return {"portfolio_regimes":[portfolio(u) for u in (0.4,0.6,TRANSITION,0.9)],
            "two_sided":two_sided(0.9,0.2),
            "linear_program":linear_program_reference(),
            "financial_report":financial_reference(),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
