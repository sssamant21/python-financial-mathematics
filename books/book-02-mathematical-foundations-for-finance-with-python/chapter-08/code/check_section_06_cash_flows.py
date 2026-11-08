"""Complete signed aggregate references; emits retained per-predicate observations."""
import hashlib,json,math,sys,itertools
from decimal import Decimal,localcontext
from pathlib import Path
import section_8_06 as s
T=math.ulp(0.);M=sys.float_info.max
CASES=[('cancel-derivatives',[(M,2.),(-M,2.)],0.),('overflow-order',[(M,0.),(M,0.),(-M,0.)],0.),('reordered-control',[(M,0.),(-M,0.),(M,0.)],0.),('signed-extremes',[(T,2000.),(-T,1998.)],-.5),('derivative-underflow',[(1.,750.),(1.,751.)],1.),('ordinary',[(100.,1.),(-40.,2.),(20.,3.)],.05),('negative-underflow',[(-1.,750.),(-1.,751.)],1.),('exact-exp-cancel',[(M,2000.),(-M,2000.)],-.5),('zero-horizon-signed',[(M,0.),(-M,0.),(T,0.)],-1e308),('final-overflow',[(M,2.)],0.),('negative-final-overflow',[(-M,2.)],0.),('signed-zero-payments',[(-0.,1000.),(0.,2000.)],-1.),('empty',[],.05),('zero-rate-different-times',[(8.,1.),(-4.,2.),(1.,4.)],0.)]
for i,p in enumerate(itertools.permutations([(M,0.),(M,0.),(-M,0.)])):CASES.append(('permutation'+str(i),list(p),0.))
def oracle(flows,rate,precision):
    with localcontext() as ctx:
        ctx.prec=precision;r=Decimal.from_float(float(rate));sums=[Decimal(0)]*3
        for c,t in flows:
            c,t=Decimal.from_float(float(c)),Decimal.from_float(float(t));pv=c*(-r*t).exp()
            for i,x in enumerate([pv,-t*pv,t*t*pv]):sums[i]+=x
        floats=[0. if x==0 else float(x) for x in sums]
        return 'ValueError' if not all(map(math.isfinite,floats)) else floats
checks=[]
def clean(x):
    if isinstance(x,float) and not math.isfinite(x):return repr(x)
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x
for name,flows,rate in CASES:
    a,b=oracle(flows,rate,1600),oracle(flows,rate,2200)
    assert a==b and (a=='ValueError' or [math.copysign(1,x) for x in a]==[math.copysign(1,x) for x in b]),name
    try:actual=list(s.cash_flow_rate_derivatives(iter(flows),rate))
    except Exception as e:actual=type(e).__name__
    if a=='ValueError':checks.append(dict(case=name,actual=clean(actual),reference=a,passed=actual==a))
    else:
        for i,(v,w) in enumerate(zip(actual if isinstance(actual,list) else [actual]*3,a)):
            ok=isinstance(v,(int,float)) and math.isfinite(v) and (v==w and math.copysign(1,v)==math.copysign(1,w) if w==0 or abs(w)<sys.float_info.min else math.isclose(v,w,rel_tol=4e-15,abs_tol=0))
            checks.append(dict(case=name,component=i,actual=clean(v),reference=w,passed=ok))
# Actual iteration and validation priority, not only arithmetic examples.
class Once:
    def __init__(self,items):self.items=items;self.calls=0
    def __iter__(self):
        self.calls+=1
        if self.calls>1:raise RuntimeError('iterated twice')
        return iter(self.items)
q=Once([(100.,1.),(-20.,2.)]);value=s.cash_flow_rate_derivatives(q,.05)
checks.append(dict(case='one-shot collection',passed=q.calls==1))
class Untouched:
    def __iter__(self):raise RuntimeError('rate should fail first')
for label,flows,rate,error in [('rate-first',Untouched(),float('nan'),'ValueError'),('negative-years',[(1.,-1.)],0.,'ValueError'),('bool-payment',[(True,1.)],0.,'TypeError'),('huge-payment',[(10**1000,1.)],0.,'ValueError'),('empty-rate-validation',[],float('inf'),'ValueError')]:
    try:s.cash_flow_rate_derivatives(flows,rate);actual='returned'
    except Exception as e:actual=type(e).__name__
    checks.append(dict(case=label,actual=actual,reference=error,passed=actual==error))
# Signed payments do not delegate through the nonnegative single-payment API.
original=s.present_value;s.present_value=lambda *a:(_ for _ in ()).throw(RuntimeError('must not call single-payment helper'))
try:
    actual=s.cash_flow_rate_derivatives([(-100.,1.)],.05);ok=actual[0]<0 and actual[1]>0 and actual[2]<0
except Exception as e:ok=False
finally:s.present_value=original
checks.append(dict(case='signed aggregate independent of nonnegative helper',passed=ok))
out=dict(source_sha256=hashlib.sha256(Path(s.__file__).read_bytes()).hexdigest(),checks=checks,oracle='Complete signed term sums at Decimal.from_float 1600/2200 digits; independent of grouped implementation',relative_tolerance=4e-15,absolute_tolerance=0,zero_policy='Exact algebraic zero canonical positive; nonzero underflow retains sign',limits='Selected complete aggregates and guards, not arbitrary cancellation/correct-rounding or resource-limit certification')
print(json.dumps(out,indent=2,allow_nan=False));raise SystemExit(not all(x['passed'] for x in checks))
