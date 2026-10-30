"""Book 02 Section 14.2: symmetric 2x2 spectral decomposition."""
import json
import math
from section_14_01 import eigenpairs_symmetric_2x2,finite

def decompose(matrix):
    # Materialize one-shot iterables once for both validation and diagnostics.
    try:
        rows=tuple(tuple(row) for row in matrix)
    except TypeError as exc:
        raise ValueError("matrix must be a 2x2 sequence") from exc
    pairs=eigenpairs_symmetric_2x2(rows)
    values=pairs["eigenvalues"]
    vectors=pairs["eigenvectors"]
    rows=tuple(tuple(finite(value,"matrix entry") for value in row) for row in rows)
    reconstruction=tuple(tuple(math.fsum(
        values[k]*vectors[k][i]*vectors[k][j] for k in range(2))
        for j in range(2)) for i in range(2))
    error=math.hypot(*(rows[i][j]-reconstruction[i][j]
                       for i in range(2) for j in range(2)))
    orthogonality=math.hypot(*(
        math.fsum(vectors[k][i]*vectors[l][i] for i in range(2))-
        (1.0 if k==l else 0.0)
        for k in range(2) for l in range(2)))
    return {"eigenvalues":values,"eigenvectors":vectors,
            "reconstructed_matrix":reconstruction,
            "reconstruction_error_frobenius":finite(error,"reconstruction error"),
            "orthogonality_error_frobenius":finite(orthogonality,"orthogonality error"),
            "eigenpair_residual_norms":pairs["eigenpair_residual_norms"],
            "trace":pairs["trace"],"determinant":pairs["determinant"],
            "runtime_certified":False}

def apply(matrix,vector):
    if len(vector)!=2:
        raise ValueError("vector must have length two")
    x=tuple(finite(v,"vector entry") for v in vector)
    a=tuple(tuple(finite(v,"matrix entry") for v in row) for row in matrix)
    if len(a)!=2 or any(len(row)!=2 for row in a):
        raise ValueError("matrix must be 2x2")
    result=tuple(finite(math.fsum(a[i][j]*x[j] for j in range(2)),
                        "matrix-vector product") for i in range(2))
    return {"product":result,
            "quadratic_form":finite(math.fsum(x[i]*result[i] for i in range(2)),
                                    "quadratic form")}

def assessment():
    matrix=((2,1),(1,2))
    return {"decomposition":decompose(matrix),"example":apply(matrix,(2,0)),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
