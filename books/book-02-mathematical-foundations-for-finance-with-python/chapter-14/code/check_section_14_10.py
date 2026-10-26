"""Independent reference checks for Book 02 Section 14.10."""
import math
from section_14_10 import assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def vector(a,b):
    assert len(a)==len(b)
    for actual,expected in zip(a,b):
        close(actual,expected)

def run():
    a=assessment()
    vector(a["eigenvalues"],(3,1))
    close(a["eigen_reconstruction_error"],0)
    close(a["quadratic_value"],14)
    vector(a["quadratic_gradient"],(8,10))
    assert a["quadratic_hessian"]==((4.0,2.0),(2.0,4.0))
    close(a["matrix_a_determinant"],3)
    close(a["covariance_determinant"],0.0035)
    close(a["portfolio_variance"],0.0336)
    close(a["portfolio_volatility"],math.sqrt(0.0336))
    close(a["cholesky_factor"][0][0],0.2)
    close(a["cholesky_factor"][1][0],0.05)
    close(a["cholesky_factor"][1][1],math.sqrt(0.0875))
    close(a["cholesky_reconstruction_error"],0)
    vector(a["exposure_singular_values"],(4,2))
    assert a["exposure_rank"]==2
    close(a["exposure_condition_number"],2)
    vector(a["least_squares_positions"],(2,2))
    vector(a["least_squares_residual"],(0,0,5))
    close(a["least_squares_half_squared_residual"],12.5)
    close(a["rank_one_frobenius_error"],2)
    close(a["rank_one_retained_squared_energy_fraction"],0.8)
    assert not a["runtime_certified"]
    assert not a["independent_review_completed"]
    print("PASS: Section 14.10 independent reference checks")

if __name__=="__main__":
    run()
