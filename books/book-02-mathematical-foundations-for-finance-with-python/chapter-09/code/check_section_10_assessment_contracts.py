"""Selected cumulative assessment complete fields and assertion-mode guard."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
from fractions import Fraction
import sys,json,math,subprocess,hashlib
import section_9_10 as m
from section_9_07 import call_payoff,put_payoff,call_slopes,put_slopes,cap_floor_slopes
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
 elif isinstance(want,(str,list)):ok=got==want
 else:ok=type(got)is float and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
flows=[(120.,.5),(120.,1.),(120.,2.),(1120.,3.)];grid=[-100.,-50.,-25.,0.,25.,50.,100.];r=.04;a=m.assessment()
with localcontext(Context(prec=2400)):
 R=Decimal.from_float(r);V=A=B=Decimal(0)
 for cash,time in flows:
  C,T=map(Decimal,(cash,time));v=C*(-R*T).exp();V+=v;A-=T*v;B+=T*T*v
 expected=dict(baseline_value=float(V),duration=float(-A/V),convexity=float(B/V))
for k,w in expected.items():add('sample baseline',k,a[k],w,'independent numerical')
for i,bp in enumerate(grid):
 x=reference(flows,r,bp,1800);y=reference(flows,r,bp,2400);assert x==y
 for k,w in y.items():add('scenario'+str(i),k,a['scenarios'][i][k],w,'reported flag policy' if k.endswith('_pass') else 'independent numerical')
add('schema','keys',sorted(a),sorted(['assessment','baseline_value','duration','convexity','scenarios','in_model_checks_passed','runtime_certified','independent_review_completed']));add('assessment title','text',a['assessment'],'Chapter 09 cumulative');add('normal mode','in model checks',a['in_model_checks_passed'],True);add('no runtime certification','flag',a['runtime_certified'],False);add('no independent review','flag',a['independent_review_completed'],False);add('grid','order',[x['shock_bp'] for x in a['scenarios']],grid);add('strict JSON','roundtrip',json.loads(json.dumps(a,allow_nan=False))==a,True);b=m.assessment();add('deterministic repeat','same',a==b,True)
a['scenarios'][0]['exact_change']=999.;add('fresh container','not aliased',b['scenarios'][0]['exact_change']!=999.,True)
for spot in (98.,100.,102.):
 C=max(Fraction(spot)-100,0);P=max(100-Fraction(spot),0);add('call'+str(spot),'payoff',call_payoff(spot,100.),float(C),'independent rational');add('put'+str(spot),'payoff',put_payoff(spot,100.),float(P),'independent rational');add('put-call identity'+str(spot),'difference',call_payoff(spot,100.)-put_payoff(spot,100.),spot-100.,'independent rational')
for label,fn,left,right in [('call',call_slopes,0.,1.),('put',put_slopes,-1.,0.)]:
 x=fn(100.,100.);add(label,'left',x['left'],left);add(label,'right',x['right'],right);add(label,'differentiable',x['differentiable'],False)
x=(call_payoff(102.,100.)-call_payoff(98.,100.))/4.;add('centered trap','slope',x,.5,'sampled quotient,not derivative')
for rate,left,right in [(.02,0.,1000.),(.05,1000.,0.)]:
 x=cap_floor_slopes(rate,1000.,.02,.05);add('threshold'+str(rate),'left',x['left'],left);add('threshold'+str(rate),'right',x['right'],right)
# Controlled wrong imported dependency must trigger the normal assert,thenrestore.
original=m.call_payoff;original_report=m.project_report
fixture=dict(baseline_value=b['baseline_value'],duration=b['duration'],convexity=b['convexity'],scenarios=b['scenarios'])
try:
 m.project_report=lambda *args:fixture
 m.call_payoff=lambda *args:3.
 try:m.assessment();kind='returned'
 except Exception as e:kind=type(e).__name__
 add('controlled faulty dependency','guard',kind,'AssertionError','controlled mutant,not correct-source failure')
finally:m.call_payoff=original;m.project_report=original_report
script="import json,section_9_10 as m;m.project_report=lambda *args:{'baseline_value':1.0,'duration':0.0,'convexity':0.0,'scenarios':[]};result={}\ntry:\n value=m.assessment();result={'outcome':'returned','in_model_checks_passed':value['in_model_checks_passed']}\nexcept Exception as e:result={'outcome':type(e).__name__,'message':str(e)}\nprint(json.dumps(result))"
z=subprocess.run([sys.executable,'-O','-c',script],cwd=Path(m.__file__).resolve().parent,capture_output=True,text=True,timeout=60);assert z.returncode==0;optimized=json.loads(z.stdout);add('optimized mode','eligibility',optimized['outcome'],'RuntimeError','controlled optimized eligibility policy')
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),optimized_command=dict(argv=[sys.executable,'-O','-c',script],returncode=z.returncode,stdout=z.stdout,stderr=z.stderr),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,limits='Constant assessment sample complete fields plus selected kink controls. Controlled faulty payoff and cached project fixture are restored. Optimized-mode project_report is a minimal controlled fixture,not a financial revaluation. Optimized mode explicitly must be rejected before a passed assessment is returned;policy/model/platform/independent approval remain open. Not coverage of all24 exercise implementations.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
