"""Book 02 Section 14.8: explicit decomposition validation reference cases."""
import json
import math
from section_14_01 import eigenpairs_symmetric_2x2
from section_14_05 import solve_2x2
from section_14_06 import diagonal_exposure_svd
from section_14_07 import low_rank_diagonal_exposure

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
    pairs=eigenpairs_symmetric_2x2(((2,1),(1,2)))
    eigenvectors=pairs["eigenvectors"]
    eigenvalues=pairs["eigenvalues"]
    eigen_reconstructed=tuple(tuple(
        math.fsum(eigenvalues[k]*eigenvectors[k][i]*eigenvectors[k][j]
                  for k in range(2)) for j in range(2)) for i in range(2))
    orthogonality=tuple(tuple(
        math.fsum(eigenvectors[k][i]*eigenvectors[k][j] for k in range(2))
        for j in range(2)) for i in range(2))
    solved=solve_2x2(((4,2),(2,3)),(6,5))
    l=solved["factorization"]["factor"]
    cholesky_reconstructed=tuple(tuple(math.fsum(l[i][k]*l[j][k] for k in range(2))
                                       for j in range(2)) for i in range(2))
    solution=solved["solution"]
    solve_residual=math.hypot(4*solution[0]+2*solution[1]-6,
                             2*solution[0]+3*solution[1]-5)
    svd=diagonal_exposure_svd(3,2,(6,4,5))
    svd_original=svd["matrix"]
    # The restricted helper keeps directions in factor order.
    magnitudes=(svd_original[0][0],svd_original[1][1])
    svd_reconstructed=tuple(tuple(math.fsum(s*u[i]*v[j] for s,u,v in
        zip(magnitudes,svd["left_singular_directions"],svd["right_singular_directions"]))
        for j in range(2)) for i in range(3))
    low_rank=low_rank_diagonal_exposure(4,2,1)
    return {"eigen_reconstruction_error":frobenius_error(((2,1),(1,2)),eigen_reconstructed),
            "eigen_orthogonality_error":frobenius_error(((1,0),(0,1)),orthogonality),
            "cholesky_reconstruction_error":frobenius_error(((4,2),(2,3)),cholesky_reconstructed),
            "cholesky_solve_residual":finite(solve_residual,"solve residual"),
            "svd_reconstruction_error":frobenius_error(svd_original,svd_reconstructed),
            "svd_singular_values":svd["singular_values"],
            "svd_condition_number":svd["condition_number_full_column_rank"],
            "low_rank_frobenius_error":frobenius_error(low_rank["original"],low_rank["approximation"]),
            "low_rank_retained_squared_energy_fraction":low_rank["retained_squared_energy_fraction"],
            "calculation_source":"computed_teaching_helpers",
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
