"""Book 02 Section 13.3: labeled column and null spaces, teaching-scale RREF."""
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

def labels(items,name):
    result=tuple(items)
    if not result or any(type(x) is not str or not x.strip() for x in result):
        raise ValueError(f"{name}: nonempty labels required")
    if len(set(result))!=len(result):
        raise ValueError(f"{name}: duplicate labels")
    return result

def matrix_checked(rows,factors,instruments):
    factors=labels(factors,"factors")
    instruments=labels(instruments,"instruments")
    data=tuple(tuple(row) for row in rows)
    if len(data)!=len(factors) or any(len(row)!=len(instruments) for row in data):
        raise ValueError("matrix shape mismatch")
    return tuple(tuple(finite(x,"coefficient") for x in row) for row in data)

def rref(rows,factors,instruments,tolerance=1e-12):
    a=matrix_checked(rows,factors,instruments)
    tol=finite(tolerance,"tolerance")
    if not 0<tol<1:
        raise ValueError("invalid tolerance")
    m,n=len(a),len(a[0])
    scale=max(abs(v) for row in a for v in row)
    work=[list(row) for row in a]
    pivots=[]
    if scale==0:
        return work,pivots
    row=0
    for col in range(n):
        if row>=m:
            break
        p=max(range(row,m),key=lambda i:abs(work[i][col]))
        if abs(work[p][col])<=tol*scale:
            continue
        work[row],work[p]=work[p],work[row]
        pivot=work[row][col]
        work[row]=[finite(v/pivot,"normalized entry") for v in work[row]]
        for i in range(m):
            if i==row:
                continue
            factor=work[i][col]
            work[i]=[finite(work[i][j]-factor*work[row][j],"elimination") for j in range(n)]
        pivots.append(col)
        row+=1
    return work,pivots

def analyze(rows,factors,instruments,tolerance=1e-12):
    factors=labels(factors,"factors")
    instruments=labels(instruments,"instruments")
    matrix=matrix_checked(rows,factors,instruments)
    reduced,pivots=rref(matrix,factors,instruments,tolerance)
    free=[j for j in range(len(instruments)) if j not in pivots]
    basis=[]
    for j in free:
        vector=[0.0]*len(instruments)
        vector[j]=1.0
        for i,p in enumerate(pivots):
            vector[p]=finite(-reduced[i][j],"null-space entry")
        basis.append(dict(zip(instruments,vector)))
    return {"rank":len(pivots),"nullity":len(free),
            "column_space_basis_instruments":[instruments[j] for j in pivots],
            "null_space_basis":basis,"runtime_certified":False}

def achieved(rows,factors,instruments,positions):
    factors=labels(factors,"factors")
    instruments=labels(instruments,"instruments")
    matrix=matrix_checked(rows,factors,instruments)
    if not isinstance(positions,dict) or len(positions)!=len(instruments) or set(positions)!=set(instruments):
        raise ValueError("instrument labels mismatch")
    x=tuple(finite(positions[name],"quantity") for name in instruments)
    return dict(zip(factors,tuple(finite(math.fsum(a*b for a,b in zip(row,x)),"achieved exposure") for row in matrix)))

def assessment():
    factors=("RATE","CREDIT")
    instruments=("BOND_A","BOND_B","BOND_C")
    rows=((2,1,4),(1,-1,2))
    first={"BOND_A":2,"BOND_B":1,"BOND_C":0}
    second={"BOND_A":0,"BOND_B":1,"BOND_C":1}
    return {"spaces":analyze(rows,factors,instruments),
            "allocation_one":achieved(rows,factors,instruments,first),
            "allocation_two":achieved(rows,factors,instruments,second),
            "rank_one":analyze(((1,2),(2,4)),factors,("HEDGE_A","HEDGE_B")),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
