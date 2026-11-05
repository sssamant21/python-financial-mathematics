"""Independent polynomial integrals, power sums, and coupled RK4 stage values."""
from fractions import Fraction as F
import json
import math
import section_19_05 as eu
import section_19_06 as rk


def power_sum(p,n):
    return [F(n),F(n*(n-1),2),F(n*(n-1)*(2*n-1),6),
            F(n*n*(n-1)*(n-1),4),
            F(n*(n-1)*(2*n-1)*(3*n*n-3*n-1),30)][p]


def near(a,q):
    assert abs(a-float(q))<=16*math.ulp(float(q)),(a,str(q))


def coupled_audit(value,events):
    expected=[(F(0),F(1)),(F(1,4),F(1)),
              (F(1,4),F(71,64)),(F(1,2),F(163,128))]
    assert [(F(t),F(y)) for t,y in events]==expected
    near(value,F(1919,1536))


def check():
    rows=[]; ratios=[]; euler_errors=[]; rk_errors=[]
    for p in range(5):
        for n in (1,2,4,8):
            h=F(1,n)
            events=[]
            def f(t,y):
                events.append((t,y))
                return t**p
            e=eu.euler(f,2,1,n)
            assert [F(t) for t,y in events]==[k*h for k in range(n)]
            er=2+h**(p+1)*power_sum(p,n)
            near(e['final_state'],er)
            assert e['steps']==n and e['status']=='completed'
            events=[]
            r=rk.fixed_rk4(f,2,1,n)
            expected_times=[v for k in range(n) for v in
                            (k*h,k*h+h/2,k*h+h/2,(k+1)*h)]
            assert [F(t) for t,y in events]==expected_times
            integral=F(2)+F(1,p+1)
            expected_rk=integral+(h**4/120 if p==4 else 0)
            near(r['final_state'],expected_rk)
            assert r['steps']==n and r['evaluations']==4*n
            assert r['status']=='completed' and r['final_time']==1
            if p==1:
                error=float(integral)-e['final_state']
                near(error,h/2)
                euler_errors.append(error)
            if p==4:
                error=r['final_state']-float(integral)
                # Difference of rounded final states: allowance uses state ulps.
                assert abs(error-float(h**4/120))<=32*math.ulp(float(integral))
                rk_errors.append(error)
            rows.append(dict(power=p,steps=n,euler=e,rk4=r,
                             euler_reference=str(er),rk4_reference=str(expected_rk)))
    for errors,order in ((euler_errors,2),(rk_errors,16)):
        for a,b in zip(errors,errors[1:]):
            ratio=a/b
            assert abs(ratio/order-1)<1e-6
            ratios.append(ratio)
    events=[]
    def coupled(t,y):
        events.append((t,y))
        return y-t*t+2*t-1
    value=rk.rk4_step(coupled,0,1,.5)
    coupled_audit(value,events)
    wrong=0
    for v,ev in [(1.25,events),(value,events[:-1]),
                 (value,[events[0],events[2],events[1],events[3]])]:
        try:
            coupled_audit(v,ev)
        except AssertionError:
            wrong+=1
    assert wrong==3
    print(json.dumps(dict(cases=rows,observed_order_ratios=ratios,
                         coupled=dict(value=value,events=events,exact_solution=1.25),
                         wrong_variants_detected=wrong),indent=2))


if __name__=='__main__':
    check()
