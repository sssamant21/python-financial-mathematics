"""Book 02 Section 17.6: two-asset convex quadratic programming lab."""
import json
import math

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

SIGMA=((0.04,0.01),(0.01,0.09))
Q=((0.08,0.02),(0.02,0.18))

def variance(w1,w2):
    x,y=finite(w1,"w1"),finite(w2,"w2")
    return finite(0.04*x*x+0.02*x*y+0.09*y*y,"variance")

def gradient(w1,w2):
    x,y=finite(w1,"w1"),finite(w2,"w2")
    return (finite(0.08*x+0.02*y,"gradient1"),
            finite(0.02*x+0.18*y,"gradient2"))

def positive_definite():
    return Q[0][0]>0 and Q[0][0]*Q[1][1]-Q[0][1]*Q[1][0]>0

def solve(cap=0.6):
    u=finite(cap,"cap")
    if not 0<=u<=1:
        raise ValueError("cap must lie in [0,1]")
    x=min(u,8/11)
    y=1-x
    grad=gradient(x,y)
    lam=-grad[1]
    mu_cap=max(0.0,grad[1]-grad[0]) if x>=u else 0.0
    return {"cap":u,"weights":(x,y),"variance":variance(x,y),
            "gradient":grad,"lambda":lam,
            "multipliers":(0.0,0.0,mu_cap)}

def kkt_report(solution,tolerance=1e-9):
    tol=finite(tolerance,"tolerance")
    if tol<0:
        raise ValueError("tolerance must be nonnegative")
    x,y=solution["weights"]
    u=solution["cap"]
    lam=solution["lambda"]
    m=solution["multipliers"]
    g=(-x,-y,x-u)
    grad=gradient(x,y)
    stationarity=(grad[0]+lam-m[0]+m[2],
                  grad[1]+lam-m[1])
    products=tuple(v*z for v,z in zip(m,g))
    equality=x+y-1
    return {"equality_residual":equality,"inequalities":g,
            "stationarity":stationarity,"complementarity":products,
            "passes":abs(equality)<=tol and all(z<=tol for z in g)
            and all(v>=-tol for v in m)
            and all(abs(z)<=tol for z in stationarity)
            and all(abs(z)<=tol for z in products)}

def assessment():
    solution=solve()
    return {"covariance":SIGMA,"canonical_hessian":Q,
            "positive_definite":positive_definite(),
            "solution":solution,"kkt":kkt_report(solution),
            "benchmark":solve(1.0),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
