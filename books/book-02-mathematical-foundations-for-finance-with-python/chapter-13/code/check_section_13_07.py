"""Independent reference checks for Book 02 Section 13.7."""
import math
from section_13_07 import finite,checked_labels,solve_weighted,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    p=assessment()["reference"]
    close(p["position"],3.25)
    close(p["achieved"]["RATE"],3.25)
    close(p["achieved"]["CREDIT"],6.5)
    close(p["residual_target_minus_achieved"]["RATE"],-0.25)
    close(p["residual_target_minus_achieved"]["CREDIT"],0.5)
    close(p["standardized_residual"]["RATE"],-0.25)
    close(p["standardized_residual"]["CREDIT"],0.25)
    close(p["weighted_objective"],0.0625)
    close(p["weighted_gradient"],0)
    assert p["factor_pass"]=={"RATE":False,"CREDIT":True}
    assert p["decision"]=="REJECT"
    assert not p["runtime_certified"]
    factors=("RATE","CREDIT")
    units={"RATE":"rate_sensitivity_units","CREDIT":"credit_sensitivity_units"}
    converted=solve_weighted(factors,{"RATE":1000,"CREDIT":2},
        {"RATE":3000,"CREDIT":7},{"RATE":1000,"CREDIT":2},
        {"RATE":200,"CREDIT":0.6},units)
    close(converted["position"],3.25)
    close(converted["weighted_objective"],0.0625)
    assert converted["factor_pass"]==p["factor_pass"]
    rejects(ValueError,solve_weighted,factors,{"RATE":1,"CREDIT":2},
        {"RATE":3,"CREDIT":7},{"RATE":0,"CREDIT":2},
        {"RATE":0.2,"CREDIT":0.6},units)
    rejects(ValueError,solve_weighted,factors,{"RATE":1,"CREDIT":2},
        {"RATE":3,"CREDIT":7},{"RATE":1,"CREDIT":2},
        {"RATE":-0.2,"CREDIT":0.6},units)
    rejects(ValueError,solve_weighted,factors,{"RATE":1,"CREDIT":2},
        {"RATE":3,"WRONG":7},{"RATE":1,"CREDIT":2},
        {"RATE":0.2,"CREDIT":0.6},units)
    rejects(ValueError,solve_weighted,factors,{"RATE":1,"CREDIT":2},
        {"RATE":3,"CREDIT":7},{"RATE":1,"CREDIT":2},
        {"RATE":0.2,"CREDIT":0.6},{"RATE":"rate_sensitivity_units","CREDIT":""})
    rejects(ValueError,checked_labels,("RATE","RATE"),"factors")
    rejects(TypeError,finite,True,"entry")
    print("PASS: Section 13.7 independent reference checks")

if __name__=="__main__":
    run()
