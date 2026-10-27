"""Book 02 Section 16.6: Newton and scalar quasi-Newton methods."""
import json
import math

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

def newton_step(x,grad,hess,damping=1.0):
    x=finite(x,"x")
    g=finite(grad(x),"gradient")
    h=finite(hess(x),"hessian")
    alpha=finite(damping,"damping")
    if not 0<alpha<=1:
        raise ValueError("damping must lie in (0,1]")
    if h<=0:
        raise ValueError("positive curvature required for descent Newton step")
    return finite(x-alpha*g/h,"newton update")

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
    y=finite(grad(x_new)-grad(x_old),"gradient difference")
    if s*y<=threshold or s==0:
        raise ValueError("nonpositive or insufficient curvature")
    return finite(y/s,"secant curvature")

def quasi_newton_step(x,grad,curvature):
    x=finite(x,"x")
    g=finite(grad(x),"gradient")
    b=finite(curvature,"curvature")
    if b<=0:
        raise ValueError("positive curvature required")
    return finite(x-g/b,"quasi-Newton update")

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
