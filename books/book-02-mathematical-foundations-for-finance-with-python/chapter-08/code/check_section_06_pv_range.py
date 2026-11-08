"""Independent range contracts for the local Section 8.6 PV/value sensitivity."""
import json,math,sys
from decimal import Decimal,localcontext
from functools import lru_cache
import section_8_06 as subject
T,M=math.ulp(0.),sys.float_info.max
NAMES=("present_value","pv_rate_first")

def zs(x):return int(math.copysign(1,x)) if x==0 else None

@lru_cache(maxsize=None)
def log(x,precision):
    with localcontext() as ctx:
        ctx.prec=precision
        return Decimal.from_float(x).ln()

def reference(args,kind,precision):
    c,r,t=map(float,args);factor=1. if kind==0 else -t
    negative=(math.copysign(1,c)<0)!=(math.copysign(1,factor)<0)
    if c==0 or factor==0:return -0. if negative else 0.
    with localcontext() as ctx:
        ctx.prec=precision
        a=log(abs(c),precision)+log(abs(factor),precision)-Decimal.from_float(r)*Decimal.from_float(t)
        if a>1000:return "ValueError"
        if a< -1000:return -0. if negative else 0.
        v=float(a.exp())
        if not math.isfinite(v):return "ValueError"
        return -v if negative else v

def observe(fn,args):
    try:
        v=fn(*args)
        return (v if math.isfinite(v) else repr(v)),zs(v),None
    except Exception as exc:return type(exc).__name__,None,str(exc)

def token(x):return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases=[(T,-.5,2000.),(2.,2.,375.),(M,-M/2,2*T),(0.,-M/2,M/2),
        (-0.,-M/2,M/2),(0.,M/2,M/2),(-0.,M/2,M/2),(M,M,M),
        (T,-M,M),(M,0.,M),(M,-0.,M),(M,-M,0.),(M,M,-0.),
        (T,0.,T),(T,T,T),(T,-T,M),(M,T,M),(M,-T,M),
        (10000.,.04,5.),(10000.,-.04,5.),(3.,-1.,708.),
        (3.,-1.,710.),(2.,2.,372.),(2.,2.,373.),(M,.5,2000.),
        (T,-.5,2900.),(T,-.5,3000.),(T,1.,0.),(M,1.,0.),
        (1.,-8e102,1e-100),(1.,.1,10.),(2.,math.nextafter(.1,0.),10.)]
    rows=[]
    for i,args in enumerate(cases):
        for kind,name in enumerate(NAMES):
            expected=reference(args,kind,1600);repeated=reference(args,kind,2200)
            assert expected==repeated and (isinstance(expected,str) or zs(expected)==zs(repeated))
            actual,sign,message=observe(getattr(subject,name),args)
            passed=actual==expected if isinstance(expected,str) else (
                type(actual) in (int,float) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0.) and sign==zs(expected))
            rows.append(dict(case=i,function=name,args=args,args_zero_signs=[zs(x) for x in args],
                expected=expected,expected_zero_sign=None if isinstance(expected,str) else zs(expected),
                actual=actual,actual_zero_sign=sign,exception_message=message,passed=passed))
    guards=[((True,.1,1.),"TypeError","payment"),((1.,True,1.),"TypeError","rate"),
        ((1.,.1,True),"TypeError","years"),((-1.,.1,1.),"ValueError","payment and years"),
        ((1.,.1,-1.),"ValueError","payment and years"),((math.inf,.1,1.),"ValueError","payment"),
        ((1.,math.nan,1.),"ValueError","rate"),((1.,.1,math.inf),"ValueError","years"),
        ((10**400,.1,1.),"ValueError","payment"),((1.,10**400,1.),"ValueError","rate"),
        ((1.,.1,10**400),"ValueError","years"),((0.,"bad",1.),"TypeError","rate"),
        ((0.,.1,-1.),"ValueError","payment and years")]
    for args,expected,prefix in guards:
        for name in NAMES:
            actual,sign,message=observe(getattr(subject,name),args)
            rows.append(dict(function=name,args=[token(x) for x in args],expected=expected,
                expected_message_prefix=prefix,actual=actual,exception_message=message,
                passed=actual==expected and message.startswith(prefix)))
    for name,prefix in zip(NAMES,("payment","years")):
        args=("bad",True,"bad");actual,sign,message=observe(getattr(subject,name),args)
        rows.append(dict(function=name,args=args,expected="TypeError",expected_message_prefix=prefix,
            actual=actual,exception_message=message,
            passed=actual=="TypeError" and message.startswith(prefix)))
    original=subject.present_value
    def forbidden(*args):raise AssertionError("first derivative called rounded present_value")
    subject.present_value=forbidden
    try:
        args=(2.,.125,4.);expected=reference(args,1,1600)
        actual,sign,message=observe(subject.pv_rate_first,args)
        rows.append(dict(contract="independent complete first sensitivity",expected=expected,
            actual=actual,exception_message=message,
            passed=type(actual) is float and math.isclose(actual,expected,rel_tol=4e-15)))
    finally:subject.present_value=original
    print(json.dumps(dict(reference="Independent complete log-amplitude at Decimal 1600/2200 digits",
        tolerance="4e-15 relative, no absolute floor; exact signs/error types",observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":run()
