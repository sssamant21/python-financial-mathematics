"""Section 10.8: discrete versus continuous payments."""
import json
import math
from section_10_05 import constant_pv
from fractions import Fraction
from decimal import Context,Decimal,localcontext

MAX_SCHEDULE_PAYMENTS=10000
MAX_PAYMENT_COUNT_BITS=4096

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def valid_horizon(T):
    t=finite(T,"horizon")
    if t<0:
        raise ValueError("horizon must be nonnegative")
    return t

def valid_count(n):
    if type(n) is not int or n<=0:
        raise ValueError("n must be a positive integer")
    return n

def continuous_pv(payment_rate,rate,horizon):
    c,r,t=finite(payment_rate,"payment_rate"),finite(rate,"rate"),valid_horizon(horizon)
    # Share the complete scaled exponential integral, preserving this API's
    # validated signed payment rate and nonnegative horizon contract.
    return constant_pv(c,r,t)

def schedule_pv(payments,rate):
    r=Fraction(finite(rate,"rate"))
    grouped={}
    # Validate all bounded rows before exponential arithmetic. Exact equal-time
    # groups cancel before any overflowing discounted component is formed.
    for index,payment in enumerate(payments):
        if index>=MAX_SCHEDULE_PAYMENTS:
            raise ValueError("payment schedule exceeds supported count")
        if not isinstance(payment,(list,tuple)) or len(payment)!=2:
            raise ValueError("payment must be (time, amount)")
        time=finite(payment[0],"time")
        if time<0:
            raise ValueError("payment time must be nonnegative")
        amount=Fraction(finite(payment[1],"amount"))
        exponent=-r*Fraction(time)
        grouped[exponent]=grouped.get(exponent,Fraction(0))+amount
    return _discounted_sum(grouped)

def _discounted_sum(grouped):
    """Complete sum for validated rational exponent/coefficient groups (internal)."""
    grouped={e:a for e,a in grouped.items() if a}
    if not grouped:
        return 0.0
    if set(grouped)=={Fraction(0)}:
        try:result=float(grouped[Fraction(0)])
        except OverflowError as exc:raise ValueError("nonfinite PV") from exc
    else:
        terms=[]
        with localcontext(Context(prec=2000)):
            for exponent,amount in sorted(grouped.items()):
                if exponent>10000:
                    raise ValueError("schedule growth outside supported range")
                if exponent < -10000:
                    continue
                terms.append(_payment_decimal(amount)*_payment_decimal(exponent).exp())
            if not terms:
                return 0.0
            value=sum(terms,Decimal(0))
            if not value:
                raise ValueError("signed sum unresolved at supported precision")
            result=float(value)
    if not math.isfinite(result):
        raise ValueError("nonfinite PV")
    return result

def _payment_decimal(value):
    return Decimal(value.numerator)/Decimal(value.denominator)

def _decay_average(x):
    # (1-exp(-x))/x on x>=0,including its continuous value at0.
    if not x:
        return Decimal(1)
    if x>10000:
        return 1/x
    if x<Decimal(".1"):
        term=total=Decimal(1)
        for k in range(1,2000):
            term*=(-x)/(k+1)
            updated=total+term
            if updated==total:
                return total
            total=updated
        raise ValueError("payment series did not converge")
    return (1-(-x).exp())/x

def equal_payment_pv(payment_rate,rate,horizon,n,timing="end"):
    c,r,t=finite(payment_rate,"payment_rate"),finite(rate,"rate"),valid_horizon(horizon)
    n=valid_count(n)
    if timing not in ("begin","mid","end"):
        raise ValueError("timing must be begin, mid, or end")
    if n.bit_length()>MAX_PAYMENT_COUNT_BITS:
        raise ValueError("payment count outside supported integer-size budget")
    if c==0 or t==0:
        return 0.0
    C,R,T=Fraction(c),Fraction(r),Fraction(t)
    full=R*T
    offset={"begin":Fraction(0),"mid":Fraction(1,2),"end":Fraction(1)}[timing]
    step=abs(full)/n
    dominant=-step*offset if full>=0 else step*(n-1+offset)
    # With the declared count-size and float inputs,these cutoffs cannot
    # discard a reportable compensated result. Final underflow remains0.
    if dominant>10000:
        raise ValueError("nonfinite PV")
    if dominant < -10000:
        return 0.0
    with localcontext(Context(prec=800)):
        value=_payment_decimal(C*T)
        if full:
            value*=_decay_average(_payment_decimal(abs(full)))/_decay_average(_payment_decimal(step))
            value*=_payment_decimal(dominant).exp()
        result=float(value)
    if not math.isfinite(result):
        raise ValueError("nonfinite PV")
    return result

def timing_ratio(rate,horizon,n,timing="end"):
    r,t=finite(rate,"rate"),valid_horizon(horizon)
    n=valid_count(n)
    if timing not in ("begin","mid","end"):
        raise ValueError("unknown timing")
    if n.bit_length()>MAX_PAYMENT_COUNT_BITS:
        raise ValueError("ratio count outside supported integer-size budget")
    x=Fraction(r)*Fraction(t)/n
    if not x:
        return 1.0
    offset={"begin":Fraction(0),"mid":Fraction(1,2),"end":Fraction(1)}[timing]
    magnitude=abs(x)
    exponent=-magnitude*(offset if x>0 else 1-offset)
    if exponent < -10000:
        return 0.0
    with localcontext(Context(prec=800)):
        result=float(_payment_decimal(exponent).exp()/_decay_average(_payment_decimal(magnitude)))
    if not math.isfinite(result):
        raise ValueError("nonfinite ratio")
    return result

def comparison(payment_rate=1200,rate=0.06,horizon=2):
    c,r,t=finite(payment_rate,"payment_rate"),finite(rate,"rate"),valid_horizon(horizon)
    total=Fraction(c)*Fraction(t)
    try:nominal_total=float(total)
    except OverflowError as exc:raise ValueError("nominal total outside report range") from exc
    if not math.isfinite(nominal_total):
        raise ValueError("nominal total outside report range")
    reference=continuous_pv(c,r,t)
    rows=[]
    for n in (2,8,24,730):
        row={"n":n,"payment_amount":float(total/n),"nominal_total":nominal_total}
        for timing in ("begin","mid","end"):
            value=equal_payment_pv(c,r,t,n,timing)
            row[timing+"_pv"]=value
            row[timing+"_difference"]=value-reference
        rows.append(row)
    return {"continuous_pv":reference,"scenarios":rows,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(comparison(),indent=2,allow_nan=False))
