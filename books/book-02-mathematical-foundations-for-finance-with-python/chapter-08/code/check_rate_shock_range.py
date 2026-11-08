"""Section 8.5 rate shock: independent difference-of-prices oracle."""
import json,math,sys
from decimal import Decimal,localcontext
import section_8_05 as subject
T,M=math.ulp(0.),sys.float_info.max

def zs(x):
    return int(math.copysign(1,x)) if x==0 else None

def reference(args,precision):
    c,r,t,h=map(float,args)
    direction=-math.copysign(1,c)*math.copysign(1,t)*math.copysign(1,h)
    if c==0 or t==0 or h==0:return math.copysign(0.,direction)
    with localcontext() as ctx:
        ctx.prec=precision
        dc,dr,dt,dh=map(Decimal.from_float,(c,r,t,h))
        before=-dr*dt
        after=-(dr+dh)*dt
        high=max(before,after)
        # With C >= min-subnormal and |t*h| >= min-subnormal**2,
        # this exponent cannot be offset into a finite binary64 difference.
        if high>10000:return "ValueError"
        if high< -10000:return math.copysign(0.,direction)
        def exp(x):return Decimal(0) if x< -20000 else x.exp()
        result=float(dc*(exp(after)-exp(before)))
        if not math.isfinite(result):return "ValueError"
        return math.copysign(0.,direction) if result==0 else result

def observe(args):
    try:
        value=subject.present_value_rate_shock(*args)
        return (value if math.isfinite(value) else repr(value)),zs(value),None
    except Exception as exc:return type(exc).__name__,None,str(exc)

def token(x):
    return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases=[
        (1.,1.,1000.,-1.),(M,-M,T,M),(M,0.,T,.1),(0.,0.,M,-M),
        (M,0.,T,-.1),(T,-1.,1000.,1.),(1.,1.,750.,-1.),
        (M,0.,M,T),(M,0.,M,-T),(M,M,M,-M),(M,M,M,-M/2),
        (M,-M,M,M),(1.,M,T,M),(1.,-M,T,-M),
        (5000.,.03,4.,.0001),(5000.,.03,4.,-.0001),
        (1.,0.,1.,T),(1.,0.,T,T),(M,0.,T,T),
        (M,-M,M,0.),(M,-M,M,-0.),(M,-M,0.,M),(M,-M,-0.,M),
        (-0.,0.,M,-M),(0.,0.,M,M),(-0.,0.,M,M),
        (1.,1.,1000.,1.),(1.,-1.,710.,1.),(1.,-1.,709.,1.),
        (T,-1.,1500.,1.),(T,-1.,1000.,-1.),
        (1.,0.,1.,math.nextafter(0.,1.)),(1.,.1,10.,.1),
        (1.,.1,10.,-.1),(M,0.,M,M),(M,0.,M,-M)]
    rows=[]
    for i,args in enumerate(cases):
        expected=reference(args,1600);other=reference(args,2200)
        assert expected==other and (isinstance(expected,str) or zs(expected)==zs(other))
        actual,sign,message=observe(args)
        passed=actual==expected if isinstance(expected,str) else (
            type(actual) in (float,int) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0.) and sign==zs(expected))
        rows.append(dict(case=i,args=args,args_zero_signs=[zs(x) for x in args],
            expected=expected,expected_zero_sign=None if isinstance(expected,str) else zs(expected),
            actual=actual,actual_zero_sign=sign,exception_message=message,passed=passed))
    guards=[
        ((True,.1,1.,.1),"TypeError","payment"),
        ((1.,True,1.,.1),"TypeError","rate"),
        ((1.,.1,True,.1),"TypeError","years"),
        ((1.,.1,1.,True),"TypeError","change"),
        ((-1.,.1,1.,.1),"ValueError","payment and years"),
        ((1.,.1,-1.,.1),"ValueError","payment and years"),
        ((math.inf,.1,1.,.1),"ValueError","payment"),
        ((1.,math.nan,1.,.1),"ValueError","rate"),
        ((1.,.1,math.inf,.1),"ValueError","years"),
        ((1.,.1,1.,math.inf),"ValueError","change"),
        ((10**400,.1,1.,.1),"ValueError","payment"),
        ((1.,10**400,1.,.1),"ValueError","rate"),
        ((1.,.1,10**400,.1),"ValueError","years"),
        ((1.,.1,1.,10**400),"ValueError","change"),
        ((0.,"bad",1.,0.),"TypeError","rate"),
        ((0.,.1,-1.,0.),"ValueError","payment and years"),
        (("bad",True,"bad","bad"),"TypeError","years"),
        (("bad",True,1.,"bad"),"TypeError","change"),
        (("bad",True,1.,1.),"TypeError","payment"),
        ((1.,True,-1.,1.),"TypeError","rate")]
    for args,expected,prefix in guards:
        actual,sign,message=observe(args)
        rows.append(dict(args=[token(x) for x in args],expected=expected,
            expected_message_prefix=prefix,actual=actual,exception_message=message,
            passed=actual==expected and message.startswith(prefix)))
    original=subject.present_value
    def forbidden(*args):raise AssertionError("shock called rounded present_value")
    subject.present_value=forbidden
    try:
        args=(2.,.125,4.,.125);expected=reference(args,1600)
        actual,sign,message=observe(args)
        rows.append(dict(contract="complete change independent of rounded PV",expected=expected,
            actual=actual,exception_message=message,
            passed=type(actual) is float and math.isclose(actual,expected,rel_tol=4e-15)))
    finally:subject.present_value=original
    print(json.dumps(dict(reference="Independent difference of complete Decimal prices at 1600/2200 digits",
        tolerance="4e-15 relative, no absolute floor; exact signs and error types",observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":run()
