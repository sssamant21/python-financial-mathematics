"""Chapter-local scaled valuation/conversion kernel; selected range evidence applies."""
import math
from fractions import Fraction
from decimal import Context, Decimal, localcontext

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

def scaled_exponential(initial,integral):
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

def _rounded_rate(value):
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError("converted rate outside floating-point range") from exc
    if not math.isfinite(result) or (value and result==0):
        raise ValueError("converted rate outside floating-point range")
    return result

def nominal_to_continuous(nominal,frequency):
    j=finite(nominal,"nominal")
    if type(frequency) is not int or frequency<1:
        raise ValueError("frequency must be a positive integer")
    q=Fraction(j)/frequency
    if q<=-1:
        raise ValueError("periodic gross growth factor must be positive")
    if abs(q)<=Fraction(1,2**26):
        # ln(1+q)/q; omitted relative tail is below 2^-103.
        return _rounded_rate(Fraction(j)*(1-q/2+q*q/3-q**3/4))
    with localcontext(Context(prec=850)):
        dm=Decimal(frequency)
        value=dm*((dm+Decimal(j))/dm).ln()
    return _rounded_rate(value)

