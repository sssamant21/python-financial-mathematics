"""Independent reference checks for Section 11.2."""
import math
from section_11_02 import Vector,finite,add,subtract,scale,linear_combination,assessment

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def close_vector(a,b):
    assert a.labels==b.labels and a.unit==b.unit and a.axis==b.axis
    assert all(math.isclose(x,y,rel_tol=1e-12,abs_tol=1e-8) for x,y in zip(a.values,b.values))

def run():
    x=Vector(("A","B","C"),(2,-3,4),"USD")
    y=Vector(("C","A","B"),(1,5,7),"USD")
    close_vector(add(x,y),Vector(("A","B","C"),(7,4,5),"USD"))
    close_vector(subtract(x,y),Vector(("A","B","C"),(-3,-10,3),"USD"))
    close_vector(scale(x,3),Vector(("A","B","C"),(6,-9,12),"USD"))
    close_vector(scale(x,0),Vector(("A","B","C"),(0,0,0),"USD"))
    close_vector(add(x,scale(x,-1)),scale(x,0))
    close_vector(add(x,y),add(y,x).align(x.labels))
    close_vector(scale(add(x,y),1.1),add(scale(x,1.1),scale(y,1.1)))
    close_vector(linear_combination(2,x,-1,y),subtract(scale(x,2),y))
    rejects(ValueError,add,x,Vector(("A","B","C"),(1,2,3),"EUR"))
    rejects(ValueError,add,x,Vector(("A","B","C"),(1,2,3),"USD","time"))
    rejects(ValueError,add,x,Vector(("A","B","D"),(1,2,3),"USD"))
    rejects(ValueError,Vector,("A","A"),(1,2),"USD")
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,scale,x,float("nan"))
    report=assessment()
    assert report["combined_exposure_USD"]=={"ALPHA":150000.0,"BETA":10000.0,"GAMMA":30000.0}
    assert report["signed_total_USD"]==190000
    assert report["incorrect_positional_exposures_USD"]==(90000.0,30000.0,70000.0)
    assert report["distributive_residual_max_USD"]<1e-8
    assert report["runtime_certified"] is False
    print("PASS: Section 11.2 independent reference checks")

if __name__=="__main__":
    run()
