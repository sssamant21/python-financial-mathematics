"""Finite-difference noise arithmetic and distinct accuracy diagnostics."""
import math,json
from fractions import Fraction
import section_8_08 as source

def observations():
    rows=[];accuracy=[];eta=2.**-40
    def check(name,actual,expected,truth):
        ok=math.isfinite(actual) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0)
        if expected==0:ok=actual==0
        rows.append(dict(name=name,actual=actual,expected=expected,passed=ok))
        accuracy.append(dict(name=name,actual=actual,analytic_derivative=truth,absolute_error=abs(actual-truth),nominal_absolute_tolerance=1e-8,within_nominal_tolerance=abs(actual-truth)<=1e-8,scope='Accuracy diagnostic,not source-arithmetic acceptance predicate'))
    for k in (5,10,20,30):
        h=2.**-k
        sign_noise=lambda x:x*x+(eta if x>0 else -eta if x<0 else 0.)
        burst_noise=lambda x:x*x+(eta if x!=0 else -eta)
        constant_noise=lambda x:x*x+eta
        # All samples and these power-of-two closed forms are exact binary values.
        check(f'bounded sign noise first h=2^-{k}',source.centered_difference(sign_noise,0.,h),eta/h,0.)
        check(f'center burst noise second h=2^-{k}',source.second_difference(burst_noise,0.,h),2.+4*eta/(h*h),2.)
        check(f'constant noise first h=2^-{k}',source.centered_difference(constant_noise,0.,h),0.,0.)
        check(f'constant noise second h=2^-{k}',source.second_difference(constant_noise,0.,h),2.,2.)
    q=2.**-10
    quantized=lambda x:round(x/q)*q
    for h,expected in [(q/4,0.),(q/2,0.),(q,1.),(1.5*q,float(Fraction(4,3))),(2*q,1.)]:
        check('quantized linear first h='+repr(h),source.centered_difference(quantized,0.,h),expected,1.)
    suggested=source.suggested_step(0.,1)
    check('suggested first step quantized linear',source.centered_difference(quantized,0.,suggested),0.,1.)
    suggested2=source.suggested_step(0.,2)
    quantized_square=lambda x:round((x*x)/q)*q
    check('suggested second step quantized square',source.second_difference(quantized_square,0.,suggested2),0.,2.)
    # Each chosen rounded callback stays within its documented deterministic bound.
    controls=[('sign-noise amplitude',abs(sign_noise(2.**-30)-(2.**-30)**2)<=eta),('burst-noise amplitude',abs(burst_noise(0.))<=eta),('quantization bound',all(abs(quantized(x)-x)<=q/2 for x in [q/4,q/2,q,1.5*q,2*q])),('step root differs from noise budget',suggested<q/2 and suggested2* suggested2<q/2)]
    for name,ok in controls:rows.append(dict(name=name,actual=ok,expected=True,passed=ok))
    return rows,accuracy
if __name__=='__main__':
    rows,accuracy=observations();print(json.dumps(dict(predicates=rows,accuracy_diagnostics=accuracy),indent=2));assert all(x['passed'] for x in rows)
    print(len(rows),'arithmetic/contract predicates passed;',sum(not x['within_nominal_tolerance'] for x in accuracy),'accuracy diagnostics exceed nominal tolerance')
