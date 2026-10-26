"""Independent mathematical checks for Book 02 Section 14.4."""
import math
from section_14_04 import classify,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    cases=assessment()["cases"]
    for expected,report in cases.items():
        assert report["classification"]==expected,(expected,report)
        assert report["absolute_eigenvalue_tolerance"]==0
        assert report["runtime_certified"] is False
    close(cases["positive_definite"]["eigenvalues"][0],3)
    close(cases["positive_definite"]["eigenvalues"][1],1)
    close(cases["positive_definite"]["determinant"],3)
    close(cases["positive_semidefinite"]["eigenvalues"][0],2)
    close(cases["positive_semidefinite"]["eigenvalues"][1],0)
    assert classify(((0,0),(0,2)))["classification"]=="positive_semidefinite"
    assert classify(((0,0),(0,-2)))["classification"]=="negative_semidefinite"
    assert classify(((1e-8,0),(0,-1e-8)))["classification"]=="indefinite"
    assert classify(((1e-8,0),(0,-1e-8)),1e-7)["classification"]=="numerically_zero"
    rejects(ValueError,classify,((1,2),(3,4)))
    rejects(ValueError,classify,((1,0),(0,1)),-0.1)
    rejects(ValueError,classify,((1,0),(0,1)),float("nan"))
    rejects(ValueError,classify,((1,float("inf")),(float("inf"),1)))
    print("PASS: Section 14.4 independent mathematical checks")

if __name__=="__main__":
    run()
