"""Section 11.6: label-safe projection onto a direction."""
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
    axis: str="asset"
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
        object.__setattr__(self,"values",tuple(finite(v,"component") for v in values))
    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(target) or set(target)!=set(self.labels):
            raise ValueError("labels must be a complete unique permutation")
        mapping=dict(zip(self.labels,self.values))
        return Vector(target,tuple(mapping[k] for k in target),self.unit,self.axis)

def projection(vector,direction):
    if not isinstance(vector,Vector) or not isinstance(direction,Vector):
        raise TypeError("expected Vector")
    if vector.axis!=direction.axis or direction.unit!="dimensionless":
        raise ValueError("expected matching axis and dimensionless direction")
    aligned=direction.align(vector.labels)
    maximum=max(abs(v) for v in aligned.values)
    if maximum==0:
        raise ValueError("zero direction")
    scaled=tuple(v/maximum for v in aligned.values)
    length=math.hypot(*scaled)
    unit_direction=tuple(v/length for v in scaled)
    signed_length=finite(math.fsum(x*u for x,u in zip(vector.values,unit_direction)),"scalar projection")
    projected=Vector(vector.labels,tuple(finite(signed_length*u,"projection component") for u in unit_direction),vector.unit,vector.axis)
    residual=Vector(vector.labels,tuple(finite(x-p,"residual component") for x,p in zip(vector.values,projected.values)),vector.unit,vector.axis)
    coefficient=finite(signed_length/(maximum*length),"projection coefficient")
    return {"coefficient":coefficient,"scalar_projection":signed_length,
            "projection":projected,"residual":residual}

def assessment():
    exposure=Vector(("ALPHA","BETA","GAMMA"),(100,50,-20),"USD")
    direction=Vector(("GAMMA","ALPHA","BETA"),(0,1,1),"dimensionless")
    result=projection(exposure,direction)
    p=result["projection"]
    e=result["residual"]
    aligned=direction.align(exposure.labels)
    orthogonality=math.fsum(x*y for x,y in zip(e.values,aligned.values))
    energy_error=math.fsum(x*x for x in exposure.values)-math.fsum(x*x for x in p.values)-math.fsum(x*x for x in e.values)
    return {"projection_coefficient_USD":result["coefficient"],
            "signed_scalar_projection_USD":result["scalar_projection"],
            "projected_exposures_USD":dict(zip(p.labels,p.values)),
            "residual_exposures_USD":dict(zip(e.labels,e.values)),
            "residual_dot_direction":orthogonality,
            "pythagorean_squared_error":energy_error,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
