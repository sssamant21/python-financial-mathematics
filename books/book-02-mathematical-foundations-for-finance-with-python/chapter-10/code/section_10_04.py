"""Section 10.4: substitution and integration by parts in finance."""
import json
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def nonnegative_horizon(T):
    t = finite(T, "horizon")
    if t < 0:
        raise ValueError("horizon must be nonnegative")
    return t

def exponential_growth_integral(scale, growth, horizon):
    c, g, t = finite(scale,"scale"), finite(growth,"growth"), nonnegative_horizon(horizon)
    x = g*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    result = c*t if g == 0 else c*t*(math.expm1(x)/x if x else 1.0)
    if not math.isfinite(result):
        raise ValueError("nonfinite integral")
    return result

def discount_integral(rate, horizon):
    r, t = finite(rate,"rate"), nonnegative_horizon(horizon)
    return exponential_growth_integral(1.0,-r,t)

def phi(x):
    x = finite(x,"x")
    if abs(x) < 0.1:
        term = 0.5
        total = term
        for k in range(1,100):
            term *= (-x)*(k+1)/(k*(k+2))
            total += term
            if abs(term) <= 1e-16*max(1.0,abs(total)):
                break
        return total
    result = (-math.expm1(-x)-x*math.exp(-x))/(x*x)
    if not math.isfinite(result):
        raise ValueError("nonfinite phi")
    return result

def time_weighted_discount_integral(rate,horizon):
    r, t = finite(rate,"rate"), nonnegative_horizon(horizon)
    x = r*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    result = t*t*phi(x)
    if not math.isfinite(result):
        raise ValueError("nonfinite integral")
    return result

def linear_cashflow_pv(intercept,slope,rate,horizon):
    a,b = finite(intercept,"intercept"),finite(slope,"slope")
    r,t = finite(rate,"rate"),nonnegative_horizon(horizon)
    result = a*discount_integral(r,t)+b*time_weighted_discount_integral(r,t)
    if not math.isfinite(result):
        raise ValueError("nonfinite present value")
    return result

def midpoint_reference(function,a,b,n=1000):
    if not callable(function):
        raise TypeError("function must be callable")
    left,right=finite(a,"a"),finite(b,"b")
    if type(n) is not int or n<=0:
        raise ValueError("n must be positive integer")
    width=(right-left)/n
    result=math.fsum(finite(function(left+(i+0.5)*width),"integrand")*width
                     for i in range(n))
    if not math.isfinite(result):
        raise ValueError("nonfinite midpoint reference")
    return result

def assessment():
    a,b,t=1000,100,2
    rows=[]
    for rate in (-0.01,0,0.01,0.04,0.08):
        exact=linear_cashflow_pv(a,b,rate,t)
        numerical=midpoint_reference(lambda x:(a+b*x)*math.exp(-rate*x),0,t)
        rows.append({"rate":rate,"discount_integral":discount_integral(rate,t),
                     "time_weighted_integral":time_weighted_discount_integral(rate,t),
                     "present_value":exact,"midpoint_reference":numerical,
                     "absolute_difference":abs(exact-numerical)})
    return {"model":"linear cash-flow rate with flat continuous discount",
            "horizon_years":t,"scenarios":rows,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
