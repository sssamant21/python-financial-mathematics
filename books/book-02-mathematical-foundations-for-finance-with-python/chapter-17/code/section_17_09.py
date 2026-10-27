"""Book 02 Section 17.9: auditable two-asset allocation decision engine."""
import json
import math

SIGMA=((0.04,0.01),(0.01,0.09))
RETURNS=(0.08,0.05)
BASELINE=8/11

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

def validate_caps(cap1,cap2):
    u,v=finite(cap1,"cap1"),finite(cap2,"cap2")
    if not (0<=u<=1 and 0<=v<=1) or u+v<1-1e-14:
        raise ValueError("infeasible or invalid asset caps")
    return u,v

def objective(weights):
    x,y=(finite(z,"weight") for z in weights)
    return 0.04*x*x+0.02*x*y+0.09*y*y

def gradient(weights):
    x,y=(finite(z,"weight") for z in weights)
    return (0.08*x+0.02*y,0.02*x+0.18*y)

def verify_candidate(weights,lam,multipliers,caps=(0.6,1.0),tol=1e-9):
    if len(weights)!=2 or len(multipliers)!=4 or len(caps)!=2:
        raise ValueError("expected two weights, four multipliers, and two caps")
    x,y=(finite(z,"weight") for z in weights)
    m=tuple(finite(z,"multiplier") for z in multipliers)
    lam=finite(lam,"lambda")
    u,v=validate_caps(*caps)
    tol=finite(tol,"tolerance")
    if tol<0:
        raise ValueError("negative tolerance")
    g=(-x,-y,x-u,y-v)
    grad=gradient((x,y))
    stat=(grad[0]+lam-m[0]+m[2],grad[1]+lam-m[1]+m[3])
    comp=tuple(a*b for a,b in zip(m,g))
    eq=x+y-1
    primal=max(abs(eq),*(max(0,z) for z in g))
    dual=max(0,*(-z for z in m))
    stationarity=max(abs(z) for z in stat)
    complementary=max(abs(z) for z in comp)
    return {"equality_residual":eq,"inequality_residuals":g,
            "stationarity":stat,"complementarity":comp,
            "primal_violation":primal,"dual_violation":dual,
            "stationarity_norm":stationarity,
            "complementarity_norm":complementary,
            "objective":objective((x,y)),
            "passes":max(primal,dual,stationarity,complementary)<=tol}

def optimize(cap1=0.6,cap2=1.0):
    u,v=validate_caps(cap1,cap2)
    lo=max(0.0,1-v)
    hi=min(1.0,u)
    if lo>hi+1e-14:
        raise ValueError("empty feasible interval")
    x=min(hi,max(lo,BASELINE))
    y=1-x
    a,b=gradient((x,y))
    # Choose lambda=-b, with all lower-bound multipliers zero.
    # An upper-cap multiplier on whichever asset is constrained
    # supplies the difference in gradient components.
    lam=-b
    mu1=mu2=mu3=mu4=0.0
    if x<BASELINE-1e-14:
        mu3=b-a
    elif x>BASELINE+1e-14:
        # The second-asset upper cap is active. With lambda=-a,
        # its multiplier is a-b.
        lam=-a
        mu4=a-b
    certificate=verify_candidate((x,y),lam,(mu1,mu2,mu3,mu4),(u,v))
    return {"caps":(u,v),"feasible_interval":(lo,hi),
            "weights":(x,y),"variance":objective((x,y)),
            "lambda":lam,"multipliers":(mu1,mu2,mu3,mu4),
            "certificate":certificate}

def financial_report(weights,current=(0.5,0.5),
                     capital=1000000.0,cost_bps=10.0):
    if len(weights)!=2 or len(current)!=2:
        raise ValueError("two-asset portfolio required")
    w=tuple(finite(z,"target weight") for z in weights)
    old=tuple(finite(z,"current weight") for z in current)
    capital=finite(capital,"capital")
    cost_bps=finite(cost_bps,"cost_bps")
    if capital<=0 or cost_bps<0 or any(z<0 for z in w+old):
        raise ValueError("invalid capital, cost, or weight")
    if abs(sum(w)-1)>1e-10 or abs(sum(old)-1)>1e-10:
        raise ValueError("weights must sum to one")
    trades=tuple(capital*(a-b) for a,b in zip(w,old))
    gross=sum(abs(z) for z in trades)
    return {"expected_return":sum(a*b for a,b in zip(w,RETURNS)),
            "signed_trades":trades,"gross_turnover":gross/capital,
            "gross_traded_notional":gross,
            "modeled_transaction_cost":gross*cost_bps/10000,
            "cost_convention":"bps of gross traded notional",
            "taxes_included":False,"market_impact_included":False}

def assessment():
    allocation=optimize()
    return {"allocation":allocation,
            "financial_report":financial_report(allocation["weights"]),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
