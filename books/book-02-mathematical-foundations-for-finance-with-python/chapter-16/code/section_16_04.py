"""Book 02 Section 16.4: convex sets and convex objectives."""
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

def convex_combination(x,y,weight):
    x,y,weight=(finite(v,"combination input") for v in (x,y,weight))
    if not 0<=weight<=1:
        raise ValueError("weight must be between zero and one")
    return finite(weight*x+(1-weight)*y,"convex combination")

def quadratic(x):
    x=finite(x,"x")
    return finite(x*x,"quadratic")

def quartic(x):
    x=finite(x,"x")
    return finite(x**4,"quartic")

def nonconvex(x):
    x=finite(x,"x")
    return finite(x*x-x**4,"nonconvex objective")

def convexity_gap(fn,x,y,weight):
    midpoint=convex_combination(x,y,weight)
    x,y,weight=(finite(v,"convexity input") for v in (x,y,weight))
    return finite(weight*fn(x)+(1-weight)*fn(y)-fn(midpoint),"convexity gap")

def portfolio_variance(w1,w2):
    w1,w2=finite(w1,"w1"),finite(w2,"w2")
    return finite(0.04*w1*w1+0.02*w1*w2+0.09*w2*w2,"variance")

def portfolio_gradient(w1,w2):
    w1,w2=finite(w1,"w1"),finite(w2,"w2")
    return (finite(0.08*w1+0.02*w2,"gradient w1"),
            finite(0.02*w1+0.18*w2,"gradient w2"))

def portfolio_hessian():
    return ((0.08,0.02),(0.02,0.18))

def covariance_determinant():
    return finite(0.04*0.09-0.01**2,"covariance determinant")

def weighted_linear_loss(theta1,theta2):
    theta1,theta2=finite(theta1,"theta1"),finite(theta2,"theta2")
    return finite(0.5*((theta1-2)**2+2*(theta2+1)**2),"weighted loss")

def weighted_linear_hessian():
    return ((1.0,0.0),(0.0,2.0))

def centered_second_difference(fn,x,step=1e-4):
    x,h=finite(x,"x"),finite(step,"step")
    if h<=0:
        raise ValueError("step must be positive")
    return finite((fn(x+h)-2*fn(x)+fn(x-h))/(h*h),"second difference")

def assessment():
    return {
        "convex_combination":convex_combination(0,2,0.25),
        "quadratic_gap":convexity_gap(quadratic,-1,3,0.5),
        "quartic_second_derivative_at_zero":0.0,
        "nonconvex_second_derivative_at_one":-10.0,
        "portfolio_variance":portfolio_variance(0.6,0.4),
        "portfolio_gradient":portfolio_gradient(0.6,0.4),
        "portfolio_hessian":portfolio_hessian(),
        "covariance_determinant":covariance_determinant(),
        "weighted_linear_minimum":weighted_linear_loss(2,-1),
        "weighted_linear_hessian":weighted_linear_hessian(),
        "quadratic_second_derivative_numeric":centered_second_difference(quadratic,1),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
