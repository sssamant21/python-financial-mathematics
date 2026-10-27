"""Book 02 Section 14.8: explicit decomposition validation reference cases."""
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

def frobenius_error(matrix,reconstruction):
    try:
        rows=tuple(tuple(finite(v,"matrix entry") for v in row) for row in matrix)
        approx=tuple(tuple(finite(v,"reconstruction entry") for v in row)
                     for row in reconstruction)
    except TypeError as exc:
        raise ValueError("matrices must be sequences") from exc
    if not rows or not rows[0] or any(len(row)!=len(rows[0]) for row in rows):
        raise ValueError("matrix must be nonempty and rectangular")
    if len(rows)!=len(approx) or any(len(a)!=len(b) for a,b in zip(rows,approx)):
        raise ValueError("matrix dimensions must match")
    # hypot scales its inputs to avoid avoidable overflow in squaring.
    return finite(math.hypot(*(a-b for row_a,row_b in zip(rows,approx)
                               for a,b in zip(row_a,row_b))),"Frobenius error")

def assessment():
    root=math.sqrt(2)
    eigenvectors=((1/root,1/root),(1/root,-1/root))
    eigenvalues=(3.0,1.0)
    eigen_reconstructed=tuple(tuple(
        math.fsum(eigenvalues[k]*eigenvectors[k][i]*eigenvectors[k][j]
                  for k in range(2)) for j in range(2)) for i in range(2))
    orthogonality=tuple(tuple(
        math.fsum(eigenvectors[k][i]*eigenvectors[k][j] for k in range(2))
        for j in range(2)) for i in range(2))
    eigen_error=frobenius_error(((2,1),(1,2)),eigen_reconstructed)
    orthogonality_error=frobenius_error(((1,0),(0,1)),orthogonality)

    l=((2.0,0.0),(1.0,root))
    cholesky_reconstructed=((l[0][0]**2,l[0][0]*l[1][0]),
                            (l[0][0]*l[1][0],l[1][0]**2+l[1][1]**2))
    cholesky_error=frobenius_error(((4,2),(2,3)),cholesky_reconstructed)
    solution=(1.0,1.0)
    solve_residual=math.hypot(4*solution[0]+2*solution[1]-6,
                              2*solution[0]+3*solution[1]-5)
    svd_original=((3.0,0.0),(0.0,2.0),(0.0,0.0))
    svd_reconstructed=((3.0,0.0),(0.0,2.0),(0.0,0.0))
    svd_error=frobenius_error(svd_original,svd_reconstructed)
    low_rank_original=((4.0,0.0),(0.0,2.0),(0.0,0.0))
    low_rank_approx=((4.0,0.0),(0.0,0.0),(0.0,0.0))
    low_rank_error=frobenius_error(low_rank_original,low_rank_approx)
    return {"eigen_reconstruction_error":eigen_error,
            "eigen_orthogonality_error":orthogonality_error,
            "cholesky_reconstruction_error":cholesky_error,
            "cholesky_solve_residual":finite(solve_residual,"solve residual"),
            "svd_reconstruction_error":svd_error,
            "svd_singular_values":(3.0,2.0),
            "svd_condition_number":1.5,
            "low_rank_frobenius_error":low_rank_error,
            "low_rank_retained_squared_energy_fraction":0.8,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
