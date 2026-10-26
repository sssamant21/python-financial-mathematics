"""Book 02 Section 13.6: educational Householder QR least-squares solver."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric (bool excluded)")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def labels(values,name):
    result=tuple(values)
    if not result or any(type(v) is not str or not v.strip() for v in result):
        raise ValueError(f"{name}: nonempty string labels required")
    if len(set(result))!=len(result):
        raise ValueError(f"{name}: duplicate labels")
    return result

def solve_qr(factors,instruments,rows,target_labels,target_values,relative_tolerance=1e-12):
    factors=labels(factors,"factor labels")
    instruments=labels(instruments,"instrument labels")
    m,n=len(factors),len(instruments)
    if m<n:
        raise ValueError("full-column-rank solver requires rows >= columns")
    data=tuple(tuple(row) for row in rows)
    if len(data)!=m or any(len(row)!=n for row in data):
        raise ValueError("matrix shape mismatch")
    a=tuple(tuple(finite(v,"matrix entry") for v in row) for row in data)
    source=labels(target_labels,"target factor labels")
    target_values=tuple(target_values)
    if len(source)!=m or len(target_values)!=m or set(source)!=set(factors):
        raise ValueError("target labels or dimensions mismatch")
    target=dict(zip(source,(finite(v,"target exposure") for v in target_values)))
    b=[target[name] for name in factors]
    tol=finite(relative_tolerance,"relative tolerance")
    if not 0<tol<1:
        raise ValueError("invalid relative tolerance")
    scale=max(abs(v) for row in a for v in row)
    if scale==0:
        raise ValueError("zero or rank-deficient exposure matrix")
    # Scale matrix and target together; the minimizer is unchanged.
    work=[[v/scale for v in row] for row in a]
    transformed=[v/scale for v in b]
    for k in range(n):
        x=[work[i][k] for i in range(k,m)]
        norm=math.hypot(*x)
        if norm<=tol:
            raise ValueError("numerically rank-deficient matrix")
        sign=1.0 if x[0]>=0 else -1.0
        v=x[:]
        v[0]+=sign*norm
        vnorm=math.hypot(*v)
        if vnorm==0:
            raise ValueError("invalid Householder vector")
        v=[z/vnorm for z in v]
        for j in range(k,n):
            projection=2*math.fsum(v[i-k]*work[i][j] for i in range(k,m))
            for i in range(k,m):
                work[i][j]-=projection*v[i-k]
        projection=2*math.fsum(v[i-k]*transformed[i] for i in range(k,m))
        for i in range(k,m):
            transformed[i]-=projection*v[i-k]
    solution=[0.0]*n
    for i in range(n-1,-1,-1):
        pivot=work[i][i]
        if abs(pivot)<=tol:
            raise ValueError("numerically rank-deficient matrix")
        rhs=transformed[i]-math.fsum(work[i][j]*solution[j] for j in range(i+1,n))
        solution[i]=finite(rhs/pivot,"position")
    achieved=[finite(math.fsum(a[i][j]*solution[j] for j in range(n)),"achieved") for i in range(m)]
    residual=[finite(b[i]-achieved[i],"residual") for i in range(m)]
    objective=finite(0.5*math.fsum(v*v for v in residual),"objective")
    gradient={instruments[j]:finite(-math.fsum(a[i][j]*residual[i] for i in range(m)),"gradient")
              for j in range(n)}
    return {"positions":dict(zip(instruments,solution)),
            "achieved":dict(zip(factors,achieved)),
            "residual_target_minus_achieved":dict(zip(factors,residual)),
            "objective_half_squared_l2":objective,
            "gradient":gradient,"solver":"educational_householder_qr",
            "runtime_certified":False}

def assessment():
    result=solve_qr(("RATE","CREDIT","LIQUIDITY"),("BOND_A","BOND_B"),
                    ((1,0),(0,1),(1,1)),
                    ("LIQUIDITY","RATE","CREDIT"),(6,2,3))
    return {"reference":result,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
