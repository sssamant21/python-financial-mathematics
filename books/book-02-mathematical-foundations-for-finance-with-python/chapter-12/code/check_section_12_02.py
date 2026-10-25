"""Independent reference checks for Section 12.2."""
import math
from section_12_02 import Matrix,finite,multiply,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    for row,expected in zip(report["AB"],((4,6),(10,12))):
        for actual,value in zip(row,expected):
            close(actual,value)
    for name,expected in {"RATE":0.7,"CREDIT":2.2}.items():
        close(report["factor_exposures"][name],expected)
    for name,expected in {"BASE":7.3,"STRESS":-0.8}.items():
        close(report["scenario_coordinates"][name],expected)
        close(report["associative_path"][name],expected)
    a=Matrix(("R1","R2"),("K1","K2"),((1,2),(3,4)),"dimensionless","rows","inner")
    b=Matrix(("K1","K2"),("C1","C2"),((2,0),(1,3)),"dimensionless","inner","columns")
    shuffled=Matrix(("K2","K1"),("C1","C2"),((1,3),(2,0)),"dimensionless","inner","columns")
    assert multiply(a,b).rows==multiply(a,shuffled).rows
    rejects(ValueError,multiply,a,Matrix(("X","Y"),("C1","C2"),((2,0),(1,3)),"dimensionless","inner","columns"))
    rejects(ValueError,multiply,a,Matrix(("K1","K2"),("C1","C2"),((2,0),(1,3)),"USD","inner","columns"))
    rejects(ValueError,multiply,a,Matrix(("K1","K2"),("C1","C2"),((2,0),(1,3)),"dimensionless","wrong_axis","columns"))
    rejects(ValueError,Matrix,("R1","R1"),("C",),((1,),(2,)),"dimensionless","row","col")
    rejects(ValueError,Matrix,("R1","R2"),("C",),((1,),(2,3)),"dimensionless","row","col")
    rejects(TypeError,finite,True,"entry")
    rejects(ValueError,Matrix,("R1",),("C",),((float("nan"),),),"dimensionless","row","col")
    assert report["runtime_certified"] is False
    print("PASS: Section 12.2 independent reference checks")

if __name__=="__main__":
    run()
