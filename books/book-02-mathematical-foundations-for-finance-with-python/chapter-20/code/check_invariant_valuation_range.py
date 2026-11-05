"""Independent invariant factor/PV/FV and actual cash-flow/report range checks."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_20_03 as lab


def reference(a,r,t,sign):
    if not a:return 0.
    exponent=D(sign)*D(r)*D(t)
    magnitude=D(abs(a)).ln()+exponent
    if abs(magnitude)>10000:return 'ValueError'
    value=D(a)*exponent.exp();result=float(value)
    return 'ValueError' if not math.isfinite(result) or (value and not result) else result


def close(actual,expected):
    return (isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=4*math.ulp(expected)
            and (actual==0)==(expected==0))


def observe(fn,args,expected):
    try:actual=fn(*args)
    except (ValueError,TypeError,OverflowError) as exc:actual=type(exc).__name__
    passed=close(actual,expected) if isinstance(expected,float) else actual==expected
    return dict(helper=fn.__name__,inputs=repr(args),expected=repr(expected),actual=repr(actual),passed=passed)


def check():
    big,tiny=sys.float_info.max,math.ulp(0.)
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for args in [(0,0),(big,0),(-big,0),(0,big),(1000,1),(-1000,1),(.04,5)]:
            rows.append(observe(lab.discount_factor,args,reference(1.,*args,-1)))
        for args in [(tiny,-1000,1),(big,1000,1),(0,-big,big),(0,big,big),
                     (1,big,big),(1,-big,big),(-tiny,-1000,1),(1000,.04,2)]:
            rows.append(observe(lab.present_value,args,reference(*args,-1)))
        for args in [(tiny,1000,1),(big,-1000,1),(0,big,big),
                     (1,-big,big),(big,0,0),(-tiny,1000,1)]:
            rows.append(observe(lab.future_value,args,reference(*args,1)))
        for args in [(tiny,1000,1),(big/2,-1000,1),(1000,.04,5)]:
            a,r,t=args
            try:
                fv=lab.future_value(a,r,t);actual=lab.present_value(fv,r,t)
                passed=close(fv,reference(a,r,t,1)) and close(actual,float(a))
            except (ValueError,OverflowError) as exc:actual=type(exc).__name__;passed=False
            rows.append(dict(helper='actual PV/FV round trip',inputs=repr(args),expected=float(a),actual=actual,passed=passed))
        for flows,r in [([(tiny,1),(tiny,1)],-1000),([(big,1),(-big/2,1)],1000),([(0,1)],-big)]:
            expected=float(sum((D(a)*(-D(r)*D(t)).exp() for a,t in flows),D(0))) if r!=-big else 0.
            rows.append(observe(lab.cash_flow_pv,(flows,r),expected))
        for fn,args,error in [(lab.present_value,(True,0,0),'TypeError'),
                              (lab.future_value,(1,0,-1),'ValueError'),
                              (lab.present_value,(0,float('nan'),0),'ValueError'),
                              (lab.discount_factor,(True,0),'TypeError'),
                              (lab.cash_flow_pv,([],float('nan')),'ValueError'),
                              (lab.cash_flow_pv,([(big,0),(big,0)],0),'OverflowError')]:
            rows.append(observe(fn,args,error))
        report=lab.assessment();df=float((-D(.04)*5).exp());pv=float(D(100)*(-D(.04)*2).exp())
        for key,expected in [('discount_zero_horizon',1.),('discount_composition_left',df),
                             ('discount_composition_right',df),('pv_split_left',pv),
                             ('pv_split_right',pv),('pv_future_round_trip',1000.),('cash_flow_split',pv)]:
            rows.append(dict(helper='assessment.'+key,expected=expected,actual=report[key],passed=close(report[key],expected)))
        assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    if hasattr(lab,'_scaled_valuation'):
        calls=[];old=lab._scaled_valuation
        def observed(a,exponent):
            calls.append((a,exponent));return 7.
        lab._scaled_valuation=observed
        try:report=lab.assessment()
        finally:lab._scaled_valuation=old
        assert len(calls)==11
        assert report['discount_composition_left']==7. and report['discount_composition_right']==49.
        assert report['pv_split_left']==7. and report['pv_split_right']==14.
        assert report['pv_future_round_trip']==7. and report['cash_flow_split']==14.
        assert (7.,-F(.04)*5) in calls
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
