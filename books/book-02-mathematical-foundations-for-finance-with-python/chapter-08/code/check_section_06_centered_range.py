"""Sampled quotient reference and callback contract; not derivative accuracy."""
import math,random
from fractions import Fraction
import section_8_06 as source

def observations():
    rows=[]
    def save(name,actual,expected,passed,trace):rows.append(dict(name=name,actual=repr(actual),expected=repr(expected),passed=bool(passed),trace=trace))
    cases=[('constant huge',0.,1.,[1e308]*3),('finite overflowing numerator',0.,2.,[1e308,0.,1e308]),('true overflow',0.,.5,[1e308,-1e308,1e308]),('tiny denominator',0.,1e-200,[1e-300,0.,1e-300]),('huge denominator',0.,1e200,[1e308,0.,1e308]),('tiny zero',0.,1e-200,[1.,1.,1.]),('negative step',0.,-2.,[1e308,0.,1e308]),('negative underflow',0.,1e150,[-5e-324,0.,0.]),('ordinary',1.,.25,[1.5625,1.,.5625]),('default step',1.,1e-3,[1.,1.,1.])]
    rng=random.Random(8062)
    for j in range(50):cases.append(('seeded '+str(j),0.,math.ldexp(1.,rng.randrange(-500,501)),[math.ldexp(rng.uniform(-1,1),rng.randrange(-500,501)) for _ in range(3)]))
    for name,x,h,values in cases:
        # Direct signed weighted sum, exact represented samples and exact h².
        exact=sum(Fraction(v)*w for v,w in zip(values,(1,-2,1)))/Fraction(h)**2
        try:
            expected=float(exact)
            if not math.isfinite(expected):raise OverflowError
            error=None
        except OverflowError:expected=ValueError;error=ValueError
        trace=[];iterator=iter(values)
        def callback(z):trace.append(z);return next(iterator)
        try:
            actual=source.centered_second_difference(callback,x) if name=='default step' else source.centered_second_difference(callback,x,h)
            ok=error is None and actual==expected
            if ok and actual==0:ok=math.copysign(1,actual)==math.copysign(1,expected)
        except Exception as exc:actual=type(exc);ok=type(exc) is error
        ok=ok and trace==[x+h,x,x-h]
        save(name,actual,expected,ok,trace)
    controls=[('callable first',None,float('nan'),0.,TypeError),('zero step',True,0.,0.,ValueError),('bool x',True,True,1.,TypeError),('collapsed',True,1.,1e-20,ValueError),('overflow perturbation',True,1e308,1e308,ValueError),('nonfinite step',True,0.,float('inf'),ValueError)]
    for name,callable_flag,x,h,error in controls:
        trace=[]
        def cb(z):trace.append(z);return 0.
        try:actual=source.centered_second_difference(cb if callable_flag else None,x,h);ok=False
        except Exception as exc:actual=type(exc);ok=type(exc) is error
        save(name,actual,error,ok and not trace,trace)
    for name,seq,error,count in [('bad first',[True,0,0],TypeError,1),('bad center',[1,float('nan'),0],ValueError,2),('bad last',[1,0,10**1000],ValueError,3)]:
        trace=[];it=iter(seq)
        def cb(z):trace.append(z);return next(it)
        try:actual=source.centered_second_difference(cb,0,1);ok=False
        except Exception as exc:actual=type(exc);ok=type(exc) is error
        save(name,actual,error,ok and len(trace)==count,trace)
    trace=[]
    def broken(z):trace.append(z);raise RuntimeError('callback sentinel')
    try:actual=source.centered_second_difference(broken,0,1);ok=False
    except RuntimeError as exc:actual=str(exc);ok=actual=='callback sentinel'
    save('callback exception',actual,'callback sentinel',ok and trace==[1.],trace)
    return rows
if __name__=='__main__':
    rows=observations()
    for row in rows:assert row['passed'],row
    print(len(rows),'sampled quotient and callback predicates passed')
