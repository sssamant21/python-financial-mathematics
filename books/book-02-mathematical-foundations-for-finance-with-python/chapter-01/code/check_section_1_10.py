"""Rate representation, calendar boundaries, and exact accrual checks."""
from datetime import date,datetime,timedelta
from fractions import Fraction as Q
from itertools import product
import json
from section_1_10 import rational,decimal_rate,year_fraction,simple_accrual
assert __debug__, 'run without -O: assertions are required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
for r in [Q(-1,100),Q(0),Q(1,100),Q(3,50),Q(5)]:
    for name,scale in [('decimal',1),('percent',100),('basis_points',10000)]:
        assert decimal_rate(r*scale,representation=name)==r
        count('rate_cases')
assert decimal_rate(5,representation='decimal')==5
assert decimal_rate(5,representation='percent')==Q(1,20)
# Independently known calendar lengths, including century leap-year rules.
intervals=[(date(2025,1,1),date(2025,1,31),30),
(date(2024,2,28),date(2024,3,1),2),
(date(2025,2,28),date(2025,3,1),1),
(date(2000,2,28),date(2000,3,1),2),
(date(1900,2,28),date(1900,3,1),1),
(date(2024,1,1),date(2025,1,1),366),
(date(2025,1,1),date(2026,1,1),365),
(date(2025,12,31),date(2026,1,1),1),
(date(2025,1,1),date(2025,1,1),0)]
for start,end,days in intervals:
    for convention,denominator in [('ACT/360',360),('ACT/365F',365)]:
        alpha=year_fraction(start,end,convention=convention)
        assert alpha==Q(days,denominator)
        count('calendar_cases')
        for p,r in product([Q(0),Q(1),Q(10000)],[Q(-1,100),Q(0),Q(3,50)]):
            report=simple_accrual(principal=p,currency='USD',rate=r*100,
                representation='percent',start=start,end=end,convention=convention)
            assert report['interest']==Q(p*r*days,denominator)
            assert report['currency']=='USD' and report['decimal_rate']==r
            count('accrual_cases')
# Additivity follows from fixed denominators and constant principal/rate.
for convention in ['ACT/360','ACT/365F']:
    a,b,c=date(2024,2,28),date(2024,3,1),date(2025,1,1)
    assert year_fraction(a,c,convention=convention)==year_fraction(a,b,convention=convention)+year_fraction(b,c,convention=convention)
    count('additivity_cases')
policy=dict(principal=10000,currency='USD',rate=6,representation='percent',start=date(2025,1,1),end=date(2025,1,31),convention='ACT/360')
assert simple_accrual(**policy)['interest']==50
assert simple_accrual(**(policy|{'convention':'ACT/365F'}))['interest']==Q(3600,73)
invalid=[(lambda:rational(.05),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),
(lambda:decimal_rate(5,representation='pct'),ValueError),
(lambda:year_fraction(date(2025,1,1),date(2024,1,1),convention='ACT/360'),ValueError),
(lambda:year_fraction('2025-01-01',date(2025,1,1),convention='ACT/360'),TypeError),
(lambda:year_fraction(datetime(2025,1,1),date(2025,1,2),convention='ACT/360'),TypeError),
(lambda:year_fraction(date(2025,1,1),date(2025,1,2),convention='ACT/365'),ValueError),
(lambda:simple_accrual(**(policy|{'principal':-1})),ValueError)]
for currency in ['usd','US','USDD','12A',None]:
    invalid.append((lambda currency=currency:simple_accrual(**(policy|{'currency':currency})),ValueError))
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
