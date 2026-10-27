"""Independent analytic reference checks for Book 02 Section 16.7."""
import math
from section_16_07 import (assessment,finite,raw_quadratic,scaled_quadratic,
                           to_scaled,to_raw,double_well,double_well_gradient,
                           local_descent,multistart)

def close(a,b,rel=1e-8,abs_=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    close(a["raw_loss"],1)
    close(a["scaled_loss"],1)
    close(a["scaled_parameters"][0],1)
    close(a["scaled_parameters"][1],1)
    close(a["round_trip"][0],0.021)
    close(a["round_trip"][1],4)
    close(raw_quadratic(0.02,3),0)
    close(scaled_quadratic(0,0),0)
    close(double_well(1),0.2)
    close(double_well(-1),-0.2)
    close(double_well_gradient(0),0.2)
    close(double_well_gradient(1),0.2)
    close(double_well_gradient(-1),0.2)
    runs=a["multistart"]["runs"]
    assert len(runs)==4
    assert all(run["status"]=="gradient_tolerance" for run in runs)
    assert any(run["x"]<0 for run in runs)
    assert any(run["x"]>0 for run in runs)
    assert a["multistart"]["best_observed"]["x"]<0
    assert a["multistart"]["global_optimality_certified"] is False
    close(a["multistart"]["best_observed"]["gradient"],0,abs_=1e-9)
    rejects(TypeError,finite,True,"input")
    rejects(ValueError,raw_quadratic,float("nan"),1)
    rejects(ValueError,local_descent,0,step=0)
    rejects(ValueError,multistart,())
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.7 independent reference checks")

if __name__=="__main__":
    run()
