"""Section 10.2: definite and indefinite integrals."""
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

def _polynomial_coefficients(coefficients):
    values = [Fraction(finite(a, "coefficient")) for a in coefficients]
    if not values:
        raise ValueError("at least one coefficient required")
    return values

def _polynomial_report(value, name):
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("nonfinite " + name) from exc
    if not math.isfinite(result):
        raise ValueError("nonfinite " + name)
    return result

def polynomial_antiderivative(coefficients,t,constant=0):
    x = Fraction(finite(t, "t"))
    c = Fraction(finite(constant, "constant"))
    values = _polynomial_coefficients(coefficients)
    result = c + sum((a*x**power/power
                      for power,a in enumerate(values,1) if a), Fraction(0))
    return _polynomial_report(result, "antiderivative")

def polynomial_definite(coefficients,a,b):
    left,right = Fraction(finite(a,"a")),Fraction(finite(b,"b"))
    values = _polynomial_coefficients(coefficients)
    if left == right:
        return 0.0
    result = sum((coefficient*(right**power-left**power)/power
                  for power,coefficient in enumerate(values,1) if coefficient),
                 Fraction(0))
    return _polynomial_report(result, "integral")

def exponential_definite(scale,growth,a,b):
    c,k,left,right=(finite(v,name) for v,name in
                    ((scale,"scale"),(growth,"growth"),(a,"a"),(b,"b")))
    if c == 0 or left == right:
        return 0.0
    width = Fraction(right)-Fraction(left)
    if k == 0:
        return _polynomial_report(Fraction(c)*width, "integral")
    # Anchor at the larger exponent; combine scale/growth before reporting.
    lo, hi = sorted((Fraction(k)*Fraction(left), Fraction(k)*Fraction(right)))
    gap = hi-lo
    # Finite binary64 inputs bound |c/k| and a nonzero gap. These cutoffs
    # are far outside their possible compensation range (see manuscript).
    if hi > 10000:
        raise ValueError("nonfinite integral")
    if hi < -10000:
        return 0.0
    with localcontext(Context(prec=800)):
        def decimal(value):
            return Decimal(value.numerator)/Decimal(value.denominator)
        tail = Decimal(1) if gap > 10000 else Decimal(1)-(-decimal(gap)).exp()
        magnitude = abs(decimal(Fraction(c)/Fraction(k)))*decimal(hi).exp()*tail
        sign = -1 if (c < 0) != (width < 0) else 1
        result = float(sign*magnitude)
    if not math.isfinite(result):
        raise ValueError("nonfinite integral")
    return result

def midpoint_sum(function,a,b,n):
    if not callable(function):
        raise TypeError("function must be callable")
    left,right=finite(a,"a"),finite(b,"b")
    if type(n) is not int or n<=0:
        raise ValueError("n must be a positive integer")
    if left==right:
        return 0.0
    # Build all rounded sample points before calling user code. Exact endpoint
    # arithmetic avoids overflow in right-left and in the midpoint expression.
    origin = Fraction(left)
    width = (Fraction(right)-origin)/n
    samples = []
    for i in range(n):
        start, stop = origin+i*width, origin+(i+1)*width
        sample = float((start+stop)/2)
        if not min(start,stop) < Fraction(sample) < max(start,stop):
            raise ValueError("midpoint not representable inside its subinterval")
        samples.append(sample)
    total = sum((Fraction(finite(function(x),"integrand"))*width
                 for x in samples), Fraction(0))
    try:
        result = float(total)
    except OverflowError as exc:
        raise ValueError("nonfinite midpoint result") from exc
    if not math.isfinite(result):
        raise ValueError("nonfinite midpoint result")
    return result

if __name__=="__main__":
    result={
        "linear_antiderivative_at_2":polynomial_antiderivative([100,20],2),
        "linear_integral_0_to_2":polynomial_definite([100,20],0,2),
        "signed_integral":polynomial_definite([-1,1],0,2),
        "growing_payment_integral":exponential_definite(500,0.03,0,2),
        "midpoint_checks":[{"n":n,"estimate":midpoint_sum(lambda t:math.exp(0.03*t)*500,0,2,n)}
                           for n in (4,16,64,256)]}
    print(json.dumps(result,indent=2,allow_nan=False))
