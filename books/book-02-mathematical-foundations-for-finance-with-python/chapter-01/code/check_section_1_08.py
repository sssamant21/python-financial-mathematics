"""Truth-table, schema, finite-domain, and exact sign reference checks."""
from fractions import Fraction as Q
from itertools import product
import json,math
from section_1_08 import implies,supported_finite,review_checks,growth_inputs_report
counts={}
def count(category):counts[category]=counts.get(category,0)+1
for p,q in product([False,True],repeat=2):
    assert implies(p,q)==((p,q)!=(True,False))
    assert implies(p,q)==implies(not q,not p)
    assert (not(p and q))==((not p) or (not q))
    assert (not(p or q))==((not p) and (not q))
    count('boolean_rows')
for bits in product([False,True],repeat=3):
    names=('a','b','c');r=review_checks(dict(zip(names,bits)),required=names)
    assert r['passed']==(bits==(True,True,True))
    assert r['failed']==tuple(n for n,b in zip(names,bits) if not b)
    count('checklist_rows')
for principal,rate,periods in product([-1,0,1000,None,True,float('nan'),float('inf'),'100'],[-2,-1,-.5,0,.04,None,True,float('nan'),float('inf')],[-1,0,3,3.0,True,None]):
    def finite(x):return type(x) in (int,float) and x==x and abs(x)!=float('inf')
    expected=(finite(principal) and principal>=0,finite(rate) and rate>-1,type(periods) is int and periods>=0)
    r=growth_inputs_report(principal=principal,period_rate=rate,periods=periods)
    assert tuple(r['conditions'].values())==expected
    assert r['passed']==all(expected)
    count('input_cases')
for p,r in product([Q(-100),Q(-1),Q(0),Q(1),Q(100)],repeat=2):
    interest=p*r
    assert implies(p>0 and r>0,interest>0)
    if p>0:assert (interest>0)==(r>0)
    count('exact_sign_cases')
assert Q(-100)*Q('-0.1')>0
assert all([]) and not any([])
assert (not(float('nan')>=0)) and not(float('nan')<0)
assert ('False' and 7)==7 and ('' or 'fallback')=='fallback'
assert not supported_finite(10**10000)
assert supported_finite(0) and supported_finite(-1.5)
assert not supported_finite(False) and not supported_finite(None)
assert not all(x>0 for x in [1,0,3]) and any(x<=0 for x in [1,0,3])
invalid=[(lambda:implies(1,True),TypeError),(lambda:implies(True,'False'),TypeError),
(lambda:review_checks({},required=()),ValueError),
(lambda:review_checks({},required=('a',)),ValueError),
(lambda:review_checks({'a':True,'b':True},required=('a',)),ValueError),
(lambda:review_checks({'a':True},required=('a','a')),ValueError),
(lambda:review_checks({'a':True},required='a'),ValueError),
(lambda:review_checks({'':True},required=('',)),ValueError),
(lambda:review_checks({1:True},required=(1,)),ValueError),
(lambda:review_checks([],required=('a',)),TypeError)]
for value in [None,1,'False',[],0.0]:
    invalid.append((lambda value=value:review_checks({'a':value},required=('a',)),TypeError))
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
