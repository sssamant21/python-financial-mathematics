"""Section 12.3: transpose, identity, diagonal and labeled multiplication."""
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

def labels_checked(values,name):
    result=tuple(values)
    if not result or any(type(k) is not str or not k.strip() for k in result):
        raise ValueError(f"{name}: nonempty string labels required")
    if len(set(result))!=len(result):
        raise ValueError(f"{name}: duplicate labels")
    return result

@dataclass(frozen=True)
class Matrix:
    row_labels: tuple
    column_labels: tuple
    rows: tuple
    unit: str
    row_axis: str
    column_axis: str
    def __post_init__(self):
        r=labels_checked(self.row_labels,"row labels")
        c=labels_checked(self.column_labels,"column labels")
        data=tuple(tuple(row) for row in self.rows)
        if len(data)!=len(r) or any(len(row)!=len(c) for row in data):
            raise ValueError("ragged or mismatched matrix")
        if any(type(x) is not str or not x.strip() for x in (self.unit,self.row_axis,self.column_axis)):
            raise ValueError("unit and axis names required")
        object.__setattr__(self,"row_labels",r)
        object.__setattr__(self,"column_labels",c)
        object.__setattr__(self,"rows",tuple(tuple(finite(v,"entry") for v in row) for row in data))
    @property
    def shape(self):
        return len(self.row_labels),len(self.column_labels)

def transpose(a):
    if not isinstance(a,Matrix):
        raise TypeError("expected Matrix")
    return Matrix(a.column_labels,a.row_labels,tuple(tuple(a.rows[i][j] for i in range(a.shape[0])) for j in range(a.shape[1])),a.unit,a.column_axis,a.row_axis)

def identity(labels,axis):
    labels=labels_checked(labels,"identity labels")
    if type(axis) is not str or not axis.strip():
        raise ValueError("axis required")
    return Matrix(labels,labels,tuple(tuple(1.0 if i==j else 0.0 for j in range(len(labels))) for i in range(len(labels))),"dimensionless",axis,axis)

def diagonal(labels,values,axis):
    labels=labels_checked(labels,"diagonal labels")
    values=tuple(finite(x,"diagonal entry") for x in values)
    if len(labels)!=len(values):
        raise ValueError("diagonal length mismatch")
    if type(axis) is not str or not axis.strip():
        raise ValueError("axis required")
    return Matrix(labels,labels,tuple(tuple(values[i] if i==j else 0.0 for j in range(len(labels))) for i in range(len(labels))),"dimensionless",axis,axis)

def multiply(a,b):
    if not isinstance(a,Matrix) or not isinstance(b,Matrix):
        raise TypeError("expected matrices")
    if a.column_axis!=b.row_axis or len(a.column_labels)!=len(b.row_labels) or set(a.column_labels)!=set(b.row_labels):
        raise ValueError("contracted axis or labels mismatch")
    if a.unit!="dimensionless" or b.unit!="dimensionless":
        raise ValueError("this lab expects dimensionless matrices")
    order={label:i for i,label in enumerate(b.row_labels)}
    data=[]
    for row in a.rows:
        out=[]
        for j in range(b.shape[1]):
            out.append(finite(math.fsum(finite(row[k]*b.rows[order[label]][j],"product") for k,label in enumerate(a.column_labels)),"matrix entry"))
        data.append(tuple(out))
    return Matrix(a.row_labels,b.column_labels,tuple(data),"dimensionless",a.row_axis,b.column_axis)

def assessment():
    s=Matrix(("ALPHA","BETA","GAMMA"),("RATE","CREDIT"),((2,1),(-1,3),(0,4)),"dimensionless","asset","factor")
    d=diagonal(("GAMMA","ALPHA","BETA"),(0.2,0.5,0.3),"asset")
    weighted=multiply(d,s)
    ordered={name:weighted.rows[i] for i,name in enumerate(weighted.row_labels)}
    totals={name:finite(math.fsum(ordered[asset][j] for asset in s.row_labels),"factor total") for j,name in enumerate(s.column_labels)}
    return {"transpose_shape":transpose(s).shape,
            "weighted_rows":ordered,
            "factor_exposures":totals,
            "identity_preserves_matrix":multiply(identity(s.row_labels,"asset"),s).rows==s.rows,
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
