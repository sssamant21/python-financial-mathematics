"""Standalone Section 19.7 depletion and assessment reference checks."""
from decimal import Decimal as D, localcontext
import json
import math
import sys

from section_19_07 import assessment, depletion_time


def outcome(*args):
    try:
        got=depletion_time(*args)
        return "infinity" if got is not None and math.isinf(got) else got
    except (ValueError, TypeError, OverflowError) as exc:
        return type(exc).__name__


def reference(a,r,w):
    with localcontext() as ctx:
        ctx.prec=1800
        a,r,w=map(D,(a,r,w))
        if a==0:
            return 0.
        if w==0 or r*a>=w:
            return None
        # Solve exp(r*t)=w/(w-r*a) directly.
        elapsed=(w/(w-r*a)).ln()/r if r else a/w
        result=float(elapsed)
        return result if math.isfinite(result) and result>0 else "ValueError"


def main():
    rows=[]
    def check(case,expected,actual):
        ok=(isinstance(actual,float) and abs(actual-expected)<=math.ulp(expected)
            if isinstance(expected,float) and expected>0 else actual==expected)
        if isinstance(expected,float) and expected>0 and isinstance(actual,float):
            ok=ok and actual>0
        rows.append(dict(case=case,expected=expected,actual=actual,passed=ok))

    m,d=sys.float_info.max,math.ulp(0.)
    q=2.**-52
    for name,args in [
        ("below_equilibrium_rounded_product",(1+q,1-q,1.)),
        ("equal_equilibrium",(2.,.5,1.)),
        ("above_equilibrium",(math.nextafter(2.,math.inf),.5,1.)),
        ("just_below_equilibrium",(math.nextafter(2.,0.),.5,1.)),
        ("zero_rate_overflow",(m,0.,d)),
        ("zero_rate_underflow",(d,0.,m)),
        ("zero_rate_subnormal",(3*d,0.,2.)),
        ("large_negative_product",(m,-m,d)),
        ("near_zero_positive_rate",(1.,d,2.)),
        ("near_zero_negative_rate",(1.,-d,2.)),
        ("subnormal_ratio_and_time",(d,d,m)),
        ("zero_initial_no_withdrawal",(0.,0.,0.)),
        ("zero_withdrawal",(5.,-.5,0.)),
        ("ordinary_negative_rate",(7.,-.125,2.)),
    ]:
        check(name,reference(*args),outcome(*args))

    check("invalid_initial","ValueError",outcome(-1.,0.,1.))
    check("invalid_withdrawal","ValueError",outcome(1.,0.,-1.))
    check("nonfinite","ValueError",outcome(1.,math.inf,1.))
    check("boolean","TypeError",outcome(1.,False,1.))
    report=assessment()
    for name,args in [
        ("depletion_positive_rate",(1000,.04,100)),
        ("depletion_zero_rate",(1000,0,100)),
        ("depletion_negative_rate",(1000,-.02,50)),
        ("no_depletion",(1000,.04,40)),
    ]:
        check("assessment_"+name,reference(*args),report[name])
    check("assessment_terminal_time",reference(1000,.04,100),
          report["terminal_depletion"]["event_time"])
    check("assessment_flags",[False,False],
          [report["runtime_certified"],report["independent_review_completed"]])
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
