"""Independent reference checks for Book 02 Section 14.1."""
import math
from section_14_01 import finite,eigenpairs_symmetric_2x2,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    p=assessment()["reference"]
    close(p["eigenvalues"][0],3)
    close(p["eigenvalues"][1],1)
    close(p["trace"],4)
    close(p["determinant"],3)
    for value,vector,residual in zip(p["eigenvalues"],p["eigenvectors"],
                                     p["eigenpair_residual_norms"]):
        close(math.hypot(*vector),1)
        close(residual,0)
        close(2*vector[0]+vector[1],value*vector[0])
        close(vector[0]+2*vector[1],value*vector[1])
    close(sum(x*y for x,y in zip(*p["eigenvectors"])),0)
    diagonal=eigenpairs_symmetric_2x2(((5,0),(0,2)))
    close(diagonal["eigenvalues"][0],5)
    close(diagonal["eigenvalues"][1],2)
    for value in diagonal["eigenpair_residual_norms"]:
        close(value,0)
    repeated=eigenpairs_symmetric_2x2(((2,0),(0,2)))
    close(repeated["eigenvalues"][0],2)
    close(repeated["eigenvalues"][1],2)
    zero=eigenpairs_symmetric_2x2(((0,0),(0,0)))
    close(zero["eigenvalues"][0],0)
    rejects(ValueError,eigenpairs_symmetric_2x2,((1,2),(3,4)))
    rejects(ValueError,eigenpairs_symmetric_2x2,((1,2,3),(4,5,6)))
    rejects(ValueError,eigenpairs_symmetric_2x2,((1,float("nan")),(float("nan"),2)))
    rejects(TypeError,finite,True,"entry")
    assert not p["runtime_certified"]
    print("PASS: Section 14.1 independent reference checks")

if __name__=="__main__":
    run()
