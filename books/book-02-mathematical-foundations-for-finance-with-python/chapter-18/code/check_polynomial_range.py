"""Known-polynomial range/knot references independent of Lagrange products."""
from decimal import Decimal as D, localcontext
import json
import math
import section_18_06 as lab


def rejects(error,fn,*args):
    try:fn(*args)
    except error:return
    raise AssertionError('expected '+error.__name__)


def check():
    rows=[];tiny=math.nextafter(0.0,1.0)
    def evaluate(name,xs,ys,q,reference):
        actual=lab.lagrange(xs,ys,q)
        assert actual==float(reference),(name,q,actual,float(reference))
        assert math.isfinite(actual) and (actual==0)==(reference==0)
        rows.append({'family':name,'xs':xs,'ys':ys,'query':q,
                     'actual':actual,'decimal_reference':str(reference)})
    with localcontext() as ctx:
        ctx.prec=2500
        for scale in (1e308,1e-200):
            s=D.from_float(scale)
            for q in (-scale,-scale/2,0.0,scale/2,scale):
                evaluate('normalized_quadratic',(-scale,0.0,scale),(1.0,0.0,1.0),q,
                         (D.from_float(q)/s)**2)
        scale=1e308;s=D.from_float(scale)
        for q in (0.0,scale/4):
            evaluate('normalized_cubic',(-scale,-scale/2,scale/2,scale),(-1.0,-0.125,0.125,1.0),q,
                     (D.from_float(q)/s)**3)
        for q in (10.0,1e308):
            evaluate('constant_extrapolation',(0.0,1.0,2.0),(scale,scale,scale),q,s)
        evaluate('small_representable_value',(-scale,0.0,scale),(scale,0.0,scale),1.0,1/s)
        evaluate('subnormal_knot_scale',(0.0,tiny,2*tiny),(0.0,1.0,4.0),3*tiny,D(9))
        xs=(-2.0,-1.0,0.0,1.0,2.0);ys=tuple(x**4-2*x*x+3 for x in xs)
        for q in (-0.5,0.5):
            x=D.from_float(q);evaluate('quartic_control',xs,ys,q,x**4-2*x*x+3)
        evaluate('large_coefficient_cancellation',(-1.0,0.0,1.0),(scale,-scale,scale),0.5,-s/2)
    rejects(ValueError,lab.lagrange,(-1e308,0.0,1e308),(1.0,0.0,1.0),1.0)
    rejects(ValueError,lab.lagrange,(-1.0,0.0,1.0),(1e308,0.0,1e308),2.0)
    invalid=(((0.0,0.0),(1.0,2.0),0.0,ValueError),
             ((1.0,0.0),(1.0,2.0),0.0,ValueError),
             ((0.0,1.0),(1.0,math.nan),0.0,ValueError),
             ((0.0,1.0),(1.0,2.0),True,TypeError))
    for xs,ys,q,error in invalid:rejects(error,lab.lagrange,xs,ys,q)
    serialized=json.dumps(rows,allow_nan=False,sort_keys=True)
    assert serialized==json.dumps(json.loads(serialized),allow_nan=False,sort_keys=True)
    return {'known_polynomial_references':rows,'final_range_rejections':2,'invalid_inputs':len(invalid),
            'scope':'selected represented-input polynomials; exact evaluation does not cure data conditioning'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
