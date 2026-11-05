"""Section 19.8 actual continuous/discrete helpers versus independent references."""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
import json
import math
import sys
import section_19_08 as lab


def scaled(a,x):
    if not a or not x:
        return float(a)
    if abs(x)>2000:
        return 'ValueError'
    with localcontext() as ctx:
        ctx.prec=1600
        y=float(D(a)*(D(x.numerator)/D(x.denominator)).exp())
        return y if math.isfinite(y) and y else 'ValueError'


def rational(q):
    try:
        value=float(q)
    except OverflowError:
        return 'ValueError'
    return value if math.isfinite(value) and (value or not q) else 'ValueError'


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    rows=[]
    def compare(fn,args,ref):
        try:
            actual=fn(*args)
        except (TypeError,ValueError,OverflowError,ZeroDivisionError) as exc:
            actual=type(exc).__name__
        ok=(isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-ref)<=3*math.ulp(ref) and (actual==0)==(ref==0)
            if isinstance(ref,float) else actual==ref)
        rows.append(dict(helper=fn.__name__,args=repr(args),expected=repr(ref),
                         actual=repr(actual),passed=ok))
    for a,r,t in [(tiny,1000,1),(big,-1000,1),(1,1000,1),(1,-1000,1),
                  (0,big,big),(1,big,0),(-tiny,1000,1),(-big,-1000,1),
                  (1000,.05,2),(tiny,tiny,tiny),(big,0,big)]:
        compare(lab.continuous_growth,(a,r,t),scaled(a,F(r)*F(t)))
    for a,j,m,p in [(big,1,1,1024),(tiny,-.5,1,1075),(1,1,1,1024),
                    (1,-.5,1,1075),(0,1,1,4096),(1,big,1,0),
                    (1000,.06,12,12),(1,tiny,10**1000,12),
                    (1,-tiny,10**1000,12),(-big,1,1,1024),
                    (big,-.5,1,1075),(1,.125,8,17),
                    (1,math.nextafter(-1.,0),1,1),
                    (1,.1,10**1000,10**1000)]:
        if m>10**100 and p==m:
            # ((1+j/m)^m) differs from exp(j) below binary64 accuracy here.
            ref=scaled(a,F(j))
        else:
            ref=rational(F(a)*(1+F(j)/m)**p)
        compare(lab.discrete_growth,(a,j,m,p),ref)
    for fn,args,error in [
        (lab.continuous_growth,(0,float('inf'),0),'ValueError'),
        (lab.continuous_growth,(1,0,-1),'ValueError'),
        (lab.discrete_growth,(0,-1,1,0),'ValueError'),
        (lab.discrete_growth,(0,0,0,0),'ValueError'),
        (lab.discrete_growth,(1,0,True,1),'ValueError'),
        (lab.discrete_growth,(1,0,1,True),'ValueError')]:
        compare(fn,args,error)
    calls=[]
    original=lab._scaled_exponential
    def observed(a,integral):
        calls.append((a,integral))
        return 7.0
    lab._scaled_exponential=observed
    try:
        assert lab.continuous_growth(1,.5,4)==7.
        assert lab.discrete_growth(1,1,1,2)==7.
    finally:
        lab._scaled_exponential=original
    assert len(calls)==2 and calls[0][1]==2
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
