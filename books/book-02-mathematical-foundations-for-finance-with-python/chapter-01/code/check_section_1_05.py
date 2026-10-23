"""Indexing, exact benchmarks, alignment, preservation, and range checks."""
from fractions import Fraction
from itertools import permutations
from math import fsum,isclose,inf
import json
from section_1_05 import dated_payments,periodic_payments,present_value

names=[]
def check(name,condition):
    assert condition,name
    names.append(name)
def close(a,b):
    return isclose(a,b,rel_tol=1e-12,abs_tol=1e-10)
def pv(records,rate):
    return present_value(periods=[t for t,c in records],amounts=[c for t,c in records],period_rate=rate)

check('one-based payment times',periodic_payments([100,120])==((1,100.),(2,120.)))
check('zero-based payment times',periodic_payments([100,120],first_period=0)==((0,100.),(1,120.)))
check('empty dated records',dated_payments(periods=[],amounts=[])==())
check('empty periodic records',periodic_payments([])==())
check('empty schedule value',present_value(periods=[],amounts=[],period_rate=.05)==0)
check('end-period exact rational benchmark',close(pv([(1,100),(2,120)],.1),float(Fraction(23000,121))))
check('earlier exact rational benchmark',close(pv([(0,100),(1,120)],.1),float(Fraction(2300,11))))
check('time-zero payment',pv([(0,-100)],.1)==-100)
check('added time-zero contribution',close(pv([(0,50),(1,100),(2,120)],.1)-pv([(1,100),(2,120)],.1),50))
check('duplicate dates retained',dated_payments(periods=[1,1,2],amounts=[100,-5,120])==((1,100.),(1,-5.),(2,120.)))
check('identical records retained',dated_payments(periods=[1,1],amounts=[100,100])==((1,100.),(1,100.)))
check('duplicate-date aggregation',close(pv([(1,100),(1,-5),(2,120)],.1),pv([(1,95),(2,120)],.1)))
check('irregular complete schedule',close(pv([(0,-100),(1,5),(3,120)],0),25))
check('finite input generators',dated_payments(periods=(x for x in [1,3]),amounts=(x for x in [10,20]))==((1,10.),(3,20.)))
check('positional re-pairing changes schedule',not close(pv([(1,100),(2,120)],.1),pv([(2,100),(1,120)],.1)))
check('inclusive summation count',tuple(range(5))==(0,1,2,3,4))
check('sequence relabeling',tuple(enumerate([20,30,40],start=1))==((1,20),(2,30),(3,40)))
check('record label differs from time',close(pv([(5,100)],.1),100/1.1**5))
check('practice same-date aggregation',close(pv([(0,-100),(1,20),(1,-5),(2,110)],.05),pv([(0,-100),(1,15),(2,110)],.05)))
check('multi-index period-one total',2*10+1*20==40)
check('multi-index period-two total',2*110+1*220==440)
check('multi-index zero-rate total',pv([(1,40),(2,440)],0)==480)
check('wrong positional pairing example',sum(h*p for h,p in zip([2,3],[20,10]))==70)
holdings={'A':2,'B':3}
for items in permutations([('A',10),('B',20)]):
    prices=dict(items)
    assert holdings.keys()==prices.keys()
    assert fsum(holdings[k]*prices[k] for k in holdings)==80
check('missing asset label detected',holdings.keys()!= {'A':10}.keys())
check('negative rate supported',close(pv([(1,100)],-.2),125))
check('zero payment extreme horizon',pv([(2000,0)],1.)==0)
# Schedule-level scaling and timing shifts on moderate independent grids.
scenario_cases=0
for count in range(6):
    amounts=[25*(i+1)*(-1 if i%2 else 1) for i in range(count)]
    for first in [0,1,4]:
        records=periodic_payments(amounts,first_period=first)
        assert tuple(t for t,c in records)==tuple(range(first,first+count))
        assert tuple(c for t,c in records)==tuple(float(c) for c in amounts)
        for rate in [-.02,0.,.05]:
            baseline=pv(records,rate)
            assert close(pv([(t,2*c) for t,c in records],rate),2*baseline)
            assert close(pv([(t+1,c) for t,c in records],rate),baseline/(1+rate))
            exact=sum((Fraction(c)/(1+Fraction(str(rate)))**t for t,c in records),Fraction(0))
            assert close(baseline,float(exact))
            scenario_cases+=1
# Reordering whole records preserves the paired schedule, including repeated dates.
records=[(0,-100),(1,20),(1,-5),(2,110)]
permutation_cases=0
for order in permutations(records):
    assert close(pv(order,.05),pv(records,.05))
    permutation_cases+=1
invalid=[(lambda:dated_payments(periods=[1,2],amounts=[10]),ValueError),
 (lambda:dated_payments(periods=[1],amounts=[10,20]),ValueError),
 (lambda:dated_payments(periods=[True],amounts=[10]),TypeError),
 (lambda:dated_payments(periods=[1.0],amounts=[10]),TypeError),
 (lambda:dated_payments(periods=[-1],amounts=[10]),ValueError),
 (lambda:dated_payments(periods=[1],amounts=[True]),TypeError),
 (lambda:dated_payments(periods=[1],amounts=['10']),TypeError),
 (lambda:dated_payments(periods=[1],amounts=[float('nan')]),ValueError),
 (lambda:dated_payments(periods=[1],amounts=[inf]),ValueError),
 (lambda:dated_payments(periods=[1],amounts=[10**1000]),ValueError),
 (lambda:periodic_payments([],first_period=-1),ValueError),
 (lambda:periodic_payments([],first_period=True),TypeError),
 (lambda:periodic_payments([],first_period=1.5),TypeError),
 (lambda:present_value(periods=[],amounts=[],period_rate=-1),ValueError),
 (lambda:present_value(periods=[],amounts=[],period_rate=float('nan')),ValueError),
 (lambda:present_value(periods=[],amounts=[],period_rate=True),TypeError),
 (lambda:pv([(2000,1)],1.),ArithmeticError),
 (lambda:pv([(2000,1)],-.5),ArithmeticError),
 (lambda:pv([(1,1e-308)],1e308),ArithmeticError),
 (lambda:pv([(0,1e308),(0,1e308)],0.),ArithmeticError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
# Strict zip detects length mismatch upon consumption, not upon construction.
iterator=zip([1,2],[10],strict=True)
check('strict pairing first record',next(iterator)==(1,10))
try:next(iterator)
except ValueError:pass
else:raise AssertionError('strict mismatch was not raised')
summary={'reference_checks':len(names),'scenario_cases':scenario_cases,
         'record_permutations':permutation_cases,'asset_orderings':2,
         'invalid_input_and_range_cases':len(invalid),'strict_iteration_failure':'PASS'}
print('PASS: '+json.dumps(summary,sort_keys=True))
