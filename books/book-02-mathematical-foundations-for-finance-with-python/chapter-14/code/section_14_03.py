"""Book 02 Section 14.3: symmetric two-factor quadratic forms."""
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

def quadratic_form(matrix,vector):
    try:
        rows=tuple(tuple(row) for row in matrix)
        x=tuple(vector)
    except TypeError as exc:
        raise ValueError("matrix and vector must be sequences") from exc
    if len(rows)!=2 or any(len(row)!=2 for row in rows):
        raise ValueError("matrix must be 2x2")
    if len(x)!=2:
        raise ValueError("vector must have length two")
    a,b=map(lambda v:finite(v,"matrix entry"),rows[0])
    c,d=map(lambda v:finite(v,"matrix entry"),rows[1])
    x1,x2=(finite(v,"vector entry") for v in x)
    scale=max(1.0,abs(a),abs(b),abs(c),abs(d))
    if abs(b-c)>1e-12*scale:
        raise ValueError("matrix must be symmetric")
    if b!=c:
        raise ValueError("matrix must be exactly symmetric for this educational lab")
    ax=(finite(a*x1+b*x2,"matrix-vector product"),
        finite(b*x1+d*x2,"matrix-vector product"))
    value=finite(math.fsum((x1*ax[0],x2*ax[1])),"quadratic value")
    polynomial=finite(math.fsum((a*x1*x1,2*b*x1*x2,d*x2*x2)),
                      "polynomial value")
    gradient=(finite(2*ax[0],"gradient"),finite(2*ax[1],"gradient"))
    hessian=((finite(2*a,"hessian"),finite(2*b,"hessian")),
             (finite(2*b,"hessian"),finite(2*d,"hessian")))
    return {"quadratic_value":value,"polynomial_value":polynomial,
            "matrix_vector_product":ax,"gradient":gradient,"hessian":hessian,
            "runtime_certified":False}

def assessment():
    return {"reference":quadratic_form(((2,1),(1,2)),(2,1)),
            "scaled":quadratic_form(((2,1),(1,2)),(4,2)),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
