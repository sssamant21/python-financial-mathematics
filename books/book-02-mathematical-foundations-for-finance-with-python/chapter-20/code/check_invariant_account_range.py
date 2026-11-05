"""Actual invariant transitions/reports compared with independent integrated references."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_20_03 as lab


def reference(a,r,u,t):
    if not r or not t:
        return float(F(a)+F(u)*F(t))
    if F(u)==-F(a)*F(r):
        return float(a)
    exp=(D(r)*D(t)).exp()
    return float(D(a)*exp+D(u)*(exp-1)/D(r))


def close(actual,expected):
    return (isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=8*math.ulp(expected)
            and (actual==0)==(expected==0))


def check():
    big,tiny=sys.float_info.max,math.ulp(0.)
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for args in [(tiny,1000,0,1),(big,-1000,0,1),(big,0,-big,2),
                     (1,1000,-1000,1),(0,tiny,big,tiny),(-tiny,1000,0,1)]:
            expected=reference(*args)
            try:
                actual=lab.account_transition(*args)
            except (ValueError,OverflowError) as exc:
                actual=type(exc).__name__
            rows.append(dict(kind='direct',inputs=repr(args),expected=expected,actual=actual,passed=close(actual,expected)))
        for a,r,u,h1,h2 in [(tiny,1000,0,.5,.5),(big,-1000,0,.5,.5),
                            (1,1000,-1000,.5,.5),(big,0,-big,1,1),
                            (1000,.04,200,2,3),(-1000,-.04,200,2,3),
                            (10,0,-7,1,2)]:
            expected_prefix=reference(a,r,u,h1)
            expected=reference(a,r,u,h1+h2)
            try:
                prefix=lab.account_transition(a,r,u,h1)
                split=lab.account_transition(prefix,r,u,h2)
                direct=lab.account_transition(a,r,u,h1+h2)
                actual=dict(prefix=prefix,split=split,direct=direct)
                passed=close(prefix,expected_prefix) and close(split,expected) and close(direct,expected)
            except (ValueError,OverflowError) as exc:
                actual=type(exc).__name__;passed=False
            rows.append(dict(kind='composition',inputs=repr((a,r,u,h1,h2)),expected_prefix=expected_prefix,expected_final=expected,actual=actual,passed=passed))
        for args,error in [((1,-1000,0,1),'ValueError'),((big,1,0,1),'ValueError'),
                           ((True,0,0,0),'TypeError'),((1,0,0,-1),'ValueError')]:
            try:
                actual=lab.account_transition(*args)
            except (ValueError,OverflowError,TypeError) as exc:
                actual=type(exc).__name__
            rows.append(dict(kind='guard',inputs=repr(args),expected=error,actual=actual,passed=actual==error))
        report=lab.assessment()
        expected=reference(1000,.04,200,5)
        for key,ref in [('account_composition_left',expected),('account_composition_right',expected),
                        ('zero_interest_reconciliation',float(F(200)*5))]:
            rows.append(dict(kind='assessment',key=key,expected=ref,actual=report[key],passed=close(report[key],ref)))
        assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    if hasattr(lab,'_account_balance'):
        calls=[];old=lab._account_balance
        def observed(*args):
            calls.append(args);return 7.0
        lab._account_balance=observed
        try:
            report=lab.assessment()
        finally:
            lab._account_balance=old
        assert report['account_composition_left']==report['account_composition_right']==7.
        assert report['zero_interest_reconciliation']==-993.
        assert calls==[(1000.,.04,200.,2.),(1000.,.04,200.,5.),(7.,.04,200.,3.),(1000.,0.,200.,5.)]
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
