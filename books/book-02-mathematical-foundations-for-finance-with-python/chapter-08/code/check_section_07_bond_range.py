"""Complete positive-flow bond contracts; exact represented-base oracle."""
import math,random
from fractions import Fraction
import section_8_07 as source

def observations():
    rows=[]
    def expect(name,call,reference=None,error=None):
        try:
            actual=call();ok=error is None and actual==reference
            if ok and actual==0:ok=math.copysign(1,actual)==math.copysign(1,reference)
            result=repr(actual)
        except Exception as exc:result=type(exc).__name__;ok=type(exc) is error
        rows.append(dict(name=name,actual=result,expected=error.__name__ if error else repr(reference),passed=ok))
    vectors=[([105.],.05),([1e308],-.5),([1e308,1e308],1e154),([105.],1e308),([5e-324],1e308),([1.,2.,3.],0.),([1e-300],math.nextafter(-1.,0.)),([1e308]*4,0.)]
    rng=random.Random(8073)
    for _ in range(40):vectors.append(([math.ldexp(rng.uniform(1,2),rng.randrange(-800,800)) for _ in range(rng.randrange(1,7))],rng.choice([-.5,.0,.05,1.,1e150,1e308])))
    for j,(flows,y) in enumerate(vectors):
        base=Fraction(1+y)
        # Direct complete discounted monomials; source uses Horner in discount.
        price=sum(Fraction(c)/base**i for i,c in enumerate(flows,1));derivative=-sum(i*Fraction(c)/base**(i+1) for i,c in enumerate(flows,1))
        for name,exact in [('bond_price',price),('bond_price_derivative',derivative),('yield_price_sensitivity',1/derivative)]:
            try:
                reference=float(exact)
                if not math.isfinite(reference):raise OverflowError
                error=None
            except OverflowError:reference=None;error=ValueError
            expect(name+' vector'+str(j),lambda:getattr(source,name)(iter(flows),y),reference,error)
    for name in ['bond_price','bond_price_derivative','yield_price_sensitivity']:
        for flows,y,error,label in [([],0.,ValueError,'empty'),([1.,0.],0.,ValueError,'zero'),([1.,-1.],0.,ValueError,'negative'),([True],0.,TypeError,'bool flow'),([float('inf')],0.,ValueError,'inf flow'),([10**1000],0.,ValueError,'oversized'),([1.],-1.,ValueError,'yield domain'),([1.],True,TypeError,'bool yield')]:expect(name+' '+label,lambda:getattr(source,name)(flows,y),error=error)
        trace=[]
        def sentinel():trace.append('consumed');yield 1.
        expect(name+' yield first',lambda:getattr(source,name)(sentinel(),float('nan')),error=ValueError)
        expect(name+' not consumed on bad yield',lambda:bool(trace),False)
        class Once:
            def __init__(self):self.used=False
            def __iter__(self):
                if self.used:raise RuntimeError('twice')
                self.used=True;yield 105.
        expect(name+' one shot',lambda:getattr(source,name)(Once(),0.),{'bond_price':105.,'bond_price_derivative':-105.,'yield_price_sensitivity':-1/105}[name])
    return rows
if __name__=='__main__':
    rows=observations()
    for row in rows:assert row['passed'],row
    print(len(rows),'bond price/derivative/reciprocal predicates passed')
