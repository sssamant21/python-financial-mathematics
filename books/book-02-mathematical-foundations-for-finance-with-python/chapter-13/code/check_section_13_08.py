"""Independent reference checks for Book 02 Section 13.8."""
import math
from section_13_08 import finite,solve_redundant_hedges,assessment

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
    close(p["positions"]["BOND_A"],1.25)
    close(p["positions"]["BOND_B"],1.25)
    close(p["achieved"]["RATE"],2.5)
    close(p["achieved"]["CREDIT"],5)
    close(p["residual_target_minus_achieved"]["RATE"],0.5)
    close(p["residual_target_minus_achieved"]["CREDIT"],1)
    close(p["data_objective"],0.625)
    close(p["penalty_objective"],3.125)
    close(p["total_objective"],3.75)
    for value in p["gradient"].values():
        close(value,0)
    assert p["factor_pass"]=={"RATE":False,"CREDIT":True}
    assert p["decision"]=="REJECT"
    assert not p["runtime_certified"]
    limits={"RATE":0.4,"CREDIT":1.1}
    low=solve_redundant_hedges(0.5,limits)
    high=solve_redundant_hedges(20,limits)
    assert low["positions"]["BOND_A"]>p["positions"]["BOND_A"]>high["positions"]["BOND_A"]
    rejects(ValueError,solve_redundant_hedges,0,limits)
    rejects(ValueError,solve_redundant_hedges,-1,limits)
    rejects(ValueError,solve_redundant_hedges,2,{"RATE":0.4})
    rejects(ValueError,solve_redundant_hedges,2,{"RATE":-1,"CREDIT":1.1})
    rejects(ValueError,solve_redundant_hedges,2,{"RATE":0.4,"CREDIT":float("nan")})
    rejects(TypeError,finite,True,"entry")
    print("PASS: Section 13.8 independent reference checks")

if __name__=="__main__":
    run()
