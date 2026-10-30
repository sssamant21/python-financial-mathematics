"""Book 02 Section 16.3: second-order classification."""
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

def quadratic_minimum(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite(2*(x-1)**2+3*(y+2)**2,"quadratic minimum")

def quadratic_maximum(x,y):
    return finite(-quadratic_minimum(x,y),"quadratic maximum")

def saddle(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite(x*x-y*y,"saddle")

def quartic_minimum(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite(x**4+y**4,"quartic minimum")

def quartic_saddle(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite(x**4-y**4,"quartic saddle")

def classify_hessian_2x2(a,b,c,tolerance=0.0):
    a,b,c=(finite(v,"Hessian entry") for v in (a,b,c))
    tol=finite(tolerance,"tolerance")
    if tol<0:
        raise ValueError("tolerance must be nonnegative")
    discriminant=finite(math.hypot(a-c,2*b),"eigenvalue discriminant")
    eig1=finite(0.5*(a+c+discriminant),"eigenvalue")
    eig2=finite(0.5*(a+c-discriminant),"eigenvalue")
    if eig2>tol:
        category="positive definite"
    elif eig1 < -tol:
        category="negative definite"
    elif eig1>tol and eig2 < -tol:
        category="indefinite"
    elif eig1>=-tol and eig2>=-tol:
        category="positive semidefinite or numerically inconclusive"
    elif eig1<=tol and eig2<=tol:
        category="negative semidefinite or numerically inconclusive"
    else:
        category="numerically inconclusive"
    return {"eigenvalues":(eig1,eig2),
            "determinant":finite(a*c-b*b,"determinant"),
            "category":category}

def financial_loss(rate):
    r=finite(rate,"rate")
    return finite((2000*r-100)**2,"financial loss")

def financial_gradient(rate):
    r=finite(rate,"rate")
    return finite(4000*(2000*r-100),"financial gradient")

def financial_hessian():
    return 8_000_000.0

def centered_second_difference(fn,x,step=1e-4):
    x=finite(x,"x")
    h=finite(step,"step")
    if h<=0:
        raise ValueError("step must be positive")
    xp,xm=finite(x+h,"x+step"),finite(x-h,"x-step")
    if not xm<x<xp:
        raise ValueError("step must change both represented inputs")
    denominator=finite(h*h,"finite-difference denominator")
    if denominator==0:
        raise ValueError("finite-difference denominator must be nonzero")
    fp,fm=finite(fn(xp),"callback at x+step"),finite(fn(xm),"callback at x-step")
    f0=finite(fn(x),"callback at x")
    return finite((fp-2*f0+fm)/denominator,"finite-difference estimate")

def assessment():
    return {
        "minimum":classify_hessian_2x2(4,0,6),
        "maximum":classify_hessian_2x2(-4,0,-6),
        "saddle":classify_hessian_2x2(2,0,-2),
        "zero_hessian":classify_hessian_2x2(0,0,0),
        "positive_quadratic_at_stationary":quadratic_minimum(1,-2),
        "negative_quadratic_at_stationary":quadratic_maximum(1,-2),
        "quartic_minimum_at_origin":quartic_minimum(0,0),
        "quartic_saddle_at_origin":quartic_saddle(0,0),
        "financial_optimum":0.05,
        "financial_loss_at_optimum":financial_loss(0.05),
        "financial_gradient_at_optimum":financial_gradient(0.05),
        "financial_hessian":financial_hessian(),
        "financial_hessian_finite_difference":
            centered_second_difference(financial_loss,0.05),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
