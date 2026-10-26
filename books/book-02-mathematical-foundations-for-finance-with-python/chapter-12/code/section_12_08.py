"""Section 12.8: financial residuals and factor-specific acceptance."""
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

def labels_checked(values,name):
    labels=tuple(values)
    if not labels or any(type(x) is not str or not x.strip() for x in labels):
        raise ValueError(f"{name}: nonempty string labels required")
    if len(set(labels))!=len(labels):
        raise ValueError(f"{name}: duplicate labels")
    return labels

@dataclass(frozen=True)
class Vector:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=labels_checked(self.labels,"vector labels")
        values=tuple(self.values)
        if len(labels)!=len(values):
            raise ValueError("vector length mismatch")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"vector value") for v in values))
    def align(self,labels):
        target=labels_checked(labels,"target labels")
        if len(target)!=len(self.labels) or set(target)!=set(self.labels):
            raise ValueError("factor labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[label] for label in target),self.unit)

@dataclass(frozen=True)
class ExposureMatrix:
    factors: tuple
    instruments: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        factors=labels_checked(self.factors,"factors")
        instruments=labels_checked(self.instruments,"instruments")
        rows=tuple(tuple(row) for row in self.rows)
        if len(rows)!=len(factors) or any(len(row)!=len(instruments) for row in rows):
            raise ValueError("ragged or mismatched matrix")
        if self.unit!="standardized_sensitivity":
            raise ValueError("matrix unit mismatch")
        object.__setattr__(self,"factors",factors)
        object.__setattr__(self,"instruments",instruments)
        object.__setattr__(self,"rows",tuple(tuple(finite(v,"matrix entry") for v in row) for row in rows))

def evaluate(matrix,positions,target,tolerances):
    if not isinstance(matrix,ExposureMatrix) or not all(isinstance(v,Vector) for v in (positions,target,tolerances)):
        raise TypeError("expected ExposureMatrix and Vector operands")
    if (positions.unit,target.unit,tolerances.unit)!=("quantity","standardized_exposure","standardized_exposure"):
        raise ValueError("unit mismatch")
    p=positions.align(matrix.instruments)
    b=target.align(matrix.factors)
    limits=tolerances.align(matrix.factors)
    if any(value<0 for value in limits.values):
        raise ValueError("tolerances must be nonnegative")
    achieved=tuple(finite(math.fsum(finite(a*x,"exposure product") for a,x in zip(row,p.values)),"achieved exposure") for row in matrix.rows)
    residual=tuple(finite(b.values[i]-achieved[i],"residual") for i in range(len(matrix.factors)))
    abs_residual=tuple(abs(v) for v in residual)
    residual_inf=max(abs_residual)
    target_inf=max(abs(v) for v in b.values)
    matrix_inf=max(math.fsum(abs(v) for v in row) for row in matrix.rows)
    positions_inf=max(abs(v) for v in p.values)
    denominator=finite(matrix_inf*positions_inf+target_inf,"normalizer")
    relative_target=residual_inf/target_inf if target_inf else (0.0 if residual_inf==0 else None)
    backward=residual_inf/denominator if denominator else (0.0 if residual_inf==0 else None)
    passed={label:abs_residual[i]<=limits.values[i] for i,label in enumerate(matrix.factors)}
    return {"positions":dict(zip(matrix.instruments,p.values)),
            "target":dict(zip(matrix.factors,b.values)),
            "achieved":dict(zip(matrix.factors,achieved)),
            "residual_target_minus_actual":dict(zip(matrix.factors,residual)),
            "tolerances":dict(zip(matrix.factors,limits.values)),
            "factor_pass":passed,"accepted":all(passed.values()),
            "residual_inf":finite(residual_inf,"residual norm"),
            "relative_target_residual_inf":finite(relative_target,"relative residual") if relative_target is not None else None,
            "normwise_backward_error_inf":finite(backward,"backward error") if backward is not None else None,
            "runtime_certified":False}

def assessment():
    a=ExposureMatrix(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),"standardized_sensitivity")
    b=Vector(("CREDIT","RATE"),(1,5),"standardized_exposure")
    limits=Vector(("CREDIT","RATE"),(0.10,0.15),"standardized_exposure")
    return {"exact":evaluate(a,Vector(("BOND_A","BOND_B"),(2,1),"quantity"),b,limits),
            "imperfect":evaluate(a,Vector(("BOND_B","BOND_A"),(1.1,1.9),"quantity"),b,limits),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
