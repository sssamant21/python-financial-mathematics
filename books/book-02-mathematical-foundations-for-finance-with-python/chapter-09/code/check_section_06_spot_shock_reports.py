"""Complete spot-shock changes/errors against independent direct references."""
from decimal import Decimal,Context,localcontext,getcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_06 as m
FIELDS=('exact_change','linear_change','linear_error')
CASES=[('saved exp rescue',[(1e-308,2.),(1.,0.)],[.5,0.],[-355.,0.]),('ordinary',[(100.,1.),(1100.,2.)],[.035,.04],[.001,-.002]),('parallel',[(100.,1.),(1100.,2.)],[.04,.04],[.005,.005]),('zero shocks',[(100.,1.),(1100.,2.)],[.035,.04],[0.,0.]),('negative zero',[(1.,1.)],[0.],[-0.]),('tiny latent error',[(1e308,1.)],[0.],[1e-200]),('tiny horizon',[(1e308,1e-308)],[0.],[1.]),('all baseline underflow',[(1e-308,2.)],[355.],[-355.]),('eligible underflowed leg',[(1e-308,2.),(1.,0.)],[355.,0.],[-355.,0.]),('baseline derivative restriction',[(1e308,2.)],[0.],[0.]),('true change overflow',[(1e308,1.)],[0.],[-2.]),('linear overflow',[(1e308,1.)],[0.],[2.]),('finite change',[(1e308,1.)],[0.],[-1.]),('zero time summed rates overflow float',[(1e308,0.)],[1e308],[1e308]),('integer inputs',[(100,1),(1100,2)],[0,0],[1,1]),('subnormal zero time',[(math.ulp(0.),0.)],[0.],[1.]),('large finite positive shift',[(1.,1.)],[0.],[10001.]),('nonparallel mixed change',[(100.,1.),(100.,1.)],[0.,0.],[.2,-.2])]
def reference(flows,rates,shocks,prec):
 with localcontext(Context(prec=prec)):
  V=Decimal(0);base=[];ds=[];parts=[]
  def amount(C,x):
   return Decimal(0) if x < -10000 else (Decimal('Infinity') if x>10000 else C*x.exp())
  for (c,t),z,h in zip(flows,rates,shocks):
   C,T,Z,H=[Decimal.from_float(float(x)) for x in (c,t,z,h)];v=amount(C,-Z*T);V+=v;ds.append(-T*v);parts.append((C,T,Z,H,v))
  try:elig=[float(V),*[float(x) for x in ds],float(sum(ds,Decimal(0)))]
  except (OverflowError,ValueError):return 'ValueError'
  if elig[0]<=0 or not all(math.isfinite(x) for x in elig):return 'ValueError'
  E=L=Decimal(0)
  for C,T,Z,H,v in parts:E+=amount(C,-T*(Z+H))-v;L-=T*v*H
  try:out=tuple(float(x) for x in (E,L,E-L))
  except (OverflowError,ValueError):return 'ValueError'
  return out if all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
for label,f,z,h in CASES:
 a=reference(f,z,h,1800);b=reference(f,z,h,2400);assert a==b,(label,a,b)
 try:actual=m.spot_shock(f,z,h)
 except Exception as e:actual=type(e).__name__
 for i,k in enumerate(FIELDS):
  want=b if isinstance(b,str) else b[i];got=actual if isinstance(actual,str) else actual[k]
  ok=got==want if isinstance(want,str) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
  rows.append(dict(case=label,field=k,actual=repr(got),expected=repr(want),passed=ok))
for label,f,z,h,want in [('flows first',None,None,None,'TypeError'),('empty first',[],None,None,'ValueError'),('cash bool first',[(True,1.)],[True],[True],'TypeError'),('rate before shock',[(1.,1.)],[True],[True],'TypeError'),('shock before length',[(1.,1.)],[],[True],'TypeError'),('short rates',[(1.,1.)],[],[0.],'ValueError'),('long rates',[(1.,1.)],[0.,0.],[0.],'ValueError'),('short shocks',[(1.,1.)],[0.],[],'ValueError'),('long shocks',[(1.,1.)],[0.],[0.,0.],'ValueError'),('negative cash',[(-1.,1.)],[0.],[0.],'ValueError'),('negative years',[(1.,-1.)],[0.],[0.],'ValueError'),('nan rate',[(1.,1.)],[math.nan],[0.],'ValueError'),('inf shock',[(1.,1.)],[0.],[math.inf],'ValueError'),('oversized cash',[(10**1000,1.)],[0.],[0.],'ValueError')]:
 try:a=m.spot_shock(f,z,h)
 except Exception as e:a=type(e).__name__
 rows.append(dict(case=label,actual=repr(a),expected=want,passed=a==want))
f=[(100.,1.),(1100.,2.)];z=[.035,.04];h=[.001,-.002];fc=f.copy();zc=z.copy();hc=h.copy();a=m.spot_shock(f,z,h)
rows.append(dict(case='ownership',passed=f==fc and z==zc and h==hc))
rows.append(dict(case='one shot inputs',passed=m.spot_shock(iter(f),iter(z),iter(h))==a))
rows.append(dict(case='paired permutation',passed=m.spot_shock(f[::-1],z[::-1],h[::-1])==a))
b=m.spot_shock([(2*c,t) for c,t in f],z,h);rows.append(dict(case='scaling',passed=all(math.isclose(b[k],2*a[k],rel_tol=5e-14,abs_tol=0.) for k in FIELDS)))
ctx=getcontext();old=ctx.copy()
with localcontext(Context(prec=9)):b=m.spot_shock(f,z,h)
rows.append(dict(case='ambient Decimal independent',passed=b==a and ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps))
b=m.parallel_shock(f,.04,.005);a=m.spot_shock(f,[.04,.04],[.005,.005]);rows.append(dict(case='selected parallel consistency (property only)',passed=all(a[k]==b[k] for k in FIELDS)))
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Spot shock only. Full spot-curve baseline eligibility retained; numeric zeros without extra sign policy. Selected fixed-precision/exponent/resource scope, not universal accuracy or independent/platform/release acceptance. Parallel consistency is a property, not independent oracle.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
