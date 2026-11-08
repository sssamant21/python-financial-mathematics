"""Implicit ratios and complete centered sampled quotient contracts."""
import math,random
from fractions import Fraction
import section_8_07 as source

def observations():
    rows=[]
    def expect(name,call,ref=None,error=None,trace=None,want_trace=None):
        try:
            actual=call();ok=error is None and actual==ref
            if ok and actual==0:ok=math.copysign(1.,actual)==math.copysign(1.,ref)
            result=repr(actual)
        except Exception as exc:result=type(exc).__name__;ok=type(exc) is error
        if trace is not None:ok=ok and trace==want_trace
        rows.append(dict(name=name,actual=result,expected=error.__name__ if error else repr(ref),passed=ok,trace=trace))
    vectors=[(1e308,1e-308,1.,1.),(1e-308,1e308,1.,1.),(3.,4.,1.,1.),(1e200,1e200,1e200,1e200),(1e-200,1e-200,1e-200,1e-200),(-0.,-1.,1e308,5e-324),(0.,1.,1.,1.)]
    rng=random.Random(8074)
    for _ in range(40):vectors.append((math.ldexp(rng.uniform(-1,1),rng.randrange(-800,800)),math.ldexp(rng.choice([-1.,1.]),rng.randrange(-800,800)),math.ldexp(rng.uniform(1,2),rng.randrange(-800,800)),math.ldexp(rng.uniform(1,2),rng.randrange(-800,800))))
    for j,(x,y,a,b) in enumerate(vectors):
        for name,args,exact in [('circle_slope',(x,y),-Fraction(x)/Fraction(y)),('exposure_slope',(x,y,a,b),-Fraction(a)*Fraction(x)/(Fraction(b)*Fraction(y)))]:
            try:
                ref=(-x/y) if x==0 else float(exact)
                if not math.isfinite(ref):raise OverflowError
                error=None
            except OverflowError:ref=None;error=ValueError
            expect(name+' '+str(j),lambda:getattr(source,name)(*args),ref,error)
    sampled=[(0.,1e308,1e308,-1e308),(0.,5e-324,5e-324,-5e-324),(0.,-1e308,1e308,-1e308),(1.,.25,1.5625,.5625),(0.,1.,-0.,0.),(0.,-1.,1.,1.),(0.,.5,1e308,-1e308)]
    for _ in range(35):sampled.append((0.,math.ldexp(rng.choice([-1.,1.]),rng.randrange(-800,800)),math.ldexp(rng.uniform(-1,1),rng.randrange(-800,800)),math.ldexp(rng.uniform(-1,1),rng.randrange(-800,800))))
    for j,(x,h,first,last) in enumerate(sampled):
        exact=(Fraction(first)-Fraction(last))/(2*Fraction(h))
        try:
            ref=(first-last)/math.copysign(1.,h) if exact==0 else float(exact)
            if not math.isfinite(ref):raise OverflowError
            error=None
        except OverflowError:ref=None;error=ValueError
        trace=[];it=iter([first,last])
        def cb(z):trace.append(z);return next(it)
        expect('centered '+str(j),lambda:source.centered_difference(cb,x,h),ref,error,trace,[x+h,x-h])
    for name,call,error in [('circle zero y',lambda:source.circle_slope(1,0),ValueError),('circle x priority',lambda:source.circle_slope(True,0),TypeError),('exposure zero y',lambda:source.exposure_slope(1,0,1,1),ValueError),('exposure bad a',lambda:source.exposure_slope(1,1,0,1),ValueError),('exposure bad b',lambda:source.exposure_slope(1,1,1,-1),ValueError),('exposure x priority',lambda:source.exposure_slope(True,1,1,0),TypeError),('callable first',lambda:source.centered_difference(None,float('nan'),0),TypeError)]:expect(name,call,error=error)
    for x,h in [(1.,1e-30),(1e308,1e308),(0.,0.),(0.,float('inf'))]:
        trace=[]
        def cb(z):trace.append(z);return 1.
        expect('preflight '+repr((x,h)),lambda:source.centered_difference(cb,x,h),error=ValueError,trace=trace,want_trace=[])
    for values,kind,n in [([True,1.],TypeError,1),([1.,float('nan')],ValueError,2)]:
        trace=[];it=iter(values)
        def cb(z):trace.append(z);return next(it)
        expect('invalid sample '+repr(values),lambda:source.centered_difference(cb,0,1),error=kind,trace=trace,want_trace=[1.,-1.][:n])
    trace=[]
    def broken(z):trace.append(z);raise RuntimeError('sentinel')
    expect('callback exception',lambda:source.centered_difference(broken,0,1),error=RuntimeError,trace=trace,want_trace=[1.])
    trace=[]
    def identity(z):trace.append(z);return z
    expect('default step',lambda:source.centered_difference(identity,0),1.,trace=trace,want_trace=[1e-4,-1e-4])
    return rows
if __name__=='__main__':
    rows=observations()
    for row in rows:assert row['passed'],row
    print(len(rows),'implicit-ratio/centered predicates passed')
