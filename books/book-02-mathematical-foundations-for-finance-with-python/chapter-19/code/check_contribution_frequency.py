"""Section 19.8: independent payment sums, integral limits and signed order."""
from decimal import Decimal as D, localcontext
import json
import math
import section_19_08 as lab


def check():
    rows=[];ratios=[];mutants=0
    with localcontext() as ctx:
        ctx.prec=100
        for r in (.04,-.04):
            for u in (200.,-200.):
                a,t=1000.,5.
                dr,du,dt=D(r),D(u),D(t)
                integral=D(a)*(dr*dt).exp()+du*((dr*dt).exp()-1)/dr
                continuous=lab.continuous_contributions(a,r,u,t)
                # The signed-flow fixture subtracts two large components. Allow
                # rounding relative to their magnitudes, not the small total.
                budget=12*(D(math.ulp(float(D(a)*(dr*dt).exp())))+
                           D(math.ulp(float(du*((dr*dt).exp()-1)/dr))))
                assert abs(D(continuous)-integral)<=budget
                errors=[];observed_errors=[]
                for n in (4,8,16,32,64):
                    h=dt/n
                    # Each separate end-period payment accumulates for T-k*h.
                    reference=D(a)*(dr*dt).exp()+sum(
                        (du*h*(dr*(dt-k*h)).exp() for k in range(1,n+1)),D(0))
                    actual=lab.end_period_contributions(a,r,u,t,n)
                    assert abs(D(actual)-reference)<=budget
                    error=integral-reference
                    observed=D(continuous)-D(actual)
                    assert (error>0)==(dr*du>0)
                    allowance=2*budget
                    assert abs(observed-error)<=allowance
                    leading=du*dt*((dr*dt).exp()-1)/(2*n)
                    assert abs(error/leading-1)<D('.01')
                    errors.append(error)
                    observed_errors.append(observed)
                    rows.append(dict(rate=r,flow=u,n=n,actual=actual,
                                     reference=str(reference),signed_error=str(error),
                                     leading_term=str(leading)))
                for first,second,ofirst,osecond in zip(errors,errors[1:],observed_errors,observed_errors[1:]):
                    ratio=first/second
                    assert D('1.98')<ratio<D('2.02')
                    observed_ratio=ofirst/osecond
                    assert D('1.98')<observed_ratio<D('2.02')
                    ratios.append(dict(reference=str(ratio),observed=str(observed_ratio)))
        for n in (1,4,64):
            assert lab.end_period_contributions(1000,0,200,5,n)==2000.
            assert lab.end_period_contributions(1000,.04,200,0,n)==1000.
        # Wrong placement (beginning instead of end), no timing gap, and
        # the opposite sign cannot satisfy the finite cash-flow reference.
        sample=rows[0]
        ref=D(sample['reference'])
        for wrong in (lab.continuous_contributions(1000,.04,200,5),
                      sample['actual']+200*5/4*(math.exp(.04*5)-1),
                      2*lab.continuous_contributions(1000,.04,200,5)-sample['actual']):
            try:
                assert abs(D(wrong)-ref)<=8*D(math.ulp(float(ref)))
            except AssertionError:
                mutants+=1
        assert mutants==3
    print(json.dumps(dict(cases=rows,order_ratios=ratios,wrong_variants_detected=mutants),indent=2))


if __name__=='__main__':
    check()
