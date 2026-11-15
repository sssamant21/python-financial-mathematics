"""Complete scenario references; retained rounded spot and finite factor gates."""
from decimal import Decimal,Context,localcontext,getcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_07 as m
FIELDS=('baseline_value','shocked_value','exact_change','left_slope','right_slope','differentiable')
CASES=[('at strike up',100.,100.,2.,.04,2.),('at strike down',100.,100.,-2.,.04,2.),('in money',102.,100.,2.,.04,2.),('out money',98.,100.,-2.,.04,2.),('cross threshold',98.,100.,4.,.04,2.),('zero shock',102.,100.,0.,.04,2.),('payoff underflow rescue',1e308,1.,0.,1.,1000.),('true report overflow',1e308,1.,0.,-1.,100.),('unused factor gate',50.,100.,0.,-355.,2.),('unrepresentable slopes',102.,100.,0.,-355.,2.),('rounded shifted spot gate',1e308,1.,1.,0.,0.),('shifted spot overflow gate',1e308,1.,1e308,1.,1000.),('huge exponent product',102.,100.,0.,1e308,1e308),('zero years',100.,100.,2.,1e308,0.),('zero spot extension behavior',0.,100.,1.,0.,0.),('integer inputs',100,100,2,0,0),('latent small change',1.,.2,math.ulp(1.),.01,1.),('negative rate',102.,100.,-1.,-.1,2.)]
def reference(s,k,h,r,t,prec):
 s,k,h,r,t=map(float,(s,k,h,r,t));shifted=s+h
 if not math.isfinite(shifted) or shifted<0:return 'ValueError'
 with localcontext(Context(prec=prec)):
  S,K,P,R,T=[Decimal.from_float(x) for x in (s,k,shifted,r,t)];exponent=-R*T
  if exponent>10000:return 'ValueError'
  factor=Decimal(0) if exponent < -10000 else exponent.exp()
  if not math.isfinite(float(factor)):return 'ValueError'
  a=max(S-K,Decimal(0));b=max(P-K,Decimal(0));left=1. if s>k else 0.;right=1. if s>=k else 0.
  vals=[float(factor*a),float(factor*b),float(factor*(b-a)),float(factor*Decimal(left)),float(factor*Decimal(right))]
  return [*vals,left==right] if all(math.isfinite(x) for x in vals) else 'ValueError'
rows=[]
def add(case,field,got,want,kind='contract'):
 ok=got==want if isinstance(want,(str,bool,list)) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
for label,s,k,h,r,t in CASES:
 want=reference(s,k,h,r,t,1800);assert want==reference(s,k,h,r,t,2400)
 try:actual=m.call_scenario(s,k,h,r,t)
 except Exception as e:actual=type(e).__name__
 for i,f in enumerate(FIELDS):add(label,f,actual if isinstance(actual,str) else actual[f],want if isinstance(want,str) else want[i],'range/prerequisite-policy' if isinstance(want,str) else 'numeric/report')
for label,args,want in [('bool spot',(True,1.,0.,0.,0.),'TypeError'),('bool strike',(1.,True,0.,0.,0.),'TypeError'),('bool shock',(1.,1.,True,0.,0.),'TypeError'),('bool rate',(1.,1.,0.,True,0.),'TypeError'),('bool years',(1.,1.,0.,0.,True),'TypeError'),('nan before years',(-1.,1.,0.,math.nan,-1.),'ValueError'),('negative years before spot',(-1.,0.,0.,0.,-1.),'ValueError'),('negative spot',(-1.,1.,0.,0.,0.),'ValueError'),('zero strike',(1.,0.,0.,0.,0.),'ValueError'),('negative shifted spot',(1.,1.,-2.,0.,0.),'ValueError'),('nan shock',(1.,1.,math.nan,0.,0.),'ValueError'),('inf rate',(1.,1.,0.,math.inf,0.),'ValueError'),('oversized int',(10**1000,1.,0.,0.,0.),'ValueError'),('inf years',(1.,1.,0.,0.,math.inf),'ValueError')]:
 try:a=m.call_scenario(*args)
 except Exception as e:a=type(e).__name__
 add(label,'rejection',a,want)
a=m.call_scenario(102.,100.,2.,.04,2.);b=m.call_scenario(204.,200.,4.,.04,2.)
for f in FIELDS:add('selected monetary scaling',f,b[f],a[f]*2 if f in FIELDS[:3] else a[f])
a=m.call_scenario(100.,100.,2.,.04,2.);add('kink remains reported','differentiable',a['differentiable'],False)
ctx=getcontext();old=ctx.copy()
with localcontext(Context(prec=9)):b=m.call_scenario(100.,100.,2.,.04,2.)
add('ambient Decimal independence','report',b==a and ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps,True)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Call scenario only; rounded shifted spot and finite unreturned factor prerequisite deliberately retained. All returned numeric fields finite. Spot0 slope flags describe formal piecewise extension, not physical-domain left derivatives. Zero signs numeric only; broad resource/model/platform/release/independent policy approval pending.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
