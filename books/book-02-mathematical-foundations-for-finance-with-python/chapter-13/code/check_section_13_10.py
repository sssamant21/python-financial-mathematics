"""Independent chapter-wide reference checks for Section 13.10."""
import math
from section_13_10 import assessment
from section_13_06 import solve_qr
from section_13_07 import solve_weighted
from section_13_08 import solve_redundant_hedges
from section_13_09 import analyze

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    assert report["chapter"]=="13" and report["section"]=="13.10"
    close(report["qr_positions"]["BOND_A"],7/3)
    close(report["qr_positions"]["BOND_B"],10/3)
    close(report["qr_objective"],1/6)
    close(report["weighted_position"],3.25)
    close(report["weighted_objective"],0.0625)
    close(report["ridge_positions"]["BOND_A"],1.25)
    close(report["ridge_positions"]["BOND_B"],1.25)
    close(report["ridge_total_objective"],3.75)
    assert report["project_decision"]=="REJECT"
    assert not report["runtime_certified"]
    assert not report["independent_review_completed"]
    f=("RATE","CREDIT","LIQUIDITY")
    instruments=("BOND_A","BOND_B")
    matrix=((1,0),(0,1),(1,1))
    target={"RATE":2,"CREDIT":3,"LIQUIDITY":6}
    scales={k:1 for k in f}
    limits={"RATE":0.4,"CREDIT":0.4,"LIQUIDITY":0.25}
    units={k:"standardized_exposure" for k in f}
    project=analyze(f,instruments,matrix,target,scales,limits,units)
    close(project["weighted_objective"],1/6)
    assert project["factor_pass"]["LIQUIDITY"] is False
    assert project["decision"]=="REJECT"
    weighted=solve_weighted(("RATE","CREDIT"),
        {"RATE":1,"CREDIT":2},{"RATE":3,"CREDIT":7},
        {"RATE":1,"CREDIT":2},{"RATE":0.2,"CREDIT":0.6},
        {"RATE":"rate_units","CREDIT":"credit_units"})
    close(weighted["weighted_gradient"],0)
    ridge=solve_redundant_hedges(2,{"RATE":0.4,"CREDIT":1.1})
    close(ridge["data_objective"]+ridge["penalty_objective"],ridge["total_objective"])
    rejects(ValueError,solve_qr,("RATE","CREDIT"),("A","B"),
        ((1,1),(2,2)),("RATE","CREDIT"),(3,6))
    print("PASS: Section 13.10 chapter-wide reference checks")

if __name__=="__main__":
    run()
