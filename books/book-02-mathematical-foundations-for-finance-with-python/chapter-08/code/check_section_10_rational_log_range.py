"""Independent complete rational/log references for Section8.10 helper copies."""
import math,sys,json,random
from decimal import Decimal,localcontext
import section_8_10 as source

def observations():
    rows=[]
    def check(name,call,expected):
        try:
            value=call();actual=repr(value);ok=not isinstance(expected,str) and math.isfinite(value) and (value==expected if expected==0 else math.isclose(value,expected,rel_tol=4e-15,abs_tol=0))
            if ok and expected==0:ok=math.copysign(1,value)==math.copysign(1,expected)
        except Exception as exc:actual=type(exc).__name__;ok=actual==expected
        rows.append(dict(name=name,actual=actual,expected=expected if isinstance(expected,str) else repr(expected),passed=ok))
    tiny=math.ulp(0.);large=sys.float_info.max
    pairs=[(80.,84.),(1e308,1e-308),(1e-308,1e308),(tiny,large),(tiny,2*tiny),(large,tiny),(1e308,math.nextafter(1e308,math.inf)),(.1,math.nextafter(.1,math.inf)),(1.,1.),(1e-200,2e-200)]
    rng=random.Random(810)
    for _ in range(15):pairs.append((math.ldexp(rng.uniform(1,2),rng.randrange(-1000,1000)),math.ldexp(rng.uniform(1,2),rng.randrange(-1000,1000))))
    for i,(start,end) in enumerate(pairs):
        refs=[]
        for precision in [120,180]:
            with localcontext() as ctx:ctx.prec=precision;refs.append(float((Decimal.from_float(end)/Decimal.from_float(start)).ln()))
        assert refs[0]==refs[1];check('log pair'+str(i),lambda s=start,e=end:source.log_return(s,e),refs[0])
    bonds=[(110.,100.),(math.nextafter(1e308,math.inf),1e308),(1e308,1e200),(1e-308,1e-200),(tiny,large),(large,tiny),(1e308,1e308),(1.,1.)]
    for i,(cash,price) in enumerate(bonds):
        refs=[]
        for precision in [1600,2200]:
            with localcontext() as ctx:
                ctx.prec=precision;C,P=Decimal.from_float(cash),Decimal.from_float(price);refs.append([float((C-P)/P),float(-C/(P*P))])
        assert refs[0]==refs[1]
        for j,function in enumerate([source.bond_yield_from_price,source.bond_yield_price_derivative]):
            ref=refs[0][j];check('bond'+str(i)+' field'+str(j),lambda f=function,c=cash,p=price:f(c,p),ref if math.isfinite(ref) else 'ValueError')
    breaks=[(45.,15.,900.),(large,-large,large),(large,0.,1.),(1.,.5,tiny),(1e-200,0.,1e-308),(1.,math.nextafter(1.,0.),1e308),(1e308,0.,1e308)]
    for i,(price,cost,fixed) in enumerate(breaks):
        refs=[]
        for precision in [1600,2200]:
            with localcontext() as ctx:
                ctx.prec=precision;P,C,K=map(Decimal.from_float,(price,cost,fixed));D=P-C;refs.append([float(K/D),float(-K/(D*D))])
        assert refs[0]==refs[1]
        for j,function in enumerate([source.break_even_quantity,source.break_even_derivative]):
            ref=refs[0][j];check('break-even'+str(i)+' field'+str(j),lambda f=function,p=price,c=cost,k=fixed:f(p,c,k),ref if math.isfinite(ref) else 'ValueError')
    for name,call,error in [('log zero',lambda:source.log_return(0,1),'ValueError'),('log negative',lambda:source.log_return(1,-1),'ValueError'),('log bool first',lambda:source.log_return(True,float('nan')),'TypeError'),('log nonfinite',lambda:source.log_return(float('nan'),1),'ValueError'),('bond zero price',lambda:source.bond_yield_from_price(1,0),'ValueError'),('bond zero cash',lambda:source.bond_yield_from_price(0,1),'ValueError'),('bond bool',lambda:source.bond_yield_price_derivative(True,1),'TypeError'),('break zero fixed',lambda:source.break_even_quantity(2,1,0),'ValueError'),('break equal price',lambda:source.break_even_derivative(1,1,1),'ValueError'),('break nonfinite first',lambda:source.break_even_derivative(float('inf'),1,1),'ValueError')]:check(name,call,error)
    return rows
if __name__=='__main__':
    rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'rational/log predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
