"""Book 02 Section 13.4: labeled orthogonal projection onto a line."""
from dataclasses import dataclass
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} out of range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def labels_checked(values,name):
    result=tuple(values)
    if not result or any(type(v) is not str or not v.strip() for v in result):
        raise ValueError(f"{name}: nonempty labels required")
    if len(set(result))!=len(result):
        raise ValueError(f"{name}: duplicate labels")
    return result

@dataclass(frozen=True)
class FactorVector:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=labels_checked(self.labels,"factor labels")
        values=tuple(self.values)
        if len(labels)!=len(values):
            raise ValueError("factor shape mismatch")
        if self.unit!="standardized_exposure":
            raise ValueError("factor unit mismatch")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"factor value") for v in values))
    def align(self,order):
        order=labels_checked(order,"factor order")
        if len(order)!=len(self.labels) or set(order)!=set(self.labels):
            raise ValueError("factor labels mismatch")
        values=dict(zip(self.labels,self.values))
        return tuple(values[k] for k in order)

def project_line(direction,target,tolerances):
    if not all(isinstance(v,FactorVector) for v in (direction,target,tolerances)):
        raise TypeError("FactorVector inputs required")
    order=direction.labels
    u=direction.values
    b=target.align(order)
    allowed=tolerances.align(order)
    if any(v<0 for v in allowed):
        raise ValueError("negative factor tolerance")
    scale=max(abs(v) for v in u)
    if scale==0:
        raise ValueError("zero direction")
    scaled=tuple(v/scale for v in u)
    denominator=finite(math.fsum(v*v for v in scaled),"scaled direction norm squared")
    numerator=finite(math.fsum(x*y for x,y in zip(scaled,b)),"scaled dot product")
    scaled_coefficient=finite(numerator/denominator,"scaled projection coefficient")
    coefficient=finite(scaled_coefficient/scale,"projection coefficient")
    p=tuple(finite(scaled_coefficient*v,"projected exposure") for v in scaled)
    r=tuple(finite(b[i]-p[i],"residual") for i in range(len(order)))
    orthogonality=finite(math.fsum(u[i]*r[i] for i in range(len(order))),"orthogonality")
    distance=finite(math.hypot(*r),"residual distance")
    passed={name:abs(r[i])<=allowed[i] for i,name in enumerate(order)}
    return {"coefficient":coefficient,
            "target":dict(zip(order,b)),
            "projected":dict(zip(order,p)),
            "residual_target_minus_projected":dict(zip(order,r)),
            "distance_l2":distance,
            "direction_dot_residual":orthogonality,
            "factor_pass":passed,
            "decision":"ACCEPT" if all(passed.values()) else "REJECT",
            "runtime_certified":False}

def assessment():
    direction=FactorVector(("RATE","CREDIT"),(1,2),"standardized_exposure")
    target=FactorVector(("CREDIT","RATE"),(7,3),"standardized_exposure")
    limits=FactorVector(("CREDIT","RATE"),(0.1,0.5),"standardized_exposure")
    exact=FactorVector(("RATE","CREDIT"),(4,8),"standardized_exposure")
    return {"approximate":project_line(direction,target,limits),
            "exact":project_line(direction,exact,limits),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
