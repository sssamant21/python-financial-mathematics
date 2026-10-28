"""Section 10.5: discounting continuous payment streams."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def horizon(value):
    t=finite(value,"horizon")
    if t<0:
        raise ValueError("horizon must be nonnegative")
    return t

def exponential_integral(scale,exponent,T):
    c,k,t=finite(scale,"scale"),finite(exponent,"exponent"),horizon(T)
    x=k*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    result=c*t if x==0 else c*t*(math.expm1(x)/x)
    if not math.isfinite(result):
        raise ValueError("nonfinite exponential integral")
    return result

def constant_pv(payment_rate,rate,T):
    return exponential_integral(payment_rate,-finite(rate,"rate"),T)

def growing_pv(initial_rate,growth,discount,T):
    g,r=finite(growth,"growth"),finite(discount,"discount")
    return exponential_integral(initial_rate,g-r,T)

def time_weighted_factor(rate,T):
    r,t=finite(rate,"rate"),horizon(T)
    x=r*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    if abs(x)<0.1:
        term=0.5
        total=term
        for k in range(1,100):
            term*=(-x)*(k+1)/(k*(k+2))
            total+=term
            if abs(term)<=1e-16*max(1,abs(total)):
                break
        result=t*t*total
    else:
        result=t*t*(-math.expm1(-x)-x*math.exp(-x))/(x*x)
    if not math.isfinite(result):
        raise ValueError("nonfinite weighted integral")
    return result

def linear_pv(intercept,slope,rate,T):
    a,b,r,t=finite(intercept,"intercept"),finite(slope,"slope"),finite(rate,"rate"),horizon(T)
    result=constant_pv(a,r,t)+b*time_weighted_factor(r,t)
    if not math.isfinite(result):
        raise ValueError("nonfinite linear PV")
    return result

def midpoint_integral(function,T,n=2000):
    if not callable(function):
        raise TypeError("function must be callable")
    t=horizon(T)
    if type(n) is not int or n<=0:
        raise ValueError("n must be a positive integer")
    dt=t/n
    result=math.fsum(finite(function((i+0.5)*dt),"integrand")*dt for i in range(n))
    if not math.isfinite(result):
        raise ValueError("nonfinite quadrature")
    return result

def variable_curve_pv(payment_rate,base_rate,slope,T,n=2000):
    if not callable(payment_rate):
        raise TypeError("payment_rate must be callable")
    r,k=finite(base_rate,"base_rate"),finite(slope,"slope")
    return midpoint_integral(
        lambda t:finite(payment_rate(t),"payment rate")*math.exp(-r*t-0.5*k*t*t),T,n)

def growing_pv_rate_derivative(initial_rate,growth,discount,T):
    c,g,r,t=(finite(v,name) for v,name in
             ((initial_rate,"initial_rate"),(growth,"growth"),(discount,"discount"),(T,"horizon")))
    horizon(t)
    return -c*time_weighted_factor(r-g,t)

def assessment():
    c,g,T=1000,0.02,4
    rows=[]
    for r in (-0.01,0,0.02,0.05,0.08):
        exact=growing_pv(c,g,r,T)
        numerical=midpoint_integral(lambda t:c*math.exp((g-r)*t),T)
        rows.append({"discount_rate":r,"exact_pv":exact,
                     "midpoint_pv":numerical,"absolute_difference":abs(exact-numerical)})
    return {"scenarios":rows,
            "parallel_rate_derivative_at_5pct":growing_pv_rate_derivative(c,g,0.05,T),
            "variable_curve_pv":variable_curve_pv(lambda t:c*math.exp(g*t),0.03,0.005,T),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
