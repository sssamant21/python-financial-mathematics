"""Independent reference checks for Section 12.4."""
import math
from section_12_04 import Matrix,Vector,finite,solve,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    result=assessment()
    close(result["financial_match"]["solution"]["BOND_A"],2)
    close(result["financial_match"]["solution"]["BOND_B"],1)
    close(result["financial_match"]["relative_residual_inf"],0)
    close(result["zero_pivot_case"]["solution"]["X"],1)
    close(result["zero_pivot_case"]["solution"]["Y"],1)
    a=Matrix(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),"standardized_sensitivity")
    x=solve(a,Vector(("RATE","CREDIT"),(5,1),"standardized_exposure"))
    y=solve(a,Vector(("CREDIT","RATE"),(1,5),"standardized_exposure"))
    assert x["solution"]==y["solution"]
    rejects(ValueError,solve,a,Vector(("RATE","WRONG"),(5,1),"standardized_exposure"))
    rejects(ValueError,solve,Matrix(("E1","E2"),("X","Y"),((1,2),(2,4)),"standardized_sensitivity"),Vector(("E1","E2"),(3,6),"standardized_exposure"))
    rejects(ValueError,solve,Matrix(("E1",),("X","Y"),((1,2),),"standardized_sensitivity"),Vector(("E1",),(3,),"standardized_exposure"))
    rejects(ValueError,Matrix,("E1","E1"),("X","Y"),((1,2),(2,3)),"standardized_sensitivity")
    rejects(ValueError,Matrix,("E1",),("X",),((float("nan"),),),"standardized_sensitivity")
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,solve,a,Vector(("RATE","CREDIT"),(5,1),"USD"))
    assert result["financial_match"]["runtime_certified"] is False
    print("PASS: Section 12.4 independent reference checks")

if __name__=="__main__":
    run()
