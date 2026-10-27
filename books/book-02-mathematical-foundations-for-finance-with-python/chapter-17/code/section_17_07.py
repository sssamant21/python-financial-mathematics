"""Book 02 Section 17.7: financial allocation assumption audit."""
import json
import math

SIGMA=((0.04,0.01),(0.01,0.09))
EXPECTED_RETURNS=(0.08,0.05)

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

def covariance_valid(matrix=SIGMA):
    if not isinstance(matrix,(tuple,list)) or len(matrix)!=2 or any(
        not isinstance(row,(tuple,list)) or len(row)!=2 for row in matrix
    ):
        raise ValueError("2x2 covariance required")
    a,b=finite(matrix[0][0],"sigma11"),finite(matrix[0][1],"sigma12")
    c,d=finite(matrix[1][0],"sigma21"),finite(matrix[1][1],"sigma22")
    return abs(b-c)<=1e-12 and a>=0 and d>=0 and a*d-b*c>=-1e-12

def variance(weights):
    x,y=weights
    x,y=finite(x,"w1"),finite(y,"w2")
    return finite(0.04*x*x+0.02*x*y+0.09*y*y,"variance")

def allocation(cap1=0.6,cap2=1.0):
    u,v=finite(cap1,"cap1"),finite(cap2,"cap2")
    if not 0<=u<=1 or not 0<=v<=1 or u+v<1:
        raise ValueError("invalid or infeasible position caps")
    lower=max(0.0,1-v)
    upper=min(1.0,u)
    x=min(upper,max(lower,8/11))
    y=1-x
    return {"weights":(x,y),"variance":variance((x,y)),
            "expected_return":0.08*x+0.05*y,
            "caps":(u,v),"feasible":x>=0 and y>=0 and x<=u and y<=v
            and abs(x+y-1)<1e-12}

def trade_report(target=(0.6,0.4),current=(0.5,0.5),
                 capital=1000000.0,cost_bps=10.0):
    if len(target)!=2 or len(current)!=2:
        raise ValueError("two-asset weights required")
    t=tuple(finite(x,"target weight") for x in target)
    c=tuple(finite(x,"current weight") for x in current)
    cash=finite(capital,"capital")
    bps=finite(cost_bps,"cost_bps")
    if cash<=0 or bps<0 or any(x<0 for x in t+c):
        raise ValueError("invalid capital, cost, or weights")
    if abs(sum(t)-1)>1e-10 or abs(sum(c)-1)>1e-10:
        raise ValueError("target and current weights must sum to one")
    trades=tuple(cash*(a-b) for a,b in zip(t,c))
    gross=sum(abs(x) for x in trades)
    return {"signed_trades":trades,"gross_turnover":gross/cash,
            "gross_traded_notional":gross,"modeled_cost":gross*bps/10000}

def assessment():
    p=allocation()
    return {"covariance_valid":covariance_valid(),
            "allocation":p,"trades":trade_report(p["weights"]),
            "assumptions":{"return_horizon":"annual",
                           "cost_convention":"bps of gross traded notional",
                           "taxes_included":False,"market_impact_included":False},
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
