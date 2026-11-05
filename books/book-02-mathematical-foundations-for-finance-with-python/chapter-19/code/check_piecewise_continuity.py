"""Independent global integrating-factor oracle for piecewise constant flows."""
from decimal import Decimal as D, localcontext
import json
import math
import section_19_03 as lab


def reference(a,r,segments):
    T=sum((D(t) for u,t in segments),D(0))
    dr=D(r)
    value=D(a)*(dr*T).exp()
    cursor=D(0)
    for u,t in segments:
        end=cursor+D(t)
        value += (D(u)*D(t) if not dr else
                  D(u)*((dr*(T-cursor)).exp()-(dr*(T-end)).exp())/dr)
        cursor=end
    return value


def near(actual,ref):
    assert abs(D(actual)-ref)<=D('2e-11'),(actual,str(ref))


def check():
    rows=[];continuity=[];wrong=0
    segments=[(200.,.5),(-300.,1.),(100.,1.5)]
    with localcontext() as ctx:
        ctx.prec=100
        for rate in (0.,.04,-.04):
            original=list(segments)
            for k in (1,2,3):
                schedule=segments[:k]
                ref=reference(1000,rate,schedule)
                actual=lab.piecewise_account(1000,rate,schedule)
                near(actual,ref)
                rows.append(dict(rate=rate,segments=schedule,actual=actual,reference=str(ref)))
                # A zero interval and same-flow subdivision do not create jumps.
                zero=[(999.,0.)]+schedule+[(999.,0.)]
                near(lab.piecewise_account(1000,rate,zero),ref)
                split=[part for u,t in schedule for part in ((u,t/2),(u,t/2))]
                near(lab.piecewise_account(1000,rate,split),ref)
            for k in (1,2):
                at=reference(1000,rate,segments[:k])
                prev=[]
                for epsilon in (2**-10,2**-11,2**-12):
                    left=segments[:k-1]+[(segments[k-1][0],segments[k-1][1]-epsilon)]
                    right=segments[:k]+[(segments[k][0],epsilon)]
                    lval=lab.piecewise_account(1000,rate,left)
                    rval=lab.piecewise_account(1000,rate,right)
                    near(lval,reference(1000,rate,left))
                    near(rval,reference(1000,rate,right))
                    errors=[abs(D(lval)-at),abs(D(rval)-at)]
                    # In these fixtures |r*A+u| is below 1000 on both sides.
                    assert max(errors)<=1000*D(epsilon)
                    if prev:
                        assert all(D('1.99')<a/b<D('2.01') for a,b in zip(prev,errors))
                    prev=errors
                    continuity.append(dict(rate=rate,boundary=k,epsilon=epsilon,
                                           left=lval,right=rval,limit=str(at)))
            assert segments==original
        sample=reference(1000,.04,segments)
        altered=[lab.piecewise_account(1000,.04,list(reversed(segments))),
                 lab.piecewise_account(1000,.04,[(u*t,t) for u,t in segments]),
                 lab.piecewise_account(1000,.04,segments)+100]
        for bad in altered:
            try:
                near(bad,sample)
            except AssertionError:
                wrong+=1
        assert wrong==3
        assert lab.piecewise_account(1000,.04,[])==1000.
    print(json.dumps(dict(prefix_references=rows,continuity=continuity,
                         wrong_variants_detected=wrong),indent=2))


if __name__=='__main__':
    check()
