"""Exact equivalent forms, model distinctions, preserved holes, and inputs."""
from fractions import Fraction as Q
from itertools import product
import json
from section_2_01 import rational,net_return_forms,two_period_forms,cancellation_forms
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
for p,r,F,k in product([Q(1),Q(10),Q(1000)],[Q(-1,2),Q(0),Q(3,50)],[Q(0),Q(5),Q(20)],[Q(0),Q(1,100),Q(1,2)]):
    report=net_return_forms(principal=p,period_rate=r,fixed_fee=F,fee_rate=k)
    # Accounting route: gross interest less fees equals net gain.
    net_gain=p*r-(F+k*p)
    expected_value=p+net_gain
    assert report['ending_value']==expected_value
    assert report['agree'] and set(report['forms'].values())=={net_gain/p}
    assert p*(1+r-k)-F==expected_value
    count('return_form_cases')
for p,r in product([Q(0),Q(1),Q(100)],[Q(-9,10),Q(-1,10),Q(0),Q(1,10),Q(1)]):
    result=two_period_forms(principal=p,period_rate=r)
    repeated=p
    for _ in range(2):repeated+=repeated*r
    assert result['factored']==result['expanded']==repeated and result['agree']
    assert repeated-p*(1+2*r)==p*r*r
    count('growth_form_cases')
for r in [Q(-3),Q(-2),Q(-1),Q(-1,10),Q(1,100),Q(1,10),Q(2)]:
    result=cancellation_forms(r)
    # Mathematical identity accepts nonzero rates outside the financial growth model.
    assert result['agree'] and result['original']==result['simplified']==2+r
    assert r*result['original']==(1+r)*(1+r)-1
    count('cancellation_cases')
for r,F,k in product([Q(-1,10),Q(0),Q(1,10)],[Q(0),Q(5)],[Q(0),Q(1,100)]):
    a=net_return_forms(principal=1000,period_rate=r,fixed_fee=F,fee_rate=k)['forms']['rate_decomposition']
    b=net_return_forms(principal=2000,period_rate=r,fixed_fee=F,fee_rate=k)['forms']['rate_decomposition']
    assert b-a==F*Q(1,2000) and b>=a
    assert (b>a)==(F>0)
    count('principal_comparison_cases')
exercise=net_return_forms(principal=800,period_rate='0.05',fixed_fee=4,fee_rate='0.01')
assert exercise['ending_value']==828 and exercise['forms']['rate_decomposition']==Q(7,200)
changed_return=(Q(800)*(1+Q('.05'))*(1-Q('.01'))-4-800)/800
assert changed_return==Q(69,2000)
assert exercise['forms']['rate_decomposition']-changed_return==Q(1,2000)
assert (1+Q('.02'))*(1+Q('.03'))-(1+Q('.02')+Q('.03'))==Q(3,5000)
assert (4*4-9)/(4-3)==7
assert (Q(100)*Q('.1')-5)/100==Q('.05') and Q('.1')-5!=Q('.05')
assert net_return_forms(principal=10,period_rate=0,fixed_fee=20,fee_rate=0)['forms']['rate_decomposition']==-2
assert (Q(100)+Q('.05'))!=Q(100)*(1+Q('.05'))
policy=dict(principal=100,period_rate='0.05',fixed_fee=5,fee_rate='0.01')
invalid=[(lambda:rational(.05),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),(lambda:cancellation_forms(0),ValueError),
(lambda:net_return_forms(**(policy|{'principal':0})),ValueError),
(lambda:net_return_forms(**(policy|{'principal':-1})),ValueError),
(lambda:net_return_forms(**(policy|{'period_rate':-1})),ValueError),
(lambda:net_return_forms(**(policy|{'fixed_fee':-1})),ValueError),
(lambda:net_return_forms(**(policy|{'fee_rate':-1})),ValueError),
(lambda:two_period_forms(principal=-1,period_rate=0),ValueError),
(lambda:two_period_forms(principal=1,period_rate=-1),ValueError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
