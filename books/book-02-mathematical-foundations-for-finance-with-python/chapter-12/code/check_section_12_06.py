"""Independent reference checks for Book 02 Section 12.6."""
import math
from section_12_06 import Matrix2,Vector2,finite,determinant,inverse,solve_exposures,assessment

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
    close(report["determinant"],-3)
    for row,expected in zip(report["inverse"],((1/3,1/3),(1/3,-2/3))):
        for actual,want in zip(row,expected):
            close(actual,want)
    a=Matrix2(("RATE","CREDIT"),("BOND_A","BOND_B"),
              ((2,1),(1,-1)),"standardized_sensitivity")
    inv=inverse(a)
    for left,right in ((a.rows,inv.rows),(inv.rows,a.rows)):
        for i in range(2):
            for j in range(2):
                close(sum(left[i][k]*right[k][j] for k in range(2)),1 if i==j else 0)
    result=report["exposure_match"]
    close(result["quantities"]["BOND_A"],2)
    close(result["quantities"]["BOND_B"],1)
    for residual in result["residual"].values():
        close(residual,0)
    reordered=solve_exposures(a,Vector2(("RATE","CREDIT"),(5,1),"standardized_exposure"))
    assert reordered["quantities"]==result["quantities"]
    singular=Matrix2(("R","C"),("A","B"),((1,2),(2,4)),"standardized_sensitivity")
    close(determinant(singular),0)
    rejects(ValueError,inverse,singular)
    rejects(ValueError,solve_exposures,a,Vector2(("RATE","WRONG"),(5,1),"standardized_exposure"))
    rejects(ValueError,solve_exposures,a,Vector2(("RATE","CREDIT"),(5,1),"USD"))
    rejects(ValueError,Matrix2,("RATE","RATE"),("A","B"),((1,2),(3,4)),"standardized_sensitivity")
    rejects(ValueError,Matrix2,("RATE","CREDIT"),("A","B"),((1,2),(3,)),"standardized_sensitivity")
    rejects(ValueError,Matrix2,("RATE","CREDIT"),("A","B"),((1,float("nan")),(3,4)),"standardized_sensitivity")
    rejects(TypeError,finite,True,"entry")
    assert result["runtime_certified"] is False
    print("PASS: Section 12.6 independent reference checks")

if __name__=="__main__":
    run()
