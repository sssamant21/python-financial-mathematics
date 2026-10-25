"""Section 12.4: labeled Gaussian elimination with partial pivoting."""
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
        labels=checked_labels(self.labels,"vector labels")
        values=tuple(self.values)
        if len(labels)!=len(values):
            raise ValueError("vector shape mismatch")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(x,"vector component") for x in values))
    def align(self,labels):
        target=checked_labels(labels,"target labels")
        if len(target)!=len(self.labels) or set(target)!=set(self.labels):
            raise ValueError("equation labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit)

@dataclass(frozen=True)
class Matrix:
    equation_labels: tuple
    unknown_labels: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        equations=checked_labels(self.equation_labels,"equation labels")
        unknowns=checked_labels(self.unknown_labels,"unknown labels")
        data=tuple(tuple(row) for row in self.rows)
        if len(data)!=len(equations) or any(len(row)!=len(unknowns) for row in data):
            raise ValueError("ragged or mismatched coefficient matrix")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"equation_labels",equations)
        object.__setattr__(self,"unknown_labels",unknowns)
        object.__setattr__(self,"rows",tuple(tuple(finite(x,"matrix entry") for x in row) for row in data))

def solve(matrix,target,pivot_tolerance=1e-12):
    if not isinstance(matrix,Matrix) or not isinstance(target,Vector):
        raise TypeError("expected Matrix and Vector")
    if matrix.unit!="standardized_sensitivity" or target.unit!="standardized_exposure":
        raise ValueError("unit mismatch")
    tolerance=finite(pivot_tolerance,"pivot tolerance")
    if tolerance<=0:
        raise ValueError("pivot tolerance must be positive")
    n=len(matrix.unknown_labels)
    if n!=len(matrix.equation_labels):
        raise ValueError("square system required")
    rhs=target.align(matrix.equation_labels)
    a=[list(row) for row in matrix.rows]
    b=list(rhs.values)
    scale=max(abs(v) for row in a for v in row)
    if scale==0:
        raise ValueError("singular matrix")
    for k in range(n):
        pivot=max(range(k,n),key=lambda i:abs(a[i][k]))
        if abs(a[pivot][k])<=tolerance*scale:
            raise ValueError("singular or numerically unresolved pivot")
        if pivot!=k:
            a[k],a[pivot]=a[pivot],a[k]
            b[k],b[pivot]=b[pivot],b[k]
        for i in range(k+1,n):
            multiplier=finite(a[i][k]/a[k][k],"elimination multiplier")
            a[i][k]=0.0
            for j in range(k+1,n):
                a[i][j]=finite(a[i][j]-multiplier*a[k][j],"elimination entry")
            b[i]=finite(b[i]-multiplier*b[k],"elimination RHS")
    x=[0.0]*n
    for i in range(n-1,-1,-1):
        tail=math.fsum(finite(a[i][j]*x[j],"back-substitution term") for j in range(i+1,n))
        x[i]=finite((b[i]-tail)/a[i][i],"solution component")
    residual=[finite(rhs.values[i]-math.fsum(finite(matrix.rows[i][j]*x[j],"residual term") for j in range(n)),"residual") for i in range(n)]
    matrix_norm=max(math.fsum(abs(v) for v in row) for row in matrix.rows)
    x_norm=max(abs(v) for v in x)
    rhs_norm=max(abs(v) for v in rhs.values)
    denominator=finite(matrix_norm*x_norm+rhs_norm,"residual denominator")
    relative=finite(max(abs(v) for v in residual)/denominator if denominator else 0.0,"relative residual")
    return {"solution":dict(zip(matrix.unknown_labels,x)),
            "residual":dict(zip(matrix.equation_labels,residual)),
            "relative_residual_inf":relative,
            "runtime_certified":False}

def assessment():
    a=Matrix(("RATE","CREDIT"),("BOND_A","BOND_B"),
             ((2,1),(1,-1)),"standardized_sensitivity")
    b=Vector(("CREDIT","RATE"),(1,5),"standardized_exposure")
    zero_pivot=Matrix(("E1","E2"),("X","Y"),((0,1),(2,3)),"standardized_sensitivity")
    rhs=Vector(("E1","E2"),(1,5),"standardized_exposure")
    return {"financial_match":solve(a,b),"zero_pivot_case":solve(zero_pivot,rhs),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
