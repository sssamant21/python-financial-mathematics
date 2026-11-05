"""Independent integral, reciprocal-log and separately compounded deposit oracles."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_19_10 as lab


def rounded(x):
    try:
        y=float(x)
    except OverflowError:
        return 'ValueError'
    return 'ValueError' if not math.isfinite(y) or (x and not y) else y


def transition(a,r,u,t):
    if not r or not t:
        return F(a)+F(u)*F(t)
    if F(u)==-F(a)*F(r):
        return F(a)
    factor=(D(r)*D(t)).exp()
    return D(a)*factor+D(u)*(factor-1)/D(r)


def observe(fn,args,expected,ulps=8):
    try:
        actual=fn(*args)
    except (ValueError,TypeError,OverflowError,ZeroDivisionError) as exc:
        actual=type(exc).__name__
    passed=(isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=ulps*math.ulp(expected)
            and (actual==0)==(expected==0)
            if isinstance(expected,float) else actual==expected)
    return dict(helper=fn.__name__,inputs=repr(args),expected=repr(expected),
                actual=repr(actual),passed=passed)


def check():
    big,tiny=sys.float_info.max,math.ulp(0.)
    upper=math.nextafter(1.,2.)
    lower=math.nextafter(math.nextafter(1.,0.),0.)
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for args in [(big,0,-big,2),(1,1000,-1000,1),(tiny,1000,0,1),
                     (big,-1000,0,1),(-tiny,1000,0,1),(0,big,0,big),
                     (1,big,big,0),(1,0,-1,1),(1000,.04,200,5),
                     (big,1,0,1),(1,-1000,0,1)]:
            rows.append(observe(lab.exact_account,args,rounded(transition(*args))))
        for args in [(upper,lower,1.),(1,1,1),(upper,1,1),
                     (big,-big,tiny),(1,-big,tiny),(tiny,0,2),
                     (big,0,tiny),(big,0,big),(0,1,0),(1,-1,0),
                     (1000,.04,100),(1000,-.02,50)]:
            a,r,w=args
            if not a:
                expected=0.
            elif not w or (r>0 and F(r)*F(a)>=F(w)):
                expected=None
            else:
                ref=F(a)/F(w) if not r else (D(w)/(D(w)-D(r)*D(a))).ln()/D(r)
                expected=rounded(ref)
            rows.append(observe(lab.depletion_time,args,expected))
        for args in [(tiny,1000,0,0,1),(big,-1000,0,0,1),(0,0,-1,0,1),
                     (big,0,-big,0,2),(1,0,-2,1,2),(1000,.05,200,2,5),
                     (1000,.05,500,1,5),(1000,.05,500,3,5),
                     (0,1000,tiny,0,1),(big,-1000,0,1,1),
                     (big,0,big,0,1),(1,-1000,0,.5,1)]:
            a,r,j,tj,T=args
            first=rounded(D(a)*(D(r)*D(tj)).exp())
            # Existing API requires representable pre/post-jump states.
            if isinstance(first,str) or rounded(F(first)+F(j))=='ValueError':
                expected='ValueError'
            else:
                # Separately grow original capital and the timed payment.
                ref=D(a)*(D(r)*D(T)).exp()+D(j)*(D(r)*(D(T)-D(tj))).exp()
                expected=rounded(ref)
            rows.append(observe(lab.deposit_at,args,expected))
        for fn,args,error in [(lab.exact_account,(1,0,0,-1),'ValueError'),
                              (lab.depletion_time,(-1,0,1),'ValueError'),
                              (lab.depletion_time,(1,0,-1),'ValueError'),
                              (lab.deposit_at,(1,0,1,2,1),'ValueError'),
                              (lab.exact_account,(True,0,0,0),'TypeError'),
                              (lab.deposit_at,(1,float('nan'),0,0,1),'ValueError')]:
            rows.append(observe(fn,args,error))
        # Exercise the real assessment's numerical fields, not copied literals.
        report=lab.assessment()
        references={'exact_growth':D(1000)*D('.1').exp(),
                    'contributions':transition(1000,.04,200,5),
                    'deposit_at_year_two':D(1000)*D('.25').exp()+D(200)*D('.15').exp()}
        for key,ref in references.items():
            value=report[key];expected=float(ref)
            rows.append(dict(helper='assessment.'+key,expected=repr(expected),
                             actual=repr(value),passed=abs(value-expected)<=8*math.ulp(expected)))
        assert report['runtime_certified'] is False
        assert report['independent_review_completed'] is False
    # Observe actual shared use through public entry points and deposit composition.
    if hasattr(lab,'_continuous_account'):
        calls=[];original=lab._continuous_account
        def observed(a,r,u,t):
            calls.append((a,r,u,t))
            return 2.0
        lab._continuous_account=observed
        try:
            assert lab.deposit_at(1,0,3,1,2)==2.
        finally:
            lab._continuous_account=original
        assert calls==[(1.,0.,0.,1.),(5.,0.,0.,1.)]
        calls=[];original=lab._account_depletion
        def observed_depletion(a,r,w):
            calls.append((a,r,w))
            return .125
        lab._account_depletion=observed_depletion
        try:
            assert lab.depletion_time(1,0,1)==.125
        finally:
            lab._account_depletion=original
        assert calls==[(1.,0.,1.)]
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
