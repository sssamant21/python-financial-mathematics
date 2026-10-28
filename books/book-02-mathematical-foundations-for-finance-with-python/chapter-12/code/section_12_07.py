"""Book 02 Section 12.7: condition numbers and financial perturbations."""
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
    if len(labels)!=2 or any(type(x) is not str or not x.strip() for x in labels):
        raise ValueError(f"{name}: exactly two nonempty labels required")
    if len(set(labels))!=2:
        raise ValueError(f"{name}: duplicate labels")
    return labels

@dataclass(frozen=True)
class Matrix2:
    row_labels: tuple
    column_labels: tuple
    rows: tuple
    unit: str
    def __post_init__(self):
        r=labels_checked(self.row_labels,"row labels")
        c=labels_checked(self.column_labels,"column labels")
        rows=tuple(tuple(row) for row in self.rows)
        if len(rows)!=2 or any(len(row)!=2 for row in rows):
            raise ValueError("matrix must be 2x2")
        if self.unit!="standardized_sensitivity":
            raise ValueError("matrix unit must be standardized_sensitivity")
        object.__setattr__(self,"row_labels",r)
        object.__setattr__(self,"column_labels",c)
        object.__setattr__(self,"rows",tuple(tuple(finite(x,"coefficient") for x in row) for row in rows))

@dataclass(frozen=True)
class Vector2:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=labels_checked(self.labels,"vector labels")
        values=tuple(self.values)
        if len(values)!=2:
            raise ValueError("vector must have two entries")
        if self.unit!="standardized_exposure":
            raise ValueError("vector unit must be standardized_exposure")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(x,"target") for x in values))
    def align(self,labels):
        target=labels_checked(labels,"target labels")
        if set(target)!=set(self.labels):
            raise ValueError("target factor labels mismatch")
        lookup=dict(zip(self.labels,self.values))
        return Vector2(target,tuple(lookup[x] for x in target),"standardized_exposure")

def inverse_rows(a):
    if not isinstance(a,Matrix2):
        raise TypeError("expected Matrix2")
    (u,v),(w,z)=a.rows
    scale=max(abs(u),abs(v),abs(w),abs(z))
    if scale==0:
        raise ValueError("singular matrix")
    uu,vv,ww,zz=u/scale,v/scale,w/scale,z/scale
    normalized=uu*zz-vv*ww
    if abs(normalized)<=1e-15:
        raise ValueError("singular or numerically unresolved matrix")
    return ((finite((zz/normalized)/scale,"inverse"),finite((-vv/normalized)/scale,"inverse")),
            (finite((-ww/normalized)/scale,"inverse"),finite((uu/normalized)/scale,"inverse")))

def infinity_norm(rows):
    return finite(max(math.fsum(abs(x) for x in row) for row in rows),"infinity norm")

def condition_inf(a):
    return finite(infinity_norm(a.rows)*infinity_norm(inverse_rows(a)),"condition number")

def solve(a,b):
    if not isinstance(a,Matrix2) or not isinstance(b,Vector2):
        raise TypeError("expected Matrix2 and Vector2")
    target=b.align(a.row_labels)
    inv=inverse_rows(a)
    x=tuple(finite(math.fsum(inv[i][j]*target.values[j] for j in range(2)),"solution") for i in range(2))
    residual=tuple(finite(target.values[i]-math.fsum(a.rows[i][j]*x[j] for j in range(2)),"residual") for i in range(2))
    return {"positions":dict(zip(a.column_labels,x)),
            "residual":dict(zip(a.row_labels,residual)),
            "gross":finite(math.fsum(abs(v) for v in x),"gross"),
            "net":finite(math.fsum(x),"net")}

def perturbation_study(a,b,delta):
    if not isinstance(delta,Vector2):
        raise TypeError("expected Vector2 perturbation")
    base=b.align(a.row_labels)
    change=delta.align(a.row_labels)
    shifted=Vector2(base.labels,tuple(finite(base.values[i]+change.values[i],"shifted target") for i in range(2)),"standardized_exposure")
    before=solve(a,base)
    after=solve(a,shifted)
    x=tuple(before["positions"][label] for label in a.column_labels)
    dx=tuple(after["positions"][label]-x[i] for i,label in enumerate(a.column_labels))
    norm_b=max(abs(v) for v in base.values)
    norm_x=max(abs(v) for v in x)
    if norm_b==0 or norm_x==0:
        raise ValueError("relative perturbation requires nonzero target and solution")
    observed=finite(max(abs(v) for v in dx)/norm_x,"observed relative change")
    input_change=finite(max(abs(v) for v in change.values)/norm_b,"relative target change")
    kappa=condition_inf(a)
    bound=finite(kappa*input_change,"condition bound")
    return {"condition_number_inf":kappa,"before":before,"after":after,
            "relative_target_change_inf":input_change,
            "relative_position_change_inf":observed,
            "worst_case_bound":bound,
            "bound_satisfied":observed<=bound+1e-10,
            "high_sensitivity_warning":kappa>=1000,
            "runtime_certified":False}

def assessment():
    stable=Matrix2(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),"standardized_sensitivity")
    fragile=Matrix2(("RATE","CREDIT"),("HEDGE_A","HEDGE_B"),((1,1),(1,1.0001)),"standardized_sensitivity")
    return {"well_conditioned":perturbation_study(stable,Vector2(("CREDIT","RATE"),(1,5),"standardized_exposure"),Vector2(("RATE","CREDIT"),(0,0.03),"standardized_exposure")),
            "nearly_dependent":perturbation_study(fragile,Vector2(("RATE","CREDIT"),(2,2.0001),"standardized_exposure"),Vector2(("CREDIT","RATE"),(0.001,0),"standardized_exposure")),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
