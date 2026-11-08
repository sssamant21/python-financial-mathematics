"""Section 8.6 curvature: independent log-amplitude references and public guards."""
import json,math,sys
from decimal import Decimal,localcontext
from functools import lru_cache
import section_8_06 as subject
T,M=math.ulp(0.),sys.float_info.max

def zs(x):return int(math.copysign(1,x)) if x==0 else None

@lru_cache(maxsize=None)
def log(x,precision):
    with localcontext() as ctx:
        ctx.prec=precision
        return Decimal.from_float(x).ln()

def reference(args,precision):
    c,r,t=map(float,args)
    if c==0 or t==0:return math.copysign(0.,c)
    with localcontext() as ctx:
        ctx.prec=precision
        amplitude=log(c,precision)+2*log(abs(t),precision)-Decimal.from_float(r)*Decimal.from_float(t)
        if amplitude>1000:return "ValueError"
        if amplitude< -1000:return 0.
        value=float(amplitude.exp())
        return value if math.isfinite(value) else "ValueError"

def observe(args):
    try:
        v=subject.pv_rate_second(*args)
        return (v if math.isfinite(v) else repr(v)),zs(v),None
    except Exception as exc:return type(exc).__name__,None,str(exc)

def token(x):return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases=[(1.,1.,750.),(T,-1.,1000.),(M,M,M),(0.,-M,M),(M,0.,1e-200),(T,0.,M),
        (-0.,-M,M),(0.,M,M),(-0.,M,M),(M,0.,0.),(M,0.,-0.),(-0.,0.,-0.),
        (M,-M,0.),(1.,0.,T),(T,0.,T),(M,T,M),(M,-T,M),
        (10000.,.04,5.),(10000.,-.04,5.),(1.,-1.,700.),(1.,1.,744.),
        (1.,1.,745.),(1.,1.,746.),(M,1.,1000.),(T,-1.,1450.),(T,-1.,1500.),
        (M,M,T),(T,T,M),(1.,0.,1.),(1.,.1,10.),(1.,-M,M),(T,0.,1e200)]
    rows=[]
    for i,args in enumerate(cases):
        expected=reference(args,1600);repeated=reference(args,2200)
        assert expected==repeated and (isinstance(expected,str) or zs(expected)==zs(repeated))
        actual,sign,message=observe(args)
        passed=actual==expected if isinstance(expected,str) else (
            type(actual) in (int,float) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0.) and sign==zs(expected))
        rows.append(dict(case=i,args=args,args_zero_signs=[zs(x) for x in args],expected=expected,
            expected_zero_sign=None if isinstance(expected,str) else zs(expected),actual=actual,
            actual_zero_sign=sign,exception_message=message,passed=passed))
    guards=[((True,.1,1.),"TypeError","payment"),((1.,True,1.),"TypeError","rate"),
        ((1.,.1,True),"TypeError","years"),((-1.,.1,1.),"ValueError","payment and years"),
        ((1.,.1,-1.),"ValueError","payment and years"),((math.inf,.1,1.),"ValueError","payment"),
        ((1.,math.nan,1.),"ValueError","rate"),((1.,.1,math.inf),"ValueError","years"),
        ((10**400,.1,1.),"ValueError","payment"),((1.,10**400,1.),"ValueError","rate"),
        ((1.,.1,10**400),"ValueError","years"),((0.,"bad",1.),"TypeError","rate"),
        ((0.,.1,-1.),"ValueError","payment and years"),(("bad",True,"bad"),"TypeError","years"),
        (("bad",True,1.),"TypeError","payment"),((0.,True,-1.),"TypeError","rate")]
    for args,expected,prefix in guards:
        actual,sign,message=observe(args)
        rows.append(dict(args=[token(x) for x in args],expected=expected,expected_message_prefix=prefix,
            actual=actual,exception_message=message,passed=actual==expected and message.startswith(prefix)))
    original=subject.present_value
    def forbidden(*args):raise AssertionError("curvature called rounded present_value")
    subject.present_value=forbidden
    try:
        args=(2.,.125,4.);expected=reference(args,1600)
        actual,sign,message=observe(args)
        rows.append(dict(contract="complete curvature independent of rounded PV",expected=expected,
            actual=actual,exception_message=message,
            passed=type(actual) is float and math.isclose(actual,expected,rel_tol=4e-15)))
    finally:subject.present_value=original
    print(json.dumps(dict(reference="Independent log-amplitude ln(C)+2*ln(t)-r*t at Decimal 1600/2200 digits",
        tolerance="4e-15 relative, no absolute floor; exact zero signs/error types",observations=rows),
        indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":run()
