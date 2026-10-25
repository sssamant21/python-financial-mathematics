"""Independent checks for Section 9.5 Taylor remainder bounds."""
import math
from section_9_05 import finite, polynomial_example, single_report, portfolio_report

def close(a,b,rel_tol=1e-9,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def bound_holds(report):
    # Mathematical bound with a small allowance for floating-point arithmetic.
    for name in ("linear","quadratic"):
        error=abs(report[name+"_error"])
        bound=report[name+"_bound"]
        assert error<=bound+1e-9*max(1,abs(report["baseline_value"])),(name,error,bound)

def run():
    for h in (-0.2,-0.1,0,0.1,0.2):
        p=polynomial_example(h)
        close(p["exact"]-p["quadratic"],h**3)
        close(abs(p["quadratic_remainder"]),p["quadratic_bound"])
    for rate in (-0.02,0,0.04,0.12):
        for h in (-0.02,-0.005,-0.001,0,0.001,0.005,0.02):
            x=single_report(10000,5,rate,h)
            v=10000*math.exp(-5*rate)
            close(x["baseline_value"],v)
            close(x["first_derivative"],-5*v)
            close(x["second_derivative"],25*v)
            close(x["exact_change"],v*math.expm1(-5*h))
            worst=10000*math.exp(-5*min(rate,rate+h))
            close(x["linear_bound"],12.5*worst*h*h)
            close(x["quadratic_bound"],125*worst*abs(h)**3/6)
            bound_holds(x)
    flows=[(100,1),(1100,2),(500,4)]
    for h in (-0.01,-0.001,0,0.001,0.01):
        bound_holds(portfolio_report(flows,0.04,h))
    zero=single_report(10000,5,0.04,0)
    assert zero["linear_bound_utilization"] is None
    assert zero["quadratic_bound_utilization"] is None
    rejects(ValueError,portfolio_report,[],0.04,0.001)
    rejects(ValueError,single_report,0,5,0.04,0.001)
    rejects(ValueError,single_report,100,-1,0.04,0.001)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 9.5 reference checks")

if __name__=="__main__":
    run()
