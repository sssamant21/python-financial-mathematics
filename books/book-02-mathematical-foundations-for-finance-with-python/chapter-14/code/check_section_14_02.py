"""Independent reference checks for Book 02 Section 14.2."""
import math
from section_14_02 import decompose,apply,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    p=assessment()
    d=p["decomposition"]
    close(d["eigenvalues"][0],3)
    close(d["eigenvalues"][1],1)
    reference=((2,1),(1,2))
    for i in range(2):
        for j in range(2):
            close(d["reconstructed_matrix"][i][j],reference[i][j])
    close(d["reconstruction_error_frobenius"],0)
    close(d["orthogonality_error_frobenius"],0)
    for residual in d["eigenpair_residual_norms"]:
        close(residual,0)
    close(d["trace"],4)
    close(d["determinant"],3)
    close(p["example"]["product"][0],4)
    close(p["example"]["product"][1],2)
    close(p["example"]["quadratic_form"],8)
    for matrix in (((5,0),(0,2)),((2,0),(0,2)),((0,0),(0,0)),((-1,0),(0,3))):
        result=decompose(matrix)
        for i in range(2):
            for j in range(2):
                close(result["reconstructed_matrix"][i][j],matrix[i][j])
    rejects(ValueError,decompose,((1,2),(3,4)))
    rejects(ValueError,decompose,((1,float("inf")),(float("inf"),1)))
    rejects(ValueError,apply,((2,1),(1,2)),(1,))
    assert not d["runtime_certified"]
    print("PASS: Section 14.2 independent reference checks")

if __name__=="__main__":
    run()
