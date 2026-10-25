"""Independent reference checks for Section 12.1."""
import math
from section_12_01 import Vector,Matrix,finite,aggregate_factors,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    assert tuple(report["matrix_shape"])==(3,2)
    close(report["factor_exposures"]["RATE"],0.7)
    close(report["factor_exposures"]["CREDIT"],2.2)
    s=Matrix(("A","B","C"),("R","C"),((2,1),(-1,3),(0,4)),"standardized_sensitivity")
    a=Vector(("A","B","C"),(0.5,0.3,0.2),"weight")
    b=Vector(("C","A","B"),(0.2,0.5,0.3),"weight")
    for x,y in zip(aggregate_factors(a,s).values,aggregate_factors(b,s).values):
        close(x,y)
    rejects(ValueError,Matrix,("A","B"),("R","C"),((1,2),(3,)),"standardized_sensitivity")
    rejects(ValueError,Matrix,("A","A"),("R",),((1,),(2,)),"standardized_sensitivity")
    rejects(ValueError,aggregate_factors,Vector(("A","B","D"),(0.5,0.3,0.2),"weight"),s)
    rejects(ValueError,aggregate_factors,Vector(a.labels,a.values,"USD"),s)
    rejects(TypeError,finite,True,"component")
    rejects(ValueError,Matrix,("A",),("R",),((float("nan"),),),"standardized_sensitivity")
    assert report["runtime_certified"] is False
    print("PASS: Section 12.1 independent reference checks")

if __name__=="__main__":
    run()
