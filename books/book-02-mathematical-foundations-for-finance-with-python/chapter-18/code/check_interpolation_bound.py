"""Exact quadratic interpolation-error bounds and interval-halving references."""
from fractions import Fraction as F
import json
import section_18_06 as lab


def audit(interpolate):
    rows=[];queries=0;halvings=0
    for a in (F(2),F(-2),F(1,8),F(-1,8),F(0)):
        b,c=F(3,8),F(-1,2)
        def polynomial(x):return a*x*x+b*x+c
        for lo,hi in ((F(0),F(2)),(F(1),F(3)),(F(-2),F(2)),(F(1,2),F(3,4))):
            curvature=2*abs(a);width=hi-lo;bound=curvature*width*width/8
            xs=(float(lo),float(hi));ys=(float(polynomial(lo)),float(polynomial(hi)))
            actuals=[];errors=[]
            for k in range(5):
                q=lo+width*F(k,4)
                actual=interpolate(xs,ys,float(q))
                error=F(actual)-polynomial(q)
                # Independent expanded-quadratic identity L(q)-f(q).
                expected=a*(q-lo)*(hi-q)
                assert error==expected,(a,lo,hi,q,actual,str(expected))
                assert abs(error)<=bound
                if k==2:assert abs(error)==bound
                if k in (0,4):assert error==0
                if a:assert error*a>=0
                actuals.append(actual);errors.append(str(error));queries+=1
            if a:
                midpoint=(lo+hi)/2
                half_xs=(float(lo),float(midpoint))
                half_ys=(float(polynomial(lo)),float(polynomial(midpoint)))
                q=(lo+midpoint)/2
                half_error=F(interpolate(half_xs,half_ys,float(q)))-polynomial(q)
                full_error=F(actuals[2])-polynomial(midpoint)
                assert abs(full_error)==4*abs(half_error)
                halvings+=1
            rows.append({'coefficients':list(map(str,(a,b,c))),'interval':list(map(str,(lo,hi))),
                         'curvature_bound':str(curvature),'maximum_error_bound':str(bound),
                         'quarter_grid_values':actuals,'signed_errors':errors})
    return rows,queries,halvings


def check():
    rows,queries,halvings=audit(lab.piecewise_linear)
    # The interpolation bound is conditional on q lying inside the interval.
    extrapolated=lab.piecewise_linear((0.0,2.0),(-0.5,8.25),4.0,True)
    exact=F(2)*16+F(3,8)*4-F(1,2)
    extrapolation_error=F(extrapolated)-exact
    assert extrapolation_error==-16 and abs(extrapolation_error)>2
    wrong=(('left_endpoint',lambda xs,ys,q:ys[0]),
           ('midpoint_everywhere',lambda xs,ys,q:(ys[0]+ys[1])/2),
           ('double_slope',lambda xs,ys,q:ys[0]+2*(q-xs[0])/(xs[1]-xs[0])*(ys[1]-ys[0])))
    detected=[]
    for name,method in wrong:
        try:audit(method)
        except AssertionError:detected.append(name)
        else:raise AssertionError('undetected interpolation variant '+name)
    assert len(detected)==3
    return {'reference_sets':rows,'quarter_grid_queries':queries,
            'additional_half_width_queries':halvings,'factor_four_checks':halvings,
            'extrapolation_signed_error':str(extrapolation_error),
            'wrong_methods_detected':detected,
            'scope':'selected dyadic quadratics/affine data only; no general smoothness or conditioning certificate'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
