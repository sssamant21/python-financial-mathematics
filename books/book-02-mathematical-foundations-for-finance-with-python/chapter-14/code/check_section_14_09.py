"""Independent mathematical reference checks for Book 02 Section 14.9."""
import math
from section_14_09 import project
from section_14_07 import low_rank_diagonal_exposure

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
    assert p["exposure_matrix"]==((4,0),(0,2),(0,0))
    assert p["rank_one_exposure_matrix"]==((4,0),(0,0),(0,0))
    assert p["portfolio_weights"]==(0.6,0.4)
    assert p["exposure_target"]==(8,4,5)
    assert p["input_units"]=={"covariance":"annualized_return_squared",
                              "weights":"dimensionless",
                              "exposure":"illustrative_factor_exposure"}
    close(p["compression_exposure_error_norm"],4)
    close(p["compression_exposure_error_bound"],4*math.sqrt(2))
    assert p["compression_exposure_error_norm"]<=p["compression_exposure_error_bound"]
    for first,second in ((4,2),(2,4),(2,2),(0,0)):
        for rank in (0,1,2):
            compressed=low_rank_diagonal_exposure(first,second,rank)
            # Derive retained coordinates directly, including tie policy.
            keep=(set() if rank==0 else {0,1} if rank==2
                  else {0} if first>=second else {1})
            dropped=(0 if 0 in keep else first,0 if 1 in keep else second)
            expected_norm=max(dropped)
            close(compressed["spectral_error"],expected_norm)
            for x in ((0,0),(1,0),(0,1),(2,-3)):
                # Multiply the ACTUAL returned residual matrices by x.
                loss=tuple(sum((a-b)*v for a,b,v in zip(row,approx,x))
                           for row,approx in zip(compressed["original"],compressed["approximation"]))
                vector(loss,(dropped[0]*x[0],dropped[1]*x[1],0))
                norm=math.hypot(*loss)
                bound=compressed["spectral_error"]*math.hypot(*x)
                assert norm<=bound+1e-12
            # A coordinate direction attaining the spectral norm.
            axis=(1,0) if dropped[0]>=dropped[1] else (0,1)
            norm=math.hypot(dropped[0]*axis[0],dropped[1]*axis[1])
            close(norm,compressed["spectral_error"])
    assert p["runtime_certified"] is False
    assert p["independent_review_completed"] is False
    print("PASS: Section 14.9 independent mathematical reference checks")

if __name__=="__main__":
    run()
