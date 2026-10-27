"""Book 02 Section 17.3: KKT certificate for capped portfolio."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric and not boolean")
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

def portfolio(cap=0.6):
    u=finite(cap,"cap")
    if not 0<=u<=1:
        raise ValueError("cap must be in [0,1]")
    if u<0:
        raise ValueError("infeasible cap")
    w1=min(u,8/11)
    w2=1-w1
    grad1=2*(0.04*w1+0.01*w2)
    grad2=2*(0.01*w1+0.09*w2)
    lam=-grad2
    mu_cap=max(0.0,grad2-grad1) if w1>=u else 0.0
    return {"weights":(w1,w2),"variance":variance(w1,w2),
            "lambda":lam,"multipliers":(0.0,0.0,mu_cap),"cap":u}

def kkt_report(weights,lam,multipliers,cap=0.6,tolerance=1e-9):
    if not isinstance(weights,(tuple,list)) or len(weights)!=2:
        raise ValueError("two weights required")
    if not isinstance(multipliers,(tuple,list)) or len(multipliers)!=3:
        raise ValueError("three inequality multipliers required")
    x,y=(finite(v,"weight") for v in weights)
    lam=finite(lam,"lambda")
    m=tuple(finite(v,"multiplier") for v in multipliers)
    u=finite(cap,"cap")
    tol=finite(tolerance,"tolerance")
    if not 0<=u<=1 or tol<0:
        raise ValueError("invalid cap or tolerance")
    g=(-x,-y,x-u)
    stationarity=(2*(0.04*x+0.01*y)+lam-m[0]+m[2],
                  2*(0.01*x+0.09*y)+lam-m[1])
    complementary=tuple(a*b for a,b in zip(m,g))
    equality=x+y-1
    return {"equality_residual":equality,"inequality_residuals":g,
            "dual_multipliers":m,"stationarity":stationarity,
            "complementarity":complementary,
            "passes":abs(equality)<=tol and all(v<=tol for v in g)
            and all(v>=-tol for v in m)
            and all(abs(v)<=tol for v in stationarity)
            and all(abs(v)<=tol for v in complementary)}

def scalar_example():
    x=0.6
    mu_lower=0.0
    mu_upper=0.4
    return {"x":x,"objective":(x-0.8)**2,
            "multipliers":(mu_lower,mu_upper),
            "stationarity":2*(x-0.8)-mu_lower+mu_upper}

def assessment():
    solution=portfolio()
    return {"solution":solution,
            "kkt":kkt_report(solution["weights"],solution["lambda"],
                             solution["multipliers"],solution["cap"]),
            "scalar":scalar_example(),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
