"""Independent signed transition and actual simulator/report range references."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_19_09 as lab


def reference(a,r,u,t):
    if r==0 or t==0:
        return F(a)+F(u)*F(t)
    if F(u)==-F(r)*F(a):
        return D(a)
    x=D(r)*D(t)
    return D(a)*x.exp()+D(u)*(x.exp()-1)/D(r)


def rounded(value):
    try:
        result=float(value)
    except OverflowError:
        return 'ValueError'
    return 'ValueError' if not math.isfinite(result) or (value and not result) else result


def close(actual,expected):
    return (isinstance(actual,(int,float)) and math.isfinite(actual)
            and abs(actual-expected)<=4*math.ulp(expected)
            and (actual==0)==(expected==0))


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for a,r,u,t in [(1,1000,-1000,1),(1,big,-big,1),
                        (tiny,1000,0,1),(big,-1000,0,1),
                        (big,0,-big,2),(1,0,-1,1),(0,big,0,big),
                        (big,1,0,1),(1,-1000,0,1),
                        (-tiny,1000,0,1),(1,big,big,0),
                        (0,tiny,big,tiny)]:
            expected=rounded(reference(a,r,u,t))
            try:
                actual=lab.transition(a,r,u,t)
            except (ValueError,OverflowError) as exc:
                actual=type(exc).__name__
            ok=close(actual,expected) if isinstance(expected,float) else actual==expected
            rows.append(dict(kind='transition',inputs=repr((a,r,u,t)),
                             expected=repr(expected),actual=repr(actual),passed=ok))
        scenarios=[
            (tiny,1000,0,1,(),rounded(reference(tiny,1000,0,1)),[]),
            (big,-1000,0,1,(),rounded(reference(big,-1000,0,1)),[]),
            (big,1,-big,3,(),big,[]),
            (1,1000,-1000,1,((.5,1),),float(1+D(500).exp()),
             [dict(type='jump',time=.5,amount=1.,balance=2.)]),
            (10,0,2,3,((1,-5),(2,7)),18.,
             [dict(type='jump',time=1.,amount=-5.,balance=7.),
              dict(type='jump',time=2.,amount=7.,balance=16.)]),
        ]
        for a,r,u,T,jumps,balance,events in scenarios:
            try:
                result=lab.simulate(a,r,u,T,jumps)
            except (ValueError,OverflowError) as exc:
                result=type(exc).__name__
            ok=(isinstance(result,dict) and result['status']=='completed'
                and close(result['final_balance'],balance) and result['final_time']==T
                and result['depletion_time'] is None and result['events']==events
                and result['scheduled_jumps']==result['applied_jumps']==len(jumps)
                and result['inputs']==dict(initial=float(a),rate=float(r),flow=float(u),
                                          horizon=float(T),jumps=jumps)
                and result['model']=='constant_rate_continuous_account'
                and result['runtime_certified'] is False)
            rows.append(dict(kind='simulator',inputs=repr((a,r,u,T,jumps)),
                             expected_balance=repr(balance),result=result,passed=ok))
        expected_time=.5+float(D(4).ln()/1000)
        try:
            result=lab.simulate(1,1000,-1000,1,((.5,-.25),))
        except (ValueError,OverflowError) as exc:
            result=type(exc).__name__
        ok=(isinstance(result,dict) and result['status']=='depleted'
            and close(result['final_time'],expected_time)
            and result['events'][0]==dict(type='jump',time=.5,amount=-.25,balance=.75)
            and result['events'][1]==dict(type='depletion',time=result['final_time'])
            and result['applied_jumps']==1 and result['final_balance']==0)
        rows.append(dict(kind='post-jump depletion',expected_time=expected_time,
                         result=result,passed=ok))
        try:
            lab.simulate(1,-1000,0,1)
        except ValueError:
            ok=True
        else:
            ok=False
        rows.append(dict(kind='no false depletion from rounded zero',passed=ok))
    original=lab._continuous_transition
    calls=[]
    def observed(a,r,u,t):
        calls.append((a,r,u,t))
        return 5.0
    lab._continuous_transition=observed
    try:
        result=lab.simulate(1,0,0,2)
        assert result['final_balance']==5.
    finally:
        lab._continuous_transition=original
    assert calls==[(1.,0.,0.,2.)]
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
