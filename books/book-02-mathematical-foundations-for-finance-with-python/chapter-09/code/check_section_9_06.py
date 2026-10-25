"""Independent reference checks for Section 9.6."""
import math
from section_9_06 import (
    finite, validate_flows, portfolio_sensitivity, parallel_shock,
    spot_curve_sensitivity, spot_shock)

def close(a,b,rel_tol=1e-8,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    for rate in (-0.02,0,0.04,0.1):
        model=portfolio_sensitivity([(10000,5)],rate)
        v=10000*math.exp(-5*rate)
        close(model["value"],v)
        close(model["first"],-5*v)
        close(model["second"],25*v)
        close(model["duration"],5)
        close(model["convexity"],25)
        close(model["cash_flow_derivatives"][0],math.exp(-5*rate))
        for h in (-0.01,-0.001,0.001,0.01):
            report=parallel_shock([(10000,5)],rate,h)
            close(report["exact_change"],v*math.expm1(-5*h))
            assert abs(report["quadratic_error"])<abs(report["linear_error"])
    flows=[(100,1),(1100,2)]
    m=portfolio_sensitivity(flows,0.04)
    v1,v2=100*math.exp(-0.04),1100*math.exp(-0.08)
    close(m["value"],v1+v2)
    close(m["duration"],(v1+2*v2)/(v1+v2))
    close(m["convexity"],(v1+4*v2)/(v1+v2))
    assert m["convexity"]>=m["duration"]**2
    close(sum(m["value_weights"]),1)
    spot=spot_curve_sensitivity(flows,[0.035,0.04])
    close(spot["value"],100*math.exp(-0.035)+1100*math.exp(-0.08))
    close(spot["spot_derivatives"][0],-100*math.exp(-0.035))
    close(spot["spot_derivatives"][1],-2200*math.exp(-0.08))
    bumps=[0.001,-0.002]
    change=spot_shock(flows,[0.035,0.04],bumps)
    exact=(100*math.exp(-0.035)*math.expm1(-0.001)
           +1100*math.exp(-0.08)*math.expm1(0.004))
    close(change["exact_change"],exact)
    close(change["linear_change"],sum(d*h for d,h in zip(spot["spot_derivatives"],bumps)))
    rejects(ValueError,validate_flows,[])
    rejects(ValueError,portfolio_sensitivity,[(0,5)],0.04)
    rejects(ValueError,portfolio_sensitivity,[(100,-1)],0.04)
    rejects(ValueError,spot_curve_sensitivity,flows,[0.04])
    rejects(ValueError,spot_shock,flows,[0.04,0.04],[0.001])
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 9.6 reference checks")

if __name__=="__main__":
    run()
