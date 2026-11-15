"""Independent complete baseline/normalized/per-cash/weight references."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_06 as m
FIELDS=('value','first','second','duration','convexity','cash_flow_derivatives','value_weights')
CASES=[('saved second rescue',[(1e308,1e-308)],0.),('normal',[(100.,1.),(1100.,2.)],.04),('negative',[(100.,1.),(1100.,2.)],-.04),('time zero',[(10.,0.),(20.,-0.)],1e308),('aggregate tiny leg',[(1e-308,2.),(1.,0.)],355.),('all underflow',[(1e-308,2.)],355.),('aggregate mixed horizon',[(1e-308,1e308),(1e308,0.)],0.),('normalized true overflow',[(1e-308,1e308)],0.),('cash derivative true overflow',[(1e-308,2.)],-355.),('near exp range',[(1e-308,2.)],-350.),('value overflow',[(1e308,0.),(1e308,0.)],0.),('first overflow',[(1e308,2.)],0.),('second overflow',[(1e308,1.5)],0.),('subnormal zero time',[(math.ulp(0.),0.)],0.),('cash derivative underflow',[(1e308,1000.),(1.,0.)],1.),('weights before rounded terms',[(math.ulp(0.),1.),(math.ulp(0.),0.)],.1),('integer inputs',[(100,1),(1100,2)],0),('tiny normalized',[(1e308,1e-308),(1.,0.)],0.)]
def ref(flows,rate,prec):
 with localcontext(Context(prec=prec)):
  R=Decimal.from_float(float(rate));V=A=B=Decimal(0);terms=[];cash=[]
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];df=(-R*T).exp();value=C*df;V+=value;A-=T*value;B+=T*T*value;terms.append(value);cash.append(df)
  try:values=[float(x) for x in (V,A,B,-A/V,B/V)];cash=[float(x) for x in cash];weights=[float(x/V) for x in terms]
  except OverflowError:return 'ValueError'
  if values[0]<=0 or not all(math.isfinite(x) for x in values+cash+weights):return 'ValueError'
  return tuple(values)+(cash,weights)
rows=[]
for label,flows,r in CASES:
 a=ref(flows,r,1800);b=ref(flows,r,2400);assert a==b,(label,a,b)
 try:actual=m.portfolio_sensitivity(flows,r)
 except Exception as e:actual=type(e).__name__
 for i,k in enumerate(FIELDS):
  want=b if isinstance(b,str) else b[i];got=actual if isinstance(actual,str) else actual[k]
  def near(a,b):return isinstance(a,float) and math.isfinite(a) and math.isclose(a,b,rel_tol=5e-14,abs_tol=0.)
  ok=got==want if isinstance(want,str) else isinstance(got,list) and len(got)==len(want) and all(near(x,y) for x,y in zip(got,want)) if isinstance(want,list) else near(got,want)
  rows.append(dict(case=label,field=k,actual=repr(got),expected=repr(want),relative_tolerance=5e-14,absolute_tolerance=0.,passed=ok))
for label,flows,r,want in [('rate priority',None,True,'TypeError'),('empty',[],0.,'ValueError'),('None',None,0.,'TypeError'),('badshape',[(1.,)],0.,'ValueError'),('negative cash',[(-1.,1.)],0.,'ValueError'),('negative time',[(1.,-1.)],0.,'ValueError'),('bool cash',[(True,1.)],0.,'TypeError'),('bool time',[(1.,True)],0.,'TypeError'),('nan cash',[(math.nan,1.)],0.,'ValueError'),('inf rate',[(1.,1.)],math.inf,'ValueError'),('oversized cash',[(10**1000,1.)],0.,'ValueError')]:
 try:got=m.portfolio_sensitivity(flows,r)
 except Exception as e:got=type(e).__name__
 rows.append(dict(case=label,actual=repr(got),expected=want,passed=got==want))
f=[(100.,1.),(1100.,2.)];copy=f.copy();a=m.portfolio_sensitivity(f,.04);rows.append(dict(case='ownership',passed=f==copy));rows.append(dict(case='one-shot iterable',passed=m.portfolio_sensitivity(iter(f),.04)==a));rows.append(dict(case='weights budget selected',passed=math.isclose(sum(a['value_weights']),1.,rel_tol=5e-14)));ctx=__import__('decimal').getcontext();old=ctx.copy();m.portfolio_sensitivity(f,.04);rows.append(dict(case='ambient Decimal unchanged',passed=ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps))
d=dict(source_blob=hashlib.sha1(b'blob '+str(len(Path(m.__file__).read_bytes())).encode()+b'\0'+Path(m.__file__).read_bytes()).hexdigest(),reference_precisions=[1800,2400],source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Portfolio_sensitivity baseline only;finite whole report/listfields and positive rounded total. Parallel/spot wrappers,universal exp rounding,resources/platform/independent acceptance remainopen.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
