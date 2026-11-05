"""Book 02 Section 18.2: floating-point and cancellation lab."""
import json
import math
import sys
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext

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

def valid_rate_periods(rate,periods):
    r,n=finite(rate,"rate"),finite(periods,"periods")
    if r<=-1 or n<0:
        raise ValueError("rate must exceed -1 and periods must be nonnegative")
    return r,n

def _compound_result(rate,periods,*,inverse=False,change=False):
    r,n=valid_rate_periods(rate,periods)
    if r==0 or n==0:
        return 0.0 if change else 1.0
    exponent=n*math.log1p(r)
    if inverse:
        exponent=-exponent
    # Conservative bounds: exp(800) overflows binary64 and
    # exp(-800) rounds to zero, or gives a change rounding to -1.
    if exponent < -800 and change:
        return -1.0
    if abs(exponent)>800:
        raise ValueError("compound result outside floating-point range")
    with localcontext(Context(prec=850)):
        power=(1+Decimal(r))**(Decimal(-n) if inverse else Decimal(n))
        result=float(power-1 if change else power)
    if not math.isfinite(result) or result==0:
        raise ValueError("compound result outside floating-point range")
    return result

def growth_factor(rate,periods):
    return _compound_result(rate,periods)

def growth_increment(rate,periods):
    return _compound_result(rate,periods,change=True)

def discount_change(rate,periods):
    return _compound_result(rate,periods,inverse=True,change=True)

def annuity_present_value(payment,rate,periods):
    c=finite(payment,"payment")
    r,n=valid_rate_periods(rate,periods)
    if c<0:
        raise ValueError("payment must be nonnegative")
    if c==0 or n==0:
        return 0.0
    if r==0:
        value=c*n
    else:
        # Use the binary exponent only for coarse range decisions. A positive
        # exponent above 2000 overflows even at the smallest positive payment
        # (and here abs(rate)<1). Below -2000 the discount is negligible.
        exponent=-n*math.log1p(r)
        if exponent>2000:
            raise ValueError("annuity PV outside floating-point range")
        # Keep tiny discount changes and the complete scaling in a wider
        # format. Even two minimum subnormal inputs give a change near 1e-647.
        with localcontext(Context(prec=850)):
            dr=Decimal(r)
            numerator=(Decimal(1) if exponent < -2000
                       else 1-(1+dr)**(-Decimal(n)))
            value=float(Decimal(c)*numerator/dr)
    if not math.isfinite(value) or value==0:
        raise ValueError("annuity PV outside floating-point range")
    return value

def decimal_cents(text):
    if not isinstance(text,str):
        raise TypeError("pass exact decimal text")
    d=Decimal(text)
    if not d.is_finite():
        raise ValueError("decimal amount must be finite")
    return str(d.quantize(Decimal("0.01"),rounding=ROUND_HALF_EVEN))

def assessment():
    x=1e-12
    naive=0.0
    for value in (1e16,1.0,-1e16):
        naive += value
    return {"machine_epsilon":sys.float_info.epsilon,
            "unit_roundoff":2**-53,
            "decimal_float_example":0.1+0.2,
            "expm1_comparison":{"direct":math.exp(x)-1,
                                 "stable":math.expm1(x)},
            "log1p_comparison":{"direct":math.log(1+x),
                                 "stable":math.log1p(x)},
            "growth_increment":growth_increment(1e-12,12),
            "growth_factor":growth_factor(1e-12,12),
            "discount_change":discount_change(1e-12,12),
            "annuity_pv":annuity_present_value(100,0.05,12),
            "zero_rate_annuity_pv":annuity_present_value(100,0,12),
            "naive_sum":naive,
            "accurate_sum":math.fsum([1e16,1.0,-1e16]),
            "decimal_cents":decimal_cents("907.025"),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
