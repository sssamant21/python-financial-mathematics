"""Independent reference checks for Section 10.1."""
import math
from section_10_01 import finite,boundaries,riemann_sum,uniform_sums,convergence_report

def close(a,b,rel_tol=1e-11,abs_tol=1e-11):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    for n in (1,2,4,8,16,64):
        row=uniform_sums(lambda t:100+20*t,0,2,n)
        close(row["midpoint"],240)
        close(row["left"],240-40/n)
        close(row["right"],240+40/n)
        assert row["left"]<=240<=row["right"]
    for n in (1,2,4,8,16,64):
        row=uniform_sums(lambda t:t*t,0,1,n)
        close(row["left"],(n-1)*n*(2*n-1)/(6*n**3))
        close(row["right"],n*(n+1)*(2*n+1)/(6*n**3))
        close(row["midpoint"],1/3-1/(12*n*n))
        assert row["left"]<=row["midpoint"]<=row["right"]
    close(riemann_sum(lambda t:800,[0,0.25],"left"),200)
    close(riemann_sum(lambda t:100+20*t,[0,0.2,0.7,2],"midpoint"),240)
    report=convergence_report(lambda t:t*t,0,1,[2,4,8,16],1/3)
    errors=[row["midpoint_absolute_error"] for row in report["rows"]]
    assert all(x>y for x,y in zip(errors,errors[1:]))
    rejects(ValueError,boundaries,1,1,4)
    rejects(ValueError,boundaries,0,1,0)
    rejects(ValueError,riemann_sum,lambda t:t,[0,0.5,0.4])
    rejects(ValueError,riemann_sum,lambda t:t,[0,1],"unknown")
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 10.1 independent reference checks")

if __name__=="__main__":
    run()
