"""Planted exact roots, symbolic descriptions, Decimal residuals, and domains."""
from decimal import Decimal,localcontext,getcontext
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
import json
from section_2_05 import rational,rational_sqrt,solve_quadratic,approximate_roots
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1
for a,(u,v) in product([Q(-2),Q(-1,10),Q(1),Q(3,2)],combinations_with_replacement([Q(-3),Q(-1),Q(0),Q(1),Q(2)],2)):
    b,c=-a*(u+v),a*u*v
    result=solve_quadratic(a=a,b=b,c=c)
    roots=result['exact_roots']
    assert roots==tuple(sorted({u,v}))
    assert result['kind']==('repeated' if u==v else 'two_real')
    assert all(a*x*x+b*x+c==0 for x in roots)
    assert u+v==-b/a and u*v==c/a
    scaled=solve_quadratic(a=-3*a,b=-3*b,c=-3*c)
    assert scaled['kind']==result['kind'] and scaled['exact_roots']==roots
    assert scaled['center']==result['center'] and scaled['spread_squared']==result['spread_squared']
    count('planted_rational_cases')
for a,h,s in product([Q(-2),Q(1),Q(3)],[Q(-3),Q(0),Q(4)],[Q(2),Q(3),Q(5)]):
    b,c=-2*a*h,a*(h*h-s)
    result=solve_quadratic(a=a,b=b,c=c)
    assert result['kind']=='two_real' and result['exact_roots'] is None
    assert result['center']==h and result['spread_squared']==s
    before=getcontext().copy()
    roots=approximate_roots(a=a,b=b,c=c,precision=40)
    after=getcontext()
    assert before.prec==after.prec and before.rounding==after.rounding
    with localcontext() as ctx:
        ctx.prec=60
        def dec(q):return Decimal(q.numerator)/Decimal(q.denominator)
        A,B,C=map(dec,(a,b,c))
        for x in roots:
            residual=A*x*x+B*x+C
            scale=abs(A)*abs(x)**2+abs(B)*abs(x)+abs(C)
            assert abs(residual)<=Decimal('1e-34')*scale
        assert abs(sum(roots)-dec(2*h))<Decimal('1e-34')
    count('irrational_description_cases')
for a,h,s in product([Q(-2),Q(1)],[Q(-3),Q(0),Q(4)],[Q(1),Q(2)]):
    # a*((x-h)^2+s) cannot vanish over the reals.
    result=solve_quadratic(a=a,b=-2*a*h,c=a*(h*h+s))
    assert result['kind']=='no_real' and result['discriminant']<0
    assert result['exact_roots']==() and approximate_roots(a=a,b=-2*a*h,c=a*(h*h+s))==()
    count('no_real_cases')
assert rational_sqrt(Q(4,9))==Q(2,3) and rational_sqrt(Q(2)) is None
assert solve_quadratic(a=1,b=0,c=0)['exact_roots']==(Q(0),)
assert solve_quadratic(a=1,b=0,c='-1e-80')['exact_roots']==(Q('-1e-40'),Q('1e-40'))
# Financial break-even roots checked through original revenue and cost, not only the polynomial.
roots=solve_quadratic(a='-.1',b=10,c=-160)['exact_roots']
assert roots==(20,80)
for q in roots:
    price=12-Q('.1')*q
    assert q>=0 and price>=0 and q*price==160+2*q
    count('break_even_original_cases')
assert tuple(q for q in roots if q<=60)==(20,)
rates=solve_quadratic(a=200,b=400,c=-42)['exact_roots']
assert rates==(Q(-21,10),Q(1,10))
assert all(200*(1+r)**2==242 for r in rates)
assert tuple(r for r in rates if r>-1)==(Q(1,10),)
assert solve_quadratic(a=1,b=2,c=1)['exact_roots']==(Q(-1),)
assert not any(r>-1 for r in solve_quadratic(a=1,b=2,c=1)['exact_roots'])
assert solve_quadratic(a=1,b=-7,c=12)['exact_roots']==(3,4)
assert solve_quadratic(a=1,b=-8,c=7)['exact_roots']==(1,7)
assert solve_quadratic(a=1,b=6,c=9)['exact_roots']==(-3,)
assert solve_quadratic(a=1,b=0,c=4)['kind']=='no_real'
assert solve_quadratic(a=2,b=0,c=-3)['spread_squared']==Q(3,2)
invalid=[(lambda:rational(.1),TypeError),(lambda:rational(True),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),(lambda:rational_sqrt(Q(-1)),ValueError),
(lambda:solve_quadratic(a=0,b=2,c=-6),ValueError),
(lambda:solve_quadratic(a=True,b=0,c=1),TypeError)]
for precision in [True,15,101,40.0]:
    invalid.append((lambda precision=precision:approximate_roots(a=1,b=0,c=-2,precision=precision),ValueError))
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
