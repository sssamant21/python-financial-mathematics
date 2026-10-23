"""Exact coefficient classification, original-domain checks, and counterexamples."""
from fractions import Fraction
from math import sqrt
import json
from section_1_06 import rational,solve_linear_equation,equation_residual,original_quotient

names=[]
def check(name,condition):
    assert condition,name
    names.append(name)

check('exact decimal quote',rational('0.05')==Fraction(1,20))
check('ratio input',rational('1/20')==Fraction(1,20))
check('integer input',rational(3)==Fraction(3))
check('Fraction input',rational(Fraction(2,3))==Fraction(2,3))
check('evaluated compound expression',Fraction(1000)*(1+Fraction('0.05'))**2==Fraction('1102.5'))
check('rate target',solve_linear_equation(a=100,b=100,c=0,d=110)==('unique',Fraction(1,10)))
check('unique linear exercise',solve_linear_equation(a=4,b=2,c=2,d=10)==('unique',Fraction(4)))
check('identity classification',solve_linear_equation(a=4,b=2,c=4,d=2)==('all',None))
check('inconsistent classification',solve_linear_equation(a=4,b=2,c=4,d=3)==('none',None))
check('zero coefficients identity',solve_linear_equation(a=0,b=0,c=0,d=0)==('all',None))
check('zero principal nonzero target',solve_linear_equation(a=0,b=0,c=0,d=10)==('none',None))
kind,candidate=solve_linear_equation(a=100,b=100,c=0,d=0)
check('financial domain removes real candidate',kind=='unique' and candidate==-1 and not candidate>-1)
check('original-equation residual',equation_residual(a=100,b=100,c=0,d=110,x='0.1')==0)
check('near-solution residual',equation_residual(a=100,b=100,c=0,d=110,x='0.0999')==Fraction(-1,100))
check('residual scaling exercise',equation_residual(a=1,b=1,c=0,d='1.1',x='0.0999')==Fraction(-1,10000))
check('tiny exact nonzero coefficient',solve_linear_equation(a='1/1000000000000000000000000000000',b=0,c=0,d=1)==('unique',Fraction(10**30)))
check('expression exercise at four percent',Fraction(500)*(1+Fraction('.04'))**2==Fraction('540.8'))
check('equation exercise at four percent',solve_linear_equation(a=500,b=500,c=0,d=520)==('unique',Fraction(1,25)))
check('false square identity counterexample',(1+Fraction(1,20))**2-(1+2*Fraction(1,20))==Fraction(1,400))
check('lost-zero solution',[x for x in [0,1,2,3] if x*(x-2)==0]==[0,2])
check('radical squared candidates',[x for x in [0,1,2,3,4] if x*x-3*x==0]==[0,3])
check('radical original rejects zero',sqrt(0+1)!=0-1)
check('radical original accepts three',sqrt(3+1)==3-1)
kind,excluded=solve_linear_equation(a=1,b=0,c=0,d=1)
check('cleared-denominator candidate has zero original denominator',kind=='unique' and excluded-1==0)
check('quotient at zero',original_quotient(0)==1)
check('quotient at two',original_quotient(2)==3)
# Full small integer coefficient grid: distinguish unique, all, and none.
coefficient_cases=0
kinds={'unique':0,'all':0,'none':0}
for a in range(-2,3):
    for b in range(-2,3):
        for c in range(-2,3):
            for d in range(-2,3):
                kind,solution=solve_linear_equation(a=a,b=b,c=c,d=d)
                kinds[kind]+=1
                if a!=c:
                    assert kind=='unique' and isinstance(solution,Fraction)
                    assert a*solution+b==c*solution+d
                    # A distinct neighboring rational cannot solve this linear equation.
                    assert a*(solution+1)+b!=c*(solution+1)+d
                elif b==d:
                    assert (kind,solution)==('all',None)
                    for x in [Fraction(-7,3),Fraction(0),Fraction(13,2)]:
                        assert a*x+b==c*x+d
                else:
                    assert (kind,solution)==('none',None)
                    for x in [Fraction(-7,3),Fraction(0),Fraction(13,2)]:
                        assert a*x+b!=c*x+d
                coefficient_cases+=1
# Exact evaluation of the stated identity on an illustrative rational grid.
identity_cases=0
for numerator in range(-5,6):
    for denominator in range(1,6):
        r=Fraction(numerator,denominator)
        assert (1+r)**2==1+2*r+r*r
        identity_cases+=1
quotient_cases=0
for x in [Fraction(-2),Fraction(0),Fraction(1,2),Fraction(2),Fraction(5,3)]:
    assert original_quotient(x)==x+1
    quotient_cases+=1
invalid=[(lambda:rational(True),TypeError),
 (lambda:rational(False),TypeError),
 (lambda:rational(.05),TypeError),
 (lambda:rational(None),TypeError),
 (lambda:rational(1j),TypeError),
 (lambda:rational([]),TypeError),
 (lambda:rational('NaN'),ValueError),
 (lambda:rational('Infinity'),ValueError),
 (lambda:rational('1/0'),ValueError),
 (lambda:rational('not-a-number'),ValueError),
 (lambda:original_quotient(1),ValueError),
 (lambda:original_quotient('1'),ValueError),
 (lambda:solve_linear_equation(a=.1,b=0,c=0,d=1),TypeError),
 (lambda:equation_residual(a=1,b=0,c=0,d=1,x=True),TypeError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
summary={'reference_checks':len(names),'coefficient_cases':coefficient_cases,
         'classification_counts':kinds,'identity_samples':identity_cases,
         'restricted_quotient_samples':quotient_cases,'invalid_input_cases':len(invalid)}
print('PASS: '+json.dumps(summary,sort_keys=True))
