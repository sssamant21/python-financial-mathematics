"""Independent final-report sensitivity/PV references and helper integration."""
from decimal import Decimal as D, localcontext
import json
import math
from unittest.mock import patch
from contextlib import ExitStack
import section_18_07 as lab
import section_18_10 as final


def near(value,reference,ulps=16):
    assert abs(D.from_float(value)-reference)<=ulps*D.from_float(math.ulp(float(reference)))


def validate(report):
    sensitivity=report['sensitivity_study'];pv=report['continuous_pv_study']
    assert sensitivity['rate']==0.05 and sensitivity['face']==1000 and sensitivity['years']==2
    assert [row['step'] for row in sensitivity['rows']]==[2e-4,1e-4,5e-5]
    assert sensitivity['step_selection']=='diagnostic only; no optimal step selected'
    with localcontext() as ctx:
        ctx.prec=100;r=D.from_float(0.05);price=D(1000)/(1+r)**2
        d1=-D(2000)/(1+r)**3;d2=D(6000)/(1+r)**4
        near(sensitivity['price'],price)
        near(sensitivity['analytic_first_derivative'],d1)
        near(sensitivity['analytic_second_derivative'],d2)
        near(sensitivity['analytic_duration'],2/(1+r))
        near(sensitivity['analytic_convexity'],6/(1+r)**2)
        for row in sensitivity['rows']:
            h=row['step'];dh=D.from_float(h)
            p0=price;pp=D(1000)/(1+D.from_float(0.05+h))**2;pm=D(1000)/(1+D.from_float(0.05-h))**2
            refs=((pp-p0)/dh,(pp-pm)/(2*dh),(pp-2*p0+pm)/dh**2)
            keys=('forward_derivative','central_derivative','second_derivative')
            budgets=[32*D.from_float(math.ulp(1000.0))/dh**order for order in (1,1,2)]
            for key,ref,budget in zip(keys,refs,budgets):
                assert abs(D.from_float(row[key])-ref)<=budget
            near(row['numerical_duration'],-D.from_float(row['central_derivative'])/D.from_float(sensitivity['price']))
            near(row['numerical_convexity'],D.from_float(row['second_derivative'])/D.from_float(sensitivity['price']))
            for field,key,reference in (('forward_error','forward_derivative','analytic_first_derivative'),
                                        ('central_error','central_derivative','analytic_first_derivative'),
                                        ('second_error','second_derivative','analytic_second_derivative')):
                assert row[field]==row[key]-sensitivity[reference]
        assert report['duration_estimate']==sensitivity['rows'][1]['numerical_duration']
        assert pv['cashflow_rate']==100 and pv['discount_rate']==0.03 and pv['years']==5
        assert [row['panels'] for row in pv['rows']]==[20,40,80]
        rho=D.from_float(0.03);years=D(5);cash=D(100)
        exact=cash*(1-(-rho*years).exp())/rho
        near(pv['analytic_reference'],exact)
        def exact_trapezoid(n):
            h=years/n;q=(-rho*h).exp()
            # Independent closed geometric sum, not the callback-weight loop.
            return cash*h*((1+q**n)/2+q*(1-q**(n-1))/(1-q))
        expected=[]
        for row in pv['rows']:
            n=row['panels'];t=exact_trapezoid(n);s=(4*t-exact_trapezoid(n//2))/3
            near(row['trapezoid'],t);near(row['simpson'],s)
            assert row['step']==5/n
            assert row['trapezoid_error']==row['trapezoid']-pv['analytic_reference']
            assert row['simpson_error']==row['simpson']-pv['analytic_reference']
            assert row['trapezoid_error']>row['simpson_error']>0
            expected.append((t-exact,s-exact))
        assert pv['refinement_estimate_is_bound'] is False
        for i,row in enumerate(pv['refinement']):
            coarse,fine=pv['rows'][i:i+2]
            assert (row['coarse_panels'],row['fine_panels'])==(coarse['panels'],fine['panels'])
            for j,method in enumerate(('trapezoid','simpson')):
                ratio=abs(coarse[method+'_error']/fine[method+'_error'])
                assert row[method+'_error_ratio']==ratio
                # A selected rounding allowance encloses the ideal ratio;
                # it is not a universal math-library error certificate.
                budget=32*D.from_float(math.ulp(float(exact)))
                ec,ef=expected[i][j],expected[i+1][j]
                assert ef>budget
                assert (ec-budget)/(ef+budget)<=D.from_float(ratio)<=(ec+budget)/(ef-budget)
        assert report['simpson_continuous_pv']==pv['rows'][1]['simpson']
        assert report['continuous_pv_reference']==pv['analytic_reference']


def check():
    report=final.assessment();validate(report)
    names=('zero_price','forward_difference','central_difference','second_difference',
           'trapezoid','simpson','continuous_cashflow_pv')
    with ExitStack() as stack:
        spies={name:stack.enter_context(patch.object(lab,name,wraps=getattr(lab,name))) for name in names}
        observed=final.assessment();validate(observed)
        expected={'zero_price':22,'forward_difference':3,'central_difference':3,'second_difference':3,
                  'trapezoid':3,'simpson':3,'continuous_cashflow_pv':1}
        assert {name:spy.call_count for name,spy in spies.items()}==expected
    detected=[]
    for name in names:
        original=getattr(lab,name)
        def wrong(*args,**kwargs):return original(*args,**kwargs)+1.0
        with patch.object(lab,name,side_effect=wrong):
            try:validate(final.assessment())
            except AssertionError:detected.append(name)
            else:raise AssertionError('undetected wrong helper '+name)
    assert len(detected)==7
    serialized=json.dumps(report,sort_keys=True,allow_nan=False)
    assert serialized==json.dumps(final.assessment(),sort_keys=True,allow_nan=False)
    assert serialized==json.dumps(json.loads(serialized),sort_keys=True,allow_nan=False)
    return {'sensitivity_study':report['sensitivity_study'],'continuous_pv_study':report['continuous_pv_study'],
            'observed_helper_calls':expected,'wrong_helpers_detected':detected,
            'scope':'fixed annual-effective bond and continuously discounted stream; selected rounding allowances only'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
