"""Direct accounting and independent feasible-bound reference checks."""
from fractions import Fraction as Q
from itertools import product
import json
from section_1_11 import rational,scenario,evaluate_transfer,minimum_transfer
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
base=dict(source=1000,destination=200,reserve=300,target=700,fixed_fee=5,fee_rate='0.01')
r=minimum_transfer(**base)
assert r['transfer']==500 and r['candidate_report']['fee']==10
assert r['candidate_report']['source_after']==490
assert r['candidate_report']['destination_after']==700
assert minimum_transfer(**(base|{'target':900}))['transfer'] is None
# Explicit no-action, fixed-fee boundary, and initially deficient source cases.
for extra,expected in [({'target':200},Q(0)),({'source':300,'target':200},Q(0)),
({'source':299,'target':200},None),({'source':810},Q(500)),
({'source':'809.99'},None),({'source':300,'fixed_fee':0,'fee_rate':0},None)]:
    assert minimum_transfer(**(base|extra))['transfer']==expected
    count('boundary_cases')
for S,D,R,T,F,k in product([0,2,5],[0,2],[0,2,6],[0,2,4],[0,1,6],[Q(0),Q(1,10)]):
    p=dict(source=S,destination=D,reserve=R,target=T,fixed_fee=F,fee_rate=k)
    gap=max(Q(0),Q(T-D))
    upper=Q(S-R-F)/(1+k)
    expected=(S>=R) if gap==0 else gap<=upper
    result=minimum_transfer(**p)
    assert result['feasible']==expected
    assert result['needed']==gap
    assert result['transfer']==(gap if expected else None)
    if expected:
        chosen=result['candidate_report']
        assert chosen['source_after']>=R and chosen['destination_after']>=T
        if gap>0:
            smaller=evaluate_transfer(transfer=gap/2,**p)
            assert not smaller['checks']['destination_target']
    for x in [Q(0),Q(1,2),Q(2),Q(5)]:
        report=evaluate_transfer(transfer=x,**p)
        expected_fee=Q(0) if x==0 else F+k*x
        # Independent conservation identity and direct original constraints.
        assert report['fee']==expected_fee
        assert report['source_after']+report['destination_after']==S+D-expected_fee
        direct=(S-x-expected_fee>=R and D+x>=T)
        assert report['feasible']==direct
        assert report['checks']=={'source_reserve':S-x-expected_fee>=R,'destination_target':D+x>=T}
        if result['transfer'] is None:assert not direct
        count('proposal_cases')
    count('scenario_cases')
exercise=dict(source=800,destination=100,reserve=200,target=500,fixed_fee=4,fee_rate='0.02')
r=minimum_transfer(**exercise)['candidate_report']
assert r['transfer']==400 and r['fee']==12 and r['source_after']==388
assert minimum_transfer(**(exercise|{'target':700}))['transfer'] is None
invalid=[(lambda:rational(.01),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),
(lambda:evaluate_transfer(transfer=-1,**base),ValueError)]
for key in base:
    invalid.append((lambda key=key:minimum_transfer(**(base|{key:-1})),ValueError))
invalid.append((lambda:minimum_transfer(**(base|{'source':None})),TypeError))
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
