"""Book 02 Section 13.2: independent columns, basis, and dimension."""
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

def checked_labels(items,name,expected=None):
    result=tuple(items)
    if not result or any(type(x) is not str or not x.strip() for x in result):
        raise ValueError(f"{name}: nonempty string labels required")
    if len(set(result))!=len(result):
        raise ValueError(f"{name}: duplicate labels")
    if expected is not None and len(result)!=expected:
        raise ValueError(f"{name}: incorrect length")
    return result

def matrix_checked(rows,factors,instruments):
    factors=checked_labels(factors,"factors")
    instruments=checked_labels(instruments,"instruments")
    rows=tuple(tuple(row) for row in rows)
    if len(rows)!=len(factors) or any(len(row)!=len(instruments) for row in rows):
        raise ValueError("matrix shape mismatch")
    return tuple(tuple(finite(v,"sensitivity") for v in row) for row in rows)

def pivot_basis(rows,factors,instruments,relative_tolerance=1e-12):
    a=matrix_checked(rows,factors,instruments)
    tol=finite(relative_tolerance,"relative tolerance")
    if not 0<tol<1:
        raise ValueError("relative tolerance must be between zero and one")
    m,n=len(a),len(a[0])
    scale=max(abs(x) for row in a for x in row)
    if scale==0:
        return {"rank":0,"dimension":0,"basis_instruments":[],
                "redundant_instruments":list(instruments),"runtime_certified":False}
    work=[list(row) for row in a]
    pivots=[]
    k=0
    for col in range(n):
        if k==m:
            break
        pivot=max(range(k,m),key=lambda i:abs(work[i][col]))
        if abs(work[pivot][col])<=tol*scale:
            continue
        work[k],work[pivot]=work[pivot],work[k]
        for i in range(k+1,m):
            multiplier=finite(work[i][col]/work[k][col],"multiplier")
            work[i][col]=0.0
            for j in range(col+1,n):
                work[i][j]=finite(work[i][j]-multiplier*work[k][j],"elimination")
        pivots.append(col)
        k+=1
    return {"rank":len(pivots),"dimension":len(pivots),
            "basis_instruments":[instruments[j] for j in pivots],
            "redundant_instruments":[instruments[j] for j in range(n) if j not in pivots],
            "runtime_certified":False}

def achieved(rows,factors,instruments,quantities):
    a=matrix_checked(rows,factors,instruments)
    if set(quantities)!=set(instruments) or len(quantities)!=len(instruments):
        raise ValueError("instrument labels mismatch")
    x=tuple(finite(quantities[name],"quantity") for name in instruments)
    return dict(zip(factors,tuple(finite(math.fsum(a[i][j]*x[j] for j in range(len(x))),"achieved") for i in range(len(factors)))))

def assessment():
    factors=("RATE","CREDIT")
    instruments=("BOND_A","BOND_B","BOND_C")
    rows=((2,1,4),(1,-1,2))
    first={"BOND_A":2,"BOND_B":1,"BOND_C":0}
    second={"BOND_A":0,"BOND_B":1,"BOND_C":1}
    return {"basis":pivot_basis(rows,factors,instruments),
            "allocation_one":achieved(rows,factors,instruments,first),
            "allocation_two":achieved(rows,factors,instruments,second),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
