"""Book 02 Section 18.7: numerical differentiation and integration lab."""
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

def step(value):
    h=finite(value,"step")
    if h<=0:
        raise ValueError("step must be positive")
    return h

def forward_difference(f,x,h):
    x,h=finite(x,"x"),step(h)
    if x+h==x:
        raise ValueError("step too small to change x")
    return finite((finite(f(x+h),"f(x+h)")-finite(f(x),"f(x)"))/h,"derivative")

def central_difference(f,x,h):
    x,h=finite(x,"x"),step(h)
    if x+h==x or x-h==x:
        raise ValueError("step too small to change x")
    return finite((finite(f(x+h),"f(x+h)")-finite(f(x-h),"f(x-h)"))/(2*h),"derivative")

def second_difference(f,x,h):
    x,h=finite(x,"x"),step(h)
    if x+h==x or x-h==x:
        raise ValueError("step too small to change x")
    return finite((finite(f(x+h),"f(x+h)")-2*finite(f(x),"f(x)")+finite(f(x-h),"f(x-h)"))/h**2,"second derivative")

def zero_price(rate,face=1000,years=2):
    r,f,t=finite(rate,"rate"),finite(face,"face"),finite(years,"years")
    if r<=-1 or f<=0 or t<=0:
        raise ValueError("invalid bond inputs")
    return finite(f*math.exp(-t*math.log1p(r)),"price")

def quadrature_inputs(a,b,n,simpson=False):
    lo,hi=finite(a,"lower"),finite(b,"upper")
    if hi<=lo or type(n) is not int or n<1 or (simpson and n%2):
        raise ValueError("invalid quadrature bounds or panel count")
    return lo,hi

def trapezoid(f,a,b,n):
    lo,hi=quadrature_inputs(a,b,n)
    h=(hi-lo)/n
    terms=[0.5*finite(f(lo),"f(lower)"),0.5*finite(f(hi),"f(upper)")]
    terms.extend(finite(f(lo+i*h),"integrand") for i in range(1,n))
    return finite(h*math.fsum(terms),"integral")

def simpson(f,a,b,n):
    lo,hi=quadrature_inputs(a,b,n,True)
    h=(hi-lo)/n
    terms=[finite(f(lo),"f(lower)"),finite(f(hi),"f(upper)")]
    terms.extend((4 if i%2 else 2)*finite(f(lo+i*h),"integrand") for i in range(1,n))
    return finite(h*math.fsum(terms)/3,"integral")

def continuous_cashflow_pv(cashflow_rate,discount_rate,years):
    c,r,t=finite(cashflow_rate,"cashflow_rate"),finite(discount_rate,"discount_rate"),finite(years,"years")
    if c<0 or t<0:
        raise ValueError("cashflow rate and maturity must be nonnegative")
    if r==0:
        return finite(c*t,"PV")
    return finite(-c*math.expm1(-r*t)/r,"PV")

def assessment():
    r=0.05
    p=zero_price(r)
    h=1e-4
    f=lambda x:zero_price(x)
    analytic_duration=2/(1+r)
    analytic_convexity=6/(1+r)**2
    rho=0.03
    g=lambda t:100*math.exp(-rho*t)
    exact=continuous_cashflow_pv(100,rho,5)
    return {"price":p,"forward_derivative":forward_difference(f,r,h),
            "central_derivative":central_difference(f,r,h),
            "second_derivative":second_difference(f,r,h),
            "analytic_duration":analytic_duration,
            "numerical_duration":-central_difference(f,r,h)/p,
            "analytic_convexity":analytic_convexity,
            "numerical_convexity":second_difference(f,r,h)/p,
            "trapezoid_20":trapezoid(g,0,5,20),
            "trapezoid_40":trapezoid(g,0,5,40),
            "simpson_20":simpson(g,0,5,20),
            "simpson_40":simpson(g,0,5,40),
            "analytic_continuous_pv":exact,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
