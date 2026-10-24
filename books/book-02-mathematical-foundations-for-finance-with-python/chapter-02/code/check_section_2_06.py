"""Original inequality membership, exact boundaries, and interval intersections."""
from fractions import Fraction as Q
from itertools import product
import json
from section_2_06 import rational,interval,contains,intersect,linear_upper,absolute_band,display
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
probes=[Q(-3),Q(-2),Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1),Q(2),Q(3)]
for a,b,limit,strict in product([-2,0,2],[-1,0,1],[-1,0,1],[False,True]):
    region=linear_upper(coefficient=a,constant=b,limit=limit,strict=strict)
    for x in probes:
        direct=(a*x+b<limit) if strict else (a*x+b<=limit)
        assert contains(region,x)==direct
        count('linear_membership_cases')
    if a:
        boundary=Q(limit-b,a)
        assert contains(region,boundary)==(not strict)
        assert contains(region,boundary-Q(1,100))==(a>0)
        assert contains(region,boundary+Q(1,100))==(a<0)
    count('linear_solutions')
for a,b,width,strict in product([-2,0,2],[-2,0,2],[-1,0,1,2],[False,True]):
    region=absolute_band(coefficient=a,constant=b,threshold=width,strict=strict)
    for x in probes:
        direct=(abs(a*x+b)<width) if strict else (abs(a*x+b)<=width)
        assert contains(region,x)==direct
        count('absolute_membership_cases')
    if a and width>=0:
        for endpoint in [Q(-width-b,a),Q(width-b,a)]:
            assert contains(region,endpoint)==(not strict)
    count('absolute_solutions')
regions=[None,interval(),interval(0,1),interval(0,1,left_closed=False),
         interval(0,1,right_closed=False),interval(-1,0,right_closed=False),
         interval(0,0),interval(1,2),interval(lower=0),interval(upper=0)]
for left,right in product(regions,repeat=2):
    result=intersect(left,right)
    assert result==intersect(right,left)
    for x in probes:
        assert contains(result,x)==(contains(left,x) and contains(right,x))
        count('intersection_membership_cases')
    count('intersection_pairs')
assert intersect(interval(0,1),interval(1,2))==interval(1,1)
assert intersect(interval(0,1,right_closed=False),interval(1,2)) is None
assert interval(2,1) is None and interval(0,0,left_closed=False) is None
assert interval()['left_closed'] is False and interval()['right_closed'] is False
assert absolute_band(coefficient=0,constant=0,threshold=0)==interval()
assert absolute_band(coefficient=0,constant=0,threshold=0,strict=True) is None
weights=absolute_band(coefficient=1,constant='-.5',threshold='.1')
cap=linear_upper(coefficient=1,constant=0,limit='.55',strict=True)
feasible=intersect(intersect(weights,interval(0,1)),cap)
assert feasible==interval('0.4','0.55',right_closed=False)
for w in map(Q,['.3999','.4','.5','.5499','.55','.6']):
    assert contains(feasible,w)==(0<=w<=1 and abs(w-Q('.5'))<=Q('.1') and w<Q('.55'))
    count('weight_boundary_cases')
# Known sign-derived regions cross-checked against original expressions.
profit=interval(20,80)
positive_capped=interval(20,60,left_closed=False)
for q in list(map(Q,range(-1,122)))+[Q('19.99'),Q('20.01'),Q('79.99'),Q('80.01')]:
    pi=-Q('.1')*q*q+10*q-160
    assert contains(profit,q)==(pi>=0)
    assert contains(positive_capped,q)==(pi>0 and q>=0 and 12-Q('.1')*q>=0 and q<=60)
    count('profit_sign_cases')
for x in map(lambda n:Q(n,2),range(-10,16)):
    union=contains(interval(upper=2),x) or contains(interval(lower=5,left_closed=False),x)
    if x==5:assert not union
    else:assert union==((x-2)/(x-5)>=0)
    count('rational_sign_cases')
# Exercise endpoints and empty/singleton policy intersections.
assert intersect(linear_upper(coefficient=-3,constant=5,limit=11,strict=True),interval(lower=0))==interval(lower=0)
assert intersect(absolute_band(coefficient=2,constant=-6,threshold=4),interval(upper=4,right_closed=False))==interval(1,4,right_closed=False)
policy=intersect(absolute_band(coefficient=1,constant='-.6',threshold='.15'),interval(0,'.7'))
assert policy==interval('.45','.7')
assert intersect(policy,interval(lower='.7',left_closed=False)) is None
assert intersect(policy,interval(lower='.7'))==interval('.7','.7')
invalid=[(lambda:rational(.1),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),(lambda:interval(0,1,left_closed=1),TypeError),
(lambda:interval(0,1,right_closed='True'),TypeError),
(lambda:linear_upper(coefficient=1,constant=0,limit=1,strict=1),TypeError),
(lambda:absolute_band(coefficient=1,constant=0,threshold=1,strict=0),TypeError),
(lambda:contains(interval(),True),TypeError),(lambda:interval(0,.1),TypeError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
