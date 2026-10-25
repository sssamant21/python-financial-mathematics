"""Book 02 Section 12.2: label-safe matrix multiplication and transformations."""
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

def checked_labels(values,name):
    labels=tuple(values)
    if not labels or any(type(v) is not str or not v.strip() for v in labels):
        raise ValueError(f"{name}: nonempty string labels required")
    if len(set(labels))!=len(labels):
        raise ValueError(f"{name}: duplicate labels")
    return labels

@dataclass(frozen=True)
class Matrix:
    row_labels: tuple
    column_labels: tuple
    rows: tuple
    unit: str
    row_axis: str
    column_axis: str
    def __post_init__(self):
        r=checked_labels(self.row_labels,"row labels")
        c=checked_labels(self.column_labels,"column labels")
        data=tuple(tuple(row) for row in self.rows)
        if len(data)!=len(r) or any(len(row)!=len(c) for row in data):
            raise ValueError("matrix shape mismatch or ragged rows")
        if any(type(s) is not str or not s.strip() for s in (self.unit,self.row_axis,self.column_axis)):
            raise ValueError("unit and axes required")
        object.__setattr__(self,"row_labels",r)
        object.__setattr__(self,"column_labels",c)
        object.__setattr__(self,"rows",tuple(tuple(finite(v,"matrix entry") for v in row) for row in data))
    @property
    def shape(self):
        return len(self.row_labels),len(self.column_labels)

def multiply(left,right):
    if not isinstance(left,Matrix) or not isinstance(right,Matrix):
        raise TypeError("expected Matrix operands")
    if left.column_axis!=right.row_axis:
        raise ValueError("contracted axes differ")
    if left.unit!="dimensionless" or right.unit!="dimensionless":
        raise ValueError("this teaching product requires dimensionless matrices")
    if len(left.column_labels)!=len(right.row_labels) or set(left.column_labels)!=set(right.row_labels):
        raise ValueError("contracted labels differ")
    lookup={label:i for i,label in enumerate(right.row_labels)}
    order=[lookup[label] for label in left.column_labels]
    result=[]
    for row in left.rows:
        out=[]
        for j in range(right.shape[1]):
            products=(finite(row[k]*right.rows[order[k]][j],"product") for k in range(left.shape[1]))
            out.append(finite(math.fsum(products),"matrix product entry"))
        result.append(tuple(out))
    return Matrix(left.row_labels,right.column_labels,tuple(result),"dimensionless",left.row_axis,right.column_axis)

def assessment():
    a=Matrix(("R1","R2"),("K1","K2"),((1,2),(3,4)),"dimensionless","rows","inner")
    b=Matrix(("K1","K2"),("C1","C2"),((2,0),(1,3)),"dimensionless","inner","columns")
    s=Matrix(("ALPHA","BETA","GAMMA"),("RATE","CREDIT"),
             ((2,1),(-1,3),(0,4)),"dimensionless","asset","factor")
    w=Matrix(("PORTFOLIO",),("GAMMA","ALPHA","BETA"),
             ((0.2,0.5,0.3),),"dimensionless","portfolio","asset")
    t=Matrix(("CREDIT","RATE"),("BASE","STRESS"),
             ((3,-1),(1,2)),"dimensionless","factor","scenario")
    factors=multiply(w,s)
    scenarios=multiply(factors,t)
    alternate=multiply(w,multiply(s,t))
    return {"AB":multiply(a,b).rows,
            "factor_exposures":dict(zip(factors.column_labels,factors.rows[0])),
            "scenario_coordinates":dict(zip(scenarios.column_labels,scenarios.rows[0])),
            "associative_path":dict(zip(alternate.column_labels,alternate.rows[0])),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
