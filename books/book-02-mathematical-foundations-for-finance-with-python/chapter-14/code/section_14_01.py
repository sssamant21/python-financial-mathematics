"""Book 02 Section 14.1: real symmetric 2x2 eigenpairs."""
import json
import math
from fractions import Fraction

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

def eigenpairs_symmetric_2x2(matrix):
    try:
        rows=tuple(tuple(row) for row in matrix)
    except TypeError as exc:
        raise ValueError("matrix must be a 2x2 sequence") from exc
    if len(rows)!=2 or any(len(row)!=2 for row in rows):
        raise ValueError("matrix must be 2x2")
    a,b=map(lambda v:finite(v,"matrix entry"),rows[0])
    c,d=map(lambda v:finite(v,"matrix entry"),rows[1])
    scale=max(1.0,abs(a),abs(b),abs(c),abs(d))
    if abs(b-c)>1e-12*scale:
        raise ValueError("matrix must be symmetric")
    off=(b+c)/2
    # Scale first to limit overflow in the eigenvalue gap calculation.
    scale=max(abs(a),abs(off),abs(d))
    if scale==0:
        values=(0.0,0.0)
        vectors=((1.0,0.0),(0.0,1.0))
    else:
        aa=a/scale
        bb=off/scale
        dd=d/scale
        gap=math.hypot(aa-dd,2*bb)
        # Compute the root with larger magnitude without trace-gap cancellation.
        trace_scaled=aa+dd
        far=finite(scale*(0.5*(trace_scaled+math.copysign(gap,trace_scaled))),
                   "eigenvalue")
        # Exact arithmetic on represented entries prevents determinant product
        # overflow/underflow and cancellation before recovering the other root.
        determinant_exact=Fraction(a)*Fraction(d)-Fraction(off)*Fraction(off)
        try:
            other=float(determinant_exact/Fraction(far)) if far else 0.0
        except OverflowError as exc:
            raise ValueError("eigenvalue outside float range") from exc
        values=tuple(sorted((far,finite(other,"eigenvalue")),reverse=True))
        if gap<=1e-14*max(1.0,abs(aa),abs(dd)):
            vectors=((1.0,0.0),(0.0,1.0))
        else:
            # For a symmetric matrix, a stable eigenvector can be selected
            # from the larger component of (off, lambda-a) or (lambda-d, off).
            x,y=(bb,0.5*(dd-aa+gap))
            if abs(x)+abs(y)<abs(0.5*(aa-dd+gap))+abs(bb):
                x,y=(0.5*(aa-dd+gap),bb)
            norm=math.hypot(x,y)
            if norm==0:
                raise ValueError("could not construct eigenvector")
            x,y=x/norm,y/norm
            if x<0 or (x==0 and y<0):
                x,y=-x,-y
            vectors=((x,y),(-y,x))
    residuals=[]
    for eigenvalue,(x,y) in zip(values,vectors):
        residuals.append(math.hypot(
            (a*x+off*y)-eigenvalue*x,
            (off*x+d*y)-eigenvalue*y))
    return {"eigenvalues":values,"eigenvectors":vectors,
            "eigenpair_residual_norms":tuple(residuals),
            "trace":finite(a+d,"trace"),
            "determinant":finite(a*d-off*off,"determinant"),
            "runtime_certified":False}

def assessment():
    return {"reference":eigenpairs_symmetric_2x2(((2,1),(1,2))),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
