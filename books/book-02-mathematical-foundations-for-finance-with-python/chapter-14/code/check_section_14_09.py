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
    covariance=((0.04,0.01),(0.01,0.09))
    assert p["covariance_matrix"]==covariance
    values=p["covariance_eigenvalues"]
    vectors=p["covariance_eigenvectors"]
    # Characteristic roots: (13 +/- sqrt(29))/200.
    expected=((13+math.sqrt(29))/200,(13-math.sqrt(29))/200)
    vector(values,expected)
    assert values[0]>values[1]>0
    assert len(vectors)==2 and all(len(v)==2 for v in vectors)
    for k in range(2):
        v=vectors[k]
        close(sum(x*x for x in v),1)
        residual=tuple(sum(covariance[i][j]*v[j] for j in range(2))-values[k]*v[i]
                       for i in range(2))
        close(math.hypot(*residual),0)
        # Spectral projectors avoid dependence on arbitrary eigenvector sign.
        other=expected[1-k]
        for i in range(2):
            for j in range(2):
                projector=(covariance[i][j]-(other if i==j else 0))/(expected[k]-other)
                close(v[i]*v[j],projector)
    close(sum(vectors[0][i]*vectors[1][i] for i in range(2)),0)
    for i in range(2):
        for j in range(2):
            close(sum(values[k]*vectors[k][i]*vectors[k][j] for k in range(2)),
                  covariance[i][j])
    close(sum(values),0.13)
    close(values[0]*values[1],0.0035)
    vector(p["covariance_eigenpair_residual_norms"],(0,0))
    close(p["covariance_spectral_reconstruction_error"],0)
    close(p["covariance_orthogonality_error"],0)
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
