"""Section 11.8: safe shapes, broadcasting and financial alignment."""
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

def labels_checked(labels):
    labels=tuple(labels)
    if not labels or any(type(x) is not str or not x.strip() for x in labels):
        raise ValueError("nonempty string labels required")
    if len(set(labels))!=len(labels):
        raise ValueError("duplicate labels")
    return labels

@dataclass(frozen=True)
class Vector:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=labels_checked(self.labels)
        values=tuple(self.values)
        if len(labels)!=len(values):
            raise ValueError("shape mismatch")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"component") for v in values))
    def align(self,labels):
        target=labels_checked(labels)
        if len(target)!=len(self.labels) or set(target)!=set(self.labels):
            raise ValueError("asset labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit)

@dataclass(frozen=True)
class Matrix:
    row_labels: tuple
    column_labels: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        dates=labels_checked(self.row_labels)
        assets=labels_checked(self.column_labels)
        rows=tuple(tuple(row) for row in self.rows)
        if len(rows)!=len(dates) or any(len(row)!=len(assets) for row in rows):
            raise ValueError("matrix shape mismatch")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"row_labels",dates)
        object.__setattr__(self,"column_labels",assets)
        object.__setattr__(self,"rows",tuple(tuple(finite(v,"matrix component") for v in row) for row in rows))

def broadcast_shape(left,right):
    left=tuple(left)
    right=tuple(right)
    for dim in left+right:
        if type(dim) is not int or dim<0:
            raise ValueError("shape dimensions must be nonnegative integers")
    result=[]
    for a,b in zip(reversed(left),reversed(right)):
        if a!=b and a!=1 and b!=1:
            raise ValueError("incompatible broadcast dimensions")
        result.append(b if a==1 else a)
    longer=left if len(left)>len(right) else right
    result.extend(reversed(longer[:abs(len(left)-len(right))]))
    return tuple(reversed(result))

def market_value(prices,holdings):
    if not isinstance(prices,Vector) or not isinstance(holdings,Vector):
        raise TypeError("expected vectors")
    if prices.unit!="USD/share" or holdings.unit!="shares":
        raise ValueError("price/holdings unit mismatch")
    aligned=holdings.align(prices.labels)
    return finite(math.fsum(finite(p*q,"position value") for p,q in zip(prices.values,aligned.values)),"market value")

def portfolio_returns(matrix,weights):
    if not isinstance(matrix,Matrix) or not isinstance(weights,Vector):
        raise TypeError("expected Matrix and Vector")
    if matrix.unit!="simple_return" or weights.unit!="weight":
        raise ValueError("return/weight unit mismatch")
    aligned=weights.align(matrix.column_labels)
    if not math.isclose(math.fsum(aligned.values),1,rel_tol=1e-12,abs_tol=1e-12):
        raise ValueError("weights must sum to one")
    values=tuple(finite(math.fsum(finite(r*w,"weighted return component") for r,w in zip(row,aligned.values)),"portfolio return") for row in matrix.rows)
    return dict(zip(matrix.row_labels,values))

def assessment():
    prices=Vector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    holdings=Vector(("GAMMA","ALPHA","BETA"),(10,2,4),"shares")
    returns=Matrix(("DAY1","DAY2"),("GAMMA","ALPHA","BETA"),
                   ((0.03,0.01,-0.02),(-0.01,0.02,0.01)),"simple_return")
    weights=Vector(("ALPHA","BETA","GAMMA"),(0.5,0.3,0.2),"weight")
    return {"market_value_USD":market_value(prices,holdings),
            "portfolio_returns":portfolio_returns(returns,weights),
            "broadcast_4x3_and_3":broadcast_shape((4,3),(3,)),
            "broadcast_3x1_and_3":broadcast_shape((3,1),(3,)),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
