"""Book 02 Section 16.2: stationary points and first-order conditions."""
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

def scalar_quadratic(x):
    x=finite(x,"x")
    return finite((x-3)**2+5,"scalar objective")

def scalar_gradient(x):
    return finite(2*(finite(x,"x")-3),"scalar gradient")

def cubic(x):
    x=finite(x,"x")
    return finite(x*x*x,"cubic")

def saddle(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite(x*x-y*y,"saddle")

def separable(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite(2*(x-1)**2+3*(y+2)**2,"separable objective")

def separable_gradient(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return (finite(4*(x-1),"gradient x"),finite(6*(y+2),"gradient y"))

def coupled_loss(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return finite((x+y-3)**2+(x-y-1)**2,"coupled loss")

def coupled_gradient(x,y):
    x,y=finite(x,"x"),finite(y,"y")
    return (finite(4*x-8,"gradient x"),finite(4*y-4,"gradient y"))

def financial_loss(rate,target=1100):
    r=finite(rate,"rate")
    y=finite(target,"target")
    return finite((1000*(1+2*r)-y)**2,"financial loss")

def financial_gradient(rate,target=1100):
    r=finite(rate,"rate")
    y=finite(target,"target")
    return finite(4000*(1000*(1+2*r)-y),"financial gradient")

def financial_optimum(target=1100):
    y=finite(target,"target")
    return finite((y/1000-1)/2,"financial optimum")

def centered_difference(fn,x,step=1e-5):
    x=finite(x,"x")
    h=finite(step,"step")
    if h<=0:
        raise ValueError("step must be positive")
    return finite((fn(x+h)-fn(x-h))/(2*h),"finite difference")

def assessment():
    optimum=financial_optimum()
    return {
        "scalar_stationary_point":3.0,
        "scalar_minimum_value":scalar_quadratic(3),
        "scalar_gradient_at_optimum":scalar_gradient(3),
        "cubic_stationary_point":0.0,
        "cubic_values_near_zero":(cubic(-0.1),cubic(0.1)),
        "saddle_axis_values":(saddle(1,0),saddle(0,1)),
        "separable_stationary_point":(1.0,-2.0),
        "separable_gradient_at_optimum":separable_gradient(1,-2),
        "coupled_stationary_point":(2.0,1.0),
        "coupled_loss_at_optimum":coupled_loss(2,1),
        "coupled_gradient_at_optimum":coupled_gradient(2,1),
        "financial_optimal_rate":optimum,
        "financial_loss_at_optimum":financial_loss(optimum),
        "financial_gradient_at_optimum":financial_gradient(optimum),
        "financial_gradient_finite_difference":centered_difference(financial_loss,0.04),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
