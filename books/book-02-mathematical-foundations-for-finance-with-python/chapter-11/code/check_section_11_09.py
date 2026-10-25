"""Independent reference checks for Section 11.9."""
import json
import math
from section_11_09 import Vector,Policy,finite,calculate,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    result=assessment()
    for asset,expected in {"ALPHA":50000,"BETA":-10000,"GAMMA":20000}.items():
        close(result["position_values_USD"][asset],expected)
    for asset,expected in {"ALPHA":0.5,"BETA":-0.1,"GAMMA":0.2}.items():
        close(result["weights"][asset],expected)
    for key,expected in {"net":0.6,"gross":0.8,"long":0.7,"short":0.1}.items():
        close(result["exposures"][key],expected)
    close(result["signed_risky_position_value_USD"],60000)
    close(result["unexplained_nav_difference_USD"],40000)
    close(result["scenarios"]["A"]["pnl_USD"],1900)
    close(result["scenarios"]["A"]["nav_return_contribution"],0.019)
    close(result["scenarios"]["B"]["pnl_USD"],-1900)
    close(result["scenarios"]["B"]["nav_return_contribution"],-0.019)
    assert result["policy"]["feasible"]
    assert json.dumps(result,sort_keys=True)==json.dumps(assessment(),sort_keys=True)
    prices=Vector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    holdings=Vector(("GAMMA","ALPHA","BETA"),(800,500,-200),"shares")
    scenarios={"A":Vector(prices.labels,(0.02,-0.01,0.04),"simple_return")}
    breached=calculate(prices,holdings,100000,scenarios,Policy(gross_cap=0.5,absolute_name_cap=0.4,max_unexplained_nav_gap_usd=100))
    assert not breached["policy"]["feasible"]
    assert "gross_cap" in breached["policy"]["breaches"]
    assert "absolute_name_cap:ALPHA" in breached["policy"]["breaches"]
    assert "unexplained_nav_gap" in breached["policy"]["breaches"]
    rejects(ValueError,calculate,prices,holdings,0,scenarios)
    rejects(ValueError,calculate,prices,holdings,100000,{"A":Vector(("ALPHA","BETA","DELTA"),(0,0,0),"simple_return")})
    rejects(ValueError,Vector,("A","A"),(1,2),"shares")
    rejects(TypeError,finite,True,"value")
    assert result["runtime_certified"] is False
    print("PASS: Section 11.9 independent reference checks")

if __name__=="__main__":
    run()
