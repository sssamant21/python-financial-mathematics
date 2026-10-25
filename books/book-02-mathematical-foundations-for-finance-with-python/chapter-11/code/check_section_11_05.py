"""Independent reference checks for Section 11.5."""
import math
from section_11_05 import Vector,finite,cosine,angle_degrees,orthogonal,assessment

def close(a,b,abs_tol=1e-10):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    x=Vector(("X","Y"),(1,0),"exposure")
    y=Vector(("Y","X"),(1,0),"exposure")
    close(cosine(x,y),0)
    close(angle_degrees(x,y),90)
    assert orthogonal(x,y)
    close(angle_degrees(x,x),0)
    close(angle_degrees(x,Vector(x.labels,(-1,0),"exposure")),180)
    diagonal=Vector(x.labels,(1,1),"exposure")
    close(cosine(diagonal,x),1/math.sqrt(2))
    close(angle_degrees(diagonal,x),45)
    a=Vector(("RATE","CREDIT"),(3,4),"exposure")
    b=Vector(("CREDIT","RATE"),(-3,4),"exposure")
    assert orthogonal(a,b)
    big=Vector(x.labels,(1e300,0),"exposure")
    big_perp=Vector(x.labels,(0,1e300),"exposure")
    close(angle_degrees(big,big_perp),90)
    rejects(ValueError,cosine,x,Vector(x.labels,(0,0),"exposure"))
    rejects(ValueError,cosine,x,Vector(("X","Z"),(1,0),"exposure"))
    rejects(ValueError,cosine,x,Vector(x.labels,(1,0),"other"))
    rejects(ValueError,orthogonal,x,y,-0.01)
    rejects(ValueError,Vector,("X","X"),(1,2),"exposure")
    rejects(TypeError,finite,True,"value")
    report=assessment()
    close(report["angle_orthogonal_degrees"],90)
    close(report["angle_positive_rescale_degrees"],0)
    close(report["angle_opposite_degrees"],180)
    assert report["is_orthogonal"] and report["runtime_certified"] is False
    print("PASS: Section 11.5 independent reference checks")

if __name__=="__main__":
    run()
