"""Check benchmark solutions against exact pivoted elimination."""
from fractions import Fraction as F
import json
import math
import sys
import section_20_02 as lab


def reference(args):
    a,b,c,d,u,v=map(F,args)
    if abs(a)<abs(c):
        a,b,c,d,u,v=c,d,a,b,v,u
    if not a:
        return 'ValueError'
    multiplier=c/a
    pivot=d-multiplier*b
    if not pivot:
        return 'ValueError'
    y=(v-multiplier*u)/pivot
    x=(u-b*y)/a
    assert all(F(p)*x+F(q)*y==F(r) for p,q,r in
               [(args[0],args[1],args[4]),(args[2],args[3],args[5])])
    try:
        result=(float(x),float(y))
    except OverflowError:
        return 'ValueError'
    if any(not math.isfinite(f) or (q and not f) for q,f in zip((x,y),result)):
        return 'ValueError'
    return result


def observe(args,expected):
    try:actual=lab.solve_two_by_two(*args)
    except (TypeError,ValueError,OverflowError) as exc:actual=type(exc).__name__
    passed=type(actual) is type(expected) and actual==expected
    return dict(inputs=repr(args),expected=expected,actual=actual,passed=passed)


def check():
    m,s=sys.float_info.max,math.ulp(0.)
    p=math.nextafter(1.,2.)
    q=math.nextafter(p,2.)
    fixtures=[(m,m,1,p,m,p),(m,0,0,m,m,m),(s,0,0,s,s,s),
              (1,p,p,q,p,q),(0,s,m,0,s,m),(m,0,0,s,m,s),
              (1,0,0,1,s,-s),(m,0,0,1,s,0),(s,0,0,1,1,0),
              (m,0,0,m,0,0),(m,m,m,m,m,m),(0,1,0,2,1,2),
              (2,1,1,3,5,7),(0,-2,3,1,4,1),(1,3,2,4,7,11),
              (-m,m,m,m,m,-m)]
    rows=[observe(a,reference(a)) for a in fixtures]
    rows.append(observe((True,0,0,1,1,1),'TypeError'))
    rows.append(observe((1,0,0,1,float('inf'),1),'ValueError'))
    report=lab.assessment()
    expected=reference((2,1,1,3,5,7))
    actual=report['linear_system_solution']
    rows.append(dict(inputs='assessment.linear_system_solution',expected=expected,
                     actual=actual,passed=type(actual) is tuple and actual==expected))
    assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    calls=[]
    old=lab.solve_two_by_two
    def observed(*args):
        calls.append(args);return 7.,11.
    lab.solve_two_by_two=observed
    try:report=lab.assessment()
    finally:lab.solve_two_by_two=old
    assert calls==[(2,1,1,3,5,7)] and report['linear_system_solution']==(7.,11.)
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
