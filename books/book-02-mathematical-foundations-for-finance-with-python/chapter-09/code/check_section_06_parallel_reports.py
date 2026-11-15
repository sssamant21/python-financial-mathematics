"""Direct latent endpoint/Taylor/error oracles;retain full baseline prerequisite."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_06 as m
FIELDS=('shock','exact_change','linear_change','quadratic_change','linear_error','quadratic_error')
CASES=[('saved exp rescue',[(1e-308,2.),(1.,0.)],.5,-355.),('ordinary',[(100.,1.),(1100.,2.)],.04,.005),('negative',[(100.,1.),(1100.,2.)],.04,-.005),('zero shock',[(100.,1.),(1100.,2.)],.04,0.),('negative zero',[(1.,1.)],0.,-0.),('tiny error',[(1e308,1.)],0.,1e-200),('tiny horizon',[(1e308,1e-308)],0.,1.),('unused cash derivative prerequisite',[(1e-308,2.)],-355.,0.),('all underflow prerequisite',[(1e-308,2.)],355.,-355.),('eligible tiny leg',[(1e-308,2.),(1.,0.)],355.,-355.),('upper finite change',[(1e308,1.)],0.,-1.),('true output overflow',[(1e308,1.)],0.,-2.),('zero time',[(1e308,0.)],1e308,1e308),('integer inputs',[(100,1),(1100,2)],0,1),('subnormal zero time',[(math.ulp(0.),0.)],0.,1.),('large finite shift',[(1.,1.)],0.,10001.)]
def reference(flows,r,h,prec):
 with localcontext(Context(prec=prec)):
  R,H=[Decimal.from_float(float(x)) for x in (r,h)];V=A=B=Decimal(0);parts=[];cash=[]
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];df=(-R*T).exp();v=C*df;V+=v;A-=T*v;B+=T*T*v;cash.append(df);parts.append((C,T,v))
  try:base=[float(x) for x in (V,A,B,-A/V,B/V)]+[float(x) for x in cash]+[float(v/V) for _,_,v in parts]
  except OverflowError:return 'ValueError'
  if base[0]<=0 or not all(math.isfinite(x) for x in base):return 'ValueError'
  E=sum((C*(-T*(R+H)).exp()-v for C,T,v in parts),Decimal(0));L=A*H;Q=L+B*H*H/2
  try:out=tuple(float(x) for x in (H,E,L,Q,E-L,E-Q))
  except OverflowError:return 'ValueError'
  return out if all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
for label,f,r,h in CASES:
 a=reference(f,r,h,1800);b=reference(f,r,h,2400);assert a==b,(label,a,b)
 try:actual=m.parallel_shock(f,r,h)
 except Exception as e:actual=type(e).__name__
 for i,k in enumerate(FIELDS):
  want=b if isinstance(b,str) else b[i];got=actual if isinstance(actual,str) else actual[k]
  ok=got==want if isinstance(want,str) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
  rows.append(dict(case=label,field=k,actual=repr(got),expected=repr(want),relative_tolerance=5e-14,absolute_tolerance=0.,passed=ok))
for label,f,r,h,want in [('flows first',None,True,True,'TypeError'),('empty first',[],True,True,'ValueError'),('bad cash before rate',[(True,1.)],True,True,'TypeError'),('rate before shock',[(1.,1.)],True,True,'TypeError'),('shock type',[(1.,1.)],0.,True,'TypeError'),('negative cash',[(-1.,1.)],0.,0.,'ValueError'),('negative years',[(1.,-1.)],0.,0.,'ValueError'),('nan cash',[(math.nan,1.)],0.,0.,'ValueError'),('inf shock',[(1.,1.)],0.,math.inf,'ValueError'),('oversized',[(10**1000,1.)],0.,0.,'ValueError'),('shape',[(1.,)],0.,0.,'ValueError')]:
 try:a=m.parallel_shock(f,r,h)
 except Exception as e:a=type(e).__name__
 rows.append(dict(case=label,actual=repr(a),expected=want,passed=a==want))
f=[(100.,1.),(1100.,2.)];copy=f.copy();a=m.parallel_shock(f,.04,.005);rows.append(dict(case='ownership',passed=f==copy));rows.append(dict(case='one-shot iterable',passed=m.parallel_shock(iter(f),.04,.005)==a));rows.append(dict(case='order selected',passed=m.parallel_shock(f[::-1],.04,.005)==a));b=m.parallel_shock([(2*c,t) for c,t in f],.04,.005);rows.append(dict(case='scaling selected',passed=all(math.isclose(b[k],a[k]*(1 if k=='shock' else 2),rel_tol=5e-14,abs_tol=0.) for k in FIELDS)));ctx=__import__('decimal').getcontext();old=ctx.copy();m.parallel_shock(f,.04,.005);rows.append(dict(case='ambient Decimal unchanged',passed=ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps))
d=dict(source_blob=hashlib.sha1(b'blob '+str(len(Path(m.__file__).read_bytes())).encode()+b'\0'+Path(m.__file__).read_bytes()).hexdigest(),reference_precisions=[1800,2400],source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Parallelreportonly;completefull-baselineprerequisiteexplicitlyretained,includingper-cashderivativeeligibility. Zero signsnumeric only;spot/universal/resource/platform/independentacceptanceopen.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
