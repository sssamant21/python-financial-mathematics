"""Independent reference checks for Book 02 Section 14.3."""
import math
from section_14_03 import quadratic_form,finite,assessment
from section_14_02 import decompose

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    p=report["reference"]
    close(p["quadratic_value"],14)
    close(p["polynomial_value"],14)
    close(p["matrix_vector_product"][0],5)
    close(p["matrix_vector_product"][1],4)
    close(p["gradient"][0],10)
    close(p["gradient"][1],8)
    assert p["hessian"]==((4.0,2.0),(2.0,4.0))
    close(report["scaled"]["quadratic_value"],56)
    spectral=decompose(((2,1),(1,2)))
    x=(2,1)
    value=0
    for eigenvalue,v in zip(spectral["eigenvalues"],spectral["eigenvectors"]):
        coordinate=x[0]*v[0]+x[1]*v[1]
        value+=eigenvalue*coordinate**2
    close(value,14)
    for m,x in [(((1,0),(0,1)),(3,4)),(((0,1),(1,0)),(2,3)),
                (((-1,0),(0,2)),(1,2))]:
        q=quadratic_form(m,x)
        close(q["quadratic_value"],q["polynomial_value"])
    rejects(ValueError,quadratic_form,((1,2),(3,4)),(1,1))
    rejects(ValueError,quadratic_form,((1,0),(0,1)),(1,))
    rejects(ValueError,quadratic_form,((1,0),(0,1)),(float("nan"),1))
    rejects(TypeError,finite,True,"entry")
    assert not p["runtime_certified"]
    print("PASS: Section 14.3 independent reference checks")

if __name__=="__main__":
    run()
