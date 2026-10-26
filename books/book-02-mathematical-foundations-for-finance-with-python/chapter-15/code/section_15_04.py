"""Book 02 Section 15.4: gradients and directional derivatives."""
import json
import math

def number(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be a real number, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def pair(values,name):
    if not isinstance(values,(tuple,list)) or len(values)!=2:
        raise ValueError(f"{name} must have two components")
    return (number(values[0],name),number(values[1],name))

def covariance(matrix):
    if not isinstance(matrix,(tuple,list)) or len(matrix)!=2:
        raise ValueError("covariance must be 2x2")
    a=pair(matrix[0],"covariance row")
    b=pair(matrix[1],"covariance row")
    if not math.isclose(a[1],b[0],rel_tol=1e-12,abs_tol=1e-14):
        raise ValueError("covariance must be symmetric")
    if a[0]<=0 or a[0]*b[1]-a[1]*b[0]<=0:
        raise ValueError("covariance must be positive definite")
    return (a,b)

def portfolio_variance(matrix,weights):
    c=covariance(matrix)
    w=pair(weights,"weights")
    cw=(c[0][0]*w[0]+c[0][1]*w[1],c[1][0]*w[0]+c[1][1]*w[1])
    return number(math.fsum(w[i]*cw[i] for i in range(2)),"portfolio variance")

def portfolio_gradient(matrix,weights):
    c=covariance(matrix)
    w=pair(weights,"weights")
    return (number(2*(c[0][0]*w[0]+c[0][1]*w[1]),"gradient"),
            number(2*(c[1][0]*w[0]+c[1][1]*w[1]),"gradient"))

def unit_direction(direction):
    d=pair(direction,"direction")
    norm=math.hypot(*d)
    if norm==0 or not math.isfinite(norm):
        raise ValueError("direction must have finite nonzero norm")
    return (d[0]/norm,d[1]/norm)

def directional_derivative(matrix,weights,direction):
    g=portfolio_gradient(matrix,weights)
    u=unit_direction(direction)
    return number(math.fsum(g[i]*u[i] for i in range(2)),"directional derivative")

def valuation_gradient(principal,rate,years):
    p=number(principal,"principal")
    r=number(rate,"rate")
    t=number(years,"years")
    if p<0 or t<0:
        raise ValueError("principal and years must be nonnegative")
    try:
        exp=math.exp(r*t)
    except OverflowError as exc:
        raise ValueError("valuation overflow") from exc
    return tuple(number(v,"valuation gradient") for v in
                 (exp,p*t*exp,p*r*exp))

def assessment():
    c=((0.04,0.01),(0.01,0.09))
    w=(0.6,0.4)
    u=unit_direction((1,-1))
    h=0.01
    base=portfolio_variance(c,w)
    shocked=portfolio_variance(c,(w[0]+h*u[0],w[1]+h*u[1]))
    gradient=portfolio_gradient(c,w)
    valuation=valuation_gradient(1000,0.05,2)
    return {
        "portfolio_variance":base,
        "portfolio_gradient":gradient,
        "unit_weight_preserving_direction":u,
        "directional_derivative":directional_derivative(c,w,(1,-1)),
        "quadratic_curvature_coefficient":0.055,
        "finite_step":h,
        "exact_variance_change":shocked-base,
        "linear_variance_change":h*directional_derivative(c,w,(1,-1)),
        "valuation_gradient":valuation,
        "valuation_path_derivative":
            math.fsum((valuation[0]*100,valuation[1]*0.01,valuation[2]*0.5)),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
