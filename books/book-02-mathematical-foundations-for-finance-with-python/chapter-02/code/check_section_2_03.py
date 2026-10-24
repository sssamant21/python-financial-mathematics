"""Rational domains, determinant classification, original substitution, fee branches."""
from fractions import Fraction as Q
from itertools import product
import json
from section_2_03 import rational,solve_ratio,principal_for_fee_target
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
for a,b,c,d,t in product([-2,0,2],repeat=5):
    result=solve_ratio(a=a,b=b,c=c,d=d,target=t)
    empty=(c==0 and d==0)
    assert result['domain_empty']==empty
    assert result['excluded']==(() if c==0 else (Q(-d,c),))
    # Independent classification from constant versus nonconstant fractional maps.
    if empty:
        expected='none'
    elif a*d-b*c==0:
        constant=Q(a,c) if c else Q(b,d)
        expected='all' if t==constant else 'none'
    else:
        expected='none' if c and t==Q(a,c) else 'unique'
    assert result['kind']==expected,(a,b,c,d,t,result)
    if expected=='unique':
        x=result['solution'];assert c*x+d!=0
        assert (a*x+b)/(c*x+d)==t and result['residual']==0
    else:assert result['solution'] is None and result['residual'] is None
    for x in [Q(-3),Q(-1),Q(0),Q(1),Q(3)]:
        defined=(c*x+d)!=0
        direct=defined and (a*x+b)/(c*x+d)==t
        classified=defined and (expected=='all' or (expected=='unique' and x==result['solution']))
        assert direct==classified
        count('original_membership_cases')
    count('ratio_classification_cases')
for F,k,q in product([Q(0),Q(1),Q(6)],[Q(0),Q(1,100),Q(1,50)],[Q(0),Q(1,200),Q(1,100),Q(1,40)]):
    result=principal_for_fee_target(fixed_fee=F,fee_rate=k,target_fraction=q)
    if F==0:
        assert result['kind']==('all' if q==k else 'none')
        assert result['admissible']==(q==k)
        if q!=k:assert result['candidate']==0 and result['reason']=='candidate_at_excluded_pole'
    elif q==k:
        assert result['kind']=='none' and not result['admissible']
    else:
        p=result['solution']
        assert result['kind']=='unique' and (F+k*p)/p==q
        assert result['admissible']==(q>k)
    for p in [Q(-10),Q(-1),Q(0),Q(1),Q(10)]:
        direct=(p>0 and (F+k*p)/p==q)
        classified=p>0 and result['admissible'] and (result['kind']=='all' or p==result['solution'])
        assert direct==classified
    count('fee_target_cases')
# Explicit excluded roots, an identity on a punctured domain, and empty domain.
hole=solve_ratio(a=1,b=-1,c=1,d=-1,target=0)
assert hole['candidate']==1 and hole['kind']=='none' and hole['residual'] is None
identity=solve_ratio(a=1,b=-1,c=1,d=-1,target=1)
assert identity['kind']=='all' and identity['excluded']==(Q(1),)
assert solve_ratio(a=0,b=0,c=0,d=0,target=0)['domain_empty']
for x in range(-5,6):
    if x in (0,-3):continue
    x=Q(x)
    assert 1/x+2/(x+3)==(3*x+3)/(x*(x+3))
    count('common_denominator_cases')
# Practice calculations and denominator-clearing diagnostics.
assert Q(1,3)+Q(2,6)==Q(2,3)
assert solve_ratio(a=3,b=2,c=1,d=-2,target=4)['solution']==10
assert 10!=2 and Q(3*10+2,10-2)==4
assert 4**2-16==8*(4-4)  # cleared candidate, original denominator remains zero
assert (Q(6)+Q('.01')*400)/400==Q('.025')
assert principal_for_fee_target(fixed_fee=6,fee_rate='.01',target_fraction='.025')['solution']==400
assert principal_for_fee_target(fixed_fee=6,fee_rate='.01',target_fraction='.005')['solution']==-1200
assert not principal_for_fee_target(fixed_fee=6,fee_rate='.01',target_fraction='.005')['admissible']
assert principal_for_fee_target(fixed_fee=0,fee_rate='.02',target_fraction='.03')['kind']=='none'
invalid=[(lambda:rational(.01),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),
(lambda:solve_ratio(a=True,b=0,c=1,d=0,target=1),TypeError),
(lambda:principal_for_fee_target(fixed_fee=-1,fee_rate=0,target_fraction=0),ValueError),
(lambda:principal_for_fee_target(fixed_fee=0,fee_rate=-1,target_fraction=0),ValueError),
(lambda:principal_for_fee_target(fixed_fee=0,fee_rate=0,target_fraction=-1),ValueError),
(lambda:principal_for_fee_target(fixed_fee=0,fee_rate=.01,target_fraction=0),TypeError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
