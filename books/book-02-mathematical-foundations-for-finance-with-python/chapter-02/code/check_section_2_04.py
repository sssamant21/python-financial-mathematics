"""Exact power references, real-root branches, endpoint inference, and domains."""
from fractions import Fraction as Q
from itertools import product
import json,math
from section_2_04 import integer_power,finite_float,real_root,infer_period_rate
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
def close(a,b):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
for base,n in product([Q(-3),Q(-1,2),Q(0),Q(1,2),Q(1),Q(3)],range(-5,6)):
    if base==0 and n<=0:continue
    reference=Q(1)
    for _ in range(abs(n)):reference*=base
    if n<0:reference=1/reference
    assert integer_power(base,n)==reference
    count('exact_power_cases')
for root,n in product([0,1,2,3], [1,2,3,4,5,7,12,120]):
    value=root**n
    actual=real_root(value,n)
    assert actual>=0 and close(actual,root)
    assert close(actual**n,value)
    count('planted_root_cases')
for root,n in product([-1,-2,-3],[1,3,5,7]):
    value=root**n
    actual=real_root(value,n)
    assert actual<0 and close(actual,root) and close(actual**n,value)
    count('negative_odd_root_cases')
for value in [0,.25,2,9,49,1e-100,1e100]:
    actual=real_root(value,2)
    assert math.isclose(actual,math.sqrt(value),rel_tol=1e-12,abs_tol=0)
    if value>0:assert actual>0
    count('square_root_reference_cases')
for initial,factor,n in product([Q(1),Q(1000)],[Q(1,2),Q(9,10),Q(1),Q(11,10),Q(2)],[1,2,3,12]):
    ending=initial*factor**n
    result=infer_period_rate(initial_value=float(initial),final_value=float(ending),periods=n)
    assert result['growth_factor']>0 and result['period_rate']>-1
    assert close(result['growth_factor'],float(factor))
    assert close(result['period_rate'],float(factor-1))
    assert close(float(initial)*(1+result['period_rate'])**n,float(ending))
    count('endpoint_reconstruction_cases')
# Principal-root identities and the six practice calculations.
assert integer_power('3/2',-2)==Q(4,9) and integer_power(7,0)==1 and integer_power(0,3)==0
assert integer_power(2,5)*integer_power(2,-2)==integer_power(2,3)
assert integer_power(integer_power(2,2),3)==integer_power(2,6)
assert real_root(49,2)==7 and real_root((-7)**2,2)==abs(-7)
assert close(real_root(81,4)**3,27)
assert close(real_root(32,5)**-2,.25)
assert close(real_root(-27,3),-3)
assert close(infer_period_rate(initial_value=500,final_value=605,periods=2)['period_rate'],.1)
assert close(infer_period_rate(initial_value=1000,final_value=729,periods=3)['period_rate'],-.1)
assert not close(500*(1+.105)**2,605)
assert isinstance((-8)**(1/3),complex)
assert close(-1.1**2,-1.21) and close((-1.1)**2,1.21)
invalid=[(lambda:integer_power(0,-1),ValueError),(lambda:integer_power(0,0),ValueError),
(lambda:integer_power(.1,2),TypeError),(lambda:integer_power(True,2),TypeError),
(lambda:integer_power(2,True),TypeError),(lambda:integer_power(2,.5),TypeError),
(lambda:finite_float(None),TypeError),(lambda:finite_float('2'),TypeError),
(lambda:finite_float(True),TypeError),(lambda:finite_float(10**10000),ValueError),
(lambda:finite_float(float('nan')),ValueError),(lambda:finite_float(float('inf')),ValueError),
(lambda:real_root(-16,4),ValueError),(lambda:real_root(1,0),ValueError),
(lambda:real_root(1,-1),ValueError),(lambda:real_root(1,121),ValueError),
(lambda:real_root(1,True),ValueError),(lambda:real_root(1,2.0),ValueError),
(lambda:infer_period_rate(initial_value=0,final_value=1,periods=2),ValueError),
(lambda:infer_period_rate(initial_value=1,final_value=0,periods=2),ValueError),
(lambda:infer_period_rate(initial_value=-1,final_value=1,periods=2),ValueError),
(lambda:infer_period_rate(initial_value=1,final_value=-1,periods=2),ValueError),
(lambda:infer_period_rate(initial_value=1,final_value=1,periods=0),ValueError),
(lambda:infer_period_rate(initial_value=1e-308,final_value=1e308,periods=2),ValueError),
(lambda:infer_period_rate(initial_value=1e308,final_value=1e-308,periods=2),ValueError),
(lambda:infer_period_rate(initial_value=1,final_value=1e-20,periods=1),ValueError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
