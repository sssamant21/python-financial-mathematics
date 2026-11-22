"""Independent reference checks for Section 10.8."""
import math
from section_10_08 import (
    finite,continuous_pv,schedule_pv,equal_payment_pv,timing_ratio,comparison)

def close(a,b,rel_tol=1e-10,abs_tol=1e-9):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_continuous_complete_scale():
    from decimal import Decimal,localcontext
    import section_10_08 as lab
    from unittest.mock import patch
    with localcontext() as ctx:
        ctx.prec=1800
        expected=float(Decimal.from_float(1e308)*(1-(-Decimal(2)).exp()))
        growth=float(Decimal.from_float(1e-308)*((Decimal(710)).exp()-1))
    assert continuous_pv(1e308,1.,2.)==expected
    assert continuous_pv(-1e308,1.,2.)==-expected
    assert continuous_pv(1e308,1e308,1e308)==1.
    assert continuous_pv(1e-308,-1.,710.)==growth
    assert continuous_pv(0.,-1e308,1e308)==0.
    assert continuous_pv(1e-308,1e308,1.)==0.  # Declared final-underflow policy.
    with patch.object(lab,"constant_pv",wraps=lab.constant_pv) as shared:
        continuous_pv(1200.,.06,2.)
        shared.assert_called_once_with(1200.,.06,2.)


def check_equal_payment_complete_scale():
    from decimal import Decimal,localcontext
    import section_10_08 as lab
    with localcontext() as ctx:
        ctx.prec=1800
        c=Decimal.from_float(1e308)
        expected=float(c*((-Decimal(1)).exp()+(-Decimal(2)).exp()))
    assert equal_payment_pv(1e308,1.,2.,2,"end")==expected
    assert equal_payment_pv(1.,1e308,1e308,2,"begin")==5e307
    assert equal_payment_pv(1.,1e308,1e308,2,"end")==0.
    with localcontext() as ctx:
        ctx.prec=1800
        immediate=float(Decimal.from_float(1e-308)*Decimal.from_float(1e308))
    assert equal_payment_pv(1e-308,-1e308,1e308,1,"begin")==immediate
    for timing in ("begin","mid","end"):
        rejects(ValueError,equal_payment_pv,1e308,0.,2.,2,timing)
        close(equal_payment_pv(1200.,.06,2.,10**400,timing),continuous_pv(1200.,.06,2.))
        rejects(ValueError,equal_payment_pv,1.,.1,1.,1<<4096,timing)


def check_schedule_complete_scale():
    from decimal import Decimal,localcontext
    import itertools
    assert schedule_pv([(0.,1e308),(1.,1e308),(2.,-1e308),(3.,-1e308),(4.,3.)],0.)==3.
    assert schedule_pv([(10001.,1e308),(10001.,-1e308),(0.,3.)],-1.)==3.
    with localcontext() as ctx:
        ctx.prec=2200
        expected=float(Decimal.from_float(1e-308)*Decimal(710).exp())
    assert schedule_pv([(710.,1e-308)],-1.)==expected
    assert schedule_pv([(1e308,0.)],-1e308)==0.
    assert schedule_pv([(0.,1e308),(math.ulp(0.),-1e308)],1e-308)==math.ulp(0.)
    assert schedule_pv([(1.,math.ulp(0.))],1.)==0.
    rejects(ValueError,schedule_pv,[(0.,1e308),(0.,1e308)],0.)
    rejects(ValueError,schedule_pv,[(10001.,1.),(-1.,1.)],-1.)
    rejects(ValueError,schedule_pv,itertools.repeat((0.,1.)),0.)


def check_ratio_complete_range_and_report():
    from decimal import Decimal,localcontext
    for rate in (710.,1500.):
        with localcontext() as ctx:
            ctx.prec=2200
            expected=float(Decimal.from_float(rate)/(Decimal.from_float(rate).exp()-1)*((Decimal.from_float(rate)/2).exp()))
        assert timing_ratio(rate,1.,1,"mid")==expected
    assert timing_ratio(1e308,1.,1,"begin")==1e308
    assert timing_ratio(-1e308,1.,1,"end")==1e308
    assert timing_ratio(1e308,1e308,1,"end")==0.
    rejects(ValueError,timing_ratio,1e308,1e308,1,"begin")
    for timing in ("begin","mid","end"):
        assert timing_ratio(.06,2.,10**400,timing)==1.
        rejects(ValueError,timing_ratio,.1,1.,1<<4096,timing)
    rejects(ValueError,comparison,1e308,1.,2.)


def run():
    check_ratio_complete_range_and_report()
    check_schedule_complete_scale()
    check_equal_payment_complete_scale()
    check_continuous_complete_scale()
    c,T=1200,2
    close(continuous_pv(c,0,T),2400)
    close(schedule_pv([(0,100),(1,100)],0),200)
    close(schedule_pv([(0,100),(1,100)],math.log(2)),150)
    for rate in (-0.02,0,0.06):
        continuous=continuous_pv(c,rate,T)
        for n in (2,8,24,730):
            for timing in ("begin","mid","end"):
                exact=equal_payment_pv(c,rate,T,n,timing)
                offset={"begin":0,"mid":0.5,"end":1}[timing]
                explicit=math.fsum((c*T/n)*math.exp(-rate*(i+offset)*T/n)
                                   for i in range(n))
                close(exact,explicit)
                close(exact,continuous*timing_ratio(rate,T,n,timing))
            start=equal_payment_pv(c,rate,T,n,"begin")
            middle=equal_payment_pv(c,rate,T,n,"mid")
            end=equal_payment_pv(c,rate,T,n,"end")
            if rate>0:
                assert start>middle>end
            elif rate<0:
                assert start<middle<end
            else:
                close(start,middle)
                close(middle,end)
        for timing in ("begin","mid","end"):
            assert abs(equal_payment_pv(c,rate,T,730,timing)-continuous)<abs(
                equal_payment_pv(c,rate,T,2,timing)-continuous)+1e-9
    close(equal_payment_pv(1000,0,2,4),2000)
    close(equal_payment_pv(0,0.06,2,4),0)
    rejects(ValueError,equal_payment_pv,1000,0.06,2,0)
    rejects(ValueError,equal_payment_pv,1000,0.06,2,2,"other")
    rejects(ValueError,continuous_pv,1000,0.06,-1)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    report=comparison()
    assert len(report["scenarios"])==4 and report["runtime_certified"] is False
    print("PASS: Section 10.8 independent reference checks")

if __name__=="__main__":
    run()
