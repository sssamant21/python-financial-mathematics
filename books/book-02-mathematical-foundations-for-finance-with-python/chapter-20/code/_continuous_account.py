"""Chapter-local account kernel, adapted from Section 19.8; selected range checks apply."""
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

def _rounded_balance(value):
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError("balance outside floating-point range") from exc
    if not math.isfinite(result) or (value and result==0):
        raise ValueError("balance outside floating-point range")
    return result

def _decimal_fraction(value):
    return Decimal(value.numerator)/Decimal(value.denominator)

def _exprel_decimal(value):
    x=_decimal_fraction(value)
    if abs(value)>Fraction(1,2**26):
        return (x.exp()-1)/x
    total=term=Decimal(1)
    k=1
    while True:
        term=term*x/(k+1)
        updated=total+term
        if updated==total:
            return total
        total=updated
        k+=1

def _exprel_fraction(value):
    if abs(value)<Fraction(1,10**400):
        # Retain tiny period corrections before multiplication by a large
        # total accumulation factor; Decimal rounding to one is too early.
        total=term=Fraction(1)
        for k in range(1,11):
            term=term*value/(k+1)
            total+=term
        return total
    return Fraction(_exprel_decimal(value))

def _limiting_balance(offset,correction_sign):
    # A nonzero correction can decide an exact half-subnormal tie even
    # when the exponential is far below the decimal evaluation range.
    try:
        value=float(offset)
    except OverflowError as exc:
        raise ValueError("balance outside floating-point range") from exc
    if not math.isfinite(value):
        raise ValueError("balance outside floating-point range")
    delta=offset-Fraction(value)
    if delta and correction_sign*delta>0:
        neighbor=math.nextafter(value,math.inf if delta>0 else -math.inf)
        if math.isfinite(neighbor) and offset==(Fraction(value)+Fraction(neighbor))/2:
            value=neighbor
    if value==0 and (offset or correction_sign):
        raise ValueError("balance outside floating-point range")
    return value

def account(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if r==0 or t==0:
        return _rounded_balance(Fraction(a)+Fraction(u)*Fraction(t))
    coefficient=Fraction(a)+Fraction(u)/Fraction(r)
    offset=-Fraction(u)/Fraction(r)
    if not coefficient:
        return _rounded_balance(offset)
    x=Fraction(r)*Fraction(t)
    if x>4000:
        raise ValueError("balance outside floating-point range")
    if x < -4000:
        return _limiting_balance(offset,1 if coefficient>0 else -1)
    with localcontext(Context(prec=1100)):
        if abs(x)<=Fraction(1,2**26):
            value=Fraction(a)+coefficient*x*_exprel_fraction(x)
        else:
            value=(_decimal_fraction(coefficient)*_decimal_fraction(x).exp()+
                   _decimal_fraction(offset))
        return _rounded_balance(value)

def depletion_time(initial,rate,withdrawal):
    a,r,w=(finite(v,n) for v,n in
           ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal")))
    if a<0 or w<0:
        raise ValueError("balance and withdrawal must be nonnegative")
    if a==0:
        return 0.0
    if w==0:
        return None
    if r==0:
        return _rounded_balance(Fraction(a)/Fraction(w))
    ratio=Fraction(r)*Fraction(a)/Fraction(w)
    if ratio>=1:
        return None
    if abs(ratio)<=Fraction(1,2**26):
        # -ln(1-q)/q, keeping the full a/w scale.
        series=1+ratio/2+ratio**2/3+ratio**3/4
        return _rounded_balance(Fraction(a)/Fraction(w)*series)
    with localcontext(Context(prec=850)):
        margin=1-ratio
        logarithm=(Decimal(margin.numerator)/Decimal(margin.denominator)).ln()
        value=-logarithm/Decimal(r)
    return _rounded_balance(value)

