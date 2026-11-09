"""Complete price/normalized sampled-ratio references;not model acceptance."""
import math,random
from decimal import Decimal,localcontext
import section_8_08 as source

def observations():
    rows=[]
    def check(name,call,reference=None,error=None,rtol=4e-15):
        try:
            value=call();ok=error is None and math.isfinite(value) and (value==reference if reference==0 else math.isclose(value,reference,rel_tol=rtol,abs_tol=0))
            if ok and reference==0:ok=math.copysign(1,value)==math.copysign(1,reference)
            actual=repr(value)
        except Exception as exc:actual=type(exc).__name__;ok=type(exc) is error
        rows.append(dict(name=name,actual=actual,expected=error.__name__ if error else repr(reference),passed=ok))
    vectors=[(1e-308,1.,-1000.),(1e308,1.,1000.),(1000.,5.,.04),(1.,0.,1e308),(1.,1e308,1e308),(1.,1.,-20000.),(5e-324,1.,0.),(1e308,1.,-1.)]
    rng=random.Random(8084)
    for _ in range(30):vectors.append((math.ldexp(rng.uniform(1,2),rng.randrange(-800,800)),rng.uniform(0,10),rng.uniform(-100,100)))
    for j,(cash,years,rate) in enumerate(vectors):
        refs=[]
        for precision in [1800,2300]:
            with localcontext() as ctx:
                ctx.prec=precision;refs.append(float(Decimal.from_float(cash)*(-Decimal.from_float(years)*Decimal.from_float(rate)).exp()))
        assert refs[0]==refs[1]
        ref=refs[0];error=None
        if not math.isfinite(ref):ref=None;error=ValueError
        check('price '+str(j),lambda:source.discounted_price(cash,years,rate),ref,error)
    normalized=[(1e-308,1.,-1000.,.01),(1e308,1.,1000.,.01),(1000.,5.,.04,.001),(1000.,0.,.04,.001),(1.,1.,1.,.625*2**-52),(1.,1e-308,0.,1e-308),(1e308,1e-297,0.,1e300)]
    for j,(cash,years,rate,h) in enumerate(normalized):
        refs=[]
        for precision in [1800,2300]:
            with localcontext() as ctx:
                ctx.prec=precision;C,T,H=map(Decimal.from_float,(cash,years,h))
                def p(r):return C*(-Decimal.from_float(r)*T).exp()
                base,up,down=p(rate),p(rate+h),p(rate-h);refs.append(tuple(float(z) for z in (base,-(up-down)/(2*H*base),(up-2*base+down)/(H*H*base))))
        assert refs[0]==refs[1]
        for field,ref in zip(['price','duration','convexity'],refs[0]):
            if years==0 and field=='duration':ref=-0.
            check('normalized '+str(j)+' '+field,lambda:source.rate_sensitivity(cash,years,rate,h)[field],ref)
        check('analytic duration '+str(j),lambda:source.rate_sensitivity(cash,years,rate,h)['analytic_duration'],years)
        check('analytic convexity '+str(j),lambda:source.rate_sensitivity(cash,years,rate,h)['analytic_convexity'],float(__import__('fractions').Fraction(years)**2))
    for name,call,error in [('cash first',lambda:source.discounted_price(True,True,float('nan')),TypeError),('years before domain',lambda:source.discounted_price(0,True,0),TypeError),('zero cash',lambda:source.discounted_price(0,1,0),ValueError),('negative years',lambda:source.discounted_price(1,-1,0),ValueError),('oversized cash',lambda:source.discounted_price(10**1000,1,0),ValueError),('price gate',lambda:source.rate_sensitivity(1,1,1000,.01),ValueError),('negative step',lambda:source.rate_sensitivity(1000,1,.04,-.01),ValueError),('collapsed step',lambda:source.rate_sensitivity(1000,1,1.,1e-30),ValueError),('nonfinite shifts',lambda:source.rate_sensitivity(1,0,1e308,1e308),ValueError),('true normalized overflow',lambda:source.rate_sensitivity(1,1000,0.,100.),ValueError),('analytic curvature range',lambda:source.rate_sensitivity(1,1e200,0.,1e-201),ValueError)]:check(name,call,error=error)
    return rows
if __name__=='__main__':
    rows=observations()
    for row in rows:assert row['passed'],row
    print(len(rows),'financial price/normalized predicates passed')
