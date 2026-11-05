"""Independent complete-discount and nominal gross-growth benchmark references."""
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


def pv_reference(f,r,t):
    if not f:
        return 0.
    exponent=-D(r)*D(t)
    # Outside this broad bound even maximal/minimal binary64 scaling cannot
    # produce a representable nonzero result. No float product is used.
    magnitude=D(abs(f)).ln()+exponent
    if abs(magnitude)>10000:
        return 'ValueError'
    return rounded(D(f)*exponent.exp())


def rate_reference(j,n):
    gross=F(n)+F(j)
    if gross<=0:
        return 'ValueError'
    factor=(D(gross.numerator)/D(gross.denominator))/D(n)
    return rounded(D(n)*factor.ln())


def observe(fn,args,expected):
    try:
        actual=fn(*args)
    except (TypeError,ValueError,OverflowError,ZeroDivisionError) as exc:
        actual=type(exc).__name__
    passed=(isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=4*math.ulp(expected)
            and (actual==0)==(expected==0)
            if isinstance(expected,float) else actual==expected)
    return dict(helper=fn.__name__,inputs=repr(args),expected=repr(expected),actual=repr(actual),passed=passed)


def check():
    big,tiny=sys.float_info.max,math.ulp(0.)
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for args in [(tiny,-1000,1),(big,1000,1),(0,-big,big),(big,big,0),
                     (1,big,big),(1,-big,big),(tiny,1,1),(-tiny,-1000,1),
                     (-big,1000,1),(big,tiny,tiny),(1,tiny,big),(1000,.05,2),(1,0,3)]:
            rows.append(observe(lab.present_value,args,pv_reference(*args)))
        for args in [(tiny,2),(-tiny,2),(1,10**1000),(big,10**1000),
                     (-1,10**1000),(1e-300,10**1000),(0,10**1000),
                     (-float(2**1000),2**1000+1),(.06,12),(-.1,12),(big,1),
                     (-math.nextafter(big,0),int(big)),(-1,1),(1,1),(-.5,1)]:
            rows.append(observe(lab.nominal_to_continuous,args,rate_reference(*args)))
        for fn,args,error in [(lab.present_value,(True,0,0),'TypeError'),
                              (lab.present_value,(1,0,-1),'ValueError'),
                              (lab.present_value,(0,float('nan'),0),'ValueError'),
                              (lab.nominal_to_continuous,(0,0),'ValueError'),
                              (lab.nominal_to_continuous,(0,True),'ValueError'),
                              (lab.nominal_to_continuous,(0,2.),'ValueError'),
                              (lab.nominal_to_continuous,(True,12),'TypeError'),
                              (lab.nominal_to_continuous,(float('nan'),12),'ValueError')]:
            rows.append(observe(fn,args,error))
        report=lab.assessment();rc=rate_reference(.06,12)
        refs={'present_value':pv_reference(1000,.05,2),
              'continuous_equivalent_rate':rc,
              'continuous_one_year_growth':float((D(1)+D(.06)/12)**12)}
        for key,expected in refs.items():
            actual=report[key]
            rows.append(dict(helper='assessment.'+key,expected=expected,actual=actual,
                             passed=abs(actual-expected)<=4*math.ulp(expected)))
        assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    if hasattr(lab,'_scaled_valuation'):
        calls=[];old_s,old_r=lab._scaled_valuation,lab._nominal_conversion
        def scaled(a,exponent):
            calls.append(('present_value',a,exponent));return 7.
        def rate(j,n):
            calls.append(('rate',j,n));return .125
        lab._scaled_valuation,lab._nominal_conversion=scaled,rate
        try:
            report=lab.assessment()
        finally:
            lab._scaled_valuation,lab._nominal_conversion=old_s,old_r
        assert report['present_value']==7. and report['continuous_equivalent_rate']==.125
        assert report['continuous_one_year_growth']==math.exp(.125)
        assert calls==[('rate',.06,12),('present_value',1000.,-F(.05)*F(2))]
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
