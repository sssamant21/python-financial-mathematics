"""Independent reference checks for Section 11.7."""
import math
from section_11_07 import Vector,finite,weights_from_values,values_from_holdings,exposures,check_constraints,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    p=Vector(("A","B","C"),(100,50,25),"USD/share")
    q=Vector(("C","A","B"),(800,500,600),"shares")
    values=values_from_holdings(p,q)
    assert values.values==(50000,30000,20000)
    weights=weights_from_values(values,100000)
    for actual,expected in zip(weights.values,(0.5,0.3,0.2)):
        close(actual,expected)
    exp=exposures(weights)
    close(exp["net"],1)
    close(exp["gross"],1)
    assert check_constraints(weights,long_only=True,absolute_cap=0.6,gross_cap=1)["feasible"]
    assert not check_constraints(weights,absolute_cap=0.4)["feasible"]
    short=weights_from_values(Vector(p.labels,(120000,-40000,20000),"USD"),100000)
    exp=exposures(short)
    for name,expected in [("net",1),("long",1.4),("short",0.4),("gross",1.8)]:
        close(exp[name],expected)
    result=check_constraints(short,long_only=True,absolute_cap=0.6,gross_cap=1.5)
    assert not result["feasible"]
    assert "long_only:B" in result["breaches"] and "gross_cap" in result["breaches"]
    rejects(ValueError,weights_from_values,values,0)
    rejects(ValueError,weights_from_values,values,-1)
    rejects(ValueError,values_from_holdings,p,Vector(("A","B","D"),(1,2,3),"shares"))
    rejects(ValueError,Vector,("A","A"),(1,2),"USD")
    rejects(TypeError,finite,True,"value")
    report=assessment()
    assert report["long_only_policy"]["feasible"]
    assert not report["long_short_policy"]["feasible"]
    assert report["runtime_certified"] is False
    print("PASS: Section 11.7 independent reference checks")

if __name__=="__main__":
    run()
