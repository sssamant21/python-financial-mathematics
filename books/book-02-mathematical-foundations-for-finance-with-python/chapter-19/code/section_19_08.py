"""Book 02 Section 19.8: continuous/discrete financial comparison."""
import json
import math
from section_19_02 import _scaled_exponential
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

def continuous_to_nominal(rate,frequency):
    r=finite(rate,"continuous rate")
    if type(frequency) is not int or frequency<1:
        raise ValueError("frequency must be a positive integer")
    q=Fraction(r)/frequency
    if abs(q)<=Fraction(1,2**26):
        # expm1(q)/q; bounded small-argument evaluation retains scaling.
        return _rounded_rate(Fraction(r)*(1+q/2+q*q/6+q**3/24))
    if q>800:
        raise ValueError("converted rate outside floating-point range")
    if q < -800:
        return _rounded_rate(-frequency)
    with localcontext(Context(prec=850)):
        dm=Decimal(frequency)
        value=dm*((Decimal(r)/dm).exp()-1)
    return _rounded_rate(value)

def continuous_growth(initial,rate,years):
    a,r,t=finite(initial,"initial"),finite(rate,"rate"),finite(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    return _scaled_exponential(a,Fraction(r)*Fraction(t))

def discrete_growth(initial,nominal,frequency,periods):
    a,j=finite(initial,"initial"),finite(nominal,"nominal")
    if type(frequency) is not int or frequency<1 or type(periods) is not int or periods<0:
        raise ValueError("frequency positive; periods nonnegative integer")
    q=Fraction(j)/frequency
    if q<=-1:
        raise ValueError("periodic gross growth factor must be positive")
    if a==0 or periods==0 or q==0:
        return a
    if abs(q)<=Fraction(1,2**26):
        integral=periods*q*(1-q/2+q*q/3-q**3/4)
    else:
        with localcontext(Context(prec=850)):
            dm=Decimal(frequency)
            logarithm=((dm+Decimal(j))/dm).ln()
        integral=periods*Fraction(logarithm)
    return _scaled_exponential(a,integral)

def _rounded_balance(value,*,reject_underflow=True):
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError("balance outside floating-point range") from exc
    if not math.isfinite(result) or (reject_underflow and value and result==0):
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

def _limiting_balance(offset,correction_sign,*,reject_underflow=True):
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
    if reject_underflow and value==0 and (offset or correction_sign):
        raise ValueError("balance outside floating-point range")
    if value==0 and not offset:
        return math.copysign(0.0,correction_sign)
    return value

def continuous_contributions(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    return _continuous_balance(a,r,u,t)

def _continuous_balance(a,r,u,t,*,reject_underflow=True):
    """Shared arithmetic for already validated float inputs."""
    if r==0 or t==0:
        return _rounded_balance(Fraction(a)+Fraction(u)*Fraction(t),
                                reject_underflow=reject_underflow)
    coefficient=Fraction(a)+Fraction(u)/Fraction(r)
    offset=-Fraction(u)/Fraction(r)
    if not coefficient:
        return _rounded_balance(offset,reject_underflow=reject_underflow)
    x=Fraction(r)*Fraction(t)
    if x>4000:
        raise ValueError("balance outside floating-point range")
    if x < -4000:
        return _limiting_balance(offset,1 if coefficient>0 else -1,
                                 reject_underflow=reject_underflow)
    # Deep but finite decay can resolve a subnormal rounding tie.
    with localcontext(Context(prec=2600 if x < -1000 else 1100)):
        if abs(x)<=Fraction(1,2**26):
            value=Fraction(a)+coefficient*x*_exprel_fraction(x)
        else:
            value=(_decimal_fraction(coefficient)*_decimal_fraction(x).exp()+
                   _decimal_fraction(offset))
        return _rounded_balance(value,reject_underflow=reject_underflow)

def end_period_contributions(initial,rate,flow,years,periods):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(periods) is not int or periods<1:
        raise ValueError("invalid years or periods")
    if r==0 or t==0:
        return _rounded_balance(Fraction(a)+Fraction(u)*Fraction(t))
    if a==0 and u==0:
        return 0.0
    if u==0:
        return continuous_growth(a,r,t)
    x=Fraction(r)*Fraction(t)
    # Explicit evaluation domain for this educational finite-payment helper.
    # This is not a claim that every excluded case has an infinite balance.
    if abs(x)>5000:
        raise ValueError("end-period exponent exceeds supported evaluation range")
    # On deep decay, preserve the growth term and the tiny correction
    # to the geometric sum; either can decide a final rounding midpoint.
    precision=3200 if x < -1000 else 1100
    with localcontext(Context(prec=precision)):
        if abs(x)<=Fraction(1,2**26):
            growth_minus_one=x*_exprel_fraction(x)
            growth=1+growth_minus_one
        else:
            growth=Fraction(_decimal_fraction(x).exp())
            growth_minus_one=growth-1
        if periods==1:
            return _rounded_balance(Fraction(a)*growth+Fraction(u)*Fraction(t))
        period_rel=_exprel_fraction(x/periods)
        # Keep the timing correction even when it is too small to affect
        # the period factor in float but is amplified by total growth.
        value=Fraction(a)*growth+(Fraction(u)/Fraction(r))*growth_minus_one/period_rel
        return _rounded_balance(value)

def euler_account(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid years or steps")
    return _euler_balance(a,r,u,t,steps)

def _euler_balance(a,r,u,t,steps,*,reject_underflow=True):
    """Shared Euler updates for validated inputs, rounding at each state."""
    if t==0:
        return a
    h=Fraction(t)/steps
    rf,uf=Fraction(r),Fraction(u)
    for _ in range(steps):
        a=_rounded_balance(Fraction(a)+h*(rf*Fraction(a)+uf),
                           reject_underflow=reject_underflow)
    return a

def rk4_account(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid years or steps")
    if t==0:
        return a
    h=Fraction(t)/steps
    rf,uf=Fraction(r),Fraction(u)
    z=rf*h
    # Exact combined RK4 stages for this autonomous affine account model.
    weight=1+z/2+z*z/6+z**3/24
    for _ in range(steps):
        a=_rounded_balance(Fraction(a)+h*(rf*Fraction(a)+uf)*weight)
    return a

def depletion_time(initial,rate,withdrawal):
    a,r,w=(finite(v,n) for v,n in
           ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal")))
    if a<0 or w<0:
        raise ValueError("balance and withdrawal must be nonnegative")
    elapsed=_depletion_elapsed(a,r,w)
    return None if elapsed is None else _rounded_balance(elapsed)

def _depletion_elapsed(a,r,w,*,for_order=False):
    """Crossing interval before float rounding, for validated inputs."""
    if a==0:
        return Fraction(0)
    if w==0:
        return None
    if r==0:
        return Fraction(a)/Fraction(w)
    ratio=Fraction(r)*Fraction(a)/Fraction(w)
    if ratio>=1:
        return None
    if not for_order and abs(ratio)<=Fraction(1,2**26):
        # -ln(1-q)/q, keeping the full a/w scale.
        series=1+ratio/2+ratio**2/3+ratio**3/4
        return Fraction(a)/Fraction(w)*series
    # For ordering, retain the difference from one even for a ratio
    # formed from two minimum subnormals divided by a maximum float.
    with localcontext(Context(prec=1200 if for_order else 850)):
        logarithm=_decimal_fraction(1-ratio).ln()
        return -logarithm/Decimal(r)

def assessment():
    j=0.06
    rc=nominal_to_continuous(j,12)
    exact=continuous_contributions(1000,0.04,200,5)
    convergence={}
    for n in (10,20,40):
        e=euler_account(1000,0.04,200,5,n)
        k=rk4_account(1000,0.04,200,5,n)
        convergence[str(n)]={"euler":e,"rk4":k,
                             "euler_absolute_error":abs(e-exact),
                             "rk4_absolute_error":abs(k-exact)}
    return {"equivalent_continuous_rate":rc,
            "nominal_annual_balance":discrete_growth(1000,j,12,12),
            "continuous_annual_balance":continuous_growth(1000,rc,1),
            "continuous_flow_balance":exact,
            "monthly_end_period_balance":end_period_contributions(1000,0.04,200,5,60),
            "convergence":convergence,
            "depletion_time":depletion_time(1000,0.04,100),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
