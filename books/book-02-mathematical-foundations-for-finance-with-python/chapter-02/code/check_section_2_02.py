"""Classification, original equations, inverse consistency, and domain checks."""
from fractions import Fraction as Q
from itertools import product
import json
from section_2_02 import rational,solve_linear,principal_for_target,rate_for_target
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
for a,b,t in product(range(-2,3),repeat=3):
    result=solve_linear(coefficient=a,constant=b,target=t)
    expected='unique' if a!=0 else ('all' if b==t else 'none')
    assert result['kind']==expected
    if a:
        x=result['solution'];assert a*x+b==t
        assert a*(x+1)+b!=t
    else:
        assert result['solution'] is None
        assert all((a*x+b==t)==(expected=='all') for x in [-10,0,10])
    count('linear_classification_cases')
for A,r,F,k in product([Q(0),Q(10),Q(100)],[Q(-1,2),Q(0),Q(1,10)],[Q(0),Q(3)],[Q(0),Q(1),Q(2)]):
    result=principal_for_target(target_value=A,period_rate=r,fixed_fee=F,fee_rate=k)
    coefficient=1+r-k
    if coefficient==0:
        expected='all' if A+F==0 else 'none'
        assert result['kind']==expected
        assert result['admissible']==(expected=='all')
        assert result['residual'] is None
    else:
        assert result['kind']=='unique'
        p=result['solution']
        assert p+p*r-F-k*p==A
        assert result['residual']==0
        assert result['admissible']==(p>0)
    for p in [Q(-2),Q(0),Q(1),Q(10)]:
        direct=(p>0 and p*(1+r)-F-k*p==A)
        classified=p>0 and result['admissible'] and (result['kind']=='all' or p==result['solution'])
        assert direct==classified
    count('principal_domain_cases')
for p,r,F,k in product([Q(1),Q(100),Q(1000)],[Q(-1,2),Q(0),Q(3,50)],[Q(0),Q(5)],[Q(0),Q(1,100),Q(1,2)]):
    target=p+p*r-F-k*p
    if target<0:continue
    rate=rate_for_target(principal=p,target_value=target,fixed_fee=F,fee_rate=k)
    assert rate['solution']==r and rate['admissible'] and rate['residual']==0
    recovered=principal_for_target(target_value=target,period_rate=r,fixed_fee=F,fee_rate=k)
    if recovered['kind']=='unique':assert recovered['solution']==p
    else:assert recovered['kind']=='all' and recovered['admissible']
    count('forward_inverse_cases')
# An exact small nonzero coefficient remains unique rather than being rounded to zero.
tiny=solve_linear(coefficient='0.000001',constant=0,target=1)
assert tiny=={'kind':'unique','solution':Q(1000000)}
negative=principal_for_target(target_value=100,period_rate=0,fixed_fee=0,fee_rate=2)
assert negative['solution']==-100 and not negative['admissible'] and negative['residual']==0
zero=principal_for_target(target_value=0,period_rate=0,fixed_fee=0,fee_rate=0)
assert zero['solution']==0 and not zero['admissible']
rate=rate_for_target(principal=100,target_value=0,fixed_fee=0,fee_rate=0)
assert rate['solution']==-1 and not rate['admissible'] and rate['residual']==0
# Exercise results checked against the original equations.
assert 4*(8-3)+5==2*8+9==25
assert solve_linear(coefficient=-3,constant=6,target=0)['solution']==2
exercise=principal_for_target(target_value=828,period_rate='.05',fixed_fee=4,fee_rate='.01')
assert exercise['solution']==800 and exercise['admissible']
r=rate_for_target(principal=800,target_value=828,fixed_fee=4,fee_rate='.01')
assert r['solution']==Q(1,20) and 800*(1+r['solution']-Q('.01'))-828==4
assert Q(30)/(2000*Q(1,4))==Q(3,50)
assert solve_linear(coefficient=0,constant=0,target=0)['kind']=='all'
assert solve_linear(coefficient=0,constant=0,target=30)['kind']=='none'
policy=dict(target_value=1045,period_rate='.06',fixed_fee=5,fee_rate='.01')
invalid=[(lambda:rational(.05),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),
(lambda:principal_for_target(**(policy|{'target_value':-1})),ValueError),
(lambda:principal_for_target(**(policy|{'period_rate':-1})),ValueError),
(lambda:principal_for_target(**(policy|{'fixed_fee':-1})),ValueError),
(lambda:principal_for_target(**(policy|{'fee_rate':-1})),ValueError),
(lambda:rate_for_target(principal=0,target_value=1,fixed_fee=0,fee_rate=0),ValueError),
(lambda:rate_for_target(principal=-1,target_value=1,fixed_fee=0,fee_rate=0),ValueError),
(lambda:rate_for_target(principal=1,target_value=-1,fixed_fee=0,fee_rate=0),ValueError),
(lambda:rate_for_target(principal=1,target_value=1,fixed_fee=-1,fee_rate=0),ValueError),
(lambda:rate_for_target(principal=1,target_value=1,fixed_fee=0,fee_rate=-1),ValueError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
