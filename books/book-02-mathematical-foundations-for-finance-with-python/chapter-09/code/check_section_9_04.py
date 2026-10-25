"""Independent reference checks for Section 9.4."""
import math
from section_9_04 import (
    finite, taylor_change, single_cash_flow, cash_flow_portfolio,
    single_shock, portfolio_shock)

def close(a,b,rel_tol=1e-9,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(taylor_change(12,12,0.1,1),1.2)
    close(taylor_change(12,12,0.1,2),1.26)
    close((2.1)**3-(8+taylor_change(12,12,0.1,2)),0.001)
    for rate in (-0.02,0,0.04,0.1):
        model=single_cash_flow(10000,5,rate)
        v=10000*math.exp(-5*rate)
        close(model["value"],v)
        close(model["first"],-5*v)
        close(model["second"],25*v)
        close(model["duration"],5)
        close(model["convexity"],25)
        for h in (-0.01,-0.001,0.001,0.01):
            report=single_shock(10000,5,rate,h)
            close(report["exact_change"],v*math.expm1(-5*h))
            assert abs(report["quadratic_error"])<abs(report["linear_error"])
    flows=[(100,1),(1100,2)]
    portfolio=cash_flow_portfolio(flows,0.04)
    v1=100*math.exp(-0.04)
    v2=1100*math.exp(-0.08)
    close(portfolio["value"],v1+v2)
    close(portfolio["duration"],(v1+2*v2)/(v1+v2))
    close(portfolio["convexity"],(v1+4*v2)/(v1+v2))
    shock=portfolio_shock(flows,0.04,0.005)
    close(shock["exact_change"],
          v1*math.expm1(-0.005)+v2*math.expm1(-0.01))
    assert abs(shock["quadratic_error"])<abs(shock["linear_error"])
    rejects(ValueError,taylor_change,1,2,0.1,3)
    rejects(ValueError,single_cash_flow,0,5,0.04)
    rejects(ValueError,single_cash_flow,100,-1,0.04)
    rejects(ValueError,cash_flow_portfolio,[],0.04)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 9.4 reference checks")

if __name__=="__main__":
    run()
