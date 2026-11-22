"""Independent mathematical reference checks for Section 10.6."""
import math
from section_10_06 import (
    finite,finite_horizon_pv,perpetuity_pv,tail_value,
    horizon_for_tail_fraction,p_integral_from_one,assessment)

def close(a,b,rel_tol=1e-10,abs_tol=1e-9):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(perpetuity_pv(1200,0,0.06),20000)
    close(perpetuity_pv(1000,0.02,0.05),1000/0.03)
    close(perpetuity_pv(0,0.05,0.05),0)
    for growth in (0,0.02,0.04,0.049):
        for T in (0,1,10,100):
            finite_value=finite_horizon_pv(1000,growth,0.05,T)
            remainder=tail_value(1000,growth,0.05,T)
            close(finite_value+remainder,perpetuity_pv(1000,growth,0.05))
            assert remainder>=0
    close(finite_horizon_pv(1000,0.05,0.05,10),10000)
    close(finite_horizon_pv(0,0.1,0.01,10),0)
    close(horizon_for_tail_fraction(0.02,0.05,0.01),math.log(100)/0.03)
    close(p_integral_from_one(2),1)
    close(p_integral_from_one(3),0.5)
    rejects(ValueError,perpetuity_pv,1000,0.05,0.05)
    rejects(ValueError,perpetuity_pv,1000,0.06,0.05)
    rejects(ValueError,tail_value,1000,0.06,0.05,10)
    rejects(ValueError,horizon_for_tail_fraction,0.02,0.05,1)
    rejects(ValueError,p_integral_from_one,1)
    rejects(ValueError,finite_horizon_pv,1000,0,0.05,-1)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    assert perpetuity_pv(0,1e308,-1e308)==0
    assert perpetuity_pv(0,-1e308,1e308)==0
    assert perpetuity_pv(1,-1e308,1e308)==5e-309
    assert perpetuity_pv(1e308,-1e308,1e308)==0.5
    assert perpetuity_pv(-1e308,-1e308,1e308)==-0.5
    assert perpetuity_pv(1,-1e-16,1)==0.9999999999999999
    assert perpetuity_pv(1e308,-1e-16,1)==9.999999999999998e307
    assert finite_horizon_pv(0,1e308,-1e308,1)==0
    assert finite_horizon_pv(1,1e308,-1e308,0)==0
    close(finite_horizon_pv(1e-300,1,0,1000),1.970071114017047e134,rel_tol=1e-14,abs_tol=0)
    assert finite_horizon_pv(math.ulp(0.),1,0,745)>0
    assert finite_horizon_pv(1e308,-1e308,1e308,1)==0.5
    assert finite_horizon_pv(1e308,0,1e308,1e308)==1
    assert finite_horizon_pv(1,0,1e-300,1e-300)==1e-300
    rejects(ValueError,finite_horizon_pv,1,1,0,1000)
    assert tail_value(0,1e308,-1e308,1)==0
    assert tail_value(0,-1e308,1e308,1)==0
    assert tail_value(1e308,-1e308,1e308,0)==0.5
    assert tail_value(1e308,-1e308,1e308,1)==0
    close(tail_value(1e308,0,.5,2),7.357588823428846e+307,rel_tol=1e-14,abs_tol=0)
    close(tail_value(-1e308,0,.5,2),-7.357588823428846e+307,rel_tol=1e-14,abs_tol=0)
    close(tail_value(1e308,0,1,1000),5.075958897549457e-127,rel_tol=1e-14,abs_tol=0)
    close(tail_value(1,-1e-16,1,700),9.85967654375908e-305,rel_tol=1e-14,abs_tol=0)
    report=assessment()
    assert len(report["scenarios"])==5
    assert not report["scenarios"][-1]["converges"]
    assert report["runtime_certified"] is False
    print("PASS: Section 10.6 independent reference checks")

if __name__=="__main__":
    run()
