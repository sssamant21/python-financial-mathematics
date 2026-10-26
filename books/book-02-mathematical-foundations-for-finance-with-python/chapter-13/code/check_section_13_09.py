"""Independent project acceptance checks for Book 02 Section 13.9."""
import math
from section_13_09 import analyze,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def inputs():
    f=("RATE","CREDIT","LIQUIDITY")
    return (f,("BOND_A","BOND_B"),((1,0),(0,1),(1,1)),
            {"RATE":2,"CREDIT":3,"LIQUIDITY":6},
            {"RATE":1,"CREDIT":1,"LIQUIDITY":1},
            {"RATE":0.4,"CREDIT":0.4,"LIQUIDITY":0.25},
            {k:"standardized_exposure" for k in f})

def run():
    p=assessment()["reference"]
    close(p["positions"]["BOND_A"],7/3)
    close(p["positions"]["BOND_B"],10/3)
    close(p["achieved"]["LIQUIDITY"],17/3)
    for f in ("RATE","CREDIT"):
        close(p["residual_target_minus_achieved"][f],-1/3)
    close(p["residual_target_minus_achieved"]["LIQUIDITY"],1/3)
    close(p["weighted_objective"],1/6)
    for v in p["weighted_gradient"].values():
        close(v,0)
    assert p["factor_pass"]=={"RATE":True,"CREDIT":True,"LIQUIDITY":False}
    assert p["decision"]=="REJECT"
    assert not p["runtime_certified"]
    f,n,a,b,s,limits,units=inputs()
    scaled=analyze(f,n,((1000,0),(0,1),(1,1)),
                   {"RATE":2000,"CREDIT":3,"LIQUIDITY":6},
                   {"RATE":1000,"CREDIT":1,"LIQUIDITY":1},
                   {"RATE":400,"CREDIT":0.4,"LIQUIDITY":0.25},units)
    close(scaled["weighted_objective"],1/6)
    close(scaled["positions"]["BOND_A"],7/3)
    assert scaled["decision"]==p["decision"]
    rejects(ValueError,analyze,f,n,a,b,{"RATE":0,"CREDIT":1,"LIQUIDITY":1},limits,units)
    rejects(ValueError,analyze,f,n,a,b,s,limits,{"RATE":"","CREDIT":"unit","LIQUIDITY":"unit"})
    rejects(ValueError,analyze,f,n,((1,1),(2,2),(3,3)),b,s,limits,units)
    rejects(ValueError,analyze,f,n,a,{"RATE":2,"CREDIT":3,"WRONG":6},s,limits,units)
    print("PASS: Section 13.9 project acceptance checks")

if __name__=="__main__":
    run()
