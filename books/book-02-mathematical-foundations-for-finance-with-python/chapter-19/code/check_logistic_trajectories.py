"""Independent reciprocal-coordinate logistic trajectories and asymptotic checks."""
from decimal import Decimal as D, localcontext
import json
import math
import section_19_02 as lab


def near(actual,reference):
    assert math.isfinite(actual)
    assert abs(D(actual)-reference)<=6*D(math.ulp(float(reference)))


def check():
    rows=[];semigroup=[]
    with localcontext() as ctx:
        ctx.prec=100
        k,r=1000.,.4
        for initial in (0.,100.,250.,1000.,2000.,4000.):
            previous=None
            for time in (0.,.5,1.,2.,4.,8.,16.,32.,80.):
                if initial==0:
                    reference=D(0)
                else:
                    inverse=1/D(k)+(1/D(initial)-1/D(k))*(-D(r)*D(time)).exp()
                    reference=1/inverse
                actual=lab.logistic(initial,r,k,time)
                near(actual,reference)
                if initial==0:
                    assert actual==0
                elif initial==k:
                    assert actual==k
                elif initial<k:
                    assert initial<=actual<=k
                    if previous is not None:
                        assert actual>=previous
                        assert k-actual<=k-previous
                else:
                    assert k<=actual<=initial
                    if previous is not None:
                        assert actual<=previous
                        assert actual-k<=previous-k
                previous=actual
                rows.append(dict(initial=initial,time=time,actual=actual,reference=str(reference)))
            if initial>0:
                # Continuous autonomous evolution is independent of the split.
                first=lab.logistic(initial,r,k,2)
                split=lab.logistic(first,r,k,3)
                total=lab.logistic(initial,r,k,5)
                assert abs(split-total)<=6*math.ulp(total)
                semigroup.append(dict(initial=initial,split=split,total=total))
        # Swapping above/below branches or freezing at the initial state
        # cannot satisfy the independent reciprocal-coordinate reference.
        reference=1/(1/D(k)+(1/D(2000)-1/D(k))*(-D(r)*5).exp())
        wrong=0
        for value in (2000.,lab.logistic(250,r,k,5),k):
            try:
                near(value,reference)
            except AssertionError:
                wrong+=1
        assert wrong==3
    print(json.dumps(dict(trajectories=rows,semigroup=semigroup,
                         wrong_variants_detected=wrong),indent=2))


if __name__=='__main__':
    check()
