"""Book 02 Section 15.6: Hessians and mixed partials."""
import json
import math

def number(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def polynomial(x,y):
    x=number(x,"x")
    y=number(y,"y")
    return number(x*x+3*x*y+2*y*y,"polynomial")

def polynomial_gradient(x,y):
    x=number(x,"x")
    y=number(y,"y")
    return (number(2*x+3*y,"gradient"),number(3*x+4*y,"gradient"))

def polynomial_hessian():
    return ((2.0,3.0),(3.0,4.0))

def value(principal,rate,years):
    p=number(principal,"principal")
    r=number(rate,"rate")
    t=number(years,"years")
    if p<0 or t<0:
        raise ValueError("principal and years must be nonnegative")
    try:
        return number(p*math.exp(r*t),"future value")
    except OverflowError as exc:
        raise ValueError("future value overflow") from exc

def rate_time_gradient(principal,rate,years):
    r=number(rate,"rate")
    t=number(years,"years")
    v=value(principal,r,t)
    return (number(t*v,"rate derivative"),number(r*v,"time derivative"))

def rate_time_hessian(principal,rate,years):
    r=number(rate,"rate")
    t=number(years,"years")
    v=value(principal,r,t)
    mixed=number(v*(1+r*t),"mixed derivative")
    return ((number(t*t*v,"rate curvature"),mixed),
            (mixed,number(r*r*v,"time curvature")))

def second_order_change(principal,rate,years,d_rate,d_years):
    dr=number(d_rate,"rate shock")
    dt=number(d_years,"time shock")
    gradient=rate_time_gradient(principal,rate,years)
    h=rate_time_hessian(principal,rate,years)
    linear=number(gradient[0]*dr+gradient[1]*dt,"linear change")
    quadratic=number(0.5*h[0][0]*dr*dr+h[0][1]*dr*dt+
                     0.5*h[1][1]*dt*dt,"quadratic correction")
    return {"linear":linear,"quadratic":quadratic,
            "second_order":number(linear+quadratic,"second order change")}

def exact_change(principal,rate,years,d_rate,d_years):
    r=number(rate,"rate")
    t=number(years,"years")
    dr=number(d_rate,"rate shock")
    dt=number(d_years,"time shock")
    return number(value(principal,r+dr,t+dt)-value(principal,r,t),
                  "exact change")

def portfolio_hessian(covariance):
    if not isinstance(covariance,(tuple,list)) or len(covariance)!=2:
        raise ValueError("covariance must be 2x2")
    rows=[]
    for row in covariance:
        if not isinstance(row,(tuple,list)) or len(row)!=2:
            raise ValueError("covariance must be 2x2")
        rows.append(tuple(number(v,"covariance entry") for v in row))
    if not math.isclose(rows[0][1],rows[1][0],rel_tol=1e-12,abs_tol=1e-14):
        raise ValueError("covariance must be symmetric")
    if rows[0][0]<=0 or rows[0][0]*rows[1][1]-rows[0][1]**2<=0:
        raise ValueError("covariance must be positive definite")
    return tuple(tuple(number(2*v,"Hessian entry") for v in row) for row in rows)

def assessment():
    p,r,t=1000.0,0.05,2.0
    dr,dt=0.01,0.5
    a=second_order_change(p,r,t,dr,dt)
    exact=exact_change(p,r,t,dr,dt)
    return {
        "polynomial_value":polynomial(1,2),
        "polynomial_gradient":polynomial_gradient(1,2),
        "polynomial_hessian":polynomial_hessian(),
        "polynomial_hessian_determinant":-1.0,
        "polynomial_exact_change":polynomial(1.1,1.8)-polynomial(1,2),
        "future_value":value(p,r,t),
        "rate_time_gradient":rate_time_gradient(p,r,t),
        "rate_time_hessian":rate_time_hessian(p,r,t),
        "first_order_change":a["linear"],
        "quadratic_correction":a["quadratic"],
        "second_order_change":a["second_order"],
        "exact_change":exact,
        "portfolio_hessian":portfolio_hessian(((0.04,0.01),(0.01,0.09))),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
