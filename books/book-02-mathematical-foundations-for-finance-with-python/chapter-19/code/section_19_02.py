"""Book 02 Section 19.2: separable equations lab."""
import json
import math
from fractions import Fraction
from decimal import Context, Decimal, localcontext

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

def _scaled_exponential(initial,integral):
    if initial==0 or integral==0:
        return initial
    # Beyond this bound no nonzero binary64 initial amount can recover
    # a representable scaled result. Test the complete exact integral.
    if abs(integral)>2000:
        raise ValueError("growth result outside floating-point range")
    with localcontext(Context(prec=850)):
        exponent=Decimal(integral.numerator)/Decimal(integral.denominator)
        result=float(Decimal(initial)*exponent.exp())
    if not math.isfinite(result) or result==0:
        raise ValueError("growth result outside floating-point range")
    return result

def growth(initial,rate,years):
    a,r,t=finite(initial,"initial"),finite(rate,"rate"),finite(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    return _scaled_exponential(a,Fraction(r)*Fraction(t))

def variable_growth(initial,a,b,years):
    start,base,slope,t=(finite(v,n) for v,n in
                         ((initial,"initial"),(a,"a"),(b,"b"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    integral=Fraction(base)*Fraction(t)+Fraction(slope)*Fraction(t)**2/2
    return _scaled_exponential(start,integral)

def logistic(initial,rate,capacity,years):
    a,r,k,t=(finite(v,n) for v,n in
               ((initial,"initial"),(rate,"rate"),(capacity,"capacity"),(years,"years")))
    if a<0 or r<=0 or k<=0 or t<0:
        raise ValueError("invalid logistic inputs")
    if a==0 or t==0 or a==k:
        return a
    # Coarse saturation lies beyond even the largest initial/capacity ratio.
    if r*t>2000:
        return k
    # Keep both positive weights, avoiding k/a and subtraction of a ratio
    # rounded to one. Tiny products need more range than binary64 supplies.
    with localcontext(Context(prec=850)):
        da,dk=Decimal(a),Decimal(k)
        decay=(-Decimal(r)*Decimal(t)).exp()
        denominator=dk*decay+da*(1-decay)
        result=float(da*dk/denominator)
    if not math.isfinite(result) or result<=0:
        raise ValueError("logistic result outside floating-point range")
    return result

def quadratic_growth(initial,rate,years):
    a,k,t=finite(initial,"initial"),finite(rate,"rate"),finite(years,"years")
    if a<=0 or k<=0 or t<0:
        raise ValueError("initial and rate must be positive; years nonnegative")
    denominator=1-Fraction(k)*Fraction(a)*Fraction(t)
    if denominator<=0:
        raise ValueError("at or beyond finite-time singularity")
    try:
        result=float(Fraction(a)/denominator)
    except OverflowError as exc:
        raise ValueError("quadratic growth outside floating-point range") from exc
    if not math.isfinite(result) or result==0:
        raise ValueError("quadratic growth outside floating-point range")
    return result

def proportional_withdrawals(initial,growth_rate,withdrawal_rate,years):
    a,r,w,t=(finite(v,n) for v,n in
              ((initial,"initial"),(growth_rate,"growth rate"),
               (withdrawal_rate,"withdrawal rate"),(years,"years")))
    if a<0 or w<0 or t<0:
        raise ValueError("invalid withdrawal inputs")
    return _scaled_exponential(a,(Fraction(r)-Fraction(w))*Fraction(t))

def assessment():
    return {"exponential_growth":growth(1000,0.04,3),
            "variable_growth":variable_growth(1000,0.03,0.002,5),
            "logistic":logistic(200,0.4,1000,5),
            "logistic_zero_equilibrium":logistic(0,0.4,1000,5),
            "quadratic_growth_before_singularity":quadratic_growth(100,0.001,5),
            "quadratic_singularity_time":10.0,
            "proportional_withdrawals":proportional_withdrawals(1000,0.04,0.06,5),
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
