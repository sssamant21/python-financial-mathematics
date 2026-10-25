"""Section 10.9: deterministic continuous cash-flow valuation engine."""
from dataclasses import dataclass
import json
import math

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
        if self.kind=="constant":
            result=self.a
        elif self.kind=="linear":
            result=self.a+self.b*t
        else:
            result=self.a*math.exp(self.b*t)
        return finite(result,"payment rate")

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
        return finite(math.exp(-(self.base+shift)*t-0.5*self.slope*t*t),"discount")

def horizon(T):
    t=finite(T,"horizon")
    if t<0:
        raise ValueError("negative horizon")
    return t

def exponential_integral(a,k,T):
    a,k,t=finite(a,"a"),finite(k,"k"),horizon(T)
    x=k*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    result=a*t if x==0 else a*t*math.expm1(x)/x
    return finite(result,"integral")

def weighted_integral(rate,T):
    r,t=finite(rate,"rate"),horizon(T)
    x=r*t
    if not math.isfinite(x):
        raise ValueError("nonfinite exponent")
    if abs(x)<0.1:
        term=0.5
        total=term
        for k in range(1,100):
            term*=(-x)*(k+1)/(k*(k+2))
            total+=term
            if abs(term)<=1e-16*max(1,abs(total)):
                break
        return finite(t*t*total,"weighted integral")
    return finite(t*t*(-math.expm1(-x)-x*math.exp(-x))/(x*x),"weighted integral")

def analytic_pv(stream,curve,T,shift=0.0):
    if not isinstance(stream,Stream) or not isinstance(curve,Curve):
        raise TypeError("expected Stream and Curve")
    if curve.slope!=0:
        raise ValueError("analytic PV requires flat curve")
    t=horizon(T)
    r=curve.base+finite(shift,"shift")
    if stream.kind=="constant":
        return exponential_integral(stream.a,-r,t)
    if stream.kind=="exponential":
        return exponential_integral(stream.a,stream.b-r,t)
    return finite(exponential_integral(stream.a,-r,t)+stream.b*weighted_integral(r,t),"PV")

def simpson(f,T,n=256):
    t=horizon(T)
    if type(n) is not int or n<=0 or n%2:
        raise ValueError("n must be positive even integer")
    if t==0:
        return 0.0
    h=t/n
    terms=[finite(f(0),"integrand"),finite(f(t),"integrand")]
    terms.extend((4 if i%2 else 2)*finite(f(i*h),"integrand") for i in range(1,n))
    return finite(h*math.fsum(terms)/3,"integral")

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
