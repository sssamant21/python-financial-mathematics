"""Finite-geometric amplification references for actual cumulative steppers/reports."""
from fractions import Fraction as F
import json
import math
import sys
import section_19_10 as lab


def reference(args,degree):
    a,r,u,t,n=args
    h=F(t)/n;z=F(r)*h
    R=1+z if degree==1 else 1+z+z*z/2+z**3/6+z**4/24
    forcing=h if degree==1 else h*(1+z/2+z*z/6+z**3/24)
    exact=F(a)*R**n+F(u)*forcing*sum((R**k for k in range(n)),F(0))
    try:
        rounded=float(exact)
    except OverflowError:
        return 'ValueError'
    return 'ValueError' if not math.isfinite(rounded) or (exact and not rounded) else rounded


def close(actual,expected,n):
    return (isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=4*n*math.ulp(expected)
            and (actual==0)==(expected==0))


def check():
    big,tiny=sys.float_info.max,math.ulp(0.)
    cases=[(2,1e308,0,1e-308,1),(0,0,big,tiny,2),
           (0,0,big,1e-308,1),(big,big,0,0,2),(1,big,-big,2,3),
           (tiny,0,tiny,tiny,3),(0,0,tiny,tiny,2),
           (1,0,-1,1,1),(1000,.05,0,2,10)]
    rows=[]
    for fn,degree in ((lab.euler,1),(lab.rk4,4)):
        for args in cases:
            expected=reference(args,degree)
            try:
                actual=fn(*args)
            except (ValueError,OverflowError) as exc:
                actual=type(exc).__name__
            passed=close(actual,expected,args[-1]) if isinstance(expected,float) else actual==expected
            rows.append(dict(helper=fn.__name__,inputs=repr(args),expected=repr(expected),actual=repr(actual),passed=passed))
        for args,error in [((1,0,0,0,0),'ValueError'),((1,0,0,-1,1),'ValueError'),((True,0,0,0,1),'TypeError')]:
            try:
                actual=fn(*args)
            except (ValueError,TypeError) as exc:
                actual=type(exc).__name__
            rows.append(dict(helper=fn.__name__,inputs=repr(args),expected=error,actual=repr(actual),passed=actual==error))
    report=lab.assessment()
    for n in (10,20,40):
        for key,degree in [('euler',1),('rk4',4)]:
            actual=report['convergence'][str(n)][key]
            expected=reference((1000,.05,0,2,n),degree)
            error=report['convergence'][str(n)][key+'_absolute_error']
            rows.append(dict(helper='assessment.'+key,steps=n,expected=expected,actual=actual,
                             passed=close(actual,expected,n) and error==abs(actual-report['exact_growth'])))
    if hasattr(lab,'_euler_account'):
        calls=[];original_e,original_r=lab._euler_account,lab._rk4_account
        def e(*args):
            calls.append(('euler',args))
            return 7.0
        def r(*args):
            calls.append(('rk4',args))
            return 11.0
        lab._euler_account,lab._rk4_account=e,r
        try:
            observed=lab.assessment()
        finally:
            lab._euler_account,lab._rk4_account=original_e,original_r
        assert calls==[(method,(1000.,.05,0.,2.,n)) for n in (10,20,40) for method in ('euler','rk4')]
        for row in observed['convergence'].values():
            assert row['euler']==7.0 and row['rk4']==11.0
            assert row['euler_absolute_error']==abs(7-observed['exact_growth'])
            assert row['rk4_absolute_error']==abs(11-observed['exact_growth'])
    assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
