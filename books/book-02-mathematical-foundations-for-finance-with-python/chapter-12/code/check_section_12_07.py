"""Independent reference checks for Book 02 Section 12.7."""
import math
from section_12_07 import Matrix2,Vector2,finite,condition_inf,solve,perturbation_study,assessment

def close(a,b,rel=1e-8,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    stable=report["well_conditioned"]
    fragile=report["nearly_dependent"]
    close(stable["condition_number_inf"],3)
    close(fragile["condition_number_inf"],40004.0001)
    close(stable["before"]["positions"]["BOND_A"],2)
    close(stable["before"]["positions"]["BOND_B"],1)
    close(stable["after"]["positions"]["BOND_A"],2.01)
    close(stable["after"]["positions"]["BOND_B"],0.98)
    close(fragile["before"]["positions"]["HEDGE_A"],1)
    close(fragile["before"]["positions"]["HEDGE_B"],1)
    close(fragile["after"]["positions"]["HEDGE_A"],-9)
    close(fragile["after"]["positions"]["HEDGE_B"],11)
    close(fragile["after"]["gross"],20)
    assert stable["bound_satisfied"] and fragile["bound_satisfied"]
    assert not stable["high_sensitivity_warning"]
    assert fragile["high_sensitivity_warning"]
    assert not stable["runtime_certified"] and not fragile["runtime_certified"]
    a=Matrix2(("RATE","CREDIT"),("A","B"),((2,1),(1,-1)),"standardized_sensitivity")
    b=Vector2(("RATE","CREDIT"),(5,1),"standardized_exposure")
    assert solve(a,b)==solve(a,Vector2(("CREDIT","RATE"),(1,5),"standardized_exposure"))
    rejects(ValueError,condition_inf,Matrix2(("RATE","CREDIT"),("A","B"),((1,2),(2,4)),"standardized_sensitivity"))
    rejects(ValueError,solve,a,Vector2(("RATE","WRONG"),(5,1),"standardized_exposure"))
    rejects(ValueError,Matrix2,("RATE","RATE"),("A","B"),((1,2),(3,4)),"standardized_sensitivity")
    rejects(ValueError,Matrix2,("RATE","CREDIT"),("A","B"),((1,2),(3,)),"standardized_sensitivity")
    rejects(ValueError,Vector2,("RATE","CREDIT"),(1,float("nan")),"standardized_exposure")
    rejects(TypeError,finite,True,"entry")
    print("PASS: Section 12.7 independent reference checks")

if __name__=="__main__":
    run()
