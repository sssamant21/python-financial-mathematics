"""Section 10.4: substitution and integration by parts in finance."""
import json
import math
from fractions import Fraction
from decimal import Context, Decimal, localcontext

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
    if c == 0 or t == 0:
        return 0.0
    if g == 0:
        value = Fraction(c)*Fraction(t)
        try:
            result = float(value)
        except OverflowError as exc:
            raise ValueError("nonfinite integral") from exc
    else:
        exponent = Fraction(g)*Fraction(t)
        high, gap = max(Fraction(0),exponent), abs(exponent)
        if high > 10000:
            raise ValueError("nonfinite integral")
        with localcontext(Context(prec=800)):
            def decimal(value):
                return Decimal(value.numerator)/Decimal(value.denominator)
            tail = Decimal(1) if gap > 10000 else Decimal(1)-(-decimal(gap)).exp()
            magnitude = abs(decimal(Fraction(c)/Fraction(g)))*decimal(high).exp()*tail
            result = float(-magnitude if c < 0 else magnitude)
    if not math.isfinite(result):
        raise ValueError("nonfinite integral")
    return result

def discount_integral(rate, horizon):
    r, t = finite(rate,"rate"), nonnegative_horizon(horizon)
    return exponential_growth_integral(1.0,-r,t)

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

def phi(x):
    value = Fraction(finite(x,"x"))
    with localcontext(Context(prec=800)):
        return _moment_report(_moment_decimal(value))

def time_weighted_discount_integral(rate,horizon):
    r, t = Fraction(finite(rate,"rate")), Fraction(nonnegative_horizon(horizon))
    if not t:
        return 0.0
    with localcontext(Context(prec=800)):
        result = _fraction_decimal(t*t)*_moment_decimal(r*t)
        return _moment_report(result)

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
