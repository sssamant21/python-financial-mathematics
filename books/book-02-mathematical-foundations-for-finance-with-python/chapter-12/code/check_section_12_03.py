"""Independent reference checks for Section 12.3."""
import math
from section_12_03 import Matrix,finite,transpose,identity,diagonal,multiply,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=Matrix(("R1","R2"),("C1","C2","C3"),((1,2,3),(4,5,6)),"dimensionless","row","column")
    at=transpose(a)
    assert at.shape==(3,2)
    assert at.rows==((1,4),(2,5),(3,6))
    assert transpose(at)==a
    assert multiply(identity(a.row_labels,"row"),a)==a
    assert multiply(a,identity(a.column_labels,"column"))==a
    b=Matrix(("C1","C2","C3"),("X","Y"),((2,1),(0,3),(1,4)),"dimensionless","column","factor")
    lhs=transpose(multiply(a,b))
    rhs=multiply(transpose(b),transpose(a))
    assert lhs.row_labels==rhs.row_labels and lhs.column_labels==rhs.column_labels
    for leftrow,rightrow in zip(lhs.rows,rhs.rows):
        for x,y in zip(leftrow,rightrow):
            close(x,y)
    d=diagonal(("R2","R1"),(3,2),"row")
    scaled=multiply(d,a)
    assert scaled.rows==((12,15,18),(2,4,6))
    report=assessment()
    assert tuple(report["transpose_shape"])==(2,3)
    close(report["factor_exposures"]["RATE"],0.7)
    close(report["factor_exposures"]["CREDIT"],2.2)
    assert report["identity_preserves_matrix"]
    rejects(ValueError,identity,("A","A"),"asset")
    rejects(ValueError,diagonal,("A","B"),(1,),"asset")
    rejects(ValueError,multiply,a,identity(("WRONG","C2","C3"),"column"))
    rejects(TypeError,finite,True,"entry")
    rejects(ValueError,Matrix,("R",),("C",),((float("inf"),),),"dimensionless","row","column")
    assert report["runtime_certified"] is False
    print("PASS: Section 12.3 independent reference checks")

if __name__=="__main__":
    run()
