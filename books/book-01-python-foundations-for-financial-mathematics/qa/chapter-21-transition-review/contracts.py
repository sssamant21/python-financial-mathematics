"""Capture exact reference-check expression outputs; independently derived rational targets."""
import importlib.util,sys,math,unittest,json
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
spec=importlib.util.spec_from_file_location('transition_source',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
expected={'test_present_value':F(100),'test_future_value':F(121),'test_npv':F(0),'test_price_return':F(1,10),'test_linked_return':F(-1,100),'test_portfolio_return':F(1,25),'test_cross_section_mean':F(1,40),'test_sample_variance':F(9,800),'test_bond_par':F(100),'test_simulation_model_expectation':F(100),'test_decimal_rounding_example':Decimal('0.02'),'test_pv_rate_sensitivity_sign':-F(110)*F(100,121)}
records=[];old=math.isclose;equal=m.TransitionChecks.assertEqual;less=m.TransitionChecks.assertLess
current=None
# Observe source expression arguments, not separately reimplement their float calculations.
def observe(actual,target=None,**kw):
    ref=expected[current];tol=1e-10 if current in ('test_present_value','test_future_value','test_npv','test_bond_par') else 1e-12
    ok=old(float(actual),float(ref),rel_tol=0,abs_tol=tol)
    records.append(dict(method=current,actual=str(actual),actual_hex=actual.hex() if isinstance(actual,float) else None,independent_expected=str(ref),absolute_tolerance=tol,passed=ok));assert ok,current

def close(a,b,**kw):observe(a);return old(a,b,**kw)
def eq(self,a,b,*args,**kw):observe(a);return equal(self,a,b,*args,**kw)
def lt(self,a,b,*args,**kw):observe(a);return less(self,a,b,*args,**kw)
math.isclose=close;m.TransitionChecks.assertEqual=eq;m.TransitionChecks.assertLess=lt
try:
    for current in expected:
        case=m.TransitionChecks(current);case.debug()
finally:
    math.isclose=old;m.TransitionChecks.assertEqual=equal;m.TransitionChecks.assertLess=less
assert len(records)==12 and all(x['passed'] for x in records)
result=dict(records=records,passed=12,limits='Observes standalone exact manuscript test expressions, not toolkit imports or model validation. Rational/decimal targets and analytical derivative independent; no newly authored unittest method claimed.')
Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n');print('PASS 12 observed expression/reference comparisons')
