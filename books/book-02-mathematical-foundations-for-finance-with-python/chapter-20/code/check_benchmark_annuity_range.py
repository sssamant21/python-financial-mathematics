"""Annuity benchmarks checked with an independent backward cash-flow recurrence."""
from fractions import Fraction as F
import json
import math
import sys
import section_20_02 as lab


def reference(c,i,n):
    # Discount one period from the final zero liability, adding one payment
    # at each backward step. This is not the implementation's term sum/formula.
    value=F(0)
    gross=1+F(i)
    for _ in range(n):
        value=(value+F(c))/gross
    try:
        expected=float(value)
    except OverflowError:
        return 'ValueError'
    return 'ValueError' if not math.isfinite(expected) or (value and not expected) else expected


def observe(fn,args,expected):
    try:
        actual=fn(*args)
    except (TypeError,ValueError,OverflowError,ZeroDivisionError) as exc:
        actual=type(exc).__name__
    passed=(isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=2*math.ulp(expected)
            and (actual==0)==(expected==0)
            if isinstance(expected,float) else actual==expected)
    return dict(helper=fn.__name__,inputs=repr(args),expected=repr(expected),actual=repr(actual),passed=passed)


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    cases=[(tiny,.01,3),(tiny,1e-20,10),(big,big,1),
           (tiny,math.nextafter(-1.,0.),24),(tiny,-.5,1075),
           (big,1,2),(big,-.5,1),(big,.5,3),(big,big,2),
           (1,tiny,3),(big,1e-308,2),(big,0,0),(big,0,1),
           (tiny,0,3),(0,math.nextafter(-1.,0.),32),(0,big,1),
           (1,big,1),(tiny,big,1),(1,2**-54,128),
           (-big,big,1),(-tiny,-.5,1075),(1,-2**-54,128),
           (100,.005,24),(100,-.01,60)]
    rows=[]
    for fn in (lab.annuity_explicit,lab.annuity_closed):
        for args in cases:
            rows.append(observe(fn,args,reference(*args)))
        for args,error in [((1,-1,0),'ValueError'),((1,.1,-1),'ValueError'),
                           ((1,.1,True),'ValueError'),((True,.1,1),'TypeError'),
                           ((1,float('nan'),0),'ValueError')]:
            rows.append(observe(fn,args,error))
    # Closed-form identities must not require converting a huge count to float.
    rows.append(observe(lab.annuity_closed,(0,.01,10**1000),0.))
    rows.append(observe(lab.annuity_closed,(1,0,10**1000),'ValueError'))
    report=lab.assessment()
    expected=reference(100,.005,24)
    for key in ('annuity_explicit','annuity_closed'):
        actual=report[key]
        rows.append(dict(helper='assessment.'+key,expected=expected,actual=actual,
                         passed=abs(actual-expected)<=2*math.ulp(expected)))
    assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
