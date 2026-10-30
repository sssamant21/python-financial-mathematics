"""Selected level-set denominator and maturity-domain boundaries."""
from fractions import Fraction as F
import math
from section_15_08 import (portfolio_gradient, iso_variance_slope,
                           exact_unchanged_value_time, future_value)

def rejected(fn,*args):
    try:
        fn(*args)
    except ValueError:
        return
    raise AssertionError("expected ValueError")

def run():
    # Decimal coefficients describe gy=.02*w1+.18*w2: (9,-1) has gy=0.
    assert F(2,100)*9-F(18,100)==0
    gx,gy=portfolio_gradient(9,-1)
    assert math.isclose(gx,0.7,abs_tol=1e-15) and gy==0
    rejected(iso_variance_slope,9,-1)
    rejected(iso_variance_slope,0,0)
    # Adjacent represented weights lie on opposite sides of the vertical tangent.
    for weight in (math.nextafter(-1,0),math.nextafter(-1,-math.inf)):
        gx,gy=portfolio_gradient(9,weight)
        slope=iso_variance_slope(9,weight)
        assert gy!=0 and math.isfinite(slope)
        assert slope*gy<0
    for r,t,dr in ((0.125,2,-0.0625),(-0.125,2,0.0625),
                   (0.125,2,0.125),(-0.125,2,-0.125)):
        actual=exact_unchanged_value_time(r,t,dr)
        expected=float(F(r)*F(t)/F(r+dr))
        assert actual==expected
        assert math.isclose(future_value(2,r+dr,actual),future_value(2,r,t),rel_tol=2e-15)
    for r,dr in ((0.125,-0.125),(-0.125,0.125)):
        rejected(exact_unchanged_value_time,r,2,dr)
    for r,dr in ((0.125,-0.25),(-0.125,0.25)):
        rejected(exact_unchanged_value_time,r,2,dr)
        # At t=0 the sign crossing still preserves the zero-time level.
        assert exact_unchanged_value_time(r,0,dr)==0
    rejected(exact_unchanged_value_time,0.125,-1,0.01)
    print("PASS: selected zero/adjacent iso-variance and signed-rate maturity-domain cases")

if __name__=="__main__":
    run()
