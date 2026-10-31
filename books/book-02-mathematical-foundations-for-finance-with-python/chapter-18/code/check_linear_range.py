"""Complete affine value, finite-result and extrapolation contract checks."""
from decimal import Decimal as D, localcontext
import json
import math
from unittest.mock import patch
import section_18_06 as lab
import section_18_10 as final


def reference(x0,y0,x1,y1,q):
    with localcontext() as ctx:
        ctx.prec=2500
        a,u,b,v,x=map(D.from_float,map(float,(x0,y0,x1,y1,q)))
        return ((b-x)*u+(x-a)*v)/(b-a)


def rejects(error,fn,*args,**kwargs):
    try:fn(*args,**kwargs)
    except error:return
    raise AssertionError('expected '+error.__name__)


def check():
    tiny=math.nextafter(0.0,1.0)
    cases=((-1e308,-1.,1e308,1.,0.),(0.,-1e308,1.,1e308,0.5),
           (0.,0.,1e308,1e308,1e-308),(0.,0.,1e308,1e308,tiny),
           (0.,0.,tiny,tiny,tiny),(-1e308,tiny,1e308,tiny,1e308),
           (0.,0.,1.,1.,2.),(0.,0.,1.,1.,-1.),(1.,2.,3.,6.,2.),
           (0.,-tiny,1.,tiny,0.5),(0.,0.,1.,tiny,1.),(0.,1.,1.,1.,1e308))
    records=[]
    for args in cases:
        expected=reference(*args);x0,y0,x1,y1,q=args
        actual=lab.piecewise_linear((x0,x1),(y0,y1),q,True)
        final_value=final.interpolate(*args)
        assert actual==final_value==float(expected),(args,actual,final_value,float(expected))
        assert math.isfinite(actual) and (actual==0)==(expected==0)
        records.append({'inputs':args,'piecewise':actual,'final':final_value,'decimal_reference':str(expected)})
    for q,expected in ((-1.,3.),(0.,1.),(1.5,4.),(-3.,7.),(4.,9.)):
        assert lab.piecewise_linear((-2.,0.,3.),(5.,1.,7.),q,True)==expected
    for q in (-1.,2.):
        rejects(ValueError,lab.piecewise_linear,(0.,1.),(0.,1.),q)
        assert lab.piecewise_linear((0.,1.),(0.,1.),q,True)==q
        assert final.interpolate(0.,0.,1.,1.,q)==q
    ranges=((0.,0.,1.,tiny,0.25),(0.,0.,1.,1e308,2.))
    for args in ranges:
        rejects(ValueError,final.interpolate,*args)
        x0,y0,x1,y1,q=args
        rejects(ValueError,lab.piecewise_linear,(x0,x1),(y0,y1),q,True)
    for args,error in (((0.,0.,0.,1.,0.),ValueError),((1.,0.,0.,1.,0.),ValueError),
                       ((0.,math.nan,1.,1.,0.5),ValueError),((0.,0.,1.,1.,True),TypeError)):
        rejects(error,final.interpolate,*args)
    with patch.object(lab,'linear_segment',wraps=lab.linear_segment) as shared:
        assert final.interpolate(0.,0.,1.,1.,0.5)==0.5
        shared.assert_called_once_with(0.,0.,1.,1.,0.5)
    with patch.object(lab,'linear_segment',return_value=0.0):
        assert final.interpolate(0.,0.,1e308,1e308,1e-308)!=float(reference(0.,0.,1e308,1e308,1e-308))
    return {'two_entrypoint_reference_sets':records,'multisegment_references':5,
            'explicit_extrapolation_cases':2,'two_entrypoint_final_range_rejections':4,
            'invalid_final_inputs':4,'observed_shared_call':1,'false_zero_variant_detected':True,
            'scope':'represented-input affine interpolation/extrapolation; no financial-curve suitability guarantee'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
