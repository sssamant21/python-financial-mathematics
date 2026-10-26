"""Independent reference checks for Section 12.8."""
import math
from section_12_08 import ExposureMatrix,Vector,finite,evaluate,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    assert report["exact"]["accepted"]
    assert not report["imperfect"]["accepted"]
    imperfect=report["imperfect"]
    close(imperfect["achieved"]["RATE"],4.9)
    close(imperfect["achieved"]["CREDIT"],0.8)
    close(imperfect["residual_target_minus_actual"]["RATE"],0.1)
    close(imperfect["residual_target_minus_actual"]["CREDIT"],0.2)
    close(imperfect["residual_inf"],0.2)
    close(imperfect["relative_target_residual_inf"],0.04)
    close(imperfect["normwise_backward_error_inf"],0.2/10.7)
    assert imperfect["factor_pass"]=={"RATE":True,"CREDIT":False}
    a=ExposureMatrix(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),"standardized_sensitivity")
    p=Vector(("BOND_A","BOND_B"),(1.9,1.1),"quantity")
    b=Vector(("RATE","CREDIT"),(5,1),"standardized_exposure")
    limits=Vector(("RATE","CREDIT"),(0.15,0.10),"standardized_exposure")
    assert evaluate(a,p,b,limits)==imperfect
    rejects(ValueError,evaluate,a,p,Vector(("RATE","WRONG"),(5,1),"standardized_exposure"),limits)
    rejects(ValueError,evaluate,a,p,b,Vector(("RATE","CREDIT"),(-1,0.1),"standardized_exposure"))
    rejects(ValueError,ExposureMatrix,("RATE","RATE"),("A","B"),((1,2),(3,4)),"standardized_sensitivity")
    rejects(ValueError,ExposureMatrix,("RATE","CREDIT"),("A","B"),((1,2),(3,)),"standardized_sensitivity")
    rejects(ValueError,Vector,("RATE",),(float("nan"),),"standardized_exposure")
    rejects(TypeError,finite,True,"value")
    assert not imperfect["runtime_certified"]
    print("PASS: Section 12.8 independent reference checks")

if __name__=="__main__":
    run()
