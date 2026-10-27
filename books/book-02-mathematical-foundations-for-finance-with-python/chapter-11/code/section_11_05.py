"""Section 11.5: label-safe cosine similarity, angles, orthogonality."""
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
    axis: str="factor"
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
        if type(self.axis) is not str or not self.axis.strip():
            raise ValueError("axis required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(x,"component") for x in values))
    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(target) or set(target)!=set(self.labels):
            raise ValueError("labels must be a complete unique permutation")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit,self.axis)

def cosine(left,right):
    if not isinstance(left,Vector) or not isinstance(right,Vector):
        raise TypeError("expected Vector")
    if left.unit!=right.unit or left.axis!=right.axis:
        raise ValueError("unit or axis mismatch")
    aligned=right.align(left.labels)
    ax=max(abs(v) for v in left.values)
    ay=max(abs(v) for v in aligned.values)
    if ax==0 or ay==0:
        raise ValueError("angle undefined for zero vector")
    x=tuple(v/ax for v in left.values)
    y=tuple(v/ay for v in aligned.values)
    nx=math.hypot(*x)
    ny=math.hypot(*y)
    value=math.fsum(a*b for a,b in zip(x,y))/(nx*ny)
    return min(1.0,max(-1.0,finite(value,"cosine")))

def angle_degrees(left,right):
    # Validate types, labels, units and nonzero vectors via the shared contract.
    cosine(left,right)
    aligned=right.align(left.labels)
    ax=max(abs(v) for v in left.values)
    ay=max(abs(v) for v in aligned.values)
    x=tuple(v/ax for v in left.values)
    y=tuple(v/ay for v in aligned.values)
    nx,ny=math.hypot(*x),math.hypot(*y)
    u=tuple(v/nx for v in x)
    v=tuple(w/ny for w in y)
    # atan2 of sums/differences is stable near zero and 180 degrees.
    return math.degrees(2*math.atan2(math.hypot(*(a-b for a,b in zip(u,v))),
                                     math.hypot(*(a+b for a,b in zip(u,v)))))

def orthogonal(left,right,tolerance=1e-12):
    tolerance=finite(tolerance,"tolerance")
    if not 0<=tolerance<=1:
        raise ValueError("tolerance must be between 0 and 1")
    return abs(cosine(left,right))<=tolerance

def assessment():
    first=Vector(("RATE","CREDIT"),(2,1),"normalized_exposure")
    second=Vector(("CREDIT","RATE"),(-2,1),"normalized_exposure")
    same=Vector(first.labels,(4,2),"normalized_exposure")
    opposite=Vector(first.labels,(-2,-1),"normalized_exposure")
    return {"cosine_orthogonal":cosine(first,second),
            "angle_orthogonal_degrees":angle_degrees(first,second),
            "is_orthogonal":orthogonal(first,second),
            "angle_positive_rescale_degrees":angle_degrees(first,same),
            "angle_opposite_degrees":angle_degrees(first,opposite),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
