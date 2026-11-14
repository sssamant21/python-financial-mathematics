"""Independent epsilon-root suggestions and represented-grid contracts; not optimality."""
import math,sys
from decimal import Decimal,localcontext
import section_8_08 as source

def root(epsilon,n,precision):
    # Newton iteration on z**n=epsilon; no floating fractional power oracle.
    with localcontext() as c:
        c.prec=precision
        z=Decimal(1)/Decimal(2)**(52//n)
        for _ in range(30):
            next_z=((n-1)*z+epsilon/(z**(n-1)))/n
            if next_z==z:break
            z=next_z
        return +z

def observations():
    rows=[]
    with localcontext() as c:
        c.prec=160
        eps=Decimal(1)/Decimal(2**52)
    roots={n:(root(eps,n,100),root(eps,n,160)) for n in (3,4)}
    def add(name,actual,expected,ok):rows.append(dict(name=name,actual=actual,expected=expected,passed=ok))
    vectors=[(0.,None),(-0.,None),(1e-308,None),(-1e-308,None),(1.,None),(-1.,None),(2.,None),(-2.,None),(1e100,None),(-1e100,None),(1e300,None),(-1e300,None),(0.,1e-300),(0.,1e300),(1.,2.),(-1.,2.)]
    for order in (1,2):
        n=order+2
        for i,(x,scale) in enumerate(vectors):
            s=max(1.,abs(x)) if scale is None else scale
            refs=[]
            for precision,z in zip((100,160),roots[n]):
                with localcontext() as c:
                    c.prec=precision;refs.append(float(Decimal.from_float(s)*z))
            assert refs[0]==refs[1]
            h=source.suggested_step(x,order,scale);expected=refs[0]
            add(f'root reference order{order} case{i}',repr(h),repr(expected),math.isclose(h,expected,rel_tol=4e-15,abs_tol=0))
            add(f'finite distinct symmetric gate order{order} case{i}',[repr(x+h),repr(x-h)],'finite and both distinct from x',h>0 and math.isfinite(h) and math.isfinite(x+h) and math.isfinite(x-h) and x+h!=x and x-h!=x)
    # Validation order and scale resources are observed separately from arithmetic.
    cases=[('x priority',(True,False,True),TypeError,'x'),('order priority',(0.,False,True),ValueError,'derivative_order'),('order float',(0.,1.,None),ValueError,'derivative_order'),('order range',(0.,3,None),ValueError,'derivative_order'),('scale type',(0.,1,True),TypeError,'scale'),('zero scale',(0.,1,0.),ValueError,'scale'),('negative scale',(0.,1,-1.),ValueError,'scale'),('nonfinite x',(float('inf'),1,None),ValueError,'x'),('nonfinite scale',(0.,1,float('nan')),ValueError,'scale'),('scale conversion range',(0.,1,10**1000),ValueError,'scale'),('subnormal step underflow',(0.,1,5e-324),ValueError,'step'),('collapsed explicit scale',(1e300,1,1.),ValueError,'step'),('finite perturbation range',(sys.float_info.max,1,None),ValueError,'step')]
    for name,args,error,prefix in cases:
        try:source.suggested_step(*args);actual='returned';ok=False;message=''
        except Exception as exc:actual=type(exc).__name__;message=str(exc);ok=type(exc) is error and message.startswith(prefix)
        add(name,dict(error=actual,message=message),dict(error=error.__name__,message_prefix=prefix),ok)
    return rows
if __name__=='__main__':
    import json
    rows=observations();print(json.dumps(rows,indent=2))
    assert all(x['passed'] for x in rows)
    print(len(rows),'suggested-step predicates passed')
