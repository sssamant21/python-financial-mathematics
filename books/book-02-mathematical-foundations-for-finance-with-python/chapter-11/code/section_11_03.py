"""Section 11.3: label-safe inner products and financial valuation."""
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
class Vector:
    labels: tuple
    values: tuple
    unit: str
    axis: str="asset"
    def __post_init__(self):
        labels=tuple(self.labels)
        values=tuple(self.values)
        if not labels or len(labels)!=len(values):
            raise ValueError("nonempty matching labels and values required")
        if any(type(k) is not str or not k.strip() for k in labels):
            raise ValueError("labels must be nonempty strings")
        if len(set(labels))!=len(labels):
            raise ValueError("duplicate labels")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        if type(self.axis) is not str or not self.axis.strip():
            raise ValueError("axis required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"component") for v in values))
    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(target) or set(target)!=set(self.labels):
            raise ValueError("labels must be a complete unique permutation")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit,self.axis)

def dot(left,right):
    if not isinstance(left,Vector) or not isinstance(right,Vector):
        raise TypeError("expected Vector operands")
    if left.axis!=right.axis:
        raise ValueError("axis mismatch")
    aligned=right.align(left.labels)
    terms=[finite(x*y,"component product") for x,y in zip(left.values,aligned.values)]
    return finite(math.fsum(terms),"dot product")

def market_value(prices,holdings):
    if prices.unit!="USD/share" or holdings.unit!="shares" or prices.axis!="asset" or holdings.axis!="asset":
        raise ValueError("expected asset prices USD/share and holdings shares")
    return dot(prices,holdings)

def gross_notional(prices,holdings):
    if prices.unit!="USD/share" or holdings.unit!="shares" or prices.axis!="asset" or holdings.axis!="asset":
        raise ValueError("expected asset prices USD/share and holdings shares")
    aligned=holdings.align(prices.labels)
    return finite(math.fsum(abs(finite(p*q,"position value")) for p,q in zip(prices.values,aligned.values)),"gross")

def weighted_return(weights,returns):
    if weights.unit!="weight" or returns.unit!="simple_return" or weights.axis!="asset" or returns.axis!="asset":
        raise ValueError("expected asset weights and simple returns")
    if not math.isclose(math.fsum(weights.values),1.0,rel_tol=1e-10,abs_tol=1e-10):
        raise ValueError("weights must sum to one")
    return dot(weights,returns)

def factor_pnl(sensitivities,shocks):
    if sensitivities.unit!="USD/factor_unit" or shocks.unit!="factor_unit" or sensitivities.axis!="factor" or shocks.axis!="factor":
        raise ValueError("expected factor sensitivities and shocks")
    return dot(sensitivities,shocks)

def assessment():
    labels=("ALPHA","BETA","GAMMA")
    prices=Vector(labels,(100,50,25),"USD/share")
    holdings=Vector(("GAMMA","ALPHA","BETA"),(10,2,4),"shares")
    short=Vector(labels,(2,-4,10),"shares")
    weights=Vector(labels,(0.5,0.3,0.2),"weight")
    returns=Vector(("GAMMA","ALPHA","BETA"),(0.04,0.02,-0.01),"simple_return")
    sensitivities=Vector(("FACTOR_A","FACTOR_B"),(10000,-5000),"USD/factor_unit","factor")
    shocks=Vector(("FACTOR_B","FACTOR_A"),(-0.02,0.01),"factor_unit","factor")
    return {"portfolio_value_USD":market_value(prices,holdings),
            "signed_short_portfolio_value_USD":market_value(prices,short),
            "gross_short_portfolio_notional_USD":gross_notional(prices,short),
            "weighted_simple_return":weighted_return(weights,returns),
            "linear_factor_pnl_USD":factor_pnl(sensitivities,shocks),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
