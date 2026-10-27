"""Book 02 Section 16.5: reproducible gradient descent lab."""
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

def normalized_loss(rate):
    r=finite(rate,"rate")
    return finite((r-0.05)**2,"loss")

def normalized_gradient(rate):
    return finite(2*(finite(rate,"rate")-0.05),"gradient")

def quadratic_loss(x,a=2.0,b=0.05):
    x,a,b=(finite(v,"quadratic input") for v in (x,a,b))
    if a<=0:
        raise ValueError("quadratic curvature must be positive")
    return finite(0.5*a*(x-b)**2,"quadratic loss")

def quadratic_gradient(x,a=2.0,b=0.05):
    x,a,b=(finite(v,"quadratic input") for v in (x,a,b))
    if a<=0:
        raise ValueError("quadratic curvature must be positive")
    return finite(a*(x-b),"quadratic gradient")

def gradient_descent(x0,objective,gradient,step=0.25,
                     tolerance=1e-9,max_iterations=100):
    x=finite(x0,"initial point")
    alpha=finite(step,"step")
    tol=finite(tolerance,"tolerance")
    if alpha<=0 or tol<0:
        raise ValueError("step must be positive and tolerance nonnegative")
    if type(max_iterations) is not int or max_iterations<1 or max_iterations>100000:
        raise ValueError("max_iterations must be an integer from 1 to 100000")
    history=[]
    status="max_iterations"
    for k in range(max_iterations+1):
        f=finite(objective(x),"objective")
        g=finite(gradient(x),"gradient")
        history.append({"iteration":k,"x":x,"objective":f,"gradient":g})
        if abs(g)<=tol:
            status="gradient_tolerance"
            break
        if k==max_iterations:
            break
        x=finite(x-alpha*g,"updated point")
    return {"x":x,"objective":history[-1]["objective"],
            "gradient":history[-1]["gradient"],"iterations":len(history)-1,
            "status":status,"history":history,"runtime_certified":False}

def armijo_step(x,objective,gradient,initial_step=1.0,
                shrink=0.5,c=1e-4,max_backtracks=30):
    x=finite(x,"x")
    alpha=finite(initial_step,"initial_step")
    beta=finite(shrink,"shrink")
    c=finite(c,"c")
    if alpha<=0 or not 0<beta<1 or not 0<c<1:
        raise ValueError("invalid Armijo parameters")
    if type(max_backtracks) is not int or not 0<=max_backtracks<=1000:
        raise ValueError("invalid backtracking budget")
    f0=finite(objective(x),"objective")
    g=finite(gradient(x),"gradient")
    if g==0:
        return {"step":0.0,"new_x":x,"new_objective":f0,"status":"stationary"}
    for attempt in range(max_backtracks+1):
        trial=finite(x-alpha*g,"trial point")
        ft=finite(objective(trial),"trial objective")
        if ft<=f0-c*alpha*g*g:
            return {"step":alpha,"new_x":trial,"new_objective":ft,
                    "status":"accepted","backtracks":attempt}
        alpha=finite(alpha*beta,"reduced step")
    return {"step":0.0,"new_x":x,"new_objective":f0,
            "status":"line_search_failed","backtracks":max_backtracks}

def assessment():
    result=gradient_descent(0.0,normalized_loss,normalized_gradient,
                            step=0.25,tolerance=1e-9,max_iterations=100)
    return {"first_five_rates":tuple(h["x"] for h in result["history"][:5]),
            "optimal_rate":0.05,"final_rate":result["x"],
            "final_loss":result["objective"],
            "iterations":result["iterations"],"status":result["status"],
            "armijo":armijo_step(0.0,normalized_loss,normalized_gradient),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
