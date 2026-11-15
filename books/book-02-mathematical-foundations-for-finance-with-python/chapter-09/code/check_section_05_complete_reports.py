"""Independent complete report/interval-extrema/bound references."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_05 as m
FIELDS=('baseline_value','first_derivative','second_derivative','exact_change','linear_change','quadratic_change','linear_error','quadratic_error','linear_bound','quadratic_bound','linear_bound_utilization','quadratic_bound_utilization')
CASES=[('saved exp rescue',[(1e-308,2.)],.5,-355.),('saved second rescue',[(1e308,1e-308)],0.,.1),('ordinary',[(10000.,5.)],.04,.001),('negative',[(10000.,5.)],.04,-.001),('portfolio',[(100.,1.),(1100.,2.)],.04,.005),('zero shock',[(1.,2.)],.04,0.),('zero time',[(1e308,0.)],1e308,1e308),('underflowed baseline',[(1e-308,2.)],355.,-355.),('aggregate underflowed leg',[(1e-308,2.),(1.,0.)],355.,-355.),('internal third derivative unused',[(1e-308,1e308),(1e308,0.)],0.,0.),('tiny error',[(1e308,1.)],0.,1e-200),('tiny shock',[(1.,1.)],0.,1e-100),('true second overflow',[(1e308,2.)],0.,0.),('bound overflow',[(1e308,1.)],0.,-2.),('integer inputs',[(100,1),(1100,2)],0,1),('subnormal time zero',[(math.ulp(0.),0.)],0.,1.)]
def reference(flows,r,h,prec):
 with localcontext(Context(prec=prec)):
  R,H=[Decimal.from_float(float(x)) for x in (r,h)];V=D1=D2=E=M2=M3=Decimal(0)
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];B=C*(-T*R).exp();endpoint=C*(-T*(R+H)).exp()
   # Positive C,T imply derivative magnitudes decrease monotonically in r.
   # Thus interval extrema occur at an endpoint;derive max independently.
   W=max(B,endpoint);V+=B;D1-=T*B;D2+=T*T*B;E+=endpoint-B;M2+=T*T*W;M3+=T*T*T*W
  L=D1*H;Q=L+D2*H*H/2;B1=M2*H*H/2;B2=M3*abs(H)**3/6;EL=E-L;EQ=E-Q
  try:out=[float(x) for x in (V,D1,D2,E,L,Q,EL,EQ,B1,B2)]
  except OverflowError:return 'ValueError'
  if out[0]<=0 or not all(math.isfinite(x) for x in out):return 'ValueError'
  out.extend([None if out[8]==0 else float(abs(EL)/B1),None if out[9]==0 else float(abs(EQ)/B2)])
  return tuple(out)
rows=[]
for label,flows,r,h in CASES:
 a=reference(flows,r,h,1800);b=reference(flows,r,h,2400);assert a==b,(label,a,b)
 try:actual=m.portfolio_report(flows,r,h)
 except Exception as e:actual=type(e).__name__
 for i,k in enumerate(FIELDS):
  want=b if isinstance(b,str) else b[i];got=actual if isinstance(actual,str) else actual[k]
  ok=got==want if want is None or isinstance(want,str) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
  rows.append(dict(case=label,field=k,actual=repr(got),expected=repr(want),relative_tolerance=5e-14,absolute_tolerance=0.,passed=ok))
 if not isinstance(b,str):rows.append(dict(case=label+' independent bound nonvacuity',passed=all(b[i] is None or 0<=b[i]<=1+1e-14 for i in (10,11)) and (b[8]>0 if h and any(t>0 for _,t in flows) and abs(h)>1e-20 else True)))
for label,flows,r,h,want in [('flows before rate',None,True,True,'TypeError'),('empty before rate',[],True,True,'ValueError'),('bad cash before rate',[(True,1.)],True,True,'TypeError'),('rate type',[(1.,1.)],True,0.,'TypeError'),('shock type',[(1.,1.)],0.,True,'TypeError'),('negative cash',[(-1.,1.)],0.,0.,'ValueError'),('negative time',[(1.,-1.)],0.,0.,'ValueError'),('nan cash',[(math.nan,1.)],0.,0.,'ValueError'),('inf rate',[(1.,1.)],math.inf,0.,'ValueError'),('oversized cash',[(10**1000,1.)],0.,0.,'ValueError'),('malformed',[(1.,)],0.,0.,'ValueError')]:
 try:got=m.portfolio_report(flows,r,h)
 except Exception as e:got=type(e).__name__
 rows.append(dict(case=label,actual=repr(got),expected=want,passed=got==want))
f=[(100.,1.),(1100.,2.)];copy=f.copy();a=m.portfolio_report(f,.04,.005);rows.append(dict(case='caller ownership',passed=f==copy));rows.append(dict(case='one-shot input',passed=m.portfolio_report(iter(f),.04,.005)==a));rows.append(dict(case='single wrapper',passed=m.single_report(100.,1.,.04,.005)==m.portfolio_report([(100.,1.)],.04,.005)))
ctx=__import__('decimal').getcontext();old=ctx.copy();m.portfolio_report(f,.04,.005);rows.append(dict(case='ambient Decimal unchanged',passed=ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps))
d=dict(source_blob=hashlib.sha1(b'blob '+str(len(Path(m.__file__).read_bytes())).encode()+b'\0'+Path(m.__file__).read_bytes()).hexdigest(),reference_precisions=[1800,2400],predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Selected positive-flow whole reports and endpoint-extremum bounds;zero signs numeric only. Polynomial_example,universal exp rounding,resource/platform/independent/release scope open.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
