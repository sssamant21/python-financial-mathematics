"""Book 02 Section 11.1: immutable, label-safe financial vectors."""
from dataclasses import dataclass
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric (bool excluded)")
    try:
        v=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} out of range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

@dataclass(frozen=True)
class LabeledVector:
    labels: tuple
    values: tuple
    unit: str
    axis: str="asset"
    def __post_init__(self):
        labels=tuple(self.labels)
        values=tuple(self.values)
        if not labels or len(labels)!=len(values):
            raise ValueError("nonempty equal-length labels and values required")
        if any(type(label) is not str or not label.strip() for label in labels):
            raise ValueError("labels must be nonempty strings")
        if len(set(labels))!=len(labels):
            raise ValueError("duplicate labels")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit must be nonempty")
        if type(self.axis) is not str or not self.axis.strip():
            raise ValueError("axis must be nonempty")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"component") for v in values))

    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(target):
            raise ValueError("target labels must be unique and complete")
        if set(target)!=set(self.labels):
            raise ValueError("missing or unexpected labels")
        mapping=dict(zip(self.labels,self.values))
        return LabeledVector(target,tuple(mapping[k] for k in target),self.unit,self.axis)

def market_values(prices,holdings):
    if not isinstance(prices,LabeledVector) or not isinstance(holdings,LabeledVector):
        raise TypeError("expected labeled vectors")
    if prices.axis!="asset" or holdings.axis!="asset":
        raise ValueError("asset axis required")
    if prices.unit!="USD/share" or holdings.unit!="shares":
        raise ValueError("expected USD/share prices and shares holdings")
    aligned=holdings.align(prices.labels)
    values=tuple(finite(p*q,"position value") for p,q in zip(prices.values,aligned.values))
    return LabeledVector(prices.labels,values,"USD","asset")

def assessment():
    prices=LabeledVector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    holdings=LabeledVector(("GAMMA","ALPHA","BETA"),(10,2,4),"shares")
    positions=market_values(prices,holdings)
    incorrect=math.fsum(p*q for p,q in zip(prices.values,holdings.values))
    return {"price_labels":prices.labels,"holdings_source_labels":holdings.labels,
            "aligned_holdings":holdings.align(prices.labels).values,
            "position_values":dict(zip(positions.labels,positions.values)),
            "portfolio_total_USD":math.fsum(positions.values),
            "invalid_positional_total_USD":incorrect,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
