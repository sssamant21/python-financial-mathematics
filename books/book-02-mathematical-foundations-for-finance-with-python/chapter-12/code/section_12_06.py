"""Book 02 Section 12.6: labeled 2x2 inverse and determinant teaching lab."""
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
    result=tuple(values)
    if len(result)!=2 or any(type(x) is not str or not x.strip() for x in result):
        raise ValueError(f"{name}: exactly two nonempty labels required")
    if len(set(result))!=2:
        raise ValueError(f"{name}: duplicate labels")
    return result

@dataclass(frozen=True)
class Matrix2:
    row_labels: tuple
    column_labels: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        rows=labels_checked(self.row_labels,"row labels")
        columns=labels_checked(self.column_labels,"column labels")
        data=tuple(tuple(row) for row in self.rows)
        if len(data)!=2 or any(len(row)!=2 for row in data):
            raise ValueError("matrix must be 2x2")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"row_labels",rows)
        object.__setattr__(self,"column_labels",columns)
        object.__setattr__(self,"rows",tuple(tuple(finite(x,"matrix entry") for x in row) for row in data))

@dataclass(frozen=True)
class Vector2:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=labels_checked(self.labels,"vector labels")
        values=tuple(self.values)
        if len(values)!=2:
            raise ValueError("vector length must be two")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(x,"vector entry") for x in values))
    def align(self,labels):
        target=labels_checked(labels,"target labels")
        if set(target)!=set(self.labels):
            raise ValueError("target labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector2(target,tuple(lookup[x] for x in target),self.unit)

def determinant(matrix):
    if not isinstance(matrix,Matrix2):
        raise TypeError("expected Matrix2")
    (a,b),(c,d)=matrix.rows
    return finite(a*d-b*c,"determinant")

def inverse(matrix,relative_tolerance=1e-12):
    if not isinstance(matrix,Matrix2):
        raise TypeError("expected Matrix2")
    tol=finite(relative_tolerance,"relative tolerance")
    if not 0<tol<1:
        raise ValueError("relative tolerance must be between zero and one")
    (a,b),(c,d)=matrix.rows
    scale=max(abs(a),abs(b),abs(c),abs(d))
    if scale==0:
        raise ValueError("singular matrix")
    # Normalized determinant avoids overflow in the determinant test.
    aa,bb,cc,dd=(a/scale,b/scale,c/scale,d/scale)
    normalized_det=aa*dd-bb*cc
    if abs(normalized_det)<=tol:
        raise ValueError("singular or numerically unresolved matrix")
    # A = scale * normalized_A; invert the normalized matrix first.
    # The unscaled determinant may overflow/underflow even when A^-1 exists
    # and every inverse entry is representable.
    result=((finite((dd/normalized_det)/scale,"inverse entry"),finite((-bb/normalized_det)/scale,"inverse entry")),
            (finite((-cc/normalized_det)/scale,"inverse entry"),finite((aa/normalized_det)/scale,"inverse entry")))
    return Matrix2(matrix.column_labels,matrix.row_labels,result,"inverse_standardized_sensitivity")

def solve_exposures(matrix,target):
    if not isinstance(matrix,Matrix2) or not isinstance(target,Vector2):
        raise TypeError("expected Matrix2 and Vector2")
    if matrix.unit!="standardized_sensitivity" or target.unit!="standardized_exposure":
        raise ValueError("unit mismatch")
    b=target.align(matrix.row_labels)
    inv=inverse(matrix)
    quantities=[]
    for row in inv.rows:
        quantities.append(finite(math.fsum(finite(x*y,"solution term") for x,y in zip(row,b.values)),"quantity"))
    residual={}
    for i,label in enumerate(matrix.row_labels):
        fitted=math.fsum(finite(matrix.rows[i][j]*quantities[j],"fitted term") for j in range(2))
        residual[label]=finite(b.values[i]-fitted,"residual")
    return {"quantities":dict(zip(matrix.column_labels,quantities)),
            "residual":residual,"runtime_certified":False}

def assessment():
    a=Matrix2(("RATE","CREDIT"),("BOND_A","BOND_B"),
              ((2,1),(1,-1)),"standardized_sensitivity")
    target=Vector2(("CREDIT","RATE"),(1,5),"standardized_exposure")
    inv=inverse(a)
    return {"determinant":determinant(a),"inverse":inv.rows,
            "exposure_match":solve_exposures(a,target),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
