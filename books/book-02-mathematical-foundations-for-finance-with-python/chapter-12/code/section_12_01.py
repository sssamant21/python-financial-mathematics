"""Book 02 Section 12.1: labeled matrices and financial factor exposures."""
from dataclasses import dataclass
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def labels_checked(values,name):
    labels=tuple(values)
    if not labels or any(type(k) is not str or not k.strip() for k in labels):
        raise ValueError(f"{name} must be nonempty strings")
    if len(set(labels))!=len(labels):
        raise ValueError(f"{name} contains duplicates")
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
            raise ValueError("vector shape mismatch")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(x,"vector component") for x in values))
    def align(self,labels):
        target=labels_checked(labels,"target labels")
        if len(target)!=len(self.labels) or set(target)!=set(self.labels):
            raise ValueError("vector labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit)

@dataclass(frozen=True)
class Matrix:
    row_labels: tuple
    column_labels: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        r=labels_checked(self.row_labels,"row labels")
        c=labels_checked(self.column_labels,"column labels")
        data=tuple(tuple(row) for row in self.rows)
        if len(data)!=len(r) or any(len(row)!=len(c) for row in data):
            raise ValueError("ragged or mismatched matrix shape")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("matrix unit required")
        object.__setattr__(self,"row_labels",r)
        object.__setattr__(self,"column_labels",c)
        object.__setattr__(self,"rows",tuple(tuple(finite(v,"matrix entry") for v in row) for row in data))
    @property
    def shape(self):
        return (len(self.row_labels),len(self.column_labels))

def aggregate_factors(weights,sensitivities):
    if not isinstance(weights,Vector) or not isinstance(sensitivities,Matrix):
        raise TypeError("expected Vector and Matrix")
    if weights.unit!="weight" or sensitivities.unit!="standardized_sensitivity":
        raise ValueError("unit mismatch")
    w=weights.align(sensitivities.row_labels)
    results=[]
    for j in range(sensitivities.shape[1]):
        terms=(finite(w.values[i]*sensitivities.rows[i][j],"factor contribution")
               for i in range(sensitivities.shape[0]))
        results.append(finite(math.fsum(terms),"factor exposure"))
    return Vector(sensitivities.column_labels,tuple(results),"standardized_exposure")

def assessment():
    S=Matrix(("ALPHA","BETA","GAMMA"),("RATE","CREDIT"),
             ((2,1),(-1,3),(0,4)),"standardized_sensitivity")
    w=Vector(("GAMMA","ALPHA","BETA"),(0.2,0.5,0.3),"weight")
    exposure=aggregate_factors(w,S)
    return {"matrix_shape":S.shape,"factor_exposures":dict(zip(exposure.labels,exposure.values)),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
