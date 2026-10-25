"""Independent checks for Section 10.7."""
import math
from section_10_07 import integrate,refinement,finance_integrand,assessment,finite

def close(x,y,tol=1e-9):
    assert math.isclose(x,y,rel_tol=tol,abs_tol=tol),(x,y)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    for method in ("midpoint","trapezoid","simpson"):
        close(integrate(lambda t:7,0,3,8,method),21)
        close(integrate(lambda t:2+3*t,0,2,8,method),10)
        close(integrate(lambda t:2+3*t,2,0,8,method),-10)
        close(integrate(lambda t:t,1,1,8,method),0)
    close(integrate(lambda t:t*t,0,1,2,"midpoint"),0.3125)
    close(integrate(lambda t:t*t,0,1,2,"trapezoid"),0.375)
    close(integrate(lambda t:t*t,0,1,2,"simpson"),1/3)
    close(integrate(lambda t:t**3,0,1,2,"simpson"),1/4)
    for method in ("midpoint","trapezoid","simpson"):
        rows=refinement(lambda t:math.exp(t),0,1,method,[8,16,32,64])
        errors=[abs(x["estimate"]-math.expm1(1)) for x in rows]
        assert all(a>b for a,b in zip(errors,errors[1:])),(method,errors)
        assert all(x.get("estimated_fine_error",0)>=0 for x in rows)
    reference=integrate(finance_integrand,0,4,8192,"simpson")
    for method in ("midpoint","trapezoid","simpson"):
        close(integrate(finance_integrand,0,4,1024,method),reference,tol=1e-5)
    rejects(ValueError,integrate,lambda t:t,0,1,3,"simpson")
    rejects(ValueError,integrate,lambda t:t,0,1,0,"midpoint")
    rejects(ValueError,integrate,lambda t:t,0,1,2,"other")
    rejects(TypeError,integrate,lambda t:t,0,1,True,"midpoint")
    rejects(ValueError,finite,float("nan"),"value")
    report=assessment()
    assert len(report["methods"])==3 and report["runtime_certified"] is False
    print("PASS: Section 10.7 independent checks")

if __name__=="__main__":
    run()
