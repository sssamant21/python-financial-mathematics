"""Book 02 Section 14.10: deterministic chapter assessment reference report."""
import json
import math

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
    root=math.sqrt(2.0)
    q=((1/root,1/root),(1/root,-1/root))
    eigen_reconstructed=tuple(tuple(
        math.fsum((3.0*q[0][i]*q[0][j],1.0*q[1][i]*q[1][j]))
        for j in range(2)) for i in range(2))
    eigen_error=math.sqrt(math.fsum(
        (a[i][j]-eigen_reconstructed[i][j])**2
        for i in range(2) for j in range(2)))
    cholesky=((0.2,0.0),(0.05,math.sqrt(0.0875)))
    cholesky_reconstructed=((cholesky[0][0]**2,
                             cholesky[0][0]*cholesky[1][0]),
                            (cholesky[0][0]*cholesky[1][0],
                             math.fsum((cholesky[1][0]**2,
                                        cholesky[1][1]**2))))
    cholesky_error=math.sqrt(math.fsum(
        (c[i][j]-cholesky_reconstructed[i][j])**2
        for i in range(2) for j in range(2)))
    exposure=((4.0,0.0),(0.0,2.0),(0.0,0.0))
    target=(8.0,4.0,5.0)
    positions=(target[0]/4.0,target[1]/2.0)
    achieved=(4.0*positions[0],2.0*positions[1],0.0)
    residual=tuple(target[i]-achieved[i] for i in range(3))
    return {
        "eigenvalues":(3.0,1.0),
        "eigen_reconstruction_error":eigen_error,
        "quadratic_value":quadratic,
        "quadratic_gradient":tuple(2.0*v for v in ax),
        "quadratic_hessian":((4.0,2.0),(2.0,4.0)),
        "matrix_a_determinant":3.0,
        "covariance_determinant":0.04*0.09-0.01**2,
        "portfolio_variance":variance,
        "portfolio_volatility":math.sqrt(variance),
        "cholesky_factor":cholesky,
        "cholesky_reconstruction_error":cholesky_error,
        "exposure_matrix":exposure,
        "exposure_singular_values":(4.0,2.0),
        "exposure_rank":2,
        "exposure_condition_number":2.0,
        "least_squares_positions":positions,
        "least_squares_residual":residual,
        "least_squares_half_squared_residual":
            0.5*math.fsum(v*v for v in residual),
        "rank_one_frobenius_error":2.0,
        "rank_one_retained_squared_energy_fraction":16.0/20.0,
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
