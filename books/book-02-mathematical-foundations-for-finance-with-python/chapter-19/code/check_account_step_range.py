"""Closed finite-geometric method references for Section 19.8 account steps."""
from fractions import Fraction as F
import json
import math
import sys
import section_19_08 as lab


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    cases=[(0,0,big,tiny,2),(0,0,big,1e-308,1),
           (big,-1e308,0,1e-308,1),(big,big,0,0,1),
           (1,big,-big,1,4),(big,0,-big,2,2),
           (tiny,0,tiny,tiny,2),(0,0,tiny,tiny,2),
           (1,0,-1,1,1),(1000,.04,200,5,4),
           (big,1,0,1,1),(-big,-1e308,0,1e-308,1)]
    rows=[]
    for fn,degree in ((lab.euler_account,1),(lab.rk4_account,4)):
        for a,r,u,t,n in cases:
            h=F(t)/n;z=F(r)*h
            # Homogeneous method amplification plus finite accumulated forcing.
            R=1+z if degree==1 else 1+z+z*z/2+z**3/6+z**4/24
            flow_factor=h if degree==1 else h*(1+z/2+z*z/6+z**3/24)
            exact=F(a)*R**n+F(u)*flow_factor*sum((R**k for k in range(n)),F(0))
            try:
                expected=float(exact)
                if not math.isfinite(expected) or (exact and not expected):
                    expected='ValueError'
            except OverflowError:
                expected='ValueError'
            rows.append(observe(fn,(a,r,u,t,n),expected,n))
        for args,error in [((1,0,0,0,0),'ValueError'),
                           ((1,0,0,-1,1),'ValueError'),
                           ((True,0,0,0,1),'TypeError')]:
            rows.append(observe(fn,args,error,1))
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


def observe(fn,args,expected,n):
    try:
        actual=fn(*args)
    except (TypeError,ValueError,OverflowError) as exc:
        actual=type(exc).__name__
    ok=(isinstance(actual,float) and math.isfinite(actual)
        and abs(actual-expected)<=4*n*math.ulp(expected)
        and (actual==0)==(expected==0)
        if isinstance(expected,float) else actual==expected)
    return dict(helper=fn.__name__,inputs=repr(args),expected=repr(expected),
                actual=repr(actual),passed=ok)


if __name__=='__main__':
    check()
