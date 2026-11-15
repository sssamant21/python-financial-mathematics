"""Direct latent endpoint/polynomial references; strict eligible baseline policy."""
import math,json,sys,hashlib
from pathlib import Path
from decimal import Decimal,Context,localcontext
import section_9_04 as m
FIELDS=('shock','exact_change','linear_change','quadratic_change','linear_error','quadratic_error')
CASES=[('saved rescue',1e-308,2.,.5,-355.),('small shock',10000.,5.,.04,.005),('negative shock',10000.,5.,.04,-.005),('zero shock',10000.,5.,.04,0.),('negative zero shock',10000.,5.,.04,-0.),('time zero',1e308,0.,1e308,1e308),('underflowed baseline',1e-308,2.,355.,-355.),('ineligible normalized',1e-308,1e308,0.,0.),('baseline overflow',1e308,1.,-1.,0.),('complete difference rescue',1e308,1.,0.,-.7),('report overflow',1e308,1.,0.,-1.),('tiny shock errors',1e308,1.,0.,1e-200),('tiny shock',1.,1.,0.,1e-100),('tiny time',1e308,1e-308,0.,1.),('near quadratic zero',100.,1.,0.,2.),('ordinary long',100.,100.,.01,.01),('integer inputs',100,1,0,1),('subnormal cash',math.ulp(0.),0.,0.,1.),('positive huge shock',1.,1.,0.,1e308),('far negative endpoint',1.,1.,0.,10001.)]

def reference(c,t,r,h,prec):
 with localcontext(Context(prec=prec)):
  C,T,R,H=[Decimal.from_float(float(x)) for x in (c,t,r,h)];B=C*(-T*R).exp()
  base=(B,-T*B,T*T*B,T,T*T)
  try:bb=[float(x) for x in base]
  except OverflowError:return 'ValueError'
  if bb[0]<=0 or not all(math.isfinite(x) for x in bb):return 'ValueError'
  X=-T*H;L=-T*B*H;Q=L+T*T*B*H*H/2
  # For enormous negative shifted exponents,the endpoint rounds away even
  # in every final difference. No production helper or cutoff is used.
  E=-B if -T*(R+H)<-100000 else C*(-T*(R+H)).exp()-B
  try:out=tuple(float(x) for x in (H,E,L,Q,E-L,E-Q))
  except OverflowError:return 'ValueError'
  return out if all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
for label,c,t,r,h in CASES:
 a=reference(c,t,r,h,1800);b=reference(c,t,r,h,2400);assert a==b,(label,a,b)
 try:actual=m.single_shock(c,t,r,h)
 except Exception as e:actual=type(e).__name__
 for i,k in enumerate(FIELDS):
  want=b if isinstance(b,str) else b[i];got=actual if isinstance(actual,str) else actual[k]
  ok=got==want if isinstance(want,str) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
  rows.append(dict(case=label,field=k,actual=repr(got),expected=repr(want),passed=ok,relative_tolerance=5e-14,absolute_tolerance=0.))
for label,c,t,r,h,want in [('shock first',None,None,None,True,'TypeError'),('cash type',True,1.,0.,0.,'TypeError'),('years type',1.,True,0.,0.,'TypeError'),('rate type',1.,1.,True,0.,'TypeError'),('cash domain',0.,1.,0.,0.,'ValueError'),('years domain',1.,-1.,0.,0.,'ValueError'),('nan cash',math.nan,1.,0.,0.,'ValueError'),('inf shock',1.,1.,0.,math.inf,'ValueError'),('oversized cash',10**1000,1.,0.,0.,'ValueError'),('oversized shock',1.,1.,0.,10**1000,'ValueError')]:
 try:got=m.single_shock(c,t,r,h)
 except Exception as e:got=type(e).__name__
 rows.append(dict(case=label,actual=repr(got),expected=want,passed=got==want))
ctx=__import__('decimal').getcontext();old=ctx.copy();m.single_shock(100.,1.,.04,.01);rows.append(dict(case='ambient Decimal unchanged',passed=ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps))
d=dict(source_blob=hashlib.sha1(b'blob '+str(len(Path(m.__file__).read_bytes())).encode()+b'\0'+Path(m.__file__).read_bytes()).hexdigest(),reference_precisions=[1800,2400],predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Selected single_shock reports;strict eligible baseline prerequisite retained. Numerical zeros compare without sign policy. Portfolio shocks,universal transcendental rounding,resources and independent/platform acceptance open.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
