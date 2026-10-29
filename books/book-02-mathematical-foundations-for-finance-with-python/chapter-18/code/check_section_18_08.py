"""Independent analytic reference checks for Book 02 Section 18.8."""
import math
from section_18_08 import assessment,audited_bisection,finite,zero_coupon_residual

def near(a,b,tol=1e-9):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def verify_audit(function,lower,upper,*controls):
    calls=[]
    def observed(x):
        calls.append(x)
        return function(x)
    report=audited_bisection(observed,lower,upper,*controls)
    assert report["evaluations"]==len(calls)
    assert report["evaluations"]==2+len(report["trace"])+(report["status"]=="stagnation")
    lo,hi=report["bracket"]
    assert lower<=lo<=hi<=upper
    assert report["width"]==hi-lo
    expected=(function(lo),function(hi))
    assert tuple(report["bracket_endpoint_residuals"])==expected
    assert report["residual"]==function(report["root"])
    if lo==hi:
        assert expected==(0,0)
    else:
        assert (expected[0]<0<expected[1]) or (expected[1]<0<expected[0])
    previous=None
    for row in report["trace"]:
        a,b=row["lower"],row["upper"]
        fa,fb=function(a),function(b)
        assert row["lower_residual"]==fa and row["upper_residual"]==fb
        assert (fa<0<fb) or (fb<0<fa)
        assert a<row["midpoint"]<b
        assert row["width"]==b-a
        assert row["residual"]==function(row["midpoint"])
        if previous is not None:
            pa,pb=previous["lower"],previous["upper"]
            mid,fmid=previous["midpoint"],previous["residual"]
            assert pa<=a<b<=pb
            if (function(pa)<0<fmid) or (fmid<0<function(pa)):
                assert (a,b)==(pa,mid)
            else:
                assert (a,b)==(mid,pb)
        previous=row
    assert report["bracket_invariant"] is True
    return report

def check_audit_paths():
    verify_audit(zero_coupon_residual,0,0.2)
    assert verify_audit(lambda x:x-1,1,2)["status"]=="endpoint_root"
    assert verify_audit(lambda x:x-2,1,2)["status"]=="endpoint_root"
    assert verify_audit(lambda x:x-0.5,0,1)["status"]=="exact_root"
    assert verify_audit(lambda x:x*x-2,1,2,1e-6,0,100)["status"]=="converged"
    assert verify_audit(lambda x:2-x*x,1,2,1e-16,0,1)["status"]=="max_iter"
    left=1.0
    right=math.nextafter(left,2)
    assert verify_audit(lambda x:-1 if x==left else 1,left,right,1e-20,0,5)["status"]=="stagnation"

def run():
    check_audit_paths()
    a=assessment()
    d=a["result"]
    exact=math.sqrt(10/9)-1
    assert d["status"] in ("converged","exact_root")
    near(d["root"],exact)
    assert d["bracket"][0]-1e-12<=exact<=d["bracket"][1]+1e-12
    assert d["width"]<=d["atol"]+d["rtol"]*max(abs(x) for x in d["bracket"])
    assert d["evaluations"]>=d["iterations"]+2
    assert d["bracket_invariant"] is True
    near(zero_coupon_residual(0),100)
    near(zero_coupon_residual(0.2),1000/1.44-900)
    for prev,curr in zip(d["trace"],d["trace"][1:]):
        assert curr["width"]<=prev["width"]
    endpoint=audited_bisection(lambda x:x-1,1,2)
    assert endpoint["status"]=="endpoint_root"
    exhausted=audited_bisection(lambda x:x*x-2,1,2,1e-16,0,1)
    assert exhausted["status"]=="max_iter"
    assert exhausted["bracket_invariant"]
    # Adjacent floating-point numbers cannot be bisected.
    x=1.0
    y=math.nextafter(x,2.0)
    stagnant=audited_bisection(lambda z:-1 if z==x else 1,x,y,1e-20,0,5)
    assert stagnant["status"]=="stagnation"
    rejects(ValueError,audited_bisection,lambda x:x*x+1,-1,1)
    rejects(ValueError,audited_bisection,lambda x:float("nan"),-1,1)
    rejects(ValueError,audited_bisection,lambda x:x,2,1)
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.8 independent analytic reference checks")

if __name__=="__main__":
    run()
