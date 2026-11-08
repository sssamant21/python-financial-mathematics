"""Independent complete Section 8.5 PV/rate-sensitivity range checks."""
import json
import math
import sys
from decimal import Decimal, localcontext
from functools import lru_cache
import section_8_05 as subject
FUNCTIONS=("present_value","present_value_rate_derivative")
T,M=math.ulp(0.),sys.float_info.max

def zs(x):
    return int(math.copysign(1,x)) if x==0 else None

@lru_cache(maxsize=None)
def log(value,precision):
    with localcontext() as ctx:
        ctx.prec=precision
        return Decimal.from_float(value).ln()

def reference(args,kind,precision):
    c,r,t=map(float,args)
    factor=1. if kind==0 else -t
    negative=(math.copysign(1,c)<0)!=(math.copysign(1,factor)<0)
    if c==0 or factor==0:
        return -0. if negative else 0.
    with localcontext() as ctx:
        ctx.prec=precision
        amplitude=log(abs(c),precision)+log(abs(factor),precision)-Decimal.from_float(r)*Decimal.from_float(t)
        if amplitude>1000:return "ValueError"
        if amplitude< -1000:return -0. if negative else 0.
        result=float(amplitude.exp())
        if not math.isfinite(result):return "ValueError"
        return -result if negative else result

def observe(fn,args):
    try:
        value=fn(*args)
        return (value if math.isfinite(value) else repr(value)),zs(value),None
    except Exception as exc:
        return type(exc).__name__,None,str(exc)

def token(x):
    return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases=[
        (T,-1.,1000.),(1.,1.,750.),(M,-M,T),(0.,-M,M),
        (-0.,-M,M),(0.,M,M),(-0.,M,M),(M,M,M),(T,-M,M),
        (M,0.,M),(M,-0.,M),(M,-M,0.),(M,M,-0.),
        (T,0.,T),(T,T,T),(T,-T,M),(M,T,M),
        (5000.,.03,4.),(5000.,-.03,4.),(1.,-1.,709.),
        (1.,-1.,710.),(1.,1.,744.),(1.,1.,745.),
        (M,1.,1000.),(T,-1.,1450.),(T,-1.,1500.),
        (T,1.,0.),(M,1.,0.),(1.,.1,10.),
        (2.,math.nextafter(.1,0.),10.),(T,-T,T),(1.,M,T)]
    rows=[]
    for i,args in enumerate(cases):
        for kind,name in enumerate(FUNCTIONS):
            expected=reference(args,kind,1600)
            other=reference(args,kind,2200)
            assert expected==other and (isinstance(expected,str) or zs(expected)==zs(other))
            actual,sign,message=observe(getattr(subject,name),args)
            passed=actual==expected if isinstance(expected,str) else (
                type(actual) in (float,int) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0.) and sign==zs(expected))
            rows.append(dict(case=i,function=name,args=args,expected=expected,
                expected_zero_sign=None if isinstance(expected,str) else zs(expected),
                actual=actual,actual_zero_sign=sign,exception_message=message,passed=passed))
    guards=[
        ((True,.1,1.),"TypeError","payment"),((1.,True,1.),"TypeError","rate"),
        ((1.,.1,True),"TypeError","years"),
        ((-1.,.1,1.),"ValueError","payment and years"),
        ((1.,.1,-1.),"ValueError","payment and years"),
        ((math.inf,.1,1.),"ValueError","payment"),
        ((1.,math.nan,1.),"ValueError","rate"),
        ((1.,.1,math.inf),"ValueError","years"),
        ((10**400,.1,1.),"ValueError","payment"),
        ((1.,10**400,1.),"ValueError","rate"),
        ((1.,.1,10**400),"ValueError","years"),
        ((0.,"bad",1.),"TypeError","rate"),
        ((0.,.1,-1.),"ValueError","payment and years")]
    for args,expected,prefix in guards:
        for name in FUNCTIONS:
            actual,sign,message=observe(getattr(subject,name),args)
            rows.append(dict(function=name,args=[token(x) for x in args],expected=expected,
                expected_message_prefix=prefix,actual=actual,exception_message=message,
                passed=actual==expected and message.startswith(prefix)))
    for name,prefix in zip(FUNCTIONS,("payment","years")):
        args=("bad",True,"bad")
        actual,sign,message=observe(getattr(subject,name),args)
        rows.append(dict(function=name,args=args,expected="TypeError",expected_message_prefix=prefix,
            actual=actual,exception_message=message,passed=actual=="TypeError" and message.startswith(prefix)))
    original=subject.present_value
    def forbidden(*args):
        raise AssertionError("sensitivity called rounded present_value")
    subject.present_value=forbidden
    try:
        args=(2.,.125,4.)
        expected=reference(args,1,1600)
        actual,sign,message=observe(subject.present_value_rate_derivative,args)
        rows.append(dict(function=FUNCTIONS[1],contract="independent complete sensitivity",
            expected=expected,actual=actual,exception_message=message,
            passed=type(actual) is float and math.isclose(actual,expected,rel_tol=4e-15)))
    finally:
        subject.present_value=original
    print(json.dumps(dict(reference="Independent log-amplitude at 1600/2200 digits with signed-zero identities",
        tolerance="4e-15 relative, no absolute floor, exact zero signs/error types",observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":
    run()
