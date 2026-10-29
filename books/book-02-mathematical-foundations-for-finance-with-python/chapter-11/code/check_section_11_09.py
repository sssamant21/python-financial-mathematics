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

def check_policy_audit():
    prices=Vector(("A",),(1,),"USD/share")
    scenarios={"zero":Vector(("A",),(0,),"simple_return")}
    def report(holding,policy):
        return calculate(prices,Vector(("A",),(holding,),"shares"),1,scenarios,policy)
    for field,breach in (("gross_cap","gross_cap"),("absolute_name_cap","absolute_name_cap:A")):
        limits={"gross_cap":1,"absolute_name_cap":1,"max_unexplained_nav_gap_usd":1}
        limits[field]=0.5
        policy=Policy(**limits)
        threshold=0.5+1e-10
        for holding,expected in ((math.nextafter(threshold,0),[]),(threshold,[]),
                                 (math.nextafter(threshold,math.inf),[breach])):
            result=report(holding,policy)
            assert result["policy"]["limits"]==limits
            assert result["policy"]["comparison_tolerances"]=={"exposure":1e-10,"nav_gap_USD":1e-8}
            assert result["policy"]["breaches"]==expected
            assert result["policy"]["feasible"] is (not expected)
            close(result["exposures"]["gross"],abs(holding))
            close(result["unexplained_nav_difference_USD"],1-holding)
    # Construct the effective gap threshold at exactly one in float arithmetic.
    gap_limit=1-1e-8
    assert gap_limit+1e-8==1
    policy=Policy(gross_cap=2,absolute_name_cap=2,max_unexplained_nav_gap_usd=gap_limit)
    for holding,expected in ((2.0**-52,[]),(0,[]),(-2.0**-52,["unexplained_nav_gap"])):
        result=report(holding,policy)
        assert result["policy"]["breaches"]==expected
        assert result["policy"]["feasible"] is (not expected)
        assert result["policy"]["limits"]["max_unexplained_nav_gap_usd"]==gap_limit
    reference=assessment()
    assert reference["policy"]["limits"]=={
        "gross_cap":1,"absolute_name_cap":0.6,"max_unexplained_nav_gap_usd":40000}
    for key in ("gross_cap","absolute_name_cap","max_unexplained_nav_gap_usd"):
        for value,exception in ((-1,ValueError),(float("nan"),ValueError),(True,TypeError)):
            try:
                Policy(**{key:value})
            except exception:
                pass
            else:
                raise AssertionError((key,value))
    rejects(ValueError,calculate,prices,Vector(("A",),(1,),"shares"),1,{})
    rejects(ValueError,calculate,prices,Vector(("A",),(1,),"shares"),1,
            {"bad":Vector(("A",),(0,),"USD")})

def run():
    check_policy_audit()
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
