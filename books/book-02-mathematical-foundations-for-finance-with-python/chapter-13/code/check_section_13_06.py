"""Independent reference checks for Book 02 Section 13.6."""
import math
from section_13_06 import finite,labels,solve_qr,assessment

def close(actual,expected):
    assert math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10),(actual,expected)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    result=assessment()["reference"]
    close(result["positions"]["BOND_A"],7/3)
    close(result["positions"]["BOND_B"],10/3)
    close(result["achieved"]["LIQUIDITY"],17/3)
    close(result["residual_target_minus_achieved"]["RATE"],-1/3)
    close(result["residual_target_minus_achieved"]["CREDIT"],-1/3)
    close(result["residual_target_minus_achieved"]["LIQUIDITY"],1/3)
    close(result["objective_half_squared_l2"],1/6)
    for g in result["gradient"].values():
        close(g,0)
    assert not result["runtime_certified"]
    factors=("RATE","CREDIT","LIQUIDITY")
    reordered=solve_qr(factors,("BOND_B","BOND_A"),((0,1),(1,0),(1,1)),
                       factors,(2,3,6))
    close(reordered["positions"]["BOND_A"],7/3)
    close(reordered["positions"]["BOND_B"],10/3)
    exact=solve_qr(("RATE","CREDIT"),("A","B"),((1,0),(0,1)),
                   ("RATE","CREDIT"),(4,8))
    close(exact["positions"]["A"],4)
    close(exact["positions"]["B"],8)
    close(exact["objective_half_squared_l2"],0)
    rejects(ValueError,solve_qr,("RATE","CREDIT"),("A","B"),((1,1),(2,2)),
            ("RATE","CREDIT"),(3,6))
    rejects(ValueError,solve_qr,("RATE",),("A","B"),((1,2),),("RATE",),(3,))
    rejects(ValueError,solve_qr,("RATE","CREDIT"),("A","B"),((1,0),(0,1)),
            ("RATE","WRONG"),(3,6))
    rejects(ValueError,solve_qr,("RATE","CREDIT"),("A","B"),((1,0),(0,float("nan"))),
            ("RATE","CREDIT"),(3,6))
    rejects(ValueError,labels,("RATE","RATE"),"factors")
    rejects(TypeError,finite,True,"entry")
    print("PASS: Section 13.6 independent reference checks")

if __name__=="__main__":
    run()
