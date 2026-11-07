"""Independent discounted-term and callback checks for Section 8.3."""
from decimal import Context, Decimal as D, localcontext
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
if len(sys.argv)==2:
    sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import section_8_03 as lab


def expected(kind,t,r,p,d):
    coefficient=Q(p) if kind=="value" else Q(d)-Q(r)*Q(p)
    if not coefficient:
        return p if kind=="value" else 0.
    with localcontext(Context(prec=1500)):
        factor=(-D(r)*D(t)).exp()
        # Separate derivative terms provide a reference distinct from the
        # production's factored product-rule coefficient.
        answer=D(p)*factor if kind=="value" else D(d)*factor-D(r)*D(p)*factor
        result=float(answer)
    return result if math.isfinite(result) else "ValueError"


def check():
    rows=[]
    def exercise(name,kind,t,r,p,d,expect=None,bad=None):
        calls=[]
        def payment(at):
            calls.append(["payment",at])
            return bad[1] if bad and bad[0]=="payment" else p
        def derivative(at):
            calls.append(["derivative",at])
            if kind=="value": raise AssertionError("unused derivative was evaluated")
            return bad[1] if bad and bad[0]=="derivative" else d
        valid=type(t) in (int,float) and type(r) in (int,float) and math.isfinite(t) and math.isfinite(r) and t>=0
        want_calls=[] if not valid else [["payment",t]] if kind=="value" else [["derivative",t],["payment",t]]
        if bad and valid and bad[0]=="derivative":
            want_calls=want_calls[:1]
        if expect is None: expect=expected(kind,t,r,p,d)
        function=lab.discounted_value if kind=="value" else lab.discounted_value_derivative
        try:
            actual=function(t,r,payment,derivative)
            if not math.isfinite(actual): actual=repr(actual)
        except Exception as exc: actual=type(exc).__name__
        if type(expect) is float:
            passed=type(actual) is float and (
                actual==expect if expect==0 or abs(expect)<sys.float_info.min
                else math.isclose(actual,expect,rel_tol=3e-14,abs_tol=0.))
            if expect==0 and passed:
                passed=math.copysign(1,actual)==math.copysign(1,expect)
        else: passed=actual==expect
        rows.append(dict(case=name,expected=expect,actual=actual,expected_calls=want_calls,
                         actual_calls=calls,passed=passed and calls==want_calls))
    M=sys.float_info.max
    u=math.ulp(0.)
    for name,t,r,p,d in [
        ("finite scaled payment",1000.,1.,M,0.),
        ("finite scaled subnormal",800.,-1.,u,0.),
        ("zero payment at overflowing factor",1000.,-1.,0.,0.),
        ("signed zero payment",1000.,-1.,-0.,0.),
        ("genuine payment overflow",800.,-1.,1.,0.),
        ("negative payment underflow",1000.,1.,-1.,0.),
        ("ordinary payment",3.,.05,106.,2.),
    ]:
        exercise(name,"value",t,r,p,d)
    for name,t,r,p,d in [
        ("finite complete coefficient",0.,M,2.,M),
        ("cancelled coefficient at huge exponent",1000.,M,1.,M),
        ("cancelled coefficient at growing exponent",1000.,-M,1.,-M),
        ("large coefficient recovered by scaling",1e-305,1e308,1e308,0.),
        ("coefficient genuine overflow",1e-308,1e308,1e308,0.),
        ("large signed coefficient",1000.,1.,M,-M),
        ("ordinary derivative",3.,.05,106.,2.),
        ("zero-time exact coefficient",0.,M,-1.,-M),
        ("signed derivative underflow",1000.,1.,1.,0.),
    ]:
        exercise(name,"derivative",t,r,p,d)
    for kind in ("value","derivative"):
        for name,t,r,error in [("negative time",-1.,.1,"ValueError"),
                               ("bool time",True,.1,"TypeError"),
                               ("nonfinite rate",1.,math.nan,"ValueError")]:
            exercise(kind+" "+name,kind,t,r,1.,2.,expect=error)
        for value,error in [(True,"TypeError"),(math.nan,"ValueError")]:
            exercise(kind+" bad payment",kind,1.,.1,1.,2.,expect=error,bad=("payment",value))
    for value,error in [(True,"TypeError"),(math.nan,"ValueError")]:
        exercise("bad derivative","derivative",1.,.1,1.,2.,expect=error,bad=("derivative",value))
    exercise("coarse decay boundary","value",M,M,1.,0.,expect=0.)
    exercise("coarse growth boundary","value",M,-M,1.,0.,expect="ValueError")
    exercise("coarse derivative decay","derivative",M,M,0.,1.,expect=0.)
    actual=lab.discounted_value(0.,0.,lambda t:2.,None)
    rows.append(dict(case="unused derivative may be None",expected=2.,actual=actual,passed=actual==2.))
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
