"""Independent recurrence, repeated multiplication, timing, and domain checks."""
from fractions import Fraction as Q
from itertools import product
import json
from section_1_12 import rational,periodic_rate,compound_balance,present_value
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
for p,r,n in product([Q(0),Q(1),Q(100)],[Q(-9,10),Q(-1,10),Q(0),Q(1,10),Q(1)],[0,1,2,5]):
    reference=p
    for _ in range(n):reference=reference+reference*r
    actual=compound_balance(principal=p,period_rate=r,periods=n)
    assert actual==reference
    # Discounting a terminal balance recovers the principal exactly.
    flows=[0]*n+[actual]
    assert present_value(cash_flows=flows,period_rate=r)['total']==p
    count('growth_cases')
for length in [1,2,3,4]:
    for flows in product([-2,0,3],repeat=length):
        for r in [Q(-1,2),Q(0),Q(1,10)]:
            # Backward recurrence uses nested division rather than powers/sum.
            reference=Q(flows[-1])
            for cash in reversed(flows[:-1]):reference=Q(cash)+reference/(1+r)
            result=present_value(cash_flows=flows,period_rate=r)
            assert result['total']==reference
            assert result['discounted_terms'][0]==flows[0]
            assert len(result['discounted_terms'])==length
            if r==0:assert result['total']==sum(flows)
            count('schedule_cases')
flows=[-100,55,'60.5'];before=flows.copy()
r=present_value(cash_flows=flows,period_rate='0.1')
assert flows==before and r['total']==0
assert r['discounted_terms']==(Q(-100),Q(50),Q(50))
assert present_value(cash_flows=(0,0,121),period_rate='0.1')['total']==100
assert present_value(cash_flows=(0,121),period_rate='0.1')['total']==110
assert compound_balance(principal=200,period_rate='-0.1',periods=2)==162
assert present_value(cash_flows=(-50,55),period_rate='0.1')['total']==0
assert -3**2==-9 and (-3)**2==9 and (3^2)==1
assert 2**3**2==512 and (2**3)**2==64
assert (1+2)/(3+3)==.5
assert rational('0.1')==Q(1,10)
assert present_value(cash_flows=[0],period_rate=0)['total']==0
invalid=[(lambda:rational(.1),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),
(lambda:periodic_rate(-1),ValueError),(lambda:periodic_rate(-2),ValueError),
(lambda:compound_balance(principal=-1,period_rate=0,periods=1),ValueError),
(lambda:compound_balance(principal=1,period_rate=0,periods=-1),ValueError),
(lambda:compound_balance(principal=1,period_rate=0,periods=True),TypeError),
(lambda:compound_balance(principal=1,period_rate=0,periods=2.0),TypeError),
(lambda:present_value(cash_flows=[],period_rate=0),ValueError),
(lambda:present_value(cash_flows=(),period_rate=0),ValueError),
(lambda:present_value(cash_flows='100',period_rate=0),TypeError),
(lambda:present_value(cash_flows=(x for x in [0]),period_rate=0),TypeError),
(lambda:present_value(cash_flows=(0,None),period_rate=0),TypeError),
(lambda:present_value(cash_flows=(0,1),period_rate=-1),ValueError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
