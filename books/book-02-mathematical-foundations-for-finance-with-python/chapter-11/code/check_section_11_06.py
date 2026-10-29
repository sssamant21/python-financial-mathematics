"""Independent reference checks for Section 11.6."""
import math
from fractions import Fraction
from section_11_06 import Vector,finite,projection,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_independent_projection():
    labels=("A","B","C")
    for values,direction in (((3,4,-2),(1,2,0)),((0,0,0),(1,2,3)),
                             ((2,-1,0),(1,2,0)),((-3,-4,2),(1,2,0))):
        x=Vector(labels,values,"USD")
        for scale in (1,2,-2,1e150,1e-150):
            d=tuple(scale*z for z in direction)
            # Exact represented-float rational dot/denominator oracle.
            fx=tuple(Fraction.from_float(float(z)) for z in values)
            fd=tuple(Fraction.from_float(float(z)) for z in d)
            coefficient=sum(a*b for a,b in zip(fx,fd))/sum(z*z for z in fd)
            expected=tuple(float(coefficient*z) for z in fd)
            vector=Vector(("C","A","B"),(d[2],d[0],d[1]),"dimensionless")
            result=projection(x,vector)
            actual=result["projection"]
            residual=result["residual"]
            assert actual.labels==residual.labels==labels
            assert actual.unit==residual.unit=="USD"
            assert actual.axis==residual.axis=="asset"
            assert math.isclose(result["coefficient"],float(coefficient),rel_tol=1e-12,abs_tol=0)
            close(result["scalar_projection"],float(coefficient)*math.hypot(*d))
            for a,b in zip(actual.values,expected):close(a,b)
            for a,b,c in zip(values,actual.values,residual.values):close(a,b+c)
            # Independent orthogonality with the unscaled direction.
            close(sum(a*b for a,b in zip(residual.values,direction)),0)
            close(sum(z*z for z in values),
                  sum(z*z for z in actual.values)+sum(z*z for z in residual.values))
    report=assessment()
    close(report["projection_coefficient_USD"],75)
    close(report["signed_scalar_projection_USD"],150/math.sqrt(2))
    close(report["residual_norm_USD"],math.sqrt(1650))
    close(report["relative_residual_norm"],math.sqrt(1650/12900))

def run():
    check_independent_projection()
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
    for k,v in {"ALPHA":75.0,"BETA":75.0,"GAMMA":0.0}.items():
        close(report["projected_exposures_USD"][k],v)
    for k,v in {"ALPHA":25.0,"BETA":-25.0,"GAMMA":-20.0}.items():
        close(report["residual_exposures_USD"][k],v)
    close(report["residual_dot_direction"],0)
    close(report["pythagorean_squared_error"],0)
    assert report["runtime_certified"] is False
    print("PASS: Section 11.6 independent reference checks")

if __name__=="__main__":
    run()
