"""Section 8.5 centered copy: exact sampled quotients and actual callback contracts."""
import json,math,sys
from fractions import Fraction
import section_8_05 as subject
T,M=math.ulp(0.),sys.float_info.max

def zs(x):return int(math.copysign(1,x)) if x==0 else None

def token(x):return repr(x) if type(x) is float and not math.isfinite(x) else x

def result(first,second,h):
    if first==second:return (first-second)*(-1. if h<0 else 1.)
    try:return float((Fraction(first)-Fraction(second))/(2*Fraction(h)))
    except OverflowError:return "ValueError"

def observed(function,x,h,default=False):
    try:
        v=subject.centered_difference(function,x) if default else subject.centered_difference(function,x,h)
        return (v if math.isfinite(v) else repr(v)),zs(v),None,None
    except Exception as exc:return type(exc).__name__,None,str(exc),exc

def row_numeric(name,x,h,first,second,default=False):
    step=1e-4 if default else h
    points=[x+step,x-step];calls=[]
    def callback(z):
        i=len(calls);calls.append(z);return (first,second)[i]
    expected=result(first,second,step)
    actual,sign,message,exc=observed(callback,x,h,default)
    passed=(actual==expected if isinstance(expected,str) else
            type(actual) in (float,int) and actual==expected and sign==zs(expected))
    return dict(case=name,x=x,step=None if default else h,callback_outputs=[first,second],
        output_zero_signs=[zs(first),zs(second)],expected=expected,
        expected_zero_sign=None if isinstance(expected,str) else zs(expected),
        expected_calls=points,actual=actual,actual_zero_sign=sign,actual_calls=calls,
        exception_message=message,passed=passed and calls==points)

def run():
    rows=[]
    specs=[(M,M,-M),(-M,-M,M),(1.,M,-M),(-1.,-M,M),(1.,M,0.),
           (T,T,-T),(-T,-T,T),(T,M,-M),(M,T,0.),(-M,T,0.),
           (1.,0.,-0.),(-1.,0.,-0.),(1.,-0.,0.),(-1.,-0.,0.),
           (M,M,M),(-M,M,M)]
    for i,(h,a,b) in enumerate(specs):rows.append(row_numeric("outputs-"+str(i),0.,h,a,b))
    # Default identity samples are rounded points; reference is not the analytic derivative.
    h=1e-4;x=1.
    rows.append(row_numeric("default",x,h,x+h,x-h,True))
    for x,h in ((1.,.1),(-3.,.125),(0.,T),(0.,-T)):
        rows.append(row_numeric("identity",x,h,x+h,x-h))
    for i,(x,h) in enumerate(((1.,T),(1.,-T),(1.,math.ulp(1.)/2),
                              (1.,-math.ulp(1.)/2),(M,M),(-M,M),(1.,0.),(1.,-0.))):
        calls=[]
        def identity(z):calls.append(token(z));return z
        actual,sign,message,exc=observed(identity,x,h)
        rows.append(dict(case="preflight-"+str(i),x=x,step=h,expected="ValueError",
            expected_calls=[],actual=actual,actual_calls=calls,exception_message=message,
            passed=actual=="ValueError" and calls==[]))
    for bad in (math.inf,math.nan,True,"bad"):
        for which in (0,1):
            calls=[]
            def callback(z):
                i=len(calls);calls.append(z)
                return bad if i==which else 0.
            actual,sign,message,exc=observed(callback,0.,1.)
            expected="TypeError" if type(bad) in (bool,str) else "ValueError"
            prefix="f(x+h)" if which==0 else "f(x-h)"
            rows.append(dict(case="invalid-output",output=token(bad),position=which,
                expected=expected,expected_calls=[1.,-1.][:which+1],actual=actual,
                actual_calls=calls,exception_message=message,
                passed=actual==expected and calls==[1.,-1.][:which+1] and message.startswith(prefix)))
    for which in (0,1):
        calls=[];sentinel=RuntimeError("original callback exception")
        def callback(z):
            i=len(calls);calls.append(z)
            if i==which:raise sentinel
            return 0.
        actual,sign,message,exc=observed(callback,0.,1.)
        rows.append(dict(case="callback-exception",position=which,expected="RuntimeError",
            expected_calls=[1.,-1.][:which+1],actual=actual,actual_calls=calls,
            same_exception=exc is sentinel,
            passed=exc is sentinel and calls==[1.,-1.][:which+1]))
    guards=[(None,True,"bad","TypeError","function"),
            ("bad",0.,0.,"TypeError","function"),
            (lambda z:z,True,"bad","TypeError","x"),
            (lambda z:z,1.,True,"TypeError","step"),
            (lambda z:z,math.inf,0.,"ValueError","x"),
            (lambda z:z,1.,math.inf,"ValueError","step"),
            (lambda z:z,10**400,1.,"ValueError","x"),
            (lambda z:z,1.,10**400,"ValueError","step")]
    for fn,x,h,expected,prefix in guards:
        calls=[]
        if callable(fn):
            def callback(z):calls.append(z);return z
        else:callback=fn
        actual,sign,message,exc=observed(callback,x,h)
        rows.append(dict(case="input-priority",x=token(x),step=token(h),expected=expected,
            expected_message_prefix=prefix,actual=actual,actual_calls=calls,exception_message=message,
            passed=actual==expected and calls==[] and message.startswith(prefix)))
    print(json.dumps(dict(reference="Exact rational sampled-output quotient; explicit signed-zero, preflight and callback contracts",
        tolerance="Exact final float equality, zero signs, exception identity and call traces",
        observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":run()
