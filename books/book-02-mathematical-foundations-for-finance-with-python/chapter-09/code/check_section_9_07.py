"""Independent reference checks for Section 9.7."""
import math
from section_9_07 import (
    finite,call_payoff,put_payoff,call_slopes,put_slopes,
    capped_floored_payment,cap_floor_slopes,difference_report,call_scenario)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    for s,call,put in ((98,0,2),(100,0,0),(102,2,0)):
        close(call_payoff(s,100),call)
        close(put_payoff(s,100),put)
        close(call-put,s-100)
    assert call_slopes(100,100)=={"left":0.0,"right":1.0,"differentiable":False}
    assert put_slopes(100,100)=={"left":-1.0,"right":0.0,"differentiable":False}
    assert call_slopes(99,100)["differentiable"]
    assert call_slopes(101,100)["differentiable"]
    d=difference_report(lambda x:call_payoff(x,100),100,2)
    close(d["left_difference"],0)
    close(d["right_difference"],1)
    close(d["centered_difference"],0.5)
    for r,expected in ((0.01,20),(0.03,30),(0.06,50)):
        close(capped_floored_payment(r,1000,0.02,0.05),expected)
    assert cap_floor_slopes(0.02,1000,0.02,0.05)=={
        "left":0.0,"right":1000.0,"differentiable":False}
    assert cap_floor_slopes(0.05,1000,0.02,0.05)=={
        "left":1000.0,"right":0.0,"differentiable":False}
    factor=math.exp(-0.08)
    up=call_scenario(100,100,2,0.04,2)
    down=call_scenario(100,100,-2,0.04,2)
    close(up["exact_change"],2*factor)
    close(down["exact_change"],0)
    close(up["left_slope"],0)
    close(up["right_slope"],factor)
    assert not up["differentiable"]
    rejects(ValueError,call_payoff,-1,100)
    rejects(ValueError,put_payoff,100,0)
    rejects(ValueError,cap_floor_slopes,0.03,1000,0.05,0.02)
    rejects(ValueError,difference_report,lambda x:x,1,0)
    rejects(ValueError,call_scenario,100,100,-101)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 9.7 reference checks")

if __name__=="__main__":
    run()
