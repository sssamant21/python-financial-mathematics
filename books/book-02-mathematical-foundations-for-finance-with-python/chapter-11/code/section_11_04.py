"""Book 02 Section 11.4: labeled vector norms and distances."""
from dataclasses import dataclass
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

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
        if len(target)!=len(self.labels) or len(set(target))!=len(target) or set(target)!=set(self.labels):
            raise ValueError("labels must be a complete unique permutation")
        mapping=dict(zip(self.labels,self.values))
        return Vector(target,tuple(mapping[k] for k in target),self.unit,self.axis)

def norm(vector,kind="l2"):
    if not isinstance(vector,Vector):
        raise TypeError("expected Vector")
    if kind=="l1":
        value=math.fsum(abs(x) for x in vector.values)
    elif kind=="l2":
        value=math.hypot(*vector.values)
    elif kind=="linf":
        value=max(abs(x) for x in vector.values)
    else:
        raise ValueError("kind must be l1, l2, or linf")
    return finite(value,"norm")

def difference(left,right):
    if not isinstance(left,Vector) or not isinstance(right,Vector):
        raise TypeError("expected Vector")
    if left.axis!=right.axis or left.unit!=right.unit:
        raise ValueError("axis or unit mismatch")
    aligned=right.align(left.labels)
    return Vector(left.labels,tuple(finite(x-y,"difference") for x,y in zip(left.values,aligned.values)),left.unit,left.axis)

def distance(left,right,kind="l2"):
    return norm(difference(left,right),kind)

def relative_distance(actual,benchmark,kind="l2"):
    denominator=norm(benchmark,kind)
    if denominator==0:
        raise ValueError("relative distance undefined for zero benchmark")
    return finite(distance(actual,benchmark,kind)/denominator,"relative distance")

def assessment():
    a=Vector(("ALPHA","BETA","GAMMA"),(100000,-20000,40000),"USD")
    b=Vector(("GAMMA","ALPHA","BETA"),(50000,90000,-10000),"USD")
    delta=difference(a,b)
    return {"deviation_USD":dict(zip(delta.labels,delta.values)),
            "l1_distance_USD":distance(a,b,"l1"),
            "l2_distance_USD":distance(a,b,"l2"),
            "linf_distance_USD":distance(a,b,"linf"),
            "relative_l2_distance":relative_distance(a,b),
            "per_asset_limit_10000_USD_satisfied":norm(delta,"linf")<=10000,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
