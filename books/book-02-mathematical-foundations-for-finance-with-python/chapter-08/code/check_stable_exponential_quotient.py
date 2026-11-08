"""Independent complete exponential-difference quotient references."""
import json,math,sys
from decimal import Decimal,localcontext
import section_8_05 as subject
T,M=math.ulp(0.),sys.float_info.max

def zs(x):return int(math.copysign(1,x)) if x==0 else None

def reference(x,h,precision):
    with localcontext() as ctx:
        ctx.prec=precision
        dx,dh=map(Decimal.from_float,(float(x),float(h)))
        before,after=dx,dx+dh
        high=max(before,after)
        if high>10000:return "ValueError"
        if high< -10000:return 0.
        def exp(v):return Decimal(0) if v< -20000 else v.exp()
        value=float((exp(after)-exp(before))/dh)
        if not math.isfinite(value):return "ValueError"
        return 0. if value==0 else value

def observe(args):
    try:
        value=subject.stable_exponential_difference_quotient(*args)
        return (value if math.isfinite(value) else repr(value)),zs(value),None
    except Exception as exc:return type(exc).__name__,None,str(exc)

def token(x):return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases=[(1000.,-M),(-1000.,1000.),(-750.,100.),(700.,10.),(0.,T),(700.,-M),
        (-M,M),(-M,math.nextafter(M,0.)),(-M,M/2),(M,-M),(0.,M),(0.,-M),
        (709.,1.),(710.,-1.),(711.,-1.),(709.,2.),(708.,2.),
        (M,T),(-M,T),(0.,-T),(T,T),(-T,-T),(744.,-M),(-744.,-M),
        (745.,-M),(-745.,1.),(-10000.,1.),(-10001.,1.),(10000.,-M),(10001.,-M)]
    for x in (-700.,0.,.3,700.):
        for h in (1e-300,-1e-300,1e-10,-1e-10,.1,-.1):
            cases.append((x,h))
    rows=[]
    for i,args in enumerate(cases):
        expected=reference(*args,1600);other=reference(*args,2200)
        assert expected==other and (isinstance(expected,str) or zs(expected)==zs(other))
        actual,sign,message=observe(args)
        passed=actual==expected if isinstance(expected,str) else (
            type(actual) in (float,int) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0.) and sign==zs(expected))
        rows.append(dict(case=i,x=args[0],step=args[1],expected=expected,
            expected_zero_sign=None if isinstance(expected,str) else zs(expected),
            actual=actual,actual_zero_sign=sign,exception_message=message,passed=passed))
    guards=[
        ((True,1.),"TypeError","x"),((1.,True),"TypeError","step"),
        (("bad",1.),"TypeError","x"),((1.,"bad"),"TypeError","step"),
        ((math.inf,1.),"ValueError","x"),((1.,math.nan),"ValueError","step"),
        ((10**400,1.),"ValueError","x"),((1.,10**400),"ValueError","step"),
        ((1.,0.),"ValueError","step"),((1.,-0.),"ValueError","step"),
        (("bad",True),"TypeError","x"),((math.inf,0.),"ValueError","x")]
    for args,expected,prefix in guards:
        actual,sign,message=observe(args)
        rows.append(dict(args=[token(x) for x in args],expected=expected,
            expected_message_prefix=prefix,actual=actual,exception_message=message,
            passed=actual==expected and message.startswith(prefix)))
    print(json.dumps(dict(reference="Difference of complete Decimal exponentials divided by represented step at 1600/2200 digits",
        tolerance="4e-15 relative, no absolute floor; exact zero signs/error types",observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":run()
