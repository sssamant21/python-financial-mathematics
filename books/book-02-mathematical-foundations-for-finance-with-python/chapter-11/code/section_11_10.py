"""Section 11.10: comprehensive Chapter 11 assessment."""
from dataclasses import dataclass
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

@dataclass(frozen=True)
class Vector:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=tuple(self.labels)
        values=tuple(self.values)
        if not labels or len(labels)!=len(values):
            raise ValueError("labels and values must have equal positive length")
        if any(type(k) is not str or not k.strip() for k in labels):
            raise ValueError("labels must be nonempty strings")
        if len(set(labels))!=len(labels):
            raise ValueError("duplicate labels")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"component") for v in values))
    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(self.labels) or set(target)!=set(self.labels):
            raise ValueError("asset labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit)

def add(a,b):
    if a.unit!=b.unit:
        raise ValueError("unit mismatch")
    aligned=b.align(a.labels)
    return Vector(a.labels,tuple(finite(x+y,"sum") for x,y in zip(a.values,aligned.values)),a.unit)

def norm(a,kind="l2"):
    if kind=="l1":
        return finite(math.fsum(abs(x) for x in a.values),"norm")
    if kind=="l2":
        return finite(math.hypot(*a.values),"norm")
    if kind=="linf":
        return finite(max(abs(x) for x in a.values),"norm")
    raise ValueError("unsupported norm")

def project(x,d):
    if d.unit!="dimensionless":
        raise ValueError("direction must be dimensionless")
    aligned=d.align(x.labels)
    magnitude=max(abs(v) for v in aligned.values)
    if magnitude==0:
        raise ValueError("zero direction")
    scaled=tuple(v/magnitude for v in aligned.values)
    length=math.hypot(*scaled)
    unit=tuple(v/length for v in scaled)
    scalar=finite(math.fsum(a*b for a,b in zip(x.values,unit)),"scalar projection")
    return Vector(x.labels,tuple(finite(scalar*v,"projection") for v in unit),x.unit)

def portfolio(prices,holdings,nav,returns):
    if prices.unit!="USD/share" or holdings.unit!="shares" or returns.unit!="simple_return":
        raise ValueError("incorrect financial units")
    nav=finite(nav,"NAV")
    if nav<=0:
        raise ValueError("NAV must be positive")
    q=holdings.align(prices.labels)
    r=returns.align(prices.labels)
    values=tuple(finite(p*h,"position value") for p,h in zip(prices.values,q.values))
    weights=tuple(finite(v/nav,"weight") for v in values)
    signed=finite(math.fsum(values),"signed value")
    long=finite(math.fsum(max(w,0) for w in weights),"long")
    short=finite(math.fsum(max(-w,0) for w in weights),"short")
    pnl=finite(math.fsum(finite(v*ret,"P&L component") for v,ret in zip(values,r.values)),"P&L")
    return {"values_USD":dict(zip(prices.labels,values)),
            "weights":dict(zip(prices.labels,weights)),
            "net":finite(math.fsum(weights),"net"),"gross":finite(long+short,"gross"),
            "long":long,"short":short,"unexplained_nav_gap_USD":finite(nav-signed,"NAV gap"),
            "scenario_pnl_USD":pnl,"nav_return_contribution":finite(pnl/nav,"return contribution")}

def assessment():
    a=Vector(("A","B","C"),(2,-1,3),"units")
    b=Vector(("C","A","B"),(1,-4,5),"units")
    projection=project(Vector(("X","Y"),(4,2),"USD"),
                       Vector(("Y","X"),(1,1),"dimensionless"))
    prices=Vector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    holdings=Vector(("GAMMA","ALPHA","BETA"),(800,500,-200),"shares")
    returns=Vector(("BETA","GAMMA","ALPHA"),(-0.01,0.04,0.02),"simple_return")
    return {"vector_sum":add(a,b).values,
            "l1_norm":norm(a,"l1"),"l2_norm":norm(a,"l2"),"linf_norm":norm(a,"linf"),
            "projection":projection.values,
            "portfolio":portfolio(prices,holdings,100000,returns),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
