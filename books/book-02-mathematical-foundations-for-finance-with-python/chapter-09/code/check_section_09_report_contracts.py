"""Complete project facade contracts and independently derived report fields."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import sys,math,json,hashlib
import section_9_09 as m
NUM=('shock_bp','shock_decimal','exact_change','linear_change','quadratic_change','exact_value','linear_error','quadratic_error','absolute_linear_error','absolute_quadratic_error','linear_bound','quadratic_bound');FIELDS=NUM+('linear_bound_pass','quadratic_bound_pass')
def reference(flows,rate,bp,prec):
 with localcontext(Context(prec=prec)):
  R=Decimal.from_float(float(rate));h=float(bp)/10000.;H=Decimal.from_float(h)
  if not math.isfinite(float(rate)+h):return 'ValueError'
  V=A=B=Decimal(0);parts=[]
  def amount(C,x):
   if x>10000:return Decimal('Infinity')
   return Decimal(0) if x < -10000 else C*x.exp()
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];v=amount(C,-R*T);V+=v;A-=T*v;B+=T*T*v;parts.append((C,T,v))
  if V==0:return 'ValueError'
  baseline=[float(x) for x in (V,A,B,-A/V,B/V)]
  if baseline[0]<=0 or not all(math.isfinite(x) for x in baseline):return 'ValueError'
  S=sum((amount(C,-(R+H)*T) for C,T,v in parts),Decimal(0));E=S-V;L=A*H;Q=L+B*H*H/2;low=min(R,R+H)
  b1=sum((T*T*amount(C,-low*T)*H*H/2 for C,T,v in parts),Decimal(0));b2=sum((T*T*T*amount(C,-low*T)*abs(H)**3/6 for C,T,v in parts),Decimal(0))
  vals=[float(bp),h]+[float(x) for x in (E,L,Q,S,E-L,E-Q,abs(E-L),abs(E-Q),b1,b2)]
  if not all(math.isfinite(x) for x in vals):return 'ValueError'
  allowance=1e-12*max(1.,abs(baseline[0]));return dict(zip(FIELDS,vals+[vals[8]<=vals[10]+allowance,vals[9]<=vals[11]+allowance]))
rows=[]
def add(case,field,got,want,kind='contract'):
 if type(want)is bool:ok=type(got)is bool and got==want
 elif isinstance(want,(str,list,set,dict)):ok=got==want
 else:ok=type(got)is float and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
def baseline_ref(f,r,prec):
 with localcontext(Context(prec=prec)):
  R=Decimal.from_float(float(r));V=A=B=Decimal(0)
  for c,t in f:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];v=C*(-R*T).exp();V+=v;A-=T*v;B+=T*T*v
  return dict(zip(('baseline_value','first_derivative','second_derivative','duration','convexity'),[float(x) for x in (V,A,B,-A/V,B/V)]))
CASES=[('sample',[(120.,.5),(120.,1.),(120.,2.),(1120.,3.)],.04,[-100.,-25.,0.,25.,100.]),('single time3',[(100.,3.)],.04,[-75.,0.,25.]),('zero time',[(100.,0.)],1e308,[-50.,0.,50.]),('vanished leg',[(1e-308,2.),(1.,0.)],355.,[-3550000.,0.,50.])]
SCHEMA={'model','rate_convention','baseline_rate','cash_flows','baseline_value','first_derivative','second_derivative','duration','convexity','scenarios','validation','limitations'}
for label,f,r,grid in CASES:
 got=m.project_report(f,r,grid);a=baseline_ref(f,r,1800);b=baseline_ref(f,r,2400);assert a==b
 for k,want in b.items():add(label,k,got[k],want,'independent numerical')
 expected_rows=[]
 for i,bp in enumerate(grid):
  a=reference(f,r,bp,1800);b=reference(f,r,bp,2400);assert a==b and isinstance(b,dict);expected_rows.append(b)
  for k,want in b.items():add(label,f'row{i} '+k,got['scenarios'][i][k],want,'reported flag policy' if k.endswith('_pass') else 'independent numerical')
 add(label,'schema',set(got),SCHEMA);add(label,'model',got['model'],'positive fixed cash flows');add(label,'units',got['rate_convention'],'decimal annual continuously compounded');add(label,'baseline rate',got['baseline_rate'],float(r));add(label,'flow metadata',got['cash_flows'],[dict(cash=float(c),years=float(t)) for c,t in f]);add(label,'grid order',[x['shock_bp'] for x in got['scenarios']],grid);add(label,'row schema',all(set(x)==set(FIELDS) for x in got['scenarios']),True)
 add(label,'validation schema',set(got['validation']),{'in_model_bound_checks_pass','runtime_certified','independent_review_completed'});add(label,'in model aggregation',got['validation']['in_model_bound_checks_pass'],all(x['linear_bound_pass'] and x['quadratic_bound_pass'] for x in expected_rows));add(label,'runtime certification',got['validation']['runtime_certified'],False);add(label,'independent review',got['validation']['independent_review_completed'],False);add(label,'limitations',got['limitations'],['Fixed positive cash flows; no optionality or credit effects','Flat continuously compounded annual discount rate','Floating-point rounding not included in mathematical Taylor bounds','Educational model; not production pricing software'])
for label,f,r,grid,want in [('none flows',None,0.,[-1.,0.,1.],'TypeError'),('empty flows',[],0.,[-1.,0.,1.],'ValueError'),('bool rate',[(1.,1.)],True,[-1.,0.,1.],'TypeError'),('none grid',[(1.,1.)],0.,None,'TypeError'),('empty grid',[(1.,1.)],0.,[],'ValueError'),('missing zero',[(1.,1.)],0.,[-1.,1.],'ValueError'),('missing positive',[(1.,1.)],0.,[-1.,0.],'ValueError'),('missing negative',[(1.,1.)],0.,[0.,1.],'ValueError'),('negative zero not negative',[(1.,1.)],0.,[-0.,0.,1.],'ValueError'),('bool grid entry',[(1.,1.)],0.,[-1.,False,1.],'TypeError'),('nan grid entry',[(1.,1.)],0.,[-1.,math.nan,1.],'ValueError'),('huge grid entry',[(1.,1.)],0.,[-1.,0.,10**1000],'ValueError')]:
 try:a=m.project_report(f,r,grid)
 except Exception as e:a=type(e).__name__
 add(label,'rejection',a,want)
f=[(100.,1.),(1100.,2.)];grid=[-25.,0.,25.,25.];fc=f.copy();gc=grid.copy();a=m.project_report(f,.04,grid);b=m.project_report(iter(f),.04,iter(grid));add('one shot','same report',a==b,True);add('ownership','unchanged',f==fc and grid==gc,True);add('duplicates','rows',a['scenarios'][2]==a['scenarios'][3],True);add('grid ordering','bps',[x['shock_bp'] for x in a['scenarios']],grid);add('JSON finite','stable',json.loads(json.dumps(a,allow_nan=False))==a,True);add('determinism','repeat serialization',json.dumps(a,sort_keys=True,allow_nan=False)==json.dumps(m.project_report(f,.04,grid),sort_keys=True,allow_nan=False),True)
sentinel=RuntimeError('grid sentinel')
def late():yield -25.;yield 0.;raise sentinel
try:m.project_report(f,.04,late());same=False
except Exception as e:same=e is sentinel
add('late grid exception','identity',same,True)
for label,flows,rate,want_trace,want_exc in [('flow before grid',[],.04,[],'ValueError'),('rate before grid',f,True,[],'TypeError'),('baseline after grid',[(1e308,2.)],0.,['negative','zero','positive'],'ValueError')]:
 trace=[]
 def traced():
  for label2,v in [('negative',-25.),('zero',0.),('positive',25.)]:trace.append(label2);yield v
 try:m.project_report(flows,rate,traced());kind='returned'
 except Exception as e:kind=type(e).__name__
 add(label,'trace',trace,want_trace);add(label,'exception',kind,want_exc)
# Mutable report containers must not alias the caller or another report.
a['cash_flows'][0]['cash']=999.;a['scenarios'][0]['shock_bp']=999.;add('returned ownership','caller and second report',f==fc and grid==gc and b['cash_flows'][0]['cash']==100. and b['scenarios'][0]['shock_bp']==-25.,True)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Complete selected project facade schema/grid/ownership/priority/serialization/aggregation checks;reuses independently derived original-input scenario oracle,not production or independent mathematical/model/platform/release approval. Resource limits and provenance/assessment gaps remain open;numeric zero signs not extra policy.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
