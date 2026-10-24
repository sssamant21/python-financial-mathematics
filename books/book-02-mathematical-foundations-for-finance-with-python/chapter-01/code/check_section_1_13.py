"""Exact audits, deliberately bad candidates, properties, and tolerance policy."""
from fractions import Fraction as Q
from itertools import product
import json,math
from section_1_12 import compound_balance
from section_1_13 import audit_growth,compare_finite,finite_float
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
for p,r,n in product([Q(0),Q(1),Q(100)],[Q(-9,10),Q(-1,10),Q(0),Q(1,10),Q(1)],[0,1,2,5]):
    reference=p
    for _ in range(n):reference+=reference*r
    inputs=dict(principal=p,period_rate=r,periods=n)
    good=audit_growth(candidate=reference,**inputs)
    assert good['passed'] and good['discrepancy']==0
    assert all(good['checks'].values())
    # A known unit perturbation must not pass an exact audit.
    bad=audit_growth(candidate=reference+1,**inputs)
    assert not bad['passed'] and bad['discrepancy']==1
    assert not bad['checks']['formula_agreement']
    assert not bad['checks']['recurrence_agreement']
    assert not bad['checks']['round_trip']
    count('exact_audit_cases')
for p,r,m,n,c in product([Q(1),Q(100)],[Q(-1,10),Q(0),Q(1,10)],[0,1,3],[0,2],[Q(0),Q(2)]):
    a=compound_balance(principal=p,period_rate=r,periods=m+n)
    staged=compound_balance(principal=compound_balance(principal=p,period_rate=r,periods=m),period_rate=r,periods=n)
    scaled=compound_balance(principal=c*p,period_rate=r,periods=m+n)
    assert a==staged and scaled==c*a
    count('property_cases')
inputs=dict(principal=100,period_rate='0.10',periods=2)
for wrong in [Q(110),Q(12100),Q(121)-1,Q(-1),Q(12100,1000)]:
    assert not audit_growth(candidate=wrong,**inputs)['passed']
    count('deliberate_error_cases')
bad=audit_growth(candidate=110,**inputs)
assert bad['checks']['nonnegative'] and bad['checks']['direction_bound']
assert bad['discrepancy']==-11
assert audit_growth(principal=200,period_rate='0.05',periods=2,candidate=210)['discrepancy']==Q('-10.5')
# Dyadic values give exact representable tolerance-boundary examples.
for a,b,rel,absolute,expected in [(1,1,0,0,True),(1,1.125,0,.125,True),
(1,1.25,0,.125,False),(0,.125,0,.125,True),(0,.25,0,.125,False),
(8,9,.125,0,True),(8,10,.125,0,False),(-8,-9,.125,0,True),
(.1+.2,.3,1e-12,0,True),(1e-12,0,1e-9,0,False),
(1e-12,0,1e-9,1e-12,True),(1e-8,0,1e-6,0,False),
(1e-8,0,1e-6,1e-8,True)]:
    assert compare_finite(a,b,rel_tol=rel,abs_tol=absolute)==expected
    assert compare_finite(b,a,rel_tol=rel,abs_tol=absolute)==expected
    count('tolerance_cases')
invalid=[(lambda:finite_float(True),TypeError),(lambda:finite_float('1'),TypeError),
(lambda:finite_float(None),TypeError),(lambda:finite_float(10**10000),ValueError),
(lambda:finite_float(float('nan')),ValueError),(lambda:finite_float(float('inf')),ValueError),
(lambda:finite_float(float('-inf')),ValueError),
(lambda:compare_finite(1,1,rel_tol=-1,abs_tol=0),ValueError),
(lambda:compare_finite(1,1,rel_tol=1,abs_tol=0),ValueError),
(lambda:compare_finite(1,1,rel_tol=0,abs_tol=-1),ValueError),
(lambda:compare_finite(1,1,rel_tol=float('nan'),abs_tol=0),ValueError),
(lambda:compare_finite(1,1,rel_tol=0,abs_tol=float('inf')),ValueError),
(lambda:compare_finite(1,float('inf'),rel_tol=0,abs_tol=0),ValueError),
(lambda:audit_growth(candidate=121.0,**inputs),TypeError),
(lambda:audit_growth(candidate=121,**(inputs|{'periods':True})),TypeError),
(lambda:audit_growth(candidate=121,**(inputs|{'period_rate':-1})),ValueError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
