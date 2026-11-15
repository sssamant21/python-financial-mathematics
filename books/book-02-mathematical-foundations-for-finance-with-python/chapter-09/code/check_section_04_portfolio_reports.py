"""Independent complete aggregate report references; not shock acceptance."""
import math,json,sys,hashlib
from decimal import Decimal,Context,localcontext
from pathlib import Path
import section_9_04 as m
FIELDS=('value','first','second','duration','convexity')
CASES=[
 ('per-leg convexity unused',[(1e-308,1e308),(1e308,0.)],0.),
 ('per-leg value underflow',[(1e-308,2.),(1.,0.)],355.),
 ('second rescued',[(1e308,1e-308),(1.,0.)],0.),
 ('sum overflow',[(1e308,1.),(1e308,1.)],0.),
 ('first overflow',[(1e308,2.)],0.),
 ('second overflow',[(1e308,1.5)],0.),
 ('normalized overflow',[(1e-308,1e308)],0.),
 ('complete exp rescue',[(1e-308,2.),(1.,0.)],-355.),
 ('subnormal single',[(math.ulp(0.),0.)],1.),
 ('all values underflow',[(1e-308,2.)],355.),
 ('ordinary',[(100.,1.),(1100.,2.)],.04),
 ('negative rate',[(100.,1.),(1100.,2.)],-.04),
 ('time zero',[(10.,0.),(20.,-0.)],.04),
 ('tiny time normalized',[(1e308,1e-308)],0.),
 ('mixed horizons',[(50.,0.),(50.,2.)],0.),
 ('integer input',[(100,1),(1100,2)],0),
 ('long discounted',[(1e308,1000.),(2.,0.)],1.),
 ('small combined',[(1e-308,1.),(1e-308,2.)],.1),
]

def oracle(flows,rate,precision):
 with localcontext(Context(prec=precision)):
  rr=Decimal.from_float(float(rate)); vv=aa=bb=Decimal(0)
  for c,t in flows:
   C=Decimal.from_float(float(c));T=Decimal.from_float(float(t));p=C*(-T*rr).exp()
   vv+=p;aa-=T*p;bb+=T*T*p
  values=(vv,aa,bb,-aa/vv,bb/vv)
  try:out=tuple(float(x) for x in values)
  except OverflowError:return 'ValueError'
  return out if out[0]>0 and all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
for label,flows,rate in CASES:
 lo=oracle(flows,rate,1800);hi=oracle(flows,rate,2400);assert lo==hi,(label,lo,hi)
 try:actual=m.cash_flow_portfolio(flows,rate)
 except Exception as e:actual=type(e).__name__
 for i,key in enumerate(FIELDS):
  want=hi if isinstance(hi,str) else hi[i];a=actual if isinstance(actual,str) else actual[key]
  ok=a==want if isinstance(want,str) else isinstance(a,float) and math.isfinite(a) and math.isclose(a,want,rel_tol=5e-14,abs_tol=0.)
  rows.append(dict(case=label,field=key,actual=repr(a),expected=repr(want),relative_tolerance=5e-14,absolute_tolerance=0.,passed=ok))
for label,flows,rate,want in [
 ('empty',[],0.,'ValueError'),('rate priority',None,True,'TypeError'),('noniterable',None,0.,'TypeError'),
 ('negative cash',[(-1.,1.)],0.,'ValueError'),('zero cash',[(0.,1.)],0.,'ValueError'),
 ('negative years',[(1.,-1.)],0.,'ValueError'),('bool cash',[(True,1.)],0.,'TypeError'),
 ('bool years',[(1.,True)],0.,'TypeError'),('nonfinite cash',[(math.nan,1.)],0.,'ValueError'),
 ('nonfinite years',[(1.,math.inf)],0.,'ValueError'),('oversized',[(10**1000,1.)],0.,'ValueError'),
 ('rate before empty',[],math.inf,'ValueError'),('malformed',[(1.,)],0.,'ValueError')]:
 try:a=m.cash_flow_portfolio(flows,rate)
 except Exception as e:a=type(e).__name__
 rows.append(dict(case=label,actual=repr(a),expected=want,passed=a==want))
flows=[(100.,1.),(1100.,2.)];copy=flows.copy();a=m.cash_flow_portfolio(flows,.04);b=m.cash_flow_portfolio(list(reversed(flows)),.04)
rows.append(dict(case='caller ownership',passed=flows==copy))
rows.append(dict(case='ordering invariant',passed=a==b))
g=m.cash_flow_portfolio(iter(flows),.04);rows.append(dict(case='one-shot iterable',passed=g==a))
scaled=m.cash_flow_portfolio([(2*c,t) for c,t in flows],.04)
rows.append(dict(case='scaling amounts and normalized invariance',passed=all(math.isclose(scaled[k],a[k]*(2 if k in FIELDS[:3] else 1),rel_tol=5e-14) for k in FIELDS)))
ctx=__import__('decimal').getcontext();before=ctx.copy();m.cash_flow_portfolio(flows,.04)
rows.append(dict(case='ambient Decimal unchanged',passed=ctx.prec==before.prec and ctx.flags==before.flags and ctx.traps==before.traps))
d=dict(source_blob=hashlib.sha1(b'blob '+str(len(Path(m.__file__).read_bytes())).encode()+b'\0'+Path(m.__file__).read_bytes()).hexdigest(),reference_precisions=[1800,2400],predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Selected positive cash-flow aggregate reports only. Zero signs compare numerically. Shocks,universal exp rounding,resource bounds and independent/platform acceptance open.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert not d['failed']
