"""Independent reference checks for Book 02 Section 14.5."""
import math
from section_14_05 import cholesky_2x2,solve_2x2,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()["reference"]
    factor=report["factorization"]
    l=factor["factor"]
    close(l[0][0],2)
    close(l[0][1],0)
    close(l[1][0],1)
    close(l[1][1],math.sqrt(2))
    for i,row in enumerate(((4,2),(2,3))):
        for j,value in enumerate(row):
            close(factor["reconstructed_matrix"][i][j],value)
    close(factor["determinant_from_factor"],8)
    close(factor["reconstruction_error_frobenius"],0)
    close(report["solution"][0],1)
    close(report["solution"][1],1)
    close(report["solve_residual_norm"],0)
    diagonal=solve_2x2(((9,0),(0,4)),(6,8))
    close(diagonal["solution"][0],2/3)
    close(diagonal["solution"][1],2)
    rejects(ValueError,cholesky_2x2,((1,1),(1,1)))
    rejects(ValueError,cholesky_2x2,((1,0),(0,-1)))
    rejects(ValueError,cholesky_2x2,((1,2),(3,4)))
    rejects(ValueError,cholesky_2x2,((0,0),(0,0)))
    rejects(ValueError,cholesky_2x2,((1,float("nan")),(float("nan"),1)))
    rejects(ValueError,solve_2x2,((1,0),(0,1)),(1,))
    assert not factor["runtime_certified"]
    print("PASS: Section 14.5 independent reference checks")

if __name__=="__main__":
    run()
