"""Independent checks for Book 02 Section 14.8."""
import math
from section_14_08 import assessment,frobenius_error

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    for name in ("eigen_reconstruction_error","eigen_orthogonality_error",
                 "cholesky_reconstruction_error","cholesky_solve_residual",
                 "svd_reconstruction_error"):
        close(a[name],0)
    close(a["svd_singular_values"][0],3)
    close(a["svd_singular_values"][1],2)
    close(a["svd_condition_number"],1.5)
    close(a["low_rank_frobenius_error"],2)
    close(a["low_rank_retained_squared_energy_fraction"],0.8)
    close(frobenius_error(((1,2),(3,4)),((1,1),(3,4))),1)
    rejects(ValueError,frobenius_error,((1,2),),((1,2),(3,4)))
    rejects(ValueError,frobenius_error,((1,2),(3,)),((1,2),(3,4)))
    rejects(ValueError,frobenius_error,(),())
    rejects(ValueError,frobenius_error,((1,float("nan")),),((1,2),))
    assert not a["runtime_certified"]
    print("PASS: Section 14.8 independent reference checks")

if __name__=="__main__":
    run()
