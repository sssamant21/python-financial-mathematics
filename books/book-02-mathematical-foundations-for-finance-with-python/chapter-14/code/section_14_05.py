"""Book 02 Section 14.5: standard-library 2x2 Cholesky and triangular solves."""
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

def cholesky_2x2(matrix):
    try:
        rows=tuple(tuple(row) for row in matrix)
    except TypeError as exc:
        raise ValueError("matrix must be a 2x2 sequence") from exc
    if len(rows)!=2 or any(len(row)!=2 for row in rows):
        raise ValueError("matrix must be 2x2")
    a,b=map(lambda v:finite(v,"matrix entry"),rows[0])
    c,d=map(lambda v:finite(v,"matrix entry"),rows[1])
    if b!=c:
        raise ValueError("matrix must be exactly symmetric")
    if a<=0:
        raise ValueError("matrix must be positive definite: first pivot")
    l11=math.sqrt(a)
    l21=finite(b/l11,"lower off-diagonal")
    pivot=finite(d-l21*l21,"second pivot")
    if pivot<=0:
        raise ValueError("matrix must be positive definite: second pivot")
    l22=math.sqrt(pivot)
    factor=((l11,0.0),(l21,l22))
    reconstruction=((finite(l11*l11,"reconstruction"),finite(l11*l21,"reconstruction")),
                    (finite(l11*l21,"reconstruction"),
                     finite(math.fsum((l21*l21,l22*l22)),"reconstruction")))
    error=finite(math.hypot(*(
        rows[i][j]-reconstruction[i][j]
        for i in range(2) for j in range(2))),"reconstruction error")
    determinant=finite((l11*l22)**2,"determinant")
    return {"factor":factor,"reconstructed_matrix":reconstruction,
            "reconstruction_error_frobenius":error,
            "determinant_from_factor":determinant,
            "runtime_certified":False}

def solve_2x2(matrix,rhs):
    try:
        rows=tuple(tuple(row) for row in matrix)
    except TypeError as exc:
        raise ValueError("matrix must be a 2x2 sequence") from exc
    result=cholesky_2x2(rows)
    try:
        vector=tuple(rhs)
    except TypeError as exc:
        raise ValueError("rhs must have two entries") from exc
    if len(vector)!=2:
        raise ValueError("rhs must have two entries")
    b0,b1=(finite(v,"rhs entry") for v in vector)
    (l11,_),(l21,l22)=result["factor"]
    y0=finite(b0/l11,"forward solve")
    y1=finite((b1-l21*y0)/l22,"forward solve")
    x1=finite(y1/l22,"backward solve")
    x0=finite((y0-l21*x1)/l11,"backward solve")
    rows=tuple(tuple(float(v) for v in row) for row in rows)
    residual=(finite(math.fsum((rows[0][0]*x0,rows[0][1]*x1))-b0,"solve residual"),
              finite(math.fsum((rows[1][0]*x0,rows[1][1]*x1))-b1,"solve residual"))
    return {"solution":(x0,x1),"forward_solution":(y0,y1),
            "solve_residual_norm":finite(math.hypot(*residual),"solve residual norm"),
            "factorization":result}

def assessment():
    matrix=((4,2),(2,3))
    return {"reference":solve_2x2(matrix,(6,5)),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
