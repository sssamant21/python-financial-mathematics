"""Representation checks and allocation invariants; run without -O."""
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP, localcontext, getcontext
from fractions import Fraction
from math import isclose, isfinite, sqrt
from section_1_02 import payment_count, split_minor_units

names=[]
def check(name,condition):
    assert condition,name
    names.append(name)

check('exact rational third',Fraction(1,3)*3==1)
check('exact rational seventh',Fraction(1,7)*7==1)
check('finite decimal rate as rational',Fraction('0.035')==Fraction(7,200))
check('binary exact eighth',Fraction(0.125)==Fraction(1,8))
check('float construction differs from decimal text',Fraction(0.1)!=Fraction('0.1'))
check('float value is an exact ratio',Fraction(*sqrt(2).as_integer_ratio())==Fraction(sqrt(2)))
check('bool is subclass of int',isinstance(True,int))
check('finite and nonfinite float policy',isfinite(.05) and not isfinite(float('nan')) and not isfinite(float('inf')))
check('approximate float comparison',isclose(.1+.2,.3,rel_tol=1e-12))
original=(getcontext().prec,getcontext().rounding)
with localcontext() as context:
    context.prec=28
    context.rounding=ROUND_HALF_EVEN
    check('exact decimal sum',Decimal('.1')+Decimal('.2')==Decimal('.3'))
    check('decimal from float preserves approximation',Decimal(.1)!=Decimal('.1'))
    check('half even',Decimal('2.685').quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN)==Decimal('2.68'))
    check('half up',Decimal('2.685').quantize(Decimal('.01'),rounding=ROUND_HALF_UP)==Decimal('2.69'))
    check('decimal infinity excluded',not Decimal('Infinity').is_finite())
    check('decimal NaN excluded',not Decimal('NaN').is_finite())
    check('context division not exact rational third',Fraction(Decimal(1)/Decimal(3))!=Fraction(1,3))
with localcontext() as context:
    context.prec=6
    low=Decimal(1)/Decimal(7)
with localcontext() as context:
    context.prec=12
    high=Decimal(1)/Decimal(7)
check('precision changes quotient',low!=high)
check('context restored',(getcontext().prec,getcontext().rounding)==original)
check('practice rate conversion',Fraction('0.0125')==Fraction(1,80))
check('practice ending balance',Fraction(800)*(1+Fraction('0.0125'))==810)
check('practice four-recipient allocation',split_minor_units(101,4)==[26,25,25,25])
check('small-total allocation',split_minor_units(2,5)==[1,1,0,0,0])
check('one-recipient allocation',split_minor_units(105,1)==[105])
check('zero count accepted',payment_count(0)==0)
check('zero-total allocation',split_minor_units(0,3)==[0,0,0])
check('ordinary lists concatenate',[1,2]+[3,4]==[1,2,3,4])
check('aligned portfolio value',sum(h*p for h,p in zip([2,3],[10,20]))==80)
# Exhaustive small grid: total preservation, shape, integer domain, balance, rule.
scenarios=0
for total in range(51):
    for recipients in range(1,9):
        result=split_minor_units(total,recipients)
        assert len(result)==recipients
        assert sum(result)==total
        assert all(type(x) is int and x>=0 for x in result)
        assert max(result)-min(result)<=1
        base,remainder=divmod(total,recipients)
        assert result==[base+1]*remainder+[base]*(recipients-remainder)
        scenarios+=1
invalid_count=[(True,TypeError),(False,TypeError),(3.0,TypeError),
               ('3',TypeError),(None,TypeError),(Fraction(3),TypeError),
               (Decimal('3'),TypeError),(-1,ValueError),
               (float('nan'),TypeError),(float('inf'),TypeError)]
for value,error in invalid_count:
    try:
        payment_count(value)
    except error:
        pass
    else:
        raise AssertionError(f'expected {error.__name__} for {value!r}')
invalid_split=[((1,0),ValueError),((-1,2),ValueError),((1,-2),ValueError),
               ((True,2),TypeError),((1,True),TypeError),((1,2.0),TypeError)]
for args,error in invalid_split:
    try:
        split_minor_units(*args)
    except error:
        pass
    else:
        raise AssertionError(f'expected {error.__name__} for {args!r}')
print(f'PASS: {len(names)} representation/reference checks; {scenarios} allocation scenarios; '
      f'{len(invalid_count)+len(invalid_split)} invalid-input cases')
