"""Complete implicit-helper references; no branch/model certification."""
import math,random
from decimal import Decimal,localcontext
from fractions import Fraction
import section_8_07 as source

def observations():
    rows=[]
    def check(name,call,expected=None,error=None):
        try:
            actual=call();passed=error is None and math.isfinite(actual) and (actual==expected if expected==0 else math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0))
            if passed and expected==0:passed=math.copysign(1,actual)==math.copysign(1,expected)
            value=repr(actual)
        except Exception as exc:value=type(exc).__name__;passed=type(exc) is error
        rows.append(dict(name=name,actual=value,expected=error.__name__ if error else repr(expected),passed=bool(passed)))
    circles=[(0.,1e308),(0.,1e-200),(1e308,1e308),(-1e308,1e308),(3.,5.),(math.nextafter(1e308,0.),1e308),(0.,5e-324),(0.,float.fromhex('0x1.fffffffffffffp1023'))]
    rng=random.Random(807)
    for _ in range(35):
        radius=math.ldexp(rng.uniform(1,2),rng.randrange(-1000,1000));circles.append((radius*rng.uniform(-1,1),radius))
    for x,radius in circles:
        refs=[]
        for precision in [200,400]:
            with localcontext() as ctx:
                ctx.prec=precision;refs.append(float((Decimal.from_float(radius)**2-Decimal.from_float(x)**2).sqrt()))
        assert refs[0]==refs[1]
        check('circle '+repr((x,radius)),lambda:source.circle_upper(x,radius),refs[0])
    economics=[(1e308,-1e308,1e308),(50.,20.,1200.),(1e200,0.,1e-200),(1e-200,0.,1e200),(1e308,0.,5e-324),(5e-324,0.,5e-324),(1e200,0.,1e308),(-1.,-2.,3.)]
    for _ in range(35):
        p=math.ldexp(rng.uniform(1,2),rng.randrange(-500,500));economics.append((p,-p,math.ldexp(rng.uniform(1,2),rng.randrange(-500,500))))
    for p,c,k in economics:
        gap=Fraction(p)-Fraction(c)
        for name,exact in [('break_even_quantity',Fraction(k)/gap),('break_even_sensitivity',-Fraction(k)/gap**2)]:
            try:
                expected=float(exact)
                if not math.isfinite(expected):raise OverflowError
                error=None
            except OverflowError:expected=None;error=ValueError
            check(name+' '+repr((p,c,k)),lambda:getattr(source,name)(p,c,k),expected,error)
    for name,call,error in [
      ('circle type priority',lambda:source.circle_upper(True,-1),TypeError),('radius type',lambda:source.circle_upper(0,True),TypeError),('zero radius',lambda:source.circle_upper(0,0),ValueError),('outside',lambda:source.circle_upper(6,5),ValueError),('nonfinite x',lambda:source.circle_upper(float('nan'),1),ValueError),('huge radius',lambda:source.circle_upper(0,10**1000),ValueError),('price before cost',lambda:source.break_even_sensitivity(True,float('inf'),1),TypeError),('cost before fixed',lambda:source.break_even_quantity(1,True,float('inf')),TypeError),('fixed before domain',lambda:source.break_even_quantity(0,1,True),TypeError),('zero fixed',lambda:source.break_even_quantity(50,20,0),ValueError),('equal price cost',lambda:source.break_even_sensitivity(1,1,1),ValueError),('invalid sensitivity fixed',lambda:source.break_even_sensitivity(1,0,float('nan')),ValueError)]:check(name,call,error=error)
    # Sensitivity must not depend on rounding/representability of quantity.
    original=source.break_even_quantity
    try:
        def forbidden(*args):raise RuntimeError('quantity dependency')
        source.break_even_quantity=forbidden
        check('complete sensitivity independent',lambda:source.break_even_sensitivity(1e200,0.,1e308),-1e-92)
    finally:source.break_even_quantity=original
    return rows
if __name__=='__main__':
    rows=observations()
    for row in rows:assert row['passed'],row
    print(len(rows),'circle/break-even contract predicates passed')
