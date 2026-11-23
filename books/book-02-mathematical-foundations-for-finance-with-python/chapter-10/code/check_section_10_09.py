"""Independent checks for Section 10.9 valuation engine."""
import math
from section_10_09 import (Stream,Curve,finite,analytic_pv,numerical_pv,
                           discrete_pv,portfolio_pv,parallel_shift_derivative,assessment,exponential_integral,weighted_integral,simpson)

def close(a,b,rel_tol=1e-8,abs_tol=1e-7):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(exponential_integral(1e308,-1,2),8.646647167633874e307,rel_tol=2e-15,abs_tol=0.)
    close(exponential_integral(1e-308,1,710),2.233994766161711,rel_tol=2e-15,abs_tol=0.)
    close(exponential_integral(1e308,-1e308,1e308),1.,rel_tol=2e-15,abs_tol=0.)
    assert exponential_integral(0,1e308,1e308)==0
    close(analytic_pv(Stream("constant",1e308),Curve(1e308),1,1e308),.5,rel_tol=2e-15,abs_tol=0.)
    close(analytic_pv(Stream("exponential",1e308,-1e308),Curve(1e308),1),.5,rel_tol=2e-15,abs_tol=0.)
    close(analytic_pv(Stream("exponential",1,1e16),Curve(1e16),1,1),.6321205588285577,rel_tol=2e-15,abs_tol=0.)
    rejects(ValueError,exponential_integral,1e308,0,2)
    close(weighted_integral(1,1e308),1.,rel_tol=3e-15,abs_tol=0.)
    assert weighted_integral(1e308,1e308)==0.
    assert analytic_pv(Stream("linear",1e308,-1e308),Curve(0),2)==0.
    close(analytic_pv(Stream("linear",0,1e308),Curve(0),1e-308),5e-309,rel_tol=3e-15,abs_tol=0.)
    close(analytic_pv(Stream("linear",0,1e308),Curve(1e308),1),1e-308,rel_tol=3e-15,abs_tol=0.)
    assert analytic_pv(Stream("linear",709,-1),Curve(-1),710)==-710.
    close(Stream("linear",1e308,-1e308).rate(2),-1e308,rel_tol=3e-15,abs_tol=0.)
    close(Stream("exponential",1e-308,1).rate(710),2.233994766161711,rel_tol=3e-15,abs_tol=0.)
    assert Stream("exponential",0,1e308).rate(1e308)==0.
    assert Curve(-1e308,1e308).discount(2)==1.
    assert Curve(1e308).discount(0,1e308)==1.
    rejects(ValueError,Stream("exponential",1,1).rate,710)
    close(simpson(lambda t:1e308,1,2),1e308,rel_tol=3e-15,abs_tol=0.)
    assert simpson(lambda t:-5e307 if t==.5 else 1e308,1,2)==0.
    close(simpson(lambda t:1e308,1e-308,2),.9999999999999999,rel_tol=3e-15,abs_tol=0.)
    rejects(ValueError,simpson,lambda t:1.,5e-324,2)
    rejects(ValueError,simpson,lambda t:1.,1.,100002)
    rejects(TypeError,simpson,3,0.,2)
    flat=Curve(0.05)
    zero=Curve(0)
    affine=Curve(0.03,0.005)
    streams=[Stream("constant",1000),Stream("linear",200,50),
             Stream("exponential",150,0.02)]
    close(analytic_pv(Stream("constant",1000),zero,4),4000)
    close(analytic_pv(Stream("linear",200,50),zero,4),1200)
    close(analytic_pv(Stream("exponential",150,0.05),flat,4),600)
    close(discrete_pv([(0,100),(2,500)],zero),600)
    close(discrete_pv([(2,500)],flat),500*math.exp(-0.1))
    for curve in (flat,zero,Curve(-0.02)):
        for stream in streams:
            close(analytic_pv(stream,curve,4),numerical_pv(stream,curve,4,512))
    for stream in streams:
        coarse=numerical_pv(stream,affine,4,128)
        fine=numerical_pv(stream,affine,4,256)
        finer=numerical_pv(stream,affine,4,512)
        assert abs(finer-fine)<abs(fine-coarse)+1e-10
    portfolio=portfolio_pv(streams,[(2,500)],flat,4,512)
    expected=sum(analytic_pv(s,flat,4) for s in streams)+500*math.exp(-0.1)
    close(portfolio["total"],expected)
    derivative=parallel_shift_derivative(streams,[(2,500)],flat,4,512)
    assert derivative<0
    h=0.0002
    plus=portfolio_pv(streams,[(2,500)],flat,4,512,h)["total"]
    minus=portfolio_pv(streams,[(2,500)],flat,4,512,-h)["total"]
    close(derivative,(plus-minus)/(2*h),rel_tol=1e-7)
    rejects(ValueError,analytic_pv,streams[0],affine,4)
    rejects(ValueError,numerical_pv,streams[0],flat,-1)
    rejects(ValueError,numerical_pv,streams[0],flat,4,3)
    rejects(ValueError,discrete_pv,[(-1,100)],flat)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    report=assessment()
    assert report["flat_absolute_reconciliation"]<1e-6
    assert report["runtime_certified"] is False
    print("PASS: Section 10.9 independent checks")

if __name__=="__main__":
    run()
