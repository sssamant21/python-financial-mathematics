"""Independent exact-ratio Decimal references for Section 8.5 log return."""
import json,math,random,struct,sys
from decimal import Decimal,localcontext
import section_8_05 as subject
T,M=math.ulp(0.),sys.float_info.max

def zs(x):return int(math.copysign(1,x)) if x==0 else None

def oracle(s,e,precision):
    with localcontext() as ctx:
        ctx.prec=precision
        return float((Decimal.from_float(e)/Decimal.from_float(s)).ln())

def observe(args):
    try:
        value=subject.log_return(*args)
        return (value if math.isfinite(value) else repr(value)),zs(value),None
    except Exception as exc:return type(exc).__name__,None,str(exc)

def token(x):return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases=[(M,T),(T,M),(1e300,1e-300),(T,1.),(M,M/2),
           (1.,math.nextafter(1.,2.)),(1.,math.nextafter(1.,0.)),(T,T)]
    # Relative branch boundaries at three scales, including adjacent prices.
    for s in (math.ldexp(1.,-1020),1.,math.ldexp(1.,1020)):
        for e in (math.nextafter(s*.5,0.),s*.5,math.nextafter(s*.5,math.inf),
                  math.nextafter(s,0.),s,math.nextafter(s,math.inf),
                  math.nextafter(s*2,0.),s*2,math.nextafter(s*2,math.inf),
                  s*.49,s*2.01):
            cases.append((s,e))
    # Adjacent prices around normalization boundaries and subnormals.
    for s in (T,2*T,3*T,sys.float_info.min,math.ldexp(1.,1023),M):
        for e in (math.nextafter(s,0.),s,math.nextafter(s,math.inf)):
            if e>0 and math.isfinite(e):cases.append((s,e))
    rng=random.Random(805117)
    def price():
        bits=rng.randrange(1,0x7ff0000000000000)
        return struct.unpack(">d",bits.to_bytes(8,"big"))[0]
    for _ in range(24):cases.append((price(),price()))
    rows=[]
    for i,args in enumerate(cases):
        expected=oracle(*args,200);repeated=oracle(*args,400)
        assert expected==repeated and zs(expected)==zs(repeated)
        actual,sign,message=observe(args)
        passed=type(actual) in (float,int) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0.) and sign==zs(expected)
        rows.append(dict(case=i,start=args[0],end=args[1],expected=expected,expected_zero_sign=zs(expected),
                         actual=actual,actual_zero_sign=sign,exception_message=message,passed=passed))
    guards=[
        ((True,1.),"TypeError","start"),((1.,True),"TypeError","end"),
        (("bad",1.),"TypeError","start"),((1.,"bad"),"TypeError","end"),
        ((math.inf,1.),"ValueError","start"),((1.,math.nan),"ValueError","end"),
        ((10**400,1.),"ValueError","start"),((1.,10**400),"ValueError","end"),
        ((0.,1.),"ValueError","prices"),((1.,-0.),"ValueError","prices"),
        ((-1.,1.),"ValueError","prices"),((1.,-1.),"ValueError","prices"),
        (("bad",True),"TypeError","start"),((0.,True),"TypeError","end")]
    for args,expected,prefix in guards:
        actual,sign,message=observe(args)
        rows.append(dict(args=[token(x) for x in args],expected=expected,expected_message_prefix=prefix,
                         actual=actual,exception_message=message,
                         passed=actual==expected and message.startswith(prefix)))
    print(json.dumps(dict(reference="Decimal logarithm of the complete represented-price ratio at 200/400 digits",
        tolerance="4e-15 relative, no absolute floor; exact equal-price zero sign and exception types",
        observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":run()
