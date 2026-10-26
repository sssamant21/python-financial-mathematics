"""Independent reference checks for Book 02 Section 13.5."""
import math
from section_13_05 import finite,checked_labels,solve_one_column,assessment

def close(actual,expected):
    assert math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10),(actual,expected)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    p=assessment()["reference"]
    close(p["position"],3.4)
    close(p["achieved"]["RATE"],3.4)
    close(p["achieved"]["CREDIT"],6.8)
    close(p["residual_target_minus_achieved"]["RATE"],-0.4)
    close(p["residual_target_minus_achieved"]["CREDIT"],0.2)
    close(p["objective_half_squared_l2"],0.1)
    close(p["gradient"],0)
    assert p["factor_pass"]=={"RATE":True,"CREDIT":False}
    assert p["decision"]=="REJECT"
    assert not p["runtime_certified"]
    reordered=solve_one_column(("RATE","CREDIT"),(1,2),
                               ("RATE","CREDIT"),(3,7),
                               ("RATE","CREDIT"),(0.5,0.1))
    assert reordered==p
    exact=solve_one_column(("RATE","CREDIT"),(1,2),
                           ("RATE","CREDIT"),(4,8),
                           ("RATE","CREDIT"),(0,0))
    close(exact["position"],4)
    close(exact["objective_half_squared_l2"],0)
    assert exact["decision"]=="ACCEPT"
    rejects(ValueError,solve_one_column,("RATE","CREDIT"),(0,0),
            ("RATE","CREDIT"),(3,7),("RATE","CREDIT"),(0.5,0.1))
    rejects(ValueError,solve_one_column,("RATE","CREDIT"),(1,2),
            ("RATE","WRONG"),(3,7),("RATE","CREDIT"),(0.5,0.1))
    rejects(ValueError,solve_one_column,("RATE","CREDIT"),(1,2),
            ("RATE","CREDIT"),(3,7),("RATE","CREDIT"),(-0.5,0.1))
    rejects(ValueError,checked_labels,("RATE","RATE"),"factors")
    rejects(ValueError,solve_one_column,("RATE","CREDIT"),(1,float("nan")),
            ("RATE","CREDIT"),(3,7),("RATE","CREDIT"),(0.5,0.1))
    rejects(TypeError,finite,True,"value")
    print("PASS: Section 13.5 independent reference checks")

if __name__=="__main__":
    run()
