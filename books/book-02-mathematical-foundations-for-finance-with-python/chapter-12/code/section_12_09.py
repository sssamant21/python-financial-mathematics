"""Book 02 Section 12.9: educational exposure-matching solver capstone."""
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
    if not labels or any(type(v) is not str or not v.strip() for v in labels):
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
            raise ValueError("vector shape mismatch")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"vector value") for v in values))
    def align(self,labels):
        target=labels_checked(labels,"target labels")
        if len(target)!=len(self.labels) or set(target)!=set(self.labels):
            raise ValueError("labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[label] for label in target),self.unit)

@dataclass(frozen=True)
class ExposureSystem:
    factors: tuple
    instruments: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        factors=labels_checked(self.factors,"factors")
        instruments=labels_checked(self.instruments,"instruments")
        data=tuple(tuple(row) for row in self.rows)
        if len(data)!=len(factors) or any(len(row)!=len(instruments) for row in data):
            raise ValueError("matrix shape mismatch")
        if self.unit!="standardized_sensitivity":
            raise ValueError("matrix unit mismatch")
        object.__setattr__(self,"factors",factors)
        object.__setattr__(self,"instruments",instruments)
        object.__setattr__(self,"rows",tuple(tuple(finite(v,"coefficient") for v in row) for row in data))

def gaussian_solve(rows,rhs,relative_pivot_tolerance):
    n=len(rows)
    if n==0 or any(len(row)!=n for row in rows) or len(rhs)!=n:
        raise ValueError("square system required")
    a=[list(row) for row in rows]
    b=list(rhs)
    scale=max(abs(v) for row in a for v in row)
    if scale==0:
        raise ValueError("singular matrix")
    for k in range(n):
        pivot=max(range(k,n),key=lambda i:abs(a[i][k]))
        if abs(a[pivot][k])<=relative_pivot_tolerance*scale:
            raise ValueError("singular or numerically unresolved pivot")
        if pivot!=k:
            a[k],a[pivot]=a[pivot],a[k]
            b[k],b[pivot]=b[pivot],b[k]
        for i in range(k+1,n):
            factor=finite(a[i][k]/a[k][k],"elimination multiplier")
            a[i][k]=0.0
            for j in range(k+1,n):
                a[i][j]=finite(a[i][j]-factor*a[k][j],"elimination entry")
            b[i]=finite(b[i]-factor*b[k],"elimination RHS")
    x=[0.0]*n
    for i in range(n-1,-1,-1):
        tail=math.fsum(finite(a[i][j]*x[j],"back-substitution product") for j in range(i+1,n))
        x[i]=finite((b[i]-tail)/a[i][i],"solution")
    return tuple(x)

def condition_inf(rows,tolerance):
    n=len(rows)
    norm_a=max(math.fsum(abs(v) for v in row) for row in rows)
    inverse_columns=[]
    for j in range(n):
        basis=tuple(1.0 if i==j else 0.0 for i in range(n))
        inverse_columns.append(gaussian_solve(rows,basis,tolerance))
    norm_inv=max(math.fsum(abs(inverse_columns[j][i]) for j in range(n)) for i in range(n))
    return finite(norm_a*norm_inv,"condition number")

def evaluate(system,target,tolerances,condition_limit=1000.0,pivot_tolerance=1e-12):
    if not isinstance(system,ExposureSystem) or not isinstance(target,Vector) or not isinstance(tolerances,Vector):
        raise TypeError("expected ExposureSystem and Vectors")
    if target.unit!="standardized_exposure" or tolerances.unit!="standardized_exposure":
        raise ValueError("target and tolerance unit mismatch")
    limit=finite(condition_limit,"condition limit")
    pivot=finite(pivot_tolerance,"pivot tolerance")
    if limit<1 or not 0<pivot<1:
        raise ValueError("invalid numerical guardrail")
    n=len(system.instruments)
    if n!=len(system.factors):
        raise ValueError("square matching system required")
    b=target.align(system.factors)
    allowed=tolerances.align(system.factors)
    if any(v<0 for v in allowed.values):
        raise ValueError("negative tolerance")
    x=gaussian_solve(system.rows,b.values,pivot)
    condition=condition_inf(system.rows,pivot)
    achieved=tuple(finite(math.fsum(finite(a*v,"exposure product") for a,v in zip(row,x)),"achieved exposure") for row in system.rows)
    residual=tuple(finite(b.values[i]-achieved[i],"residual") for i in range(n))
    factor_pass={label:abs(residual[i])<=allowed.values[i] for i,label in enumerate(system.factors)}
    norm_a=max(math.fsum(abs(v) for v in row) for row in system.rows)
    norm_x=max(abs(v) for v in x)
    norm_b=max(abs(v) for v in b.values)
    norm_r=max(abs(v) for v in residual)
    denominator=finite(norm_a*norm_x+norm_b,"normalizer")
    backward=finite(norm_r/denominator if denominator else 0.0,"backward error")
    condition_pass=condition<=limit
    accepted=all(factor_pass.values()) and condition_pass
    reason="accepted" if accepted else ("condition_guardrail_exceeded" if not condition_pass else "factor_tolerance_exceeded")
    return {"decision":"ACCEPT" if accepted else "REJECT","reason":reason,
            "positions":dict(zip(system.instruments,x)),
            "target":dict(zip(system.factors,b.values)),
            "achieved":dict(zip(system.factors,achieved)),
            "residual_target_minus_actual":dict(zip(system.factors,residual)),
            "factor_pass":factor_pass,
            "factor_tolerances":dict(zip(system.factors,allowed.values)),
            "condition_number_inf":condition,"condition_limit":limit,
            "residual_inf":norm_r,"normwise_backward_error_inf":backward,
            "gross_position":finite(math.fsum(abs(v) for v in x),"gross position"),
            "net_position":finite(math.fsum(x),"net position"),
            "pivot_tolerance":pivot,
            "runtime_certified":False,"independent_review_completed":False}

def assessment():
    reference=ExposureSystem(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),"standardized_sensitivity")
    fragile=ExposureSystem(("RATE","CREDIT"),("HEDGE_A","HEDGE_B"),((1,1),(1,1.0001)),"standardized_sensitivity")
    return {"reference":evaluate(reference,Vector(("CREDIT","RATE"),(1,5),"standardized_exposure"),Vector(("CREDIT","RATE"),(0.10,0.15),"standardized_exposure")),
            "near_duplicate":evaluate(fragile,Vector(("RATE","CREDIT"),(2,2.0001),"standardized_exposure"),Vector(("RATE","CREDIT"),(0.01,0.01),"standardized_exposure"))}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
