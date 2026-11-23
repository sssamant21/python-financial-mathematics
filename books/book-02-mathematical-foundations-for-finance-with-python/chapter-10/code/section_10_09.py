"""Section 10.9: deterministic continuous cash-flow valuation engine."""
from dataclasses import dataclass
import json
import math
from fractions import Fraction
from decimal import Decimal,Context,localcontext
from section_10_07 import integrate as _shared_integrate
from section_10_05 import (_exponential_integral as _shared_exponential_integral,
                           time_weighted_factor as _shared_time_weighted_factor,
                           _linear_pv as _shared_linear_pv)

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        y=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(y):
        raise ValueError(f"{name} must be finite")
    return y

def _scalar_report(value):
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError("nonfinite scalar result") from exc
    return finite(result,"scalar result")

def _scaled_exp(scale,exponent):
    """Complete validated binary-input value; bounded Decimal exponential."""
    if not scale:
        return 0.0
    if not exponent:
        return _scalar_report(scale)
    if exponent>10000:
        raise ValueError("unsupported growing scalar exponent")
    if exponent < -10000:
        return 0.0
    # Ordinary bounded values avoid a high-precision exponential per quadrature
    # node. Outside this range retain complete Decimal scaling before reporting.
    if abs(exponent)<=1 and Fraction(1,10**200)<=abs(scale)<=10**200:
        return _scalar_report(float(scale)*math.exp(float(exponent)))
    with localcontext(Context(prec=800)):
        coefficient=Decimal(scale.numerator)/Decimal(scale.denominator)
        power=Decimal(exponent.numerator)/Decimal(exponent.denominator)
        return _scalar_report(coefficient*power.exp())

@dataclass(frozen=True)
class Stream:
    kind: str
    a: float
    b: float=0.0
    def __post_init__(self):
        if self.kind not in ("constant","linear","exponential"):
            raise ValueError("unknown stream kind")
        finite(self.a,"a")
        finite(self.b,"b")
    def rate(self,t):
        t=finite(t,"t")
        if t<0:
            raise ValueError("negative time")
        a,b=Fraction(finite(self.a,"a")),Fraction(finite(self.b,"b"))
        time=Fraction(t)
        if self.kind=="constant":
            return _scalar_report(a)
        if self.kind=="linear":
            return _scalar_report(a+b*time)
        return _scaled_exp(a,b*time)

@dataclass(frozen=True)
class Curve:
    base: float
    slope: float=0.0
    def __post_init__(self):
        finite(self.base,"base")
        finite(self.slope,"slope")
    def discount(self,t,shift=0.0):
        t=finite(t,"t")
        if t<0:
            raise ValueError("negative time")
        shift=finite(shift,"shift")
        time=Fraction(t)
        rate=Fraction(finite(self.base,"base"))+Fraction(shift)
        slope=Fraction(finite(self.slope,"slope"))
        exponent=-rate*time-slope*time*time/2
        return _scaled_exp(Fraction(1),exponent)

def horizon(T):
    t=finite(T,"horizon")
    if t<0:
        raise ValueError("negative horizon")
    return t

def exponential_integral(a,k,T):
    a,k,t=finite(a,"a"),finite(k,"k"),horizon(T)
    # Preserve the complete binary-input value through scaling and exponentiation.
    # The shared helper retains its 800-digit/cutoff/final-underflow policies.
    return _shared_exponential_integral(Fraction(a),Fraction(k),Fraction(t))

def weighted_integral(rate,T):
    r,t=finite(rate,"rate"),horizon(T)
    return _shared_time_weighted_factor(r,t)

def analytic_pv(stream,curve,T,shift=0.0):
    if not isinstance(stream,Stream) or not isinstance(curve,Curve):
        raise TypeError("expected Stream and Curve")
    if curve.slope!=0:
        raise ValueError("analytic PV requires flat curve")
    t=horizon(T)
    shift=finite(shift,"shift")
    rate=Fraction(finite(curve.base,"base"))+Fraction(shift)
    if stream.kind=="constant":
        return _shared_exponential_integral(Fraction(finite(stream.a,"a")),-rate,Fraction(t))
    if stream.kind=="exponential":
        growth=Fraction(finite(stream.b,"b"))-rate
        return _shared_exponential_integral(Fraction(finite(stream.a,"a")),growth,Fraction(t))
    # Combine both terms before reporting: individually unreportable moments
    # can cancel, or a tiny moment can be rescued by its finite coefficient.
    return _shared_linear_pv(Fraction(finite(stream.a,"a")),
                             Fraction(finite(stream.b,"b")),rate,Fraction(t))

def simpson(f,T,n=256):
    t=horizon(T)
    if type(n) is not int or n<=0 or n%2:
        raise ValueError("n must be positive even integer")
    # Shared exact weighted sum,once-rounded grid and bounded callback work.
    return _shared_integrate(f,0.,t,n,"simpson")

def numerical_pv(stream,curve,T,n=256,shift=0.0):
    if not isinstance(stream,Stream) or not isinstance(curve,Curve):
        raise TypeError("expected Stream and Curve")
    return simpson(lambda t:stream.rate(t)*curve.discount(t,shift),T,n)

def discrete_pv(payments,curve,shift=0.0):
    if not isinstance(curve,Curve):
        raise TypeError("expected Curve")
    terms=[]
    for time,amount in payments:
        time=finite(time,"payment time")
        if time<0:
            raise ValueError("negative payment time")
        amount=finite(amount,"amount")
        terms.append(finite(amount*curve.discount(time,shift),"discounted payment"))
    return finite(math.fsum(terms),"discrete PV")

def portfolio_pv(streams,payments,curve,T,n=256,shift=0.0):
    components=[numerical_pv(s,curve,T,n,shift) for s in streams]
    discrete=discrete_pv(payments,curve,shift)
    return {"continuous_components":components,"discrete":discrete,
            "total":finite(math.fsum(components+[discrete]),"total PV")}

def parallel_shift_derivative(streams,payments,curve,T,n=256,bump=0.0001):
    bump=finite(bump,"bump")
    if bump<=0:
        raise ValueError("bump must be positive")
    if not isinstance(curve,Curve):
        raise TypeError("expected Curve")
    if not math.isfinite(curve.base+bump) or not math.isfinite(curve.base-bump) or curve.base+bump==curve.base or curve.base-bump==curve.base:
        raise ValueError("bump must produce finite distinct rate shifts")
    if not math.isfinite(2*bump):
        raise OverflowError("derivative denominator exceeds float range")
    # Both revaluations must use the same data, including one-shot iterators.
    streams=tuple(streams)
    payments=tuple(payments)
    up=portfolio_pv(streams,payments,curve,T,n,bump)["total"]
    down=portfolio_pv(streams,payments,curve,T,n,-bump)["total"]
    return finite((up-down)/(2*bump),"rate derivative")

def assessment():
    streams=[Stream("constant",1000),Stream("linear",200,50),
             Stream("exponential",150,0.02)]
    payments=[(2,500)]
    flat=Curve(0.05)
    affine=Curve(0.03,0.005)
    flat_numeric=portfolio_pv(streams,payments,flat,4,512)
    flat_exact=[analytic_pv(s,flat,4) for s in streams]
    exact_total=math.fsum(flat_exact+[discrete_pv(payments,flat)])
    affine_result=portfolio_pv(streams,payments,affine,4,512)
    return {"horizon_years":4,"units":"currency; rates 1/year",
            "flat_numeric":flat_numeric,"flat_analytic_total":exact_total,
            "flat_absolute_reconciliation":abs(flat_numeric["total"]-exact_total),
            "affine_numeric":affine_result,
            "flat_parallel_rate_derivative":parallel_shift_derivative(
                streams,payments,flat,4,512),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
