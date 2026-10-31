"""Complete-stencil range references and pre-callback sample-point guards."""
from decimal import Decimal as D, localcontext
import json
import math
from unittest.mock import patch
import section_18_07 as lab
import section_18_10 as final


def rejects(exc,fn,*args):
    try:fn(*args)
    except exc:return
    raise AssertionError('expected '+exc.__name__)


def check():
    tiny=math.nextafter(0.0,1.0);big=1.7e308
    with localcontext() as ctx:
        ctx.prec=2500
        cases=(('large_2h',lab.central_difference,lambda t:t/1e308,0.0,1e308,1/D.from_float(1e308)),
               ('final_large_2h',final.central_derivative,lambda t:t/1e308,0.0,1e308,1/D.from_float(1e308)),
               ('forward_one_sided_domain',lab.forward_difference,lambda t:t/1e308,-1e308,1e308,1/D.from_float(1e308)),
               ('cancel_large_numerator_denominator',lab.central_difference,lambda t:t,0.0,big,D(1)),
               ('forward_large_numerator',lab.forward_difference,lambda t:big if t>0 else -big,-1.0,2.0,D.from_float(big)),
               ('second_large_square',lab.second_difference,abs,0.0,1e200,2/D.from_float(1e200)),
               ('second_large_constant',lab.second_difference,lambda t:1e308,0.0,1.0,D(0)),
               ('second_tiny_square_constant',lab.second_difference,lambda t:1.0,0.0,2**-600,D(0)),
               ('second_representable_tiny_square',lab.second_difference,lambda t:t*t,0.0,2**-500,D(2)),
               ('forward_control',lab.forward_difference,lambda t:t*t,0.5,0.125,D('1.125')),
               ('central_control',lab.central_difference,lambda t:t*t,0.5,0.125,D(1)),
               ('second_control',lab.second_difference,lambda t:t*t,0.5,0.125,D(2)),
               ('final_control',final.central_derivative,lambda t:t*t,0.5,0.125,D(1)))
        results=[]
        for name,method,f,x,h,reference in cases:
            events=[]
            def callback(q):
                value=f(q);events.append((q,value));return value
            actual=method(callback,x,h)
            assert actual==float(reference),(name,actual,float(reference))
            assert math.isfinite(actual)
            results.append({'case':name,'x':x,'h':h,'actual':actual,
                            'decimal_reference':str(reference),'callback_samples':events})
    methods=(lab.forward_difference,lab.central_difference,lab.second_difference,final.central_derivative)
    guarded=0;bad_callbacks=0
    for method in methods:
        for x,h in ((1e308,1e308),(1.0,tiny)):
            calls=[]
            def should_not_run(q):calls.append(q);return 0.0
            rejects(ValueError,method,should_not_run,x,h)
            assert calls==[];guarded+=1
        for value,exc in ((math.nan,ValueError),(math.inf,ValueError),(True,TypeError)):
            rejects(exc,method,lambda q:value,0.0,1.0);bad_callbacks+=1
    underflow=lambda t:tiny if t>0 else -tiny
    for method in (lab.central_difference,lab.second_difference,final.central_derivative):
        calls=[]
        def invalid_minus(q):calls.append(q);return 0.0
        rejects(ValueError,method,invalid_minus,-1e308,1e308)
        assert calls==[];guarded+=1
    rejects(ValueError,lab.central_difference,underflow,0.0,1e308)
    rejects(ValueError,final.central_derivative,underflow,0.0,1e308)
    rejects(ValueError,lab.forward_difference,lambda t:1.0 if t>0 else 0.0,0.0,tiny)
    rejects(ValueError,lab.second_difference,abs,0.0,tiny)
    with patch.object(final,'_shared_central_difference',wraps=lab.central_difference) as shared:
        assert final.central_derivative(lambda t:t,0.0,1.0)==1.0
        shared.assert_called_once()
    return {'complete_stencil_references':results,'pre_callback_point_rejections':guarded,
            'nonfinite_bool_callback_rejections':bad_callbacks,'final_range_rejections':4,
            'observed_final_shared_call':1,
            'scope':'represented finite callback samples; not recovery of callback rounding or smoothness proof'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
