"""Book 02 Section 16.6: Newton and scalar quasi-Newton methods."""
import json
import math
from fractions import Fraction

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def loss(rate):
    r=finite(rate,"rate")
    return finite((r-0.05)**2,"loss")

def gradient(rate):
    return finite(2*(finite(rate,"rate")-0.05),"gradient")

def hessian(rate):
    finite(rate,"rate")
    return 2.0

def _curvature_update(x,g,curvature,damping):
    """Round the combined update once, avoiding intermediate range loss."""
    exact=Fraction(x)-Fraction(damping)*Fraction(g)/Fraction(curvature)
    try:
        result=float(exact)
    except OverflowError as exc:
        raise ValueError("curvature update outside floating-point range") from exc
    return finite(result,"curvature update")

def newton_step(x,grad,hess,damping=1.0):
    x=finite(x,"x")
    g=finite(grad(x),"gradient")
    h=finite(hess(x),"hessian")
    alpha=finite(damping,"damping")
    if not 0<alpha<=1:
        raise ValueError("damping must lie in (0,1]")
    if h<=0:
        raise ValueError("positive curvature required for descent Newton step")
    return _curvature_update(x,g,h,alpha)

def newton_solve(x0,grad,hess,tolerance=1e-12,max_iterations=30):
    x=finite(x0,"initial point")
    tol=finite(tolerance,"tolerance")
    if tol<0 or type(max_iterations) is not int or not 1<=max_iterations<=10000:
        raise ValueError("invalid stopping controls")
    history=[]
    status="max_iterations"
    for k in range(max_iterations+1):
        g=finite(grad(x),"gradient")
        history.append({"iteration":k,"x":x,"gradient":g})
        if abs(g)<=tol:
            status="gradient_tolerance"
            break
        if k==max_iterations:
            break
        x=newton_step(x,grad,hess)
    return {"x":x,"iterations":len(history)-1,"status":status,
            "history":history,"runtime_certified":False}

def scalar_secant_curvature(x_old,x_new,grad,threshold=1e-14):
    x_old=finite(x_old,"old point")
    x_new=finite(x_new,"new point")
    threshold=finite(threshold,"threshold")
    if threshold<0:
        raise ValueError("threshold must be nonnegative")
    s=finite(x_new-x_old,"displacement")
    g_new=finite(grad(x_new),"gradient at new point")
    g_old=finite(grad(x_old),"gradient at old point")
    y=finite(g_new-g_old,"gradient difference")
    # Compare the exact product of represented differences: avoid underflow,
    # overflow, or rounding across the user's strict absolute threshold.
    if s==0 or Fraction(s)*Fraction(y)<=Fraction(threshold):
        raise ValueError("nonpositive or insufficient curvature")
    curvature=finite(y/s,"secant curvature")
    if curvature<=0:
        raise ValueError("positive secant curvature is outside floating-point range")
    return curvature

def quasi_newton_step(x,grad,curvature):
    x=finite(x,"x")
    g=finite(grad(x),"gradient")
    b=finite(curvature,"curvature")
    if b<=0:
        raise ValueError("positive curvature required")
    return _curvature_update(x,g,b,1.0)

def assessment():
    solved=newton_solve(0.0,gradient,hessian)
    curvature=scalar_secant_curvature(0.0,0.1,gradient)
    return {"financial_optimum":0.05,"newton_result":solved,
            "secant_curvature":curvature,
            "quasi_newton_update":quasi_newton_step(0,gradient,curvature),
            "loss_at_optimum":loss(0.05),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
