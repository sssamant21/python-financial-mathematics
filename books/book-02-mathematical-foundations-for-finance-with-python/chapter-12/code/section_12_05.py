"""Section 12.5: classify existence of solutions using numerical rank."""
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
    labels=tuple(values)
    if not labels or any(type(x) is not str or not x.strip() for x in labels):
        raise ValueError(f"{name}: nonempty string labels required")
    if len(set(labels))!=len(labels):
        raise ValueError(f"{name}: duplicate labels")
    return labels

@dataclass(frozen=True)
class Matrix:
    equation_labels: tuple
    unknown_labels: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        eq=labels_checked(self.equation_labels,"equation labels")
        un=labels_checked(self.unknown_labels,"unknown labels")
        rows=tuple(tuple(row) for row in self.rows)
        if len(rows)!=len(eq) or any(len(row)!=len(un) for row in rows):
            raise ValueError("ragged or mismatched matrix shape")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("matrix unit required")
        object.__setattr__(self,"equation_labels",eq)
        object.__setattr__(self,"unknown_labels",un)
        object.__setattr__(self,"rows",tuple(tuple(finite(x,"coefficient") for x in row) for row in rows))

@dataclass(frozen=True)
class Vector:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=labels_checked(self.labels,"target labels")
        values=tuple(self.values)
        if len(labels)!=len(values):
            raise ValueError("target shape mismatch")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("target unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(x,"target") for x in values))
    def align(self,labels):
        target=labels_checked(labels,"equation labels")
        if len(target)!=len(self.labels) or set(target)!=set(self.labels):
            raise ValueError("equation labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[x] for x in target),self.unit)

def column_scaled(rows):
    """Normalize each nonzero column by its maximum absolute entry."""
    scales=tuple(max(abs(row[j]) for row in rows) for j in range(len(rows[0])))
    return tuple(tuple(value/scale if scale else 0.0
                       for value,scale in zip(row,scales)) for row in rows)

def echelon_rank(rows,absolute_threshold):
    a=[list(row) for row in rows]
    m=len(a)
    n=len(a[0])
    pivot_row=0
    for j in range(n):
        if pivot_row==m:
            break
        chosen=max(range(pivot_row,m),key=lambda i:abs(a[i][j]))
        if abs(a[chosen][j])<=absolute_threshold:
            continue
        a[pivot_row],a[chosen]=a[chosen],a[pivot_row]
        for i in range(pivot_row+1,m):
            factor=finite(a[i][j]/a[pivot_row][j],"elimination factor")
            a[i][j]=0.0
            for k in range(j+1,n):
                a[i][k]=finite(a[i][k]-factor*a[pivot_row][k],"elimination entry")
        pivot_row+=1
    return pivot_row

def classify(matrix,target,relative_tolerance=1e-12):
    if not isinstance(matrix,Matrix) or not isinstance(target,Vector):
        raise TypeError("expected Matrix and Vector")
    if matrix.unit!="standardized_sensitivity" or target.unit!="standardized_exposure":
        raise ValueError("unit mismatch")
    tol=finite(relative_tolerance,"relative tolerance")
    if not 0<tol<1:
        raise ValueError("relative tolerance must be between zero and one")
    b=target.align(matrix.equation_labels)
    augmented=tuple(row+(b.values[i],) for i,row in enumerate(matrix.rows))
    # A's normalized columns are identical in both arrays, independent of b.
    rank_a=echelon_rank(column_scaled(matrix.rows),tol)
    rank_aug=echelon_rank(column_scaled(augmented),tol)
    n=len(matrix.unknown_labels)
    if rank_a<rank_aug:
        status="no_solution"
        free=None
    elif rank_a==n:
        status="unique"
        free=0
    else:
        status="infinitely_many"
        free=n-rank_a
    return {"rank_A":rank_a,"rank_augmented":rank_aug,"unknown_count":n,
            "free_variables":free,"classification":status,
            "relative_tolerance":tol,
            "rank_scaling":"nonzero columns normalized by maximum absolute entry",
            "numerical_rank_warning":"Tolerance-dependent estimate; not an SVD rank certification",
            "runtime_certified":False}

def assessment():
    unique=Matrix(("RATE","CREDIT"),("HEDGE_A","HEDGE_B"),
                  ((2,1),(1,-1)),"standardized_sensitivity")
    redundant=Matrix(("RATE","CREDIT"),("HEDGE_A","HEDGE_B"),
                     ((1,2),(2,4)),"standardized_sensitivity")
    return {"unique":classify(unique,Vector(("CREDIT","RATE"),(1,5),"standardized_exposure")),
            "redundant_consistent":classify(redundant,Vector(("RATE","CREDIT"),(3,6),"standardized_exposure")),
            "redundant_inconsistent":classify(redundant,Vector(("CREDIT","RATE"),(7,3),"standardized_exposure")),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
