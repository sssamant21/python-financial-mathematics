"""Independent collective latent endpoint/Taylor/error references."""
from pathlib import Path
from decimal import Decimal,Context,localcontext
import math,json,sys,hashlib
import section_9_04 as m
FIELDS=('shock','exact_change','linear_change','quadratic_change','linear_error','quadratic_error')
CASES=[('saved zero shock',[(1e-308,1e308),(1e308,0.)],0.,0.),('saved exp rescue',[(1e-308,2.),(1.,0.)],.5,-355.),('saved aggregate eligibility',[(1e-308,2.),(1.,0.)],355.,-355.),('ordinary',[(100.,1.),(1100.,2.)],.04,.005),('negative shock',[(100.,1.),(1100.,2.)],.04,-.005),('tiny error',[(1e308,1.)],0.,1e-200),('tiny time',[(1e308,1e-308)],0.,1.),('ineligible aggregate',[(1e-308,2.)],355.,-355.),('value overflow',[(1e308,0.),(1e308,0.)],0.,0.),('normalized overflow',[(1e-308,1e308)],0.,0.),('aggregate time zero',[(10.,0.),(20.,0.)],1e308,1e308),('whole polynomial cancellation',[(12.,1.),(1.,4.)],0.,1.),('integer inputs',[(100,1),(1100,2)],0,1),('upper finite change',[(1e308,1.)],0.,-1.),('whole output overflow',[(1e308,1.)],0.,-2.),('subnormal amount',[(math.ulp(0.),0.)],0.,.1),('huge positive shock',[(1.,1.)],0.,1e308),('far endpoint',[(1.,1.)],0.,10001.)]

def reference(flows,rate,shock,prec):
 with localcontext(Context(prec=prec)):
  R,H=[Decimal.from_float(float(x)) for x in (rate,shock)];parts=[];V=D1=D2=Decimal(0)
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];B=C*(-T*R).exp();V+=B;D1-=T*B;D2+=T*T*B;parts.append((C,T,B))
  try:base=[float(x) for x in (V,D1,D2,-D1/V,D2/V)]
  except OverflowError:return 'ValueError'
  if base[0]<=0 or not all(math.isfinite(x) for x in base):return 'ValueError'
  exact=Decimal(0)
  for C,T,B in parts:
   endpoint=Decimal(0) if -T*(R+H)<-100000 else C*(-T*(R+H)).exp()
   exact+=endpoint-B
  linear=D1*H;quad=D1*H+D2*H*H/2
  try:out=tuple(float(x) for x in (H,exact,linear,quad,exact-linear,exact-quad))
  except OverflowError:return 'ValueError'
  return out if all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
for label,flows,r,h in CASES:
 a=reference(flows,r,h,1800);b=reference(flows,r,h,2400);assert a==b,(label,a,b)
 try:actual=m.portfolio_shock(flows,r,h)
 except Exception as e:actual=type(e).__name__
 for i,k in enumerate(FIELDS):
  want=b if isinstance(b,str) else b[i];got=actual if isinstance(actual,str) else actual[k]
  ok=got==want if isinstance(want,str) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
  rows.append(dict(case=label,field=k,actual=repr(got),expected=repr(want),relative_tolerance=5e-14,absolute_tolerance=0.,passed=ok))
for label,flows,r,h,want in [('shock first',None,True,True,'TypeError'),('rate before materialize',None,True,0.,'TypeError'),('noniterable',None,0.,0.,'TypeError'),('empty',[],0.,0.,'ValueError'),('malformed',[(1.,)],0.,0.,'ValueError'),('cash negative',[(-1.,1.)],0.,0.,'ValueError'),('years negative',[(1.,-1.)],0.,0.,'ValueError'),('bool cash',[(True,1.)],0.,0.,'TypeError'),('bool years',[(1.,True)],0.,0.,'TypeError'),('nan cash',[(math.nan,1.)],0.,0.,'ValueError'),('inf years',[(1.,math.inf)],0.,0.,'ValueError'),('oversized cash',[(10**1000,1.)],0.,0.,'ValueError'),('inf shock',[(1.,1.)],0.,math.inf,'ValueError')]:
 try:got=m.portfolio_shock(flows,r,h)
 except Exception as e:got=type(e).__name__
 rows.append(dict(case=label,actual=repr(got),expected=want,passed=got==want))
flows=[(100.,1.),(1100.,2.)];copy=flows.copy();a=m.portfolio_shock(flows,.04,.005)
rows.append(dict(case='caller unchanged',passed=flows==copy));rows.append(dict(case='one-shot iterable',passed=m.portfolio_shock(iter(flows),.04,.005)==a));rows.append(dict(case='order invariance',passed=m.portfolio_shock(flows[::-1],.04,.005)==a))
b=m.portfolio_shock([(2*c,t) for c,t in flows],.04,.005);rows.append(dict(case='scaling',passed=all(math.isclose(b[k],a[k]*(1 if k=='shock' else 2),rel_tol=5e-14,abs_tol=0.) for k in FIELDS)))
ctx=__import__('decimal').getcontext();old=ctx.copy();m.portfolio_shock(flows,.04,.005);rows.append(dict(case='ambient Decimal unchanged',passed=ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps))
d=dict(source_blob=hashlib.sha1(b'blob '+str(len(Path(m.__file__).read_bytes())).encode()+b'\0'+Path(m.__file__).read_bytes()).hexdigest(),reference_precisions=[1800,2400],predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Selected positive-flow portfolio shock reports;existing aggregate baseline prerequisite retained. Zero signs numeric only. Universal exp rounding,collection resources,other sections and independent/platform acceptance open.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
