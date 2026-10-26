"""Independent reference checks for Book 02 Section 13.4."""
import math
from section_13_04 import FactorVector,finite,project_line,assessment

def close(actual,expected):
    assert math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10),(actual,expected)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    p=report["approximate"]
    close(p["coefficient"],3.4)
    close(p["projected"]["RATE"],3.4)
    close(p["projected"]["CREDIT"],6.8)
    close(p["residual_target_minus_projected"]["RATE"],-0.4)
    close(p["residual_target_minus_projected"]["CREDIT"],0.2)
    close(p["distance_l2"],math.sqrt(0.2))
    close(p["direction_dot_residual"],0)
    assert p["factor_pass"]=={"RATE":True,"CREDIT":False}
    assert p["decision"]=="REJECT"
    assert report["exact"]["decision"]=="ACCEPT"
    close(report["exact"]["distance_l2"],0)
    direction=FactorVector(("RATE","CREDIT"),(1,2),"standardized_exposure")
    target=FactorVector(("RATE","CREDIT"),(3,7),"standardized_exposure")
    limits=FactorVector(("RATE","CREDIT"),(0.5,0.1),"standardized_exposure")
    assert project_line(direction,target,limits)==p
    rejects(ValueError,project_line,
            FactorVector(("RATE","CREDIT"),(0,0),"standardized_exposure"),target,limits)
    rejects(ValueError,project_line,direction,target,
            FactorVector(("RATE","CREDIT"),(-1,1),"standardized_exposure"))
    rejects(ValueError,project_line,direction,
            FactorVector(("RATE","WRONG"),(3,7),"standardized_exposure"),limits)
    rejects(ValueError,FactorVector,("RATE","RATE"),(1,2),"standardized_exposure")
    rejects(ValueError,FactorVector,("RATE",),(float("nan"),),"standardized_exposure")
    rejects(TypeError,finite,True,"value")
    assert not p["runtime_certified"]
    print("PASS: Section 13.4 independent reference checks")

if __name__=="__main__":
    run()
