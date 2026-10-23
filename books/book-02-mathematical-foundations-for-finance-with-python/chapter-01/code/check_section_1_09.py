"""Exact comparison identities, witness validity, and domain checks."""
from fractions import Fraction as Q
from itertools import combinations,product
import json
from section_1_09 import rational,fee_metrics,search_pairs
assert __debug__, 'run without -O: assertions are required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
assert rational('0.01')==Q(1,100)
assert fee_metrics(amount=100,fixed_fee=5,fee_rate='0.01')=={'total':Q(6),'effective':Q(3,50)}
assert fee_metrics(amount=300,fixed_fee=3,fee_rate='0.02')=={'total':Q(9),'effective':Q(3,100)}
xs=(Q(1,2),Q(1),Q(100),Q(200))
for F,k in product([Q(0),Q(1,2),Q(5)],[Q(0),Q(1,100),Q(1)]):
    for a,b in combinations(xs,2):
        ma=fee_metrics(amount=a,fixed_fee=F,fee_rate=k)
        mb=fee_metrics(amount=b,fixed_fee=F,fee_rate=k)
        assert ma['effective']-mb['effective']==F*(b-a)/(a*b)
        assert mb['total']-ma['total']==k*(b-a)
        assert (mb['effective']<ma['effective'])==(F>0)
        assert (mb['total']>ma['total'])==(k>0)
        assert mb['effective']<=ma['effective']
        count('exact_pair_cases')
    for claim in ['effective_nonincreasing','effective_strictly_decreasing']:
        r=search_pairs(amounts=xs,fixed_fee=F,fee_rate=k,claim=claim)
        assert r['pairs_checked']==6
        expected_failure=(claim=='effective_strictly_decreasing' and F==0)
        assert (r['counterexample'] is not None)==expected_failure
        if expected_failure:
            w=r['counterexample']
            assert w['a']==xs[0] and w['b']==xs[1] and 0<w['a']<w['b']
            assert w['effective_a']==w['effective_b']==k
        count('search_cases')
# A positive total-fee difference coexists with a negative effective-rate difference.
a=fee_metrics(amount=100,fixed_fee=5,fee_rate='0.01')
b=fee_metrics(amount=200,fixed_fee=5,fee_rate='0.01')
assert b['total']>a['total'] and b['effective']<a['effective']
policy=dict(amounts=(100,200),fixed_fee=0,fee_rate='0.01',claim='effective_nonincreasing')
invalid=[(lambda:rational(.01),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),
(lambda:fee_metrics(amount=0,fixed_fee=0,fee_rate=0),ValueError),
(lambda:fee_metrics(amount=-1,fixed_fee=0,fee_rate=0),ValueError),
(lambda:fee_metrics(amount=1,fixed_fee=-1,fee_rate=0),ValueError),
(lambda:fee_metrics(amount=1,fixed_fee=0,fee_rate=-1),ValueError)]
for amounts in [(),(1,),(0,1),(2,1),(1,1)]:
    invalid.append((lambda amounts=amounts:search_pairs(**(policy|{'amounts':amounts})),ValueError))
invalid.append((lambda:search_pairs(**(policy|{'claim':'unknown'})),ValueError))
invalid.append((lambda:search_pairs(**(policy|{'fixed_fee':-1})),ValueError))
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
