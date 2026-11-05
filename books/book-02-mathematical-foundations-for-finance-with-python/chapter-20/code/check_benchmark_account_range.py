"""Independent actual benchmark account/depletion and assessment references."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_20_02 as lab


def rounded(value):
    try:
        result=float(value)
    except OverflowError:
        return 'ValueError'
    return 'ValueError' if not math.isfinite(result) or (value and not result) else result


def balance(a,r,u,t):
    if not r or not t:
        return F(a)+F(u)*F(t)
    if F(u)==-F(r)*F(a):
        return F(a)
    exp=(D(r)*D(t)).exp()
    return D(a)*exp+D(u)*(exp-1)/D(r)


def observe(fn,args,expected):
    try:
        actual=fn(*args)
    except (ValueError,TypeError,OverflowError,ZeroDivisionError) as exc:
        actual=type(exc).__name__
    passed=(isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=4*math.ulp(expected)
            and (actual==0)==(expected==0)
            if isinstance(expected,float) else actual==expected)
    return dict(helper=fn.__name__,inputs=repr(args),expected=repr(expected),actual=repr(actual),passed=passed)


def check():
    big,tiny=sys.float_info.max,math.ulp(0.)
    upper=math.nextafter(1.,2.)
    lower=math.nextafter(math.nextafter(1.,0.),0.)
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for args in [(big,0,-big,2),(1,1000,-1000,1),(tiny,1000,0,1),
                     (big,-1000,0,1),(-tiny,1000,0,1),(0,big,0,big),
                     (1,big,big,0),(1,0,-1,1),(0,tiny,big,tiny),
                     (big,1,0,1),(1,-1000,0,1),(1000,.04,200,5)]:
            rows.append(observe(lab.account,args,rounded(balance(*args))))
        # At half the minimum subnormal, the sign of an arbitrarily small
        # exponential correction determines which float is nearest.
        rows.append(observe(lab.account,(tiny,-2,tiny,2500),tiny))
        rows.append(observe(lab.account,(0,-2,tiny,2500),'ValueError'))
        for args in [(upper,lower,1.),(1,1,1),(upper,1,1),(big,-big,tiny),
                     (1,-big,tiny),(tiny,0,2),(big,0,tiny),(big,0,big),
                     (0,1,0),(1,-1,0),(1000,.04,100),(1000,-.02,50),
                     (1,tiny,1),(tiny,big,big)]:
            a,r,w=args
            if not a:
                expected=0.
            elif not w or (r>0 and F(r)*F(a)>=F(w)):
                expected=None
            else:
                reference=F(a)/F(w) if not r else (D(w)/(D(w)-D(r)*D(a))).ln()/D(r)
                expected=rounded(reference)
            rows.append(observe(lab.depletion_time,args,expected))
        for fn,args,error in [(lab.account,(True,0,0,0),'TypeError'),
                              (lab.account,(1,0,0,-1),'ValueError'),
                              (lab.account,(0,float('nan'),0,0),'ValueError'),
                              (lab.depletion_time,(-1,0,1),'ValueError'),
                              (lab.depletion_time,(1,0,-1),'ValueError'),
                              (lab.depletion_time,(True,0,0),'TypeError')]:
            rows.append(observe(fn,args,error))
        report=lab.assessment()
        refs={'continuous_account':float(balance(1000,.04,200,5)),
              'depletion_time':float((D(100)/(D(100)-D(.04)*1000)).ln()/D(.04))}
        for key,expected in refs.items():
            value=report[key]
            rows.append(dict(helper='assessment.'+key,expected=expected,actual=value,
                             passed=abs(value-expected)<=4*math.ulp(expected)))
        assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    if hasattr(lab,'_account_balance'):
        calls=[];old_a,old_d=lab._account_balance,lab._account_depletion
        def a(*args):
            calls.append(('account',args));return 7.0
        def d(*args):
            calls.append(('depletion',args));return .125
        lab._account_balance,lab._account_depletion=a,d
        try:
            report=lab.assessment()
        finally:
            lab._account_balance,lab._account_depletion=old_a,old_d
        assert report['continuous_account']==7.0 and report['depletion_time']==.125
        assert calls==[('account',(1000.,.04,200.,5.)),('depletion',(1000.,.04,100.))]
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
