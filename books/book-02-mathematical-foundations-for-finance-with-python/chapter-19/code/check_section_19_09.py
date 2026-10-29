"""Independent analytic reference checks for Book 02 Section 19.9."""
import math
import json
from section_19_09 import (assessment,finite,transition,depletion_time,simulate)

def near(a,b,rel=1e-10,abs_=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_report_contract():
    before=math.nextafter(2.0,0.0)
    after=math.nextafter(2.0,math.inf)
    cases=(
        (100,0,10,3,[],"completed"),
        (0,0,0,2,[(1,100)],"depleted"),
        (100,0,-50,5,[(3,1000)],"depleted"),
        (100,0,0,3,[(1,-150),(2,200)],"depleted"),
        (0,0,0,2,[(0,-1),(1,100)],"depleted"),
        (0,0,0,2,[(0,100)],"completed"),
        (100,0,-50,3,[(2,100)],"depleted"),
        (100,0,-50,3,[(before,100)],"completed"),
        (100,0,-50,3,[(after,100)],"depleted"),
        (100,0,0,0,[(0,10)],"completed"),
    )
    for initial,rate,flow,horizon,jumps,status in cases:
        caller_jumps=[list(event) for event in jumps]
        saved=[event.copy() for event in caller_jumps]
        report=simulate(initial,rate,flow,horizon,caller_jumps)
        expected={"initial":float(initial),"rate":float(rate),
                  "flow":float(flow),"horizon":float(horizon),
                  "jumps":tuple(tuple(float(v) for v in event) for event in jumps)}
        assert report["inputs"]==expected
        assert report["status"]==status
        assert report["scheduled_jumps"]==len(jumps)
        assert report["model"]=="constant_rate_continuous_account"
        assert report["event_policy"]=={
            "initial_jump":"before_initial_depletion",
            "coincident_future_jump":"depletion_first"}
        assert caller_jumps==saved
        encoded=json.dumps(report,sort_keys=True,allow_nan=False)
        assert encoded==json.dumps(simulate(initial,rate,flow,horizon,jumps),
                                   sort_keys=True,allow_nan=False)
        assert json.loads(encoded)["inputs"]==json.loads(json.dumps(expected))
        caller_jumps.append([horizon,999])
        if saved:
            caller_jumps[0][1]=999
        assert report["inputs"]==expected

    negative=simulate(100,0,0,3,[(1,-150),(2,200)])
    assert negative["events"]==[
        {"type":"jump","time":1.0,"amount":-150.0,"balance":-50.0},
        {"type":"depletion","time":1.0}]
    assert negative["applied_jumps"]==1
    assert negative["final_time"]==negative["depletion_time"]==1
    assert negative["final_balance"]==0

    rescue=simulate(0,0,0,2,[(0,100)])
    assert rescue["events"]==[
        {"type":"jump","time":0.0,"amount":100.0,"balance":100.0}]
    near(rescue["final_balance"],100)
    for event_time,applied in ((before,1),(2.0,0),(after,0)):
        result=simulate(100,0,-50,3,[(event_time,100)])
        assert result["applied_jumps"]==applied
        if applied:
            assert result["events"]==[
                {"type":"jump","time":event_time,"amount":100.0,"balance":100.0+100-50*event_time}]
            near(result["final_balance"],50)
        else:
            assert result["events"]==[{"type":"depletion","time":2.0}]
            assert result["depletion_time"]==result["final_time"]==2
            assert result["final_balance"]==0

def run():
    check_report_contract()
    near(transition(0,5e-324,100,0.5),50)
    near(depletion_time(0.5,5e-324,-1),0.5)
    a=assessment()
    growth=a["growth"]
    assert growth["status"]=="completed"
    near(growth["final_balance"],1000*math.exp(0.2))
    contribution=a["contributions"]
    near(contribution["final_balance"],1000*math.exp(0.2)+200*math.expm1(0.2)/0.04)
    depleted=a["depletion"]
    assert depleted["status"]=="depleted"
    near(depleted["depletion_time"],-math.log(0.6)/0.04)
    near(depleted["final_balance"],0)
    jump=a["scheduled_deposit"]
    near(jump["final_balance"],1000*math.exp(0.25)+200*math.exp(0.15))
    assert jump["applied_jumps"]==1
    late=a["late_deposit"]
    assert late["status"]=="depleted"
    near(late["depletion_time"],2)
    assert late["applied_jumps"]==0
    near(transition(1000,0,200,5),2000)
    near(depletion_time(1000,0,-100),10)
    assert depletion_time(1000,0.04,-40) is None
    assert depletion_time(1000,0.04,-30) is None
    assert depletion_time(1000,0.04,0) is None
    near(simulate(0,0,0,2,[(0,100)])["final_balance"],100)
    assert simulate(0,0,0,2)["status"]=="depleted"
    assert simulate(100,0,-50,2,[(2,1000)])["applied_jumps"]==0
    assert simulate(100,0,-50,2,[(1,100)])["status"]=="completed"
    assert simulate(100,0,-50,2,[(1,100)])["applied_jumps"]==1
    assert simulate(100,0,0,1,[(1,10)])["applied_jumps"]==1
    rejects(ValueError,simulate,-1,0,0,1)
    rejects(ValueError,simulate,100,0,0,-1)
    rejects(ValueError,simulate,100,0,0,5,[(2,10),(1,20)])
    rejects(ValueError,simulate,100,0,0,5,[(2,10),(2,20)])
    rejects(ValueError,simulate,100,0,0,5,[(6,10)])
    rejects(ValueError,transition,100,0,0,-1)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.9 independent analytic reference checks")

if __name__=="__main__":
    run()
