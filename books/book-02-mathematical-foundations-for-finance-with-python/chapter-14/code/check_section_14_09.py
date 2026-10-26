"""Independent mathematical reference checks for Book 02 Section 14.9."""
import math
from section_14_09 import project

def close(actual,expected):
    assert math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10),(actual,expected)

def vector(actual,expected):
    assert len(actual)==len(expected)
    for a,b in zip(actual,expected):
        close(a,b)

def run():
    p=project()
    close(p["weight_sum"],1)
    close(p["portfolio_variance"],0.0336)
    close(p["portfolio_volatility"],math.sqrt(0.0336))
    vector(p["variance_gradient"],(0.056,0.084))
    close(p["covariance_determinant"],0.0035)
    assert p["covariance_positive_definite"]
    factor=p["cholesky_factor"]
    close(factor[0][0],0.2)
    close(factor[1][0],0.05)
    close(factor[1][1],math.sqrt(0.0875))
    close(p["cholesky_reconstruction_error"],0)
    vector(p["cholesky_recovered_weights"],(0.6,0.4))
    close(p["cholesky_solve_residual_norm"],0)
    vector(p["exposure_singular_values"],(4,2))
    close(p["exposure_condition_number"],2)
    vector(p["least_squares_positions"],(2,2))
    vector(p["least_squares_residual"],(0,0,5))
    close(p["least_squares_half_squared_residual"],12.5)
    close(p["rank_one_frobenius_error"],2)
    close(p["rank_one_spectral_error"],2)
    close(p["rank_one_retained_squared_energy_fraction"],0.8)
    vector(p["exposure_lost_by_compression_at_solution"],(0,4,0))
    assert p["runtime_certified"] is False
    assert p["independent_review_completed"] is False
    print("PASS: Section 14.9 independent mathematical reference checks")

if __name__=="__main__":
    run()
