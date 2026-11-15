"""Independent whole-change/error references and explicit direct-helper contracts."""
from decimal import Decimal,Context,localcontext,getcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_08 as m
FIELDS=('exact_change','linear_change','quadratic_change','linear_error','quadratic_error','absolute_linear_error','absolute_quadratic_error')
CASES=[('ordinary',[100.,1100.],[1.,2.],[.001,-.002]),('zero shock',[100.,1100.],[1.,2.],[0.,0.]),('tiny shock',[1e308],[1.],[1e-200]),('tiny horizon',[1e308],[1e-308],[1.]),('exp rescue',[1e-308],[2.],[-355.]),('collective rescue',[1e308,5.4e307],[1.,1.],[1.5,-1.5]),('true complete error overflow',[1e308,5.5e307],[1.,1.],[1.5,-1.5]),('true change overflow',[1e308],[1.],[-2.]),('zero term huge inverse factor',[0.],[2.],[-1e308]),('empty vectors',[],[],[]),('zero term',[0.],[1.],[.1]),('zero time',[1e308],[0.],[1e308]),('integer inputs',[100,1100],[1,2],[1,1]),('unused baseline sum overflow',[1e308,1e308],[1.,1.],[0.,0.]),('large positive shift',[1.],[1.],[10001.]),('finite large negative shift',[1e308],[1.],[-1.])]
def reference(values,years,shocks,prec):
 with localcontext(Context(prec=prec)):
  E=L=Q2=Decimal(0)
  for v,t,h in zip(values,years,shocks):
   V,T,H=[Decimal.from_float(float(x)) for x in (v,t,h)];x=-T*H
   if V==0:endpoint=Decimal(0)
   elif x>10000:return 'ValueError'
   else:endpoint=Decimal(0) if x < -10000 else V*x.exp()
   E+=endpoint-V;L-=T*V*H;Q2+=T*T*V*H*H/2
  Q=L+Q2;out=[float(x) for x in (E,L,Q,E-L,E-Q,abs(E-L),abs(E-Q))]
  return out if all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
def add(case,field,got,want,kind='contract'):
 ok=got==want if isinstance(want,(str,list,bool)) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
for label,v,t,h in CASES:
 want=reference(v,t,h,1800);assert want==reference(v,t,h,2400)
 try:a=m.scenario_from_terms(v,t,h)
 except Exception as e:a=type(e).__name__
 for i,k in enumerate(FIELDS):add(label,k,a if isinstance(a,str) else a[k],want if isinstance(want,str) else want[i],'range-policy' if isinstance(want,str) else 'numerical')
for label,v,t,h,want in [('short years',[100.,200.],[1.],[.01],'ValueError'),('short shock',[100.],[1.],[],'ValueError'),('long shock',[100.],[1.],[.01,.02],'ValueError'),('negative term',[-100.],[1.],[.01],'ValueError'),('negative time',[100.],[-1.],[.01],'ValueError'),('bool term',[True],[1.],[.01],'TypeError'),('bool time',[100.],[True],[.01],'TypeError'),('bool shock',[100.],[1.],[True],'TypeError'),('nan term',[math.nan],[1.],[.01],'ValueError'),('inf time',[100.],[math.inf],[.01],'ValueError'),('inf shock',[100.],[1.],[math.inf],'ValueError'),('oversized term',[10**1000],[1.],[.01],'ValueError'),('none first',None,None,None,'TypeError')]:
 try:a=m.scenario_from_terms(v,t,h)
 except Exception as e:a=type(e).__name__
 add(label,'precondition',a,want,'direct-contract-policy')
v=[100.,1100.];t=[1.,2.];h=[.001,-.002];copies=[v.copy(),t.copy(),h.copy()];a=m.scenario_from_terms(v,t,h)
add('ownership','inputs',[v,t,h]==copies,True)
try:b=m.scenario_from_terms(iter(v),iter(t),iter(h));ok=b==a
except Exception:ok=False
add('one-shot vectors','report',ok,True,'collection')
class Once:
 def __init__(self,values):self.values=values;self.calls=0
 def __iter__(self):
  self.calls+=1
  if self.calls>1:raise RuntimeError('iterated twice')
  return iter(self.values)
x,y,z=Once(v),Once(t),Once(h)
try:b=m.scenario_from_terms(x,y,z);ok=b==a and [x.calls,y.calls,z.calls]==[1,1,1]
except Exception:ok=False
add('single traversal','report',ok,True,'collection')
add('paired permutation','report',m.scenario_from_terms(v[::-1],t[::-1],h[::-1])==a,True)
b=m.scenario_from_terms([2*x for x in v],t,h)
for k in FIELDS:add('scaling',k,b[k],2*a[k])
ctx=getcontext();old=ctx.copy()
with localcontext(Context(prec=9)):b=m.scenario_from_terms(v,t,h)
add('ambient context','unchanged',b==a and ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps,True)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Direct helper on represented baseline terms,not original cash/rate latent amounts. Equal-length finite nonnegative term/time vectors and finite shocks are explicit new direct preconditions; equal empty vectors allowed. No added baseline valuation gate. Wrapper exact values/tolerance flags and full spot numerical contracts remain open. Zero signs numeric only; broad resource/platform/model/independent acceptance pending.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
