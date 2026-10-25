"""Independent reference checks for Section 9.8."""
import math
from section_9_08 import (
    finite,bp_to_decimal,parallel_report,spot_scenario,validate_flows)

def close(a,b,rel_tol=1e-9,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(bp_to_decimal(25),0.0025)
    close(bp_to_decimal(-50),-0.005)
    flows=[(100,1),(1100,2)]
    report=parallel_report(flows,0.04,[-100,-50,0,50,100],0.25)
    v1,v2=100*math.exp(-0.04),1100*math.exp(-0.08)
    value=v1+v2
    close(report["baseline_value"],value)
    close(report["first_derivative"],-v1-2*v2)
    close(report["second_derivative"],v1+4*v2)
    assert len(report["scenarios"])==5
    for row in report["scenarios"]:
        h=row["shock_decimal"]
        exact=v1*math.expm1(-h)+v2*math.expm1(-2*h)
        linear=(-v1-2*v2)*h
        quadratic=linear+0.5*(v1+4*v2)*h*h
        close(row["exact_change"],exact)
        close(row["linear_change"],linear)
        close(row["quadratic_change"],quadratic)
        close(row["exact_value"],value+exact)
        assert abs(row["quadratic_error"])<=abs(row["linear_error"])+1e-10
        assert row["quadratic_within_tolerance"]==(abs(row["quadratic_error"])<=0.25)
        if h>0:
            assert exact<0
        if h<0:
            assert exact>0
        if h==0:
            close(exact,0)
            close(row["linear_change"],0)
            close(row["quadratic_change"],0)
    spot=spot_scenario(flows,[0.035,0.04],[10,-20])
    expected=100*math.exp(-0.035)*math.expm1(-0.001)+1100*math.exp(-0.08)*math.expm1(0.004)
    close(spot["exact_change"],expected)
    rejects(ValueError,validate_flows,[])
    rejects(ValueError,parallel_report,flows,0.04,[0],-0.1)
    rejects(ValueError,spot_scenario,flows,[0.04],[10,20])
    rejects(ValueError,spot_scenario,flows,[0.04,0.04],[10])
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("inf"),"value")
    print("PASS: Section 9.8 reference checks")

if __name__=="__main__":
    run()
