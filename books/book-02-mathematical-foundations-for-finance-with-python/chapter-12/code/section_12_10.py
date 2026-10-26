"""Book 02 Section 12.10: cumulative matrix and finance assessment."""
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

def checked_labels(labels,name):
    labels=tuple(labels)
    if not labels or any(type(x) is not str or not x.strip() for x in labels):
        raise ValueError(f"{name}: nonempty labels required")
    if len(set(labels))!=len(labels):
        raise ValueError(f"{name}: duplicate labels")
    return labels

def align(labels,values,order):
    labels=checked_labels(labels,"source labels")
    order=checked_labels(order,"target labels")
    values=tuple(finite(v,"vector component") for v in values)
    if len(labels)!=len(values) or len(order)!=len(labels) or set(labels)!=set(order):
        raise ValueError("label or shape mismatch")
    mapping=dict(zip(labels,values))
    return tuple(mapping[x] for x in order)

def matrix_checked(rows,n):
    rows=tuple(tuple(row) for row in rows)
    if len(rows)!=n or any(len(row)!=n for row in rows):
        raise ValueError("square matrix required")
    return tuple(tuple(finite(x,"matrix entry") for x in row) for row in rows)

def gaussian_solve(rows,b,relative_tolerance=1e-12):
    tol=finite(relative_tolerance,"pivot tolerance")
    if not 0<tol<1:
        raise ValueError("invalid pivot tolerance")
    n=len(b)
    a=[list(row) for row in matrix_checked(rows,n)]
    rhs=[finite(v,"target") for v in b]
    scale=max(abs(v) for row in a for v in row)
    if scale==0:
        raise ValueError("singular matrix")
    for k in range(n):
        p=max(range(k,n),key=lambda i:abs(a[i][k]))
        if abs(a[p][k])<=tol*scale:
            raise ValueError("singular or numerically unresolved pivot")
        a[k],a[p]=a[p],a[k]
        rhs[k],rhs[p]=rhs[p],rhs[k]
        for i in range(k+1,n):
            factor=finite(a[i][k]/a[k][k],"elimination factor")
            a[i][k]=0.0
            for j in range(k+1,n):
                a[i][j]=finite(a[i][j]-factor*a[k][j],"elimination entry")
            rhs[i]=finite(rhs[i]-factor*rhs[k],"elimination target")
    x=[0.0]*n
    for i in range(n-1,-1,-1):
        tail=math.fsum(a[i][j]*x[j] for j in range(i+1,n))
        x[i]=finite((rhs[i]-tail)/a[i][i],"solution")
    return tuple(x)

def condition_inf(rows):
    n=len(rows)
    rows=matrix_checked(rows,n)
    norm_a=max(math.fsum(abs(v) for v in row) for row in rows)
    columns=[gaussian_solve(rows,tuple(float(i==j) for i in range(n))) for j in range(n)]
    norm_inv=max(math.fsum(abs(columns[j][i]) for j in range(n)) for i in range(n))
    return finite(norm_a*norm_inv,"condition number")

def assess(rows,factors,instruments,target_labels,target_values,tolerance_labels,tolerance_values,condition_limit=1000.0):
    factors=checked_labels(factors,"factor labels")
    instruments=checked_labels(instruments,"instrument labels")
    if len(factors)!=len(instruments):
        raise ValueError("square exposure system required")
    a=matrix_checked(rows,len(factors))
    b=align(target_labels,target_values,factors)
    limits=align(tolerance_labels,tolerance_values,factors)
    if any(v<0 for v in limits):
        raise ValueError("negative tolerance")
    guardrail=finite(condition_limit,"condition guardrail")
    if guardrail<1:
        raise ValueError("condition guardrail must be at least one")
    x=gaussian_solve(a,b)
    achieved=tuple(finite(math.fsum(a[i][j]*x[j] for j in range(len(x))),"achieved") for i in range(len(b)))
    residual=tuple(finite(b[i]-achieved[i],"residual") for i in range(len(b)))
    passed={factor:abs(residual[i])<=limits[i] for i,factor in enumerate(factors)}
    kappa=condition_inf(a)
    accepted=all(passed.values()) and kappa<=guardrail
    return {"positions":dict(zip(instruments,x)),"achieved":dict(zip(factors,achieved)),
            "residual":dict(zip(factors,residual)),"factor_pass":passed,
            "condition_number_inf":kappa,
            "decision":"ACCEPT" if accepted else "REJECT",
            "reason":"accepted" if accepted else ("condition_guardrail_exceeded" if kappa>guardrail else "factor_tolerance_exceeded"),
            "runtime_certified":False}

def assessment():
    a=((2,1),(1,-1))
    reference=assess(a,("RATE","CREDIT"),("BOND_A","BOND_B"),
                     ("CREDIT","RATE"),(1,5),("CREDIT","RATE"),(0.10,0.15))
    fragile=assess(((1,1),(1,1.0001)),("RATE","CREDIT"),("HEDGE_A","HEDGE_B"),
                   ("RATE","CREDIT"),(2,2.0001),("RATE","CREDIT"),(0.01,0.01))
    return {"reference":reference,"fragile":fragile,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
