"""Independent mathematical checks for Chapter 11 final assessment."""
import json
import math
from section_11_10 import Vector,finite,add,norm,project,portfolio,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_final_nonfinite_paths():
    labels=("A","B")
    for unit in ("USD/share","shares","simple_return"):
        for index in range(2):
            for invalid in (math.nan,math.inf,-math.inf):
                values=[1,2]
                values[index]=invalid
                rejects(ValueError,Vector,labels,tuple(values),unit)
    prices=Vector(labels,(100,50),"USD/share")
    holdings=Vector(labels,(1,2),"shares")
    returns=Vector(labels,(0.01,0.02),"simple_return")
    for invalid in (math.nan,math.inf,-math.inf,-1):
        rejects(ValueError,portfolio,prices,holdings,invalid,returns)
    rejects(TypeError,portfolio,prices,holdings,True,returns)
    # Valid finite records whose subsequent arithmetic is unrepresentable.
    rejects(ValueError,portfolio,Vector(("A",),(1e308,),"USD/share"),
            Vector(("A",),(2,),"shares"),1e308,
            Vector(("A",),(0,),"simple_return"))
    rejects(ValueError,portfolio,Vector(("A",),(1e308,),"USD/share"),
            Vector(("A",),(1,),"shares"),1e308,
            Vector(("A",),(2,),"simple_return"))
    rejects(ValueError,portfolio,prices,holdings,5e-324,returns)
    rejects(ValueError,portfolio,Vector(labels,(100,50),"EUR/share"),
            holdings,1000,returns)
    # The successful assessment must serialize with nonfinite JSON disabled.
    encoded=json.dumps(assessment(),sort_keys=True,allow_nan=False)
    assert json.loads(encoded)["portfolio"]["scenario_pnl_USD"]==1900

def run():
    check_final_nonfinite_paths()
    report=assessment()
    assert tuple(report["vector_sum"])==(-2.0,4.0,4.0)
    close(report["l1_norm"],6)
    close(report["l2_norm"],math.sqrt(14))
    close(report["linf_norm"],3)
    for actual,expected in zip(report["projection"],(3,3)):
        close(actual,expected)
    p=report["portfolio"]
    for asset,expected in {"ALPHA":50000,"BETA":-10000,"GAMMA":20000}.items():
        close(p["values_USD"][asset],expected)
    for asset,expected in {"ALPHA":0.5,"BETA":-0.1,"GAMMA":0.2}.items():
        close(p["weights"][asset],expected)
    for name,expected in {"net":0.6,"gross":0.8,"long":0.7,"short":0.1}.items():
        close(p[name],expected)
    close(p["unexplained_nav_gap_USD"],40000)
    close(p["scenario_pnl_USD"],1900)
    close(p["nav_return_contribution"],0.019)
    assert json.dumps(report,sort_keys=True)==json.dumps(assessment(),sort_keys=True)
    x=Vector(("X","Y"),(4,2),"USD")
    rejects(ValueError,project,x,Vector(("X","Y"),(0,0),"dimensionless"))
    rejects(ValueError,project,x,Vector(("X","Y"),(1,1),"USD"))
    rejects(ValueError,Vector,("X","X"),(1,2),"USD")
    rejects(TypeError,finite,True,"component")
    prices=Vector(("ALPHA","BETA"),(100,50),"USD/share")
    holdings=Vector(("ALPHA","BETA"),(1,2),"shares")
    returns=Vector(("ALPHA","BETA"),(0.01,0.02),"simple_return")
    rejects(ValueError,portfolio,prices,holdings,0,returns)
    rejects(ValueError,portfolio,prices,holdings,1000,Vector(("ALPHA","GAMMA"),(0.01,0.02),"simple_return"))
    assert report["runtime_certified"] is False
    print("PASS: Section 11.10 independent reference checks")

if __name__=="__main__":
    run()
