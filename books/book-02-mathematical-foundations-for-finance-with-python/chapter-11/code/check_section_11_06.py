"""Independent reference checks for Section 11.6."""
import math
from section_11_06 import Vector,finite,projection,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    x=Vector(("X","Y"),(3,4),"USD")
    horizontal=Vector(("Y","X"),(0,1),"dimensionless")
    result=projection(x,horizontal)
    assert result["projection"].values==(3,0)
    assert result["residual"].values==(0,4)
    close(result["coefficient"],3)
    diagonal=Vector(("X","Y"),(1,1),"dimensionless")
    result=projection(x,diagonal)
    for a,b in zip(result["projection"].values,(3.5,3.5)):
        close(a,b)
    for a,b in zip(result["residual"].values,(-0.5,0.5)):
        close(a,b)
    reversed_direction=Vector(diagonal.labels,(-1,-1),"dimensionless")
    reversed_result=projection(x,reversed_direction)
    for a,b in zip(result["projection"].values,reversed_result["projection"].values):
        close(a,b)
    scaled=Vector(diagonal.labels,(10,10),"dimensionless")
    for a,b in zip(result["projection"].values,projection(x,scaled)["projection"].values):
        close(a,b)
    close(sum(a*b for a,b in zip(result["residual"].values,diagonal.values)),0)
    close(sum(a*a for a in x.values),
          sum(a*a for a in result["projection"].values)+sum(a*a for a in result["residual"].values))
    rejects(ValueError,projection,x,Vector(x.labels,(0,0),"dimensionless"))
    rejects(ValueError,projection,x,Vector(x.labels,(1,0),"USD"))
    rejects(ValueError,projection,x,Vector(("X","Z"),(1,0),"dimensionless"))
    rejects(TypeError,finite,True,"component")
    report=assessment()
    assert report["projected_exposures_USD"]=={"ALPHA":75.0,"BETA":75.0,"GAMMA":0.0}
    assert report["residual_exposures_USD"]=={"ALPHA":25.0,"BETA":-25.0,"GAMMA":-20.0}
    close(report["residual_dot_direction"],0)
    close(report["pythagorean_squared_error"],0)
    assert report["runtime_certified"] is False
    print("PASS: Section 11.6 independent reference checks")

if __name__=="__main__":
    run()
