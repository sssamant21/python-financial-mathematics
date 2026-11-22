"""Section 10.5: discounting continuous payment streams."""
import json
import math
from fractions import Fraction
from decimal import Context, Decimal, localcontext

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

def _exponential_integral(c,k,t):
    # Inputs are exact fractions of validated finite floats. Preserve the full
    # growth-minus-discount difference and scale before final float reporting.
    if not c or not t:
        return 0.0
    if not k:
        value=c*t
        try:
            result=float(value)
        except OverflowError as exc:
            raise ValueError("nonfinite exponential integral") from exc
    else:
        exponent=k*t
        high,gap=max(Fraction(0),exponent),abs(exponent)
        if high>10000:
            raise ValueError("nonfinite exponential integral")
        with localcontext(Context(prec=800)):
            def decimal(value):
                return Decimal(value.numerator)/Decimal(value.denominator)
            tail=Decimal(1) if gap>10000 else Decimal(1)-(-decimal(gap)).exp()
            magnitude=abs(decimal(c/k))*decimal(high).exp()*tail
            result=float(-magnitude if c<0 else magnitude)
    if not math.isfinite(result):
        raise ValueError("nonfinite exponential integral")
    return result

def exponential_integral(scale,exponent,T):
    c,k,t=finite(scale,"scale"),finite(exponent,"exponent"),horizon(T)
    return _exponential_integral(Fraction(c),Fraction(k),Fraction(t))

def constant_pv(payment_rate,rate,T):
    return exponential_integral(payment_rate,-finite(rate,"rate"),T)

def growing_pv(initial_rate,growth,discount,T):
    c=finite(initial_rate,"initial_rate")
    g,r=finite(growth,"growth"),finite(discount,"discount")
    t=horizon(T)
    return _exponential_integral(Fraction(c),Fraction(g)-Fraction(r),Fraction(t))

def _moment_report(value):
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("nonfinite time-weighted result") from exc
    if not math.isfinite(result):
        raise ValueError("nonfinite time-weighted result")
    return result

def _fraction_decimal(value):
    return Decimal(value.numerator)/Decimal(value.denominator)

def _moment_decimal(x):
    if x < -10000:
        raise ValueError("nonfinite time-weighted result")
    if x > 10000:
        return _fraction_decimal(1/(x*x))
    value = _fraction_decimal(x)
    if abs(x) < Fraction(1,10):
        term = total = Decimal("0.5")
        for k in range(1,2000):
            term *= (-value)*(k+1)/(k*(k+2))
            updated = total+term
            if updated == total:
                return total
            total = updated
        raise ValueError("moment series did not converge")
    return (1-(1+value)*(-value).exp())/(value*value)

def time_weighted_factor(rate,T):
    r, t = Fraction(finite(rate,"rate")), Fraction(horizon(T))
    if not t:
        return 0.0
    with localcontext(Context(prec=800)):
        result = _fraction_decimal(t*t)*_moment_decimal(r*t)
        return _moment_report(result)

def _pv_report(value):
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("nonfinite present value") from exc
    if not math.isfinite(result):
        raise ValueError("nonfinite present value")
    return result

def linear_pv(intercept,slope,rate,T):
    a,b = Fraction(finite(intercept,"intercept")),Fraction(finite(slope,"slope"))
    r,t = Fraction(finite(rate,"rate")),Fraction(horizon(T))
    if not t or not (a or b):
        return 0.0
    if not r:
        return _pv_report(a*t+b*t*t/2)
    constant = a*r+b
    exponential = constant+b*r*t
    denominator = r*r
    if not exponential:
        return _pv_report(constant/denominator)
    exponent = r*t
    if exponent > 10000:
        return _pv_report(constant/denominator)
    if exponent < -10000:
        raise ValueError("nonfinite present value")
    with localcontext(Context(prec=2000)):
        numerator = (_fraction_decimal(constant)
                     -_fraction_decimal(exponential)*(-_fraction_decimal(exponent)).exp())
        return _pv_report(numerator/_fraction_decimal(denominator))

def midpoint_integral(function,T,n=2000):
    if not callable(function):
        raise TypeError("function must be callable")
    t=horizon(T)
    if type(n) is not int or n<=0:
        raise ValueError("n must be a positive integer")
    if not t:
        return 0.0
    width=Fraction(t)/n
    samples=[]
    # Validate every rounded point before executing caller code. A collapsed
    # midpoint is not an interior sample of its exact partition interval.
    for i in range(n):
        left,right=i*width,(i+1)*width
        sample=float((left+right)/2)
        if not left<Fraction(sample)<right:
            raise ValueError("midpoint not representable inside its subinterval")
        samples.append(sample)
    total=sum((Fraction(finite(function(x),"integrand"))*width
               for x in samples),Fraction(0))
    try:
        result=float(total)
    except OverflowError as exc:
        raise ValueError("nonfinite quadrature") from exc
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
