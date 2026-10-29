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

def check_isolated_budget_and_boundaries():
    isolated=check_constraints(Vector(("A","B"),(0.5,0.25),"weight"),
                               long_only=True,absolute_cap=0.6,gross_cap=1)
    assert isolated["feasible"] is False and isolated["breaches"]==["budget"]
    assert isolated["exposures"]=={"net":0.75,"long":0.75,"short":0,"gross":0.75}
    tol=2.0**-20  # exact dyadic value within the supported tolerance range
    for weight,expected in ((1-tol,[]),(1+tol,[]),
                            (math.nextafter(1-tol,0),["budget"]),
                            (math.nextafter(1+tol,math.inf),["budget"])):
        result=check_constraints(Vector(("A",),(weight,),"weight"),tolerance=tol)
        assert result["breaches"]==expected
        assert result["feasible"] is (not expected)
    exact=Vector(("A",),(1,),"weight")
    adjacent=Vector(("A",),(math.nextafter(1,math.inf),),"weight")
    assert check_constraints(exact,tolerance=0)["feasible"]
    assert check_constraints(adjacent,tolerance=0)["breaches"]==["budget"]

    for setting,breach in (("absolute_cap","absolute_cap:A"),("gross_cap","gross_cap")):
        for weight,expected in ((0.5+tol,[]),(math.nextafter(0.5+tol,math.inf),[breach])):
            result=check_constraints(Vector(("A",),(weight,),"weight"),
                                     budget=weight,tolerance=tol,**{setting:0.5})
            assert result["breaches"]==expected
            assert result["feasible"] is (not expected)
    for short,expected in ((-tol,[]),(math.nextafter(-tol,-math.inf),["long_only:B"])):
        weights=Vector(("A","B"),(1-short,short),"weight")
        result=check_constraints(weights,long_only=True,tolerance=tol)
        assert result["breaches"]==expected
    for control in ({"tolerance":-1},{"tolerance":1e-5},{"absolute_cap":-1},{"gross_cap":-1}):
        try:
            check_constraints(exact,**control)
        except ValueError:
            pass
        else:
            raise AssertionError(control)

def run():
    check_isolated_budget_and_boundaries()
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
