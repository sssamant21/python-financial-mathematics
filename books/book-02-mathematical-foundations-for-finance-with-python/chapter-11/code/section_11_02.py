"""Section 11.2: label-safe vector addition and scalar multiplication."""
from dataclasses import dataclass
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
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
    axis: str="asset"
    def __post_init__(self):
        labels=tuple(self.labels)
        values=tuple(self.values)
        if not labels or len(labels)!=len(values):
            raise ValueError("labels and values must have equal positive length")
        if any(type(x) is not str or not x.strip() for x in labels):
            raise ValueError("labels must be nonempty strings")
        if len(set(labels))!=len(labels):
            raise ValueError("duplicate labels")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        if type(self.axis) is not str or not self.axis.strip():
            raise ValueError("axis required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(x,"component") for x in values))

    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(target):
            raise ValueError("incomplete or repeated target labels")
        if set(target)!=set(self.labels):
            raise ValueError("different label universe")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit,self.axis)

def compatible(left,right):
    if not isinstance(left,Vector) or not isinstance(right,Vector):
        raise TypeError("expected Vector operands")
    if left.unit!=right.unit or left.axis!=right.axis:
        raise ValueError("unit or axis mismatch")
    return right.align(left.labels)

def add(left,right):
    aligned=compatible(left,right)
    return Vector(left.labels,tuple(finite(a+b,"sum") for a,b in zip(left.values,aligned.values)),left.unit,left.axis)

def scale(value,scalar):
    if not isinstance(value,Vector):
        raise TypeError("expected Vector")
    k=finite(scalar,"scalar")
    return Vector(value.labels,tuple(finite(k*x,"scaled component") for x in value.values),value.unit,value.axis)

def subtract(left,right):
    return add(left,scale(right,-1))

def linear_combination(a,left,b,right):
    return add(scale(left,a),scale(right,b))

def assessment():
    desk_a=Vector(("ALPHA","BETA","GAMMA"),(100000,-20000,40000),"USD")
    desk_b=Vector(("GAMMA","ALPHA","BETA"),(-10000,50000,30000),"USD")
    total=add(desk_a,desk_b)
    incorrect=tuple(a+b for a,b in zip(desk_a.values,desk_b.values))
    stressed=scale(total,1.1)
    distributed=add(scale(desk_a,1.1),scale(desk_b,1.1))
    return {"desk_a_labels":desk_a.labels,"desk_b_source_labels":desk_b.labels,
            "combined_exposure_USD":dict(zip(total.labels,total.values)),
            "signed_total_USD":math.fsum(total.values),
            "gross_total_USD":math.fsum(abs(v) for v in total.values),
            "incorrect_positional_exposures_USD":incorrect,
            "stressed_exposure_USD":dict(zip(stressed.labels,stressed.values)),
            "distributive_residual_max_USD":max(abs(a-b) for a,b in zip(stressed.values,distributed.values)),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
