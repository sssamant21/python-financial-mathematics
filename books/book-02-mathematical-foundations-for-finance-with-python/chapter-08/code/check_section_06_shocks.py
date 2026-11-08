"""Local Section 8.6 shocks: independent expanded-coefficient and two-price oracles."""
import json,math,sys
from decimal import Decimal,localcontext
import section_8_06 as subject
T,M=math.ulp(0.),sys.float_info.max
S=math.ldexp(1.,-600);H=math.ldexp(1.,601)
LABELS=("taylor1","taylor2","exact")

def zs(x):return int(math.copysign(1,x)) if x==0 else None

def reference(args,kind,precision):
    c,r,t,h=map(float,args)
    if c==0 or t==0 or h==0:
        first=-0.*c*t*h
        return first+math.copysign(0.,c) if kind==1 else first
    with localcontext() as ctx:
        ctx.prec=precision
        dc,dr,dt,dh=map(Decimal.from_float,(c,r,t,h))
        if kind<2:
            first=-dc*dt*dh
            # Expanded independently; implementation factors the rational polynomial.
            coefficient=first if kind==0 else first+dc*dt*dt*dh*dh/2
            if not coefficient:return 0.
            amplitude=abs(coefficient).ln()-dr*dt
            if amplitude>1000:return "ValueError"
            if amplitude< -1000:return -0. if coefficient<0 else 0.
            result=float(amplitude.exp())
            if not math.isfinite(result):return "ValueError"
            return -result if coefficient<0 else result
        before,after=-dr*dt,-(dr+dh)*dt
        high=max(before,after)
        if high>20000:return "ValueError"
        if high< -20000:return math.copysign(0.,-h)
        def exp(x):return Decimal(0) if x< -40000 else x.exp()
        value=float(dc*(exp(after)-exp(before)))
        if not math.isfinite(value):return "ValueError"
        return math.copysign(0.,-h) if value==0 else value

def observe(args,kind):
    try:
        value=(subject.pv_shock(*args,order=kind+1) if kind<2 else subject.pv_shock_exact(*args))
        return (value if math.isfinite(value) else repr(value)),zs(value),None
    except Exception as exc:return type(exc).__name__,None,str(exc)

def token(x):return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases=[(1.,1.,1000.,-1.),(M,0.,S,H),(M,0.,M,0.),(M,0.,2*T,.125),
        (M,0.,S,math.nextafter(H,math.inf)),(M,0.,S,math.nextafter(H,0.)),
        (M,0.,M,-0.),(M,-M,0.,M),(M,-M,-0.,M),
        (0.,-M,M,-M),(-0.,-M,M,-M),(0.,0.,M,M),(-0.,0.,M,M),
        (0.,0.,1.,0.),(-0.,0.,1.,0.),(0.,0.,1.,-0.),(-0.,0.,1.,-0.),
        (10000.,.04,5.,.01),(10000.,.04,5.,-.01),
        (M,-M,T,M),(M,M,M,-M),(M,M,M,-M/2),
        (1.,M,T,M),(1.,-M,T,-M),(T,-.5,2000.,1.),
        (1.,0.,1.,T),(1.,0.,T,T),(M,0.,T,T),
        (1.,1.,1000.,1.),(1.,-1.,710.,1.),(M,0.,1.,3.)]
    rows=[]
    for i,args in enumerate(cases):
        for kind,label in enumerate(LABELS):
            expected=reference(args,kind,1600);other=reference(args,kind,2200)
            assert expected==other and (isinstance(expected,str) or zs(expected)==zs(other))
            actual,sign,message=observe(args,kind)
            passed=actual==expected if isinstance(expected,str) else (
                type(actual) in (int,float) and math.isclose(actual,expected,rel_tol=4e-15,abs_tol=0.) and sign==zs(expected))
            rows.append(dict(case=i,helper=label,args=args,args_zero_signs=[zs(x) for x in args],
                expected=expected,expected_zero_sign=None if isinstance(expected,str) else zs(expected),
                actual=actual,actual_zero_sign=sign,exception_message=message,passed=passed))
    guards=[((True,.1,1.,.1),"TypeError","payment"),((1.,True,1.,.1),"TypeError","rate"),
        ((1.,.1,True,.1),"TypeError","years"),((1.,.1,1.,True),"TypeError","shock"),
        ((-1.,.1,1.,.1),"ValueError","payment and years"),
        ((1.,.1,-1.,.1),"ValueError","payment and years"),
        ((math.inf,.1,1.,.1),"ValueError","payment"),((1.,math.nan,1.,.1),"ValueError","rate"),
        ((1.,.1,math.inf,.1),"ValueError","years"),((1.,.1,1.,math.inf),"ValueError","shock"),
        ((10**400,.1,1.,.1),"ValueError","payment"),((1.,10**400,1.,.1),"ValueError","rate"),
        ((1.,.1,10**400,.1),"ValueError","years"),((1.,.1,1.,10**400),"ValueError","shock"),
        ((0.,"bad",1.,0.),"TypeError","rate"),((0.,.1,-1.,0.),"ValueError","payment and years"),
        (("bad",True,"bad","bad"),"TypeError","shock"),
        (("bad",True,"bad",1.),"TypeError","years"),
        (("bad",True,1.,1.),"TypeError","payment")]
    for args,expected,prefix in guards:
        for kind,label in enumerate(LABELS):
            actual,sign,message=observe(args,kind)
            rows.append(dict(helper=label,args=[token(x) for x in args],expected=expected,
                expected_message_prefix=prefix,actual=actual,exception_message=message,
                passed=actual==expected and message.startswith(prefix)))
    for order in (True,False,0,3,-1,1.0,"2",None):
        try:actual=subject.pv_shock("bad","bad",1.,.1,order);message=None
        except Exception as exc:actual=type(exc).__name__;message=str(exc)
        rows.append(dict(helper="order-priority",order=order,expected="ValueError",actual=actual,
            exception_message=message,passed=actual=="ValueError" and message.startswith("order")))
    for args,prefix in ((("bad","bad","bad",True),"shock"),(("bad","bad",True,1.),"years")):
        try:actual=subject.pv_shock(*args,order=3);message=None
        except Exception as exc:actual=type(exc).__name__;message=str(exc)
        rows.append(dict(helper="controls-before-order",expected="TypeError",actual=actual,
            exception_message=message,passed=actual=="TypeError" and message.startswith(prefix)))
    originals={n:getattr(subject,n) for n in ("present_value","pv_rate_first","pv_rate_second")}
    def forbidden(*args):raise AssertionError("shock called a separately rounded value/derivative")
    for name in originals:setattr(subject,name,forbidden)
    try:
        for kind,label in enumerate(LABELS):
            args=(2.,.125,4.,.125);expected=reference(args,kind,1600)
            actual,sign,message=observe(args,kind)
            rows.append(dict(helper=label,contract="independent complete shock",
                expected=expected,actual=actual,exception_message=message,
                passed=type(actual) is float and math.isclose(actual,expected,rel_tol=4e-15)))
    finally:
        for n,v in originals.items():setattr(subject,n,v)
    print(json.dumps(dict(reference="Expanded Decimal Taylor coefficients/log-amplitude and direct two-price differences at 1600/2200 digits",
        tolerance="4e-15 relative, no absolute floor; exact zero signs/error types",observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows),str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":run()
