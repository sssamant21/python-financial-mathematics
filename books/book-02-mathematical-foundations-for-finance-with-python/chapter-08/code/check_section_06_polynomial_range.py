"""Complete polynomial/derivative output contract; exact monomial oracle."""
import math, random
from fractions import Fraction
import section_8_06 as source

def observations(include_resource=True):
    rows=[]
    def expect(name, call, reference=None, error=None):
        try:
            actual=call(); passed=error is None and actual==reference
            # Signed underflow/zero convention is checked separately below.
            rows.append(dict(name=name,passed=passed,actual=repr(actual),expected=error.__name__ if error else repr(reference)))
        except Exception as exc:
            rows.append(dict(name=name,passed=error is not None and type(exc) is error,actual=type(exc).__name__,expected=error.__name__ if error else repr(reference)))
    cases=[([-1e308,-1e308,1e308],2.),([5e-324,5e-324],.5),([1e308,1e308],2.),([1e308,-1e308],1.),([7.],2.),([1.,2.,3.],2.),([0.,-5e-324],.25)]
    rng=random.Random(806)
    for _ in range(100):
        cases.append(([math.ldexp(rng.uniform(-1,1),rng.randrange(-500,501)) for _ in range(rng.randrange(1,9))],rng.choice([-.5,-1.,1.,2.,0.])))
    for j,(coeff,x) in enumerate(cases):
        exact=sum(Fraction(v)*Fraction(x)**i for i,v in enumerate(coeff))
        try:
            ref=float(exact)
            if not math.isfinite(ref):raise OverflowError
            expect('monomial '+str(j),lambda:source.polynomial(iter(coeff),x),ref)
            if ref==0:
                expect('zero sign '+str(j),lambda:math.copysign(1,source.polynomial(coeff,x)),math.copysign(1,ref))
        except OverflowError:expect('monomial '+str(j),lambda:source.polynomial(coeff,x),error=ValueError)
    for coeff,order in [([0.,0.,1e308],1),([0.,0.,1e308],3),([1.,2.,3.],0),([1.,2.,3.],2),([1.],10**100),([5e-324,5e-324],1)]:
        if not include_resource and order>1000:continue
        # Direct falling-factorial references; no repeated differentiation.
        if order>=len(coeff):ref=(0.,)
        else:
            try:
                ref=tuple(float(Fraction(coeff[i])*math.prod(range(i-order+1,i+1))) for i in range(order,len(coeff)))
                if not all(map(math.isfinite,ref)):raise OverflowError
            except OverflowError:ref=None
        expect('derivative '+repr((coeff,order)),lambda:source.derivative_coefficients(iter(coeff),order),ref,error=ValueError if ref is None else None)
    for name,call,error in [
        ('empty polynomial',lambda:source.polynomial([],float('nan')),ValueError),
        ('coefficient before x',lambda:source.polynomial([True],float('nan')),TypeError),
        ('invalid x',lambda:source.polynomial([1.],True),TypeError),
        ('nonfinite coefficient',lambda:source.polynomial([float('inf')],0),ValueError),
        ('huge coefficient',lambda:source.polynomial([10**1000],0),ValueError),
        ('nonfinite x',lambda:source.polynomial([1.],float('inf')),ValueError),
        ('empty derivative',lambda:source.derivative_coefficients([],True),ValueError),
        ('coefficient before order',lambda:source.derivative_coefficients([True],-1),TypeError),
        ('negative order',lambda:source.derivative_coefficients([1.],-1),ValueError),
        ('bool order',lambda:source.derivative_coefficients([1.],True),ValueError),
        ('float order',lambda:source.derivative_coefficients([1.],1.),ValueError)]:expect(name,call,error=error)
    class Once:
        def __init__(self):self.used=False
        def __iter__(self):
            if self.used:raise RuntimeError('twice')
            self.used=True;yield from (1.,2.,3.)
    expect('polynomial one shot',lambda:source.polynomial(Once(),2),17.)
    expect('derivative one shot',lambda:source.derivative_coefficients(Once(),2),(6.,))
    return rows
if __name__=='__main__':
    rows=observations()
    for row in rows:
        assert row['passed'],row
    print(len(rows),'polynomial exact-reference/contract predicates passed')
