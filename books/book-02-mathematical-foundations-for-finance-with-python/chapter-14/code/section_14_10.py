"""Book 02 Section 14.10: deterministic chapter assessment reference report."""
import json
import math
from section_14_01 import eigenpairs_symmetric_2x2
from section_14_05 import cholesky_2x2
from section_14_06 import diagonal_exposure_svd
from section_14_07 import low_rank_diagonal_exposure

def assessment():
    a=((2.0,1.0),(1.0,2.0))
    x=(1.0,2.0)
    ax=(a[0][0]*x[0]+a[0][1]*x[1],
        a[1][0]*x[0]+a[1][1]*x[1])
    quadratic=math.fsum(x[i]*ax[i] for i in range(2))
    c=((0.04,0.01),(0.01,0.09))
    w=(0.6,0.4)
    cw=(math.fsum(c[i][j]*w[j] for j in range(2)) for i in range(2))
    cw=tuple(cw)
    variance=math.fsum(w[i]*cw[i] for i in range(2))
    pairs=eigenpairs_symmetric_2x2(a)
    values=pairs["eigenvalues"]
    q=pairs["eigenvectors"]
    eigen_reconstructed=tuple(tuple(math.fsum(values[k]*q[k][i]*q[k][j] for k in range(2))
                                    for j in range(2)) for i in range(2))
    eigen_error=math.hypot(*(a[i][j]-eigen_reconstructed[i][j] for i in range(2) for j in range(2)))
    cholesky=cholesky_2x2(c)["factor"]
    cholesky_reconstructed=tuple(tuple(math.fsum(cholesky[i][k]*cholesky[j][k] for k in range(2))
                                       for j in range(2)) for i in range(2))
    cholesky_error=math.hypot(*(c[i][j]-cholesky_reconstructed[i][j] for i in range(2) for j in range(2)))
    target=(8.0,4.0,5.0)
    svd=diagonal_exposure_svd(4,2,target)
    exposure=svd["matrix"]
    positions=svd["positions"]
    achieved=tuple(math.fsum(exposure[i][j]*positions[j] for j in range(2)) for i in range(3))
    residual=tuple(target[i]-achieved[i] for i in range(3))
    compressed=low_rank_diagonal_exposure(4,2,1)
    compression_error=math.hypot(*(compressed["original"][i][j]-compressed["approximation"][i][j]
                                  for i in range(3) for j in range(2)))
    return {
        "eigenvalues":values,
        "eigen_reconstruction_error":eigen_error,
        "quadratic_value":quadratic,
        "quadratic_gradient":tuple(2.0*v for v in ax),
        "quadratic_hessian":tuple(tuple(2*v for v in row) for row in a),
        "matrix_a_determinant":pairs["determinant"],
        "covariance_determinant":0.04*0.09-0.01**2,
        "portfolio_variance":variance,
        "portfolio_volatility":math.sqrt(variance),
        "cholesky_factor":cholesky,
        "cholesky_reconstruction_error":cholesky_error,
        "exposure_matrix":exposure,
        "exposure_singular_values":svd["singular_values"],
        "exposure_rank":svd["rank_at_tolerance"],
        "exposure_condition_number":svd["condition_number_full_column_rank"],
        "least_squares_positions":positions,
        "least_squares_residual":residual,
        "least_squares_half_squared_residual":
            0.5*math.fsum(v*v for v in residual),
        "rank_one_frobenius_error":compression_error,
        "rank_one_retained_squared_energy_fraction":compressed["retained_squared_energy_fraction"],
        "calculation_source":"computed_teaching_helpers",
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
