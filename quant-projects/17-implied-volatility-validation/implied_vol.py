"""Bounded synthetic European option implied volatility; no trading or market data."""
import math
import argparse
from statistics import NormalDist
N=NormalDist()
def bounds(kind,s,k,t,r,q=0):
    if kind not in ("call","put") or any(isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) for x in (s,k,t,r,q)):
        raise ValueError("invalid input")
    if s<=0 or k<=0 or not 0<t<=30 or abs(r)>1 or abs(q)>1:
        raise ValueError("outside educational limits")
    a=s*math.exp(-q*t); b=k*math.exp(-r*t)
    return (max(0,a-b),a) if kind=="call" else (max(0,b-a),b)
def price(kind,s,k,t,r,v,q=0):
    bounds(kind,s,k,t,r,q)
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<v<=5:
        raise ValueError("invalid volatility")
    d1=(math.log(s/k)+(r-q+v*v/2)*t)/(v*math.sqrt(t)); d2=d1-v*math.sqrt(t)
    a=s*math.exp(-q*t); b=k*math.exp(-r*t)
    return max(0,a*N.cdf(d1)-b*N.cdf(d2)) if kind=="call" else max(0,b*N.cdf(-d2)-a*N.cdf(-d1))
def implied_vol(kind,s,k,t,r,quote,q=0,low=1e-6,high=3.0,tol=1e-8,iterations=150):
    lower,upper=bounds(kind,s,k,t,r,q)
    if isinstance(quote,bool) or not isinstance(quote,(float,int)) or not math.isfinite(quote) or not lower<quote<upper:
        raise ValueError("quote outside strict no-arbitrage bounds")
    if not (math.isfinite(low) and math.isfinite(high) and 0<low<high<=5 and math.isfinite(tol) and 0<tol<=1e-3 and type(iterations)==int and 1<=iterations<=1000):
        raise ValueError("invalid solver controls")
    if not price(kind,s,k,t,r,low,q)<=quote<=price(kind,s,k,t,r,high,q):
        raise ValueError("quote outside volatility bracket")
    for _ in range(iterations):
        mid=(low+high)/2
        p=price(kind,s,k,t,r,mid,q)
        if abs(p-quote)<=tol: return mid
        if p<quote: low=mid
        else: high=mid
    raise ArithmeticError("price residual tolerance not reached")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--kind",choices=["call","put"],default="call")
    p.add_argument("--quote",type=float,default=10.450583572185565)
    a=p.parse_args()
    v=implied_vol(a.kind,100,100,1,.05,a.quote)
    print(f"synthetic implied volatility={v:.8f}; repriced={price(a.kind,100,100,1,.05,v):.8f}")
