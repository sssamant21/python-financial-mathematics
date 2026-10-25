"""Independent checks for Section 10.9 valuation engine."""
import math
from section_10_09 import (Stream,Curve,finite,analytic_pv,numerical_pv,
                           discrete_pv,portfolio_pv,parallel_shift_derivative,assessment)

def close(a,b,rel_tol=1e-8,abs_tol=1e-7):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
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
