"""Section 11.7: label-safe portfolio weights and exposure constraints."""
from dataclasses import dataclass
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric (bool excluded)")
    try:
        value=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value

@dataclass(frozen=True)
class Vector:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=tuple(self.labels)
        values=tuple(self.values)
        if not labels or len(labels)!=len(values):
            raise ValueError("nonempty matching labels and values required")
        if any(type(x) is not str or not x.strip() for x in labels):
            raise ValueError("labels must be nonempty strings")
        if len(set(labels))!=len(labels):
            raise ValueError("duplicate labels")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"component") for v in values))
    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(target) or set(target)!=set(self.labels):
            raise ValueError("labels must be a complete unique permutation")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit)

def weights_from_values(values,nav):
    if not isinstance(values,Vector) or values.unit!="USD":
        raise ValueError("expected USD position values")
    nav=finite(nav,"NAV")
    if nav<=0:
        raise ValueError("NAV must be positive")
    return Vector(values.labels,tuple(finite(v/nav,"weight") for v in values.values),"weight")

def values_from_holdings(prices,holdings):
    if not isinstance(prices,Vector) or not isinstance(holdings,Vector):
        raise TypeError("expected vectors")
    if prices.unit!="USD/share" or holdings.unit!="shares":
        raise ValueError("expected USD/share and shares")
    aligned=holdings.align(prices.labels)
    return Vector(prices.labels,tuple(finite(p*q,"position value") for p,q in zip(prices.values,aligned.values)),"USD")

def exposures(weights):
    if not isinstance(weights,Vector) or weights.unit!="weight":
        raise ValueError("expected weights")
    long=math.fsum(max(w,0) for w in weights.values)
    short=math.fsum(max(-w,0) for w in weights.values)
    return {"net":finite(math.fsum(weights.values),"net"),
            "long":finite(long,"long"),"short":finite(short,"short"),
            "gross":finite(long+short,"gross")}

def check_constraints(weights,budget=1.0,long_only=False,absolute_cap=None,gross_cap=None,tolerance=1e-10):
    if not isinstance(weights,Vector) or weights.unit!="weight":
        raise ValueError("expected weights")
    budget=finite(budget,"budget")
    tolerance=finite(tolerance,"tolerance")
    if tolerance<0 or tolerance>1e-6:
        raise ValueError("tolerance outside allowed range")
    if type(long_only) is not bool:
        raise TypeError("long_only must be bool")
    if absolute_cap is not None:
        absolute_cap=finite(absolute_cap,"absolute cap")
        if absolute_cap<0:
            raise ValueError("absolute cap must be nonnegative")
    if gross_cap is not None:
        gross_cap=finite(gross_cap,"gross cap")
        if gross_cap<0:
            raise ValueError("gross cap must be nonnegative")
    exp=exposures(weights)
    breaches=[]
    if abs(exp["net"]-budget)>tolerance:
        breaches.append("budget")
    if long_only:
        breaches.extend(f"long_only:{label}" for label,w in zip(weights.labels,weights.values) if w< -tolerance)
    if absolute_cap is not None:
        breaches.extend(f"absolute_cap:{label}" for label,w in zip(weights.labels,weights.values) if abs(w)>absolute_cap+tolerance)
    if gross_cap is not None and exp["gross"]>gross_cap+tolerance:
        breaches.append("gross_cap")
    return {"feasible":not breaches,"breaches":breaches,"exposures":exp}

def assessment():
    prices=Vector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    holdings=Vector(("GAMMA","ALPHA","BETA"),(800,500,600),"shares")
    values=values_from_holdings(prices,holdings)
    weights=weights_from_values(values,100000)
    long_only=check_constraints(weights,long_only=True,absolute_cap=0.6,gross_cap=1.0)
    short_weights=weights_from_values(Vector(prices.labels,(120000,-40000,20000),"USD"),100000)
    short_report=check_constraints(short_weights,long_only=True,absolute_cap=0.6,gross_cap=1.5)
    return {"position_values_USD":dict(zip(values.labels,values.values)),
            "long_only_weights":dict(zip(weights.labels,weights.values)),
            "long_only_policy":long_only,
            "long_short_exposures":exposures(short_weights),
            "long_short_policy":short_report,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
