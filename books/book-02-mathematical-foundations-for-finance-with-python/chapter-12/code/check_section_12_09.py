"""Independent reference checks for Section 12.9 capstone."""
import math
from unittest.mock import patch
from section_12_09 import gaussian_solve
from section_12_09 import ExposureSystem,Vector,finite,evaluate,assessment

def close(a,b,rel=1e-8,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_rejection_contract():
    system=ExposureSystem(("RATE","CREDIT"),("A","B"),((2,1),(1,-1)),"standardized_sensitivity")
    target=Vector(("RATE","CREDIT"),(5,1),"standardized_exposure")
    limits=Vector(("CREDIT","RATE"),(0.25,0.25),"standardized_exposure")
    def imperfect(rows,rhs,tolerance):
        # Inject an imperfect target solve while retaining actual inverse solves
        # used for condition estimation.
        return (1.75,1.0) if tuple(rhs)==(5,1) else gaussian_solve(rows,rhs,tolerance)
    with patch("section_12_09.gaussian_solve",side_effect=imperfect):
        rejected=evaluate(system,target,limits)
        on_boundary=evaluate(system,target,Vector(("RATE","CREDIT"),(0.5,0.25),"standardized_exposure"))
        outside=evaluate(system,target,Vector(("RATE","CREDIT"),(math.nextafter(0.5,0),0.25),"standardized_exposure"))
    assert rejected["decision"]=="REJECT" and rejected["reason"]=="factor_tolerance_exceeded"
    assert rejected["factor_tolerances"]=={"RATE":0.25,"CREDIT":0.25}
    assert rejected["achieved"]=={"RATE":4.5,"CREDIT":0.75}
    assert rejected["residual_target_minus_actual"]=={"RATE":0.5,"CREDIT":0.25}
    assert rejected["factor_pass"]=={"RATE":False,"CREDIT":True}
    close(rejected["condition_number_inf"],3)
    close(rejected["residual_inf"],0.5)
    close(rejected["normwise_backward_error_inf"],2/41)
    close(rejected["gross_position"],2.75)
    close(rejected["net_position"],2.75)
    assert on_boundary["decision"]=="ACCEPT"
    assert outside["decision"]=="REJECT" and outside["factor_pass"]["RATE"] is False
    assert on_boundary["factor_tolerances"]=={"RATE":0.5,"CREDIT":0.25}
    # The exact condition number is three; guardrail equality is accepted.
    assert evaluate(system,target,limits,3)["decision"]=="ACCEPT"
    guarded=evaluate(system,target,limits,math.nextafter(3,0))
    assert guarded["decision"]=="REJECT" and guarded["reason"]=="condition_guardrail_exceeded"
    for bad in (float("nan"),float("inf")):
        rejects(ValueError,ExposureSystem,("RATE","CREDIT"),("A","B"),((bad,1),(1,-1)),"standardized_sensitivity")
    rejects(TypeError,ExposureSystem,("RATE","CREDIT"),("A","B"),((True,1),(1,-1)),"standardized_sensitivity")
    rejects(ValueError,ExposureSystem,("RATE","CREDIT"),("A","B"),((2,1),(1,-1)),"wrong_unit")
    rectangular=ExposureSystem(("RATE",),("A","B"),((2,1),),"standardized_sensitivity")
    rejects(ValueError,evaluate,rectangular,Vector(("RATE",),(5,),"standardized_exposure"),
            Vector(("RATE",),(0.1,),"standardized_exposure"))
    for condition,pivot in ((0.5,1e-12),(1000,0),(1000,1)):
        rejects(ValueError,evaluate,system,target,limits,condition,pivot)

def run():
    check_rejection_contract()
    report=assessment()
    ref=report["reference"]
    assert ref["decision"]=="ACCEPT" and ref["reason"]=="accepted"
    close(ref["positions"]["BOND_A"],2)
    close(ref["positions"]["BOND_B"],1)
    close(ref["condition_number_inf"],3)
    close(ref["residual_inf"],0)
    assert all(ref["factor_pass"].values())
    fragile=report["near_duplicate"]
    assert fragile["decision"]=="REJECT"
    assert fragile["reason"]=="condition_guardrail_exceeded"
    close(fragile["condition_number_inf"],40004.0001)
    assert not fragile["runtime_certified"]
    a=ExposureSystem(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),"standardized_sensitivity")
    b=Vector(("RATE","CREDIT"),(5,1),"standardized_exposure")
    t=Vector(("RATE","CREDIT"),(0.15,0.10),"standardized_exposure")
    assert evaluate(a,b,t)==ref
    rejects(ValueError,evaluate,a,Vector(("RATE","WRONG"),(5,1),"standardized_exposure"),t)
    rejects(ValueError,evaluate,a,b,Vector(("RATE","CREDIT"),(-0.1,0.1),"standardized_exposure"))
    rejects(ValueError,evaluate,ExposureSystem(("RATE","CREDIT"),("A","B"),((1,2),(2,4)),"standardized_sensitivity"),b,t)
    rejects(ValueError,ExposureSystem,("RATE","RATE"),("A","B"),((1,2),(3,4)),"standardized_sensitivity")
    rejects(ValueError,ExposureSystem,("RATE","CREDIT"),("A","B"),((1,2),(3,)),"standardized_sensitivity")
    rejects(ValueError,Vector,("RATE",),(float("nan"),),"standardized_exposure")
    rejects(TypeError,finite,True,"value")
    print("PASS: Section 12.9 independent reference checks")

if __name__=="__main__":
    run()
