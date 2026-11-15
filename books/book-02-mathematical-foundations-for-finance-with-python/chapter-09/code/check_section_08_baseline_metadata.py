"""Independent complete baseline references; separate spot iterator metadata checks."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_08 as m
FIELDS=('baseline_value','first_derivative','second_derivative','duration','convexity')
CASES=[('ordinary',[(100.,1.),(1100.,2.)],.04),('negative',[(100.,1.),(1100.,2.)],-.04),('factor overflow rescue',[(1e-308,2.)],-355.),('factor underflow rescue',[(1e308,1000.)],1.),('tiny weighted second',[(1e308,1e-308)],0.),('tiny normalized duration',[(1e-308,1e-308)],0.),('tiny all derivatives',[(1e-308,1.)],0.),('zero time',[(1e308,0.)],1e308),('subnormal zero time',[(math.ulp(0.),0.)],0.),('true sum overflow',[(1e308,0.),(1e308,0.)],0.),('true derivative overflow',[(1e308,2.)],0.),('unrepresentable convexity',[(1e-308,1e200)],0.),('small cash big time',[(1e-308,1e154)],0.),('all value underflow',[(1e-308,2.)],355.),('integer inputs',[(100,1),(1100,2)],0),('mixed time',[(1.,0.),(100.,5.)],.03)]
def reference(flows,rate,prec):
 with localcontext(Context(prec=prec)):
  R=Decimal.from_float(float(rate));V=A=B=Decimal(0)
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];x=-R*T
   if x>10000:return 'ValueError'
   amount=Decimal(0) if x < -10000 else C*x.exp();V+=amount;A-=T*amount;B+=T*T*amount
  if V==0:return 'ValueError'
  out=[float(x) for x in (V,A,B,-A/V,B/V)]
  return out if out[0]>0 and all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
def add(case,field,got,want,kind='contract'):
 ok=got==want if isinstance(want,(str,list,bool)) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
for label,f,r in CASES:
 a=reference(f,r,1800);b=reference(f,r,2400);assert a==b
 try:actual=m.parallel_report(f,r,[])
 except Exception as e:actual=type(e).__name__
 for i,key in enumerate(FIELDS):add(label,key,actual if isinstance(actual,str) else actual[key],b if isinstance(b,str) else b[i],'range-policy' if isinstance(b,str) else 'numeric')
for label,f,r,tol,want in [('flows first',None,True,None,'TypeError'),('empty first',[],True,None,'ValueError'),('bool cash',[(True,1.)],0.,None,'TypeError'),('negative cash',[(-1.,1.)],0.,None,'ValueError'),('negative years',[(1.,-1.)],0.,None,'ValueError'),('bool rate',[(1.,1.)],True,None,'TypeError'),('nan rate',[(1.,1.)],math.nan,None,'ValueError'),('inf cash',[(math.inf,1.)],0.,None,'ValueError'),('oversized cash',[(10**1000,1.)],0.,None,'ValueError'),('bool tolerance',[(1.,1.)],0.,True,'TypeError'),('negative tolerance',[(1.,1.)],0.,-1.,'ValueError'),('inf tolerance',[(1.,1.)],0.,math.inf,'ValueError')]:
 try:a=m.parallel_report(f,r,[],tol)
 except Exception as e:a=type(e).__name__
 add(label,'rejection',a,want)
f=[(100.,1.),(1100.,2.)];fc=f.copy();a=m.parallel_report(f,.04,[]);b=m.parallel_report(iter(f),.04,iter([]))
add('baseline ownership','unchanged',f==fc,True);add('one shot flows/empty grid','report',a==b,True)
add('baseline model metadata','model',a['model'],'positive fixed cash flows; flat continuous annual rate');add('baseline empty scenarios','scenarios',a['scenarios'],[]);add('baseline cash metadata','rows',a['cash_flows'],[{'cash':100.,'years':1.},{'cash':1100.,'years':2.}]);add('baseline optional tolerance','none',a['error_tolerance_currency'] is None,True)
b=m.parallel_report(f,.04,[0.],0.);add('selected zero-shock inherited scenario property','value',b['scenarios'][0]['exact_value'],b['baseline_value'])
for label,flows,rates,values,container in [('list',[(100.,1.)],[.04],[25.],list),('tuple',[(100.,1.)],[.04],[25.],tuple),('iterator',[(100.,1.)],[.04],[25.],iter),('two shock iterator',[(100.,1.),(1100.,2.)],[.035,.04],[10.,-20.],iter)]:
 a=m.spot_scenario(flows,rates,container(values));canonical=m.spot_scenario(flows,rates,list(values))
 add(label,'shock metadata',a['shock_bp'],values,'collection/provenance');add(label,'metadata/compute consistency property',a==canonical,True,'collection/provenance')
class Once:
 def __init__(self):self.calls=0
 def __iter__(self):
  self.calls+=1
  if self.calls>1:raise RuntimeError('input iterated twice')
  return iter([25.])
x=Once()
try:a=m.spot_scenario([(100.,1.)],[.04],x);ok=a['shock_bp']==[25.] and x.calls==1
except Exception:ok=False
add('single traversal shock source','once',ok,True,'collection/provenance')
for values,want in [(iter([True]),'TypeError'),(iter([]),'ValueError'),(iter([math.nan]),'ValueError')]:
 try:a=m.spot_scenario([(100.,1.)],[.04],values)
 except Exception as e:a=type(e).__name__
 add('spot metadata invalid iterable','rejection',a,want,'collection/provenance')
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Parallel baseline slice with empty grids,plus separate spot shock metadata/iteration properties. Selected zero-shock property is not independent scenario oracle. Legacy scenario/error/tolerance/spot numerical contracts remain open; no universal/resource/platform/independent acceptance; zero signs numeric only.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
