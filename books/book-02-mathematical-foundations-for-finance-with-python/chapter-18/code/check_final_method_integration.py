"""Actual final method/curve integration with independent Decimal references."""
import copy
from decimal import Decimal as D, localcontext
import json
import math
from unittest.mock import patch
import section_18_06 as curve
import section_18_09 as project
import section_18_10 as final


def close_float(value,reference,ulps=8):
    assert abs(D.from_float(value)-reference)<=ulps*D.from_float(math.ulp(float(reference)))


def validate_comparison(comparison):
    assert comparison['initial_bracket']==(0.0,0.2)
    assert comparison['absolute_width_tolerance']==1e-12
    b=comparison['bisection'];n=comparison['safeguarded_newton']
    with localcontext() as ctx:
        ctx.prec=100;root=(D(10)/9).sqrt()-1
        for result in (b,n):
            assert result['status'] in ('converged','exact_root')
            lo,hi=result['bracket'];width=hi-lo
            assert 0<=width<=1e-12
            assert abs(D.from_float(result['root'])-root)<=D.from_float(width)/2+D('2e-15')
        assert comparison['bisection_width']==b['bracket'][1]-b['bracket'][0]
        residual=D(1000)/(1+D.from_float(b['root']))**2-900
        assert abs(D.from_float(comparison['bisection_residual'])-residual)<=8*D.from_float(math.ulp(900.0))
        residual=D(1000)/(1+D.from_float(n['root']))**2-900
        assert abs(D.from_float(n['residual'])-residual)<=8*D.from_float(math.ulp(900.0))
    assert n['tolerances']=={'atol':1e-12,'rtol':0.0}
    expected_calls=b['iterations']+(2 if b['status']=='exact_root' else 3)
    assert comparison['bisection_function_evaluations']==expected_calls
    assert comparison['bisection_residual_evaluations']==1


def validate_report(report):
    comparison=report['solver_comparison'];validate_comparison(comparison)
    assert report['yield_solution']==comparison['bisection']
    actual=report['interpolation_comparison']
    with localcontext() as ctx:
        ctx.prec=100
        r1,r3=D.from_float(0.04),D.from_float(0.05)
        midpoint=float((r1+r3)/2)
        d1=1/(1+r1);d3=1/(1+r3)**3
        expected={'rate_midpoint':D.from_float(midpoint),
                  'discount_from_rate':1/(1+D.from_float(midpoint))**2,
                  'discount_linear':(d1+d3)/2,'discount_log_linear':(d1*d3).sqrt()}
        for key,reference in expected.items():close_float(actual[key],reference)
        for value,reference in zip(actual['discount_endpoints'],(d1,d3)):close_float(value,reference)
    assert report['rate_interpolation']==actual['rate_midpoint']
    assert report['discount_interpolation']==actual['discount_linear']
    assert report['discount_log_interpolation']==actual['discount_log_linear']
    assert report['discount_from_rate_interpolation']==actual['discount_from_rate']
    assert abs(actual['discount_log_linear']-actual['discount_linear'])>1e-6
    assert report['runtime_certified'] is False and report['independent_review_completed'] is False


def check():
    validate_report(final.assessment())
    with patch.object(project,'solve',wraps=project.solve) as solve, \
         patch.object(curve,'financial_comparison',wraps=curve.financial_comparison) as interpolate:
        report=final.assessment();validate_report(report)
        solve.assert_called_once_with(project.zero_coupon,project.zero_coupon_derivative,0.0,0.2,
                                      atol=1e-12,rtol=0.0,max_iter=200)
        interpolate.assert_called_once_with()
    with patch.object(final,'zero_price',wraps=final.zero_price) as price, \
         patch.object(project,'zero_coupon',wraps=project.zero_coupon) as objective, \
         patch.object(project,'zero_coupon_derivative',wraps=project.zero_coupon_derivative) as derivative:
        observed=final.solver_comparison();validate_comparison(observed)
        assert price.call_count==observed['bisection_function_evaluations']+observed['bisection_residual_evaluations']
        assert objective.call_count==observed['safeguarded_newton']['function_evaluations']
        assert derivative.call_count==observed['safeguarded_newton']['derivative_evaluations']
    detected=[];real_solve=project.solve;real_curve=curve.financial_comparison
    for field in ('root','residual'):
        def bad_solve(*args,**kwargs):
            result=real_solve(*args,**kwargs);result[field]+=0.01;return result
        with patch.object(project,'solve',side_effect=bad_solve):
            try:validate_report(final.assessment())
            except AssertionError:detected.append('solve.'+field)
            else:raise AssertionError('wrong solve output not detected')
    for field in ('rate_midpoint','discount_from_rate','discount_log_linear'):
        def bad_curve():
            result=real_curve();result[field]+=0.01;return result
        with patch.object(curve,'financial_comparison',side_effect=bad_curve):
            try:validate_report(final.assessment())
            except AssertionError:detected.append('financial_comparison.'+field)
            else:raise AssertionError('wrong curve output not detected')
    assert len(detected)==5
    serialized=json.dumps(report,sort_keys=True,allow_nan=False)
    assert serialized==json.dumps(final.assessment(),sort_keys=True,allow_nan=False)
    assert serialized==json.dumps(json.loads(serialized),sort_keys=True,allow_nan=False)
    return {'integrated_report':report,'observed_solver_comparison':observed,
            'actual_method_helper_calls':2,'wrong_helper_outputs_detected':detected,
            'scope':'fixed zero-coupon/curve example; selected floating accuracy and counts, not speed or model certification'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
