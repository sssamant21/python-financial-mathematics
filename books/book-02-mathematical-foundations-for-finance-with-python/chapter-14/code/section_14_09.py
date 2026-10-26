"""Book 02 Section 14.9: quadratic exposure and decomposition capstone."""
import json
import math
from section_14_05 import cholesky_2x2,solve_2x2
from section_14_06 import diagonal_exposure_svd
from section_14_07 import low_rank_diagonal_exposure

def project():
    covariance=((0.04,0.01),(0.01,0.09))
    weights=(0.6,0.4)
    cw=(math.fsum((covariance[i][0]*weights[0],
                   covariance[i][1]*weights[1])) for i in range(2))
    cw=tuple(cw)
    variance=math.fsum(weights[i]*cw[i] for i in range(2))
    determinant=0.04*0.09-0.01**2
    chol=cholesky_2x2(covariance)
    recovered=solve_2x2(covariance,cw)
    exposure=diagonal_exposure_svd(4,2,(8,4,5))
    compression=low_rank_diagonal_exposure(4,2,1)
    positions=exposure["positions"]
    full=(4*positions[0],2*positions[1],0.0)
    compressed=(4*positions[0],0.0,0.0)
    lost=tuple(full[i]-compressed[i] for i in range(3))
    return {
        "weight_sum":math.fsum(weights),
        "portfolio_variance":variance,
        "portfolio_volatility":math.sqrt(variance),
        "variance_gradient":tuple(2*v for v in cw),
        "covariance_determinant":determinant,
        "covariance_positive_definite":0.04>0 and determinant>0,
        "cholesky_factor":chol["factor"],
        "cholesky_reconstruction_error":chol["reconstruction_error_frobenius"],
        "cholesky_recovered_weights":recovered["solution"],
        "cholesky_solve_residual_norm":recovered["solve_residual_norm"],
        "exposure_singular_values":exposure["singular_values"],
        "exposure_condition_number":exposure["condition_number_full_column_rank"],
        "least_squares_positions":positions,
        "least_squares_residual":exposure["signed_residual"],
        "least_squares_half_squared_residual":exposure["half_squared_residual"],
        "rank_one_frobenius_error":compression["frobenius_error"],
        "rank_one_spectral_error":compression["spectral_error"],
        "rank_one_retained_squared_energy_fraction":
            compression["retained_squared_energy_fraction"],
        "exposure_lost_by_compression_at_solution":lost,
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(project(),indent=2,allow_nan=False))
