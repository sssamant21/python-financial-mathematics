"""Independent represented-gross references for Section 20.4."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_20_04 as lab


def rounded(value):
    try:
        result=float(value)
    except OverflowError:
        return 'OverflowError'
    return result if math.isfinite(result) else 'OverflowError'


def pv_reference(a,r,n):
    gross=F(1)+F(r)
    return rounded(F(a)/gross**n)


def annuity_reference(c,r,n):
    # Work backward one payment at a time, not from the closed form.
    gross=F(1)+F(r)
    total=F(0)
    for _ in range(n):
        total=(total+F(c))/gross
    return rounded(total)


def observe(fn,args,expected):
    try:
        actual=fn(*args)
    except (ValueError,TypeError,OverflowError) as exc:
        actual=type(exc).__name__
    passed=type(actual) is type(expected) and actual==expected
    if passed and isinstance(expected,float) and expected==0:
        passed=math.copysign(1.,actual)==math.copysign(1.,expected)
    return dict(helper=fn.__name__,inputs=repr(args),expected=expected,actual=actual,passed=passed)


def check():
    m,s=sys.float_info.max,math.ulp(0.)
    near=math.nextafter(-1.,0.)
    huge=10**1000
    rows=[]
    for args in [(s,near,21),(-s,near,21),(m,1,1075),(m,1,2098),
                 (m,1,2099),(-m,1,2099),(s,1,1),(s,near,1),
                 (m,near,2),(100,.25,3),(100,-.1,3),
                 (m,s,128),(1,.1,128),(1,.1,129),(1,near,129)]:
        rows.append(observe(lab.present_value,args,pv_reference(*args)))
    for args in [(s,-.5,1075),(-s,-.5,1075),(s,near,21),(m,.5,129),
                 (s,m,1),(-s,m,1),(m,-.5,2),(.1,s,3),
                 (100,.25,12),(100,-.1,12),(100,0,5),(s,0,1),
                 (m,1,128),(m,1,129),(s,.1,129)]:
        rows.append(observe(lab.annuity_pv,args,annuity_reference(*args)))
    # For n=1/s, 1-s/2 <= n*ln(1+s) <= 1. The correction is
    # too small to change either of these rounded exponential limits.
    with localcontext() as ctx:
        ctx.prec=500
        inv_e=(-Decimal(1)).exp()
        inv_e_upper=inv_e*(1+Decimal(s))
        assert inv_e_upper>inv_e
        assert float(inv_e)==float(inv_e_upper)
        assert float(1-inv_e)==float(1-inv_e_upper)
        rows.append(observe(lab.present_value,(1,s,2**1074),float(inv_e)))
        rows.append(observe(lab.annuity_pv,(s,s,2**1074),float(1-inv_e)))
    for fn,args,expected in [
        (lab.present_value,(0,near,huge),0.),
        (lab.present_value,(-0.,near,huge),-0.),
        (lab.present_value,(7,0,huge),7.),
        (lab.present_value,(-m,near,0),-m),
        (lab.present_value,(-m,1,huge),-0.),
        (lab.present_value,(s,near,huge),'OverflowError'),
        (lab.annuity_pv,(0,near,huge),0.),
        (lab.annuity_pv,(m,0,0),0.),
        (lab.annuity_pv,(0,0,huge),0.),
        (lab.annuity_pv,(s,0,huge),'OverflowError'),
        (lab.annuity_pv,(s,near,huge),'OverflowError'),
        (lab.annuity_pv,(4,2,huge),2.),
        # 3*s/2 is the exact midpoint between s and 2*s. A finite
        # positive-rate sum approaches it strictly from below.
        (lab.annuity_pv,(3*s,2,huge),s),
        (lab.annuity_pv,(-3*s,2,huge),-s),
        (lab.annuity_pv,(s,2,huge),0.),
        (lab.annuity_pv,(m,.5,huge),'OverflowError'),
    ]:
        rows.append(observe(fn,args,expected))
    for fn in (lab.present_value,lab.annuity_pv):
        for args,expected in [((0,-1,0),'ValueError'),((0,0,-1),'ValueError'),
                              ((0,0,True),'TypeError'),((0,0,1.),'TypeError'),
                              ((True,0,0),'TypeError'),((0,float('inf'),0),'ValueError')]:
            rows.append(observe(fn,args,expected))
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
