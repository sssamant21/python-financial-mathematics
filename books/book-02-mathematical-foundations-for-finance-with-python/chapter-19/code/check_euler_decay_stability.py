"""Observed Euler updates versus exact dyadic amplification references."""
from fractions import Fraction as F
import json
import section_19_05 as lab


def audit(result,events,lam,h,n):
    factor=1+F(lam)*F(h)
    assert len(events)==n
    for k,(t,y) in enumerate(events):
        assert F(t)==k*F(h)
        assert F(y)==factor**k
    assert F(result['final_state'])==factor**n
    assert result['steps']==n and result['step_size']==h
    assert result['status']=='completed'


def check():
    rows=[];wrong=0
    for lam,h,n in [(-2.,.25,4),(-2.,.5,4),(-2.,.75,4),
                    (-2.,1.,4),(-2.,1.25,4),(-.5,1.,4)]:
        events=[]
        def rhs(t,y):
            events.append((t,y))
            return lam*y
        result=lab.euler(rhs,1.,h*n,n)
        audit(result,events,lam,h,n)
        factor=1+F(lam)*F(h)
        assert lab.linear_amplification(lam,h)==float(factor)
        assert lab.stable_linear_decay(lam,h)==(abs(factor)<1)
        rows.append(dict(rate=lam,step=h,result=result,events=events,
                         factor=str(factor),stable=abs(factor)<1))
        if h==.25:
            for bad in (dict(result,final_state=1.),
                        dict(result,steps=n+1),
                        dict(result,status='converged')):
                try:
                    audit(bad,events,lam,h,n)
                except AssertionError:
                    wrong+=1
    assert wrong==3
    print(json.dumps(dict(cases=rows,wrong_variants_detected=wrong),indent=2))


if __name__=='__main__':
    check()
