"""Book 02 Section 18.1: financial numerical error taxonomy lab."""
import json
import math
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def _round_result(value,name):
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(result) or (value and result==0):
        raise ValueError(f"{name} outside floating-point range")
    return result

def present_value(payment,rate,periods):
    c,r,n=(finite(v,name) for v,name in
           ((payment,"payment"),(rate,"rate"),(periods,"periods")))
    if c<0 or r<=-1 or n<0:
        raise ValueError("invalid payment, rate, or period")
    if c==0 or n==0 or r==0:
        return c
    # This coarse bound is beyond the combined payment and result ranges.
    if abs(n*math.log1p(r))>2000:
        raise ValueError("present value outside floating-point range")
    with localcontext(Context(prec=850)):
        value=Decimal(c)*(1+Decimal(r))**(-Decimal(n))
    return _round_result(value,"present value")

def errors(reference,estimate):
    y=finite(reference,"reference")
    z=finite(estimate,"estimate")
    delta=abs(Fraction(z)-Fraction(y))
    return {"absolute":_round_result(delta,"absolute error"),
            "relative":None if y==0 else _round_result(
                delta/abs(Fraction(y)),"relative error")}

def exponential_approximation(x):
    x=finite(x,"x")
    exact=math.exp(x)
    first_order=1+x
    return {"exact":exact,"first_order":first_order,
            "error":errors(exact,first_order)}

def cancellation_demo(x=1e-12):
    x=finite(x,"x")
    return {"x":x,"direct":math.exp(x)-1,
            "stable":math.expm1(x)}

def money_cents(value):
    v=finite(value,"value")
    return str(Decimal(str(v)).quantize(Decimal("0.01"),
                                       rounding=ROUND_HALF_EVEN))

def assessment():
    reference=present_value(1000,0.05,2)
    wrong_period=present_value(1000,0.05,3)
    wrong_rate=present_value(1000,5,2)
    return {"present_value_reference":reference,
            "period_specification_error":{"estimate":wrong_period,
                                          "errors":errors(reference,wrong_period)},
            "rate_unit_error":{"estimate":wrong_rate,
                               "errors":errors(reference,wrong_rate)},
            "approximation":exponential_approximation(0.1),
            "cancellation":cancellation_demo(),
            "binary_float_example":0.1+0.2,
            "rounded_cents":money_cents(reference),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
