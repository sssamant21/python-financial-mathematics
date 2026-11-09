"""Complete represented sampled quotients;not analytical derivative accuracy."""
import math,random
from fractions import Fraction as F
import section_8_08 as source

def observations():
    rows=[]
    def emit(name,actual,ref,ok,trace):rows.append(dict(name=name,actual=repr(actual),expected=repr(ref),passed=bool(ok),trace=trace))
    vectors=[(0.,2.,[1e308,-1e308,1e308]),(0.,1e308,[1e308,-1e308,1e308]),(0.,1e-200,[1.,1.,1.]),(1.,.25,[1.5625,1.,.5625]),(0.,1.,[-0.,0.,-0.])]
    rng=random.Random(808)
    for _ in range(30):vectors.append((0.,math.ldexp(1.,rng.randrange(-800,800)),[math.ldexp(rng.uniform(-1,1),rng.randrange(-800,800)) for _ in range(3)]))
    for j,(x,h,values) in enumerate(vectors):
        for name,weights,den,points in [('forward_difference',(1,-1),F(h),[x+h,x]),('backward_difference',(1,-1),F(h),[x,x-h]),('centered_difference',(1,-1),2*F(h),[x+h,x-h]),('second_difference',(1,-2,1),F(h)**2,[x+h,x,x-h])]:
            selected=values[:len(weights)];exact=sum(F(y)*w for y,w in zip(selected,weights))/den
            try:
                ref=(selected[0]-selected[1]) if exact==0 and len(weights)==2 else float(exact)
                if not math.isfinite(ref):raise OverflowError
                error=None
            except OverflowError:ref=ValueError;error=ValueError
            trace=[];it=iter(selected)
            def cb(z):trace.append(z);return next(it)
            try:
                actual=getattr(source,name)(cb,x,h);ok=error is None and actual==ref
                if ok and actual==0:ok=math.copysign(1,actual)==math.copysign(1,ref)
            except Exception as exc:actual=type(exc);ok=type(exc) is error
            emit(name+' '+str(j),actual,ref,ok and trace==points,trace)
    rich=[(.5,[1e308,0.,-5e307,0.]),(2.**-1024,[4.,0.,.5,0.]),(.25,[2.5e307,-2.5e307,1.25e307,-1.25e307])]
    for j,(h,values) in enumerate(rich):
        half=h/2;coarse=(F(values[0])-F(values[1]))/(2*F(h));fine=(F(values[2])-F(values[3]))/(2*F(half));exact=(4*fine-coarse)/3
        try:ref=float(exact);error=None
        except OverflowError:ref=ValueError;error=ValueError
        trace=[];it=iter(values)
        def cb(z):trace.append(z);return next(it)
        try:actual=source.richardson_first(cb,0.,h);ok=error is None and actual==ref
        except Exception as exc:actual=type(exc);ok=type(exc) is error
        emit('Richardson '+str(j),actual,ref,ok and trace==[h,-h,half,-half],trace)
    methods=['forward_difference','backward_difference','centered_difference','second_difference','richardson_first']
    for name in methods:
        for x,h,error in [(1.,0.,ValueError),(1.,-.1,ValueError),(1.,1e-30,ValueError),(1e308,1e308,ValueError),(True,.1,TypeError)]:
            trace=[]
            def cb(z):trace.append(z);return z
            try:actual=getattr(source,name)(cb,x,h);ok=False
            except Exception as exc:actual=type(exc);ok=type(exc) is error
            emit(name+' invalid '+repr((x,h)),actual,error,ok and not trace,trace)
        try:actual=getattr(source,name)(None,1.,0.);ok=False
        except ValueError:actual=ValueError;ok=True
        emit(name+' controls before callable',actual,ValueError,ok,[])
        trace=[]
        def bad(z):trace.append(z);return True
        try:actual=getattr(source,name)(bad,0.,.25);ok=False
        except TypeError:actual=TypeError;ok=True
        emit(name+' first invalid sample',actual,TypeError,ok and len(trace)==1,trace)
    trace=[]
    def cb(z):trace.append(z);return z
    try:actual=source.richardson_first(cb,1.,2.**-52);ok=False
    except ValueError:actual=ValueError;ok=True
    emit('Richardson halfstep priority',actual,ValueError,ok and trace==[1.+2.**-52,1.-2.**-52],trace)
    return rows
if __name__=='__main__':
    rows=observations()
    for row in rows:assert row['passed'],row
    print(len(rows),'complete quotient/Richardson predicates passed')
