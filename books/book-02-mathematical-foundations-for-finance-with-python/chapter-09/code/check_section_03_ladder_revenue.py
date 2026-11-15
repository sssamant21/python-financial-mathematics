"""Explicit ladder prerequisites and exact-decimal polynomial model references."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_03 as source
FIELDS=['baseline_value','exact_change','linear_change','linear_value','signed_error','absolute_error','relative_change_error']
def observations():
 rows=[]
 def eq(a,b):
  if isinstance(b,float):return isinstance(a,(int,float)) and math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,b) if b==0 else math.isclose(a,b,rel_tol=5e-14,abs_tol=0))
  return a==b
 def test(name,fn,want,category='source contract'):
  try:a=fn()
  except Exception as e:a=type(e).__name__
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=eq(a,want),category=category))
 def f(z):
  a=float(z);return a if math.isfinite(a) else 'ValueError'
 def polynomial(q):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    Q=Decimal(q);refs.append([q if q==0 else f(40*Q-Decimal('0.1')*Q*Q),f(40-Decimal('0.2')*Q)])
  assert refs[0]==refs[1];return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.)
 quantities=[0.,-0.,1.,100.,200.,400.,math.nextafter(400.,0.),math.nextafter(400.,math.inf),math.nextafter(200.,0.),math.nextafter(200.,math.inf),tiny,1e154,1e155,mx,1e-308]
 for i,q in enumerate(quantities):
  want=polynomial(q);test('decimal-model revenue'+str(i),lambda q=q:source.revenue(q),want[0],'decimal polynomial/range contract');test('decimal-model derivative'+str(i),lambda q=q:source.revenue_derivative(q),want[1],'decimal polynomial/range contract')
 # Integration oracle uses independently rounded polynomial callbacks,then complete generic report.
 for i,(q,h) in enumerate([(math.nextafter(400.,0.),math.ulp(400.)),(200.,math.ulp(200.)),(tiny,tiny)]):
  v0,d=polynomial(q);v1=polynomial(q+h)[0];refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    V,W,D,H=map(Decimal,(v0,v1,d,h));E=W-V;A=D*H;R=E-A;refs.append([f(V),f(E),f(A),f(V+A),f(R),f(abs(R)),None if E==0 else f(abs(R)/abs(E))])
  assert refs[0]==refs[1]
  for j,key in enumerate(FIELDS):test('revenue report'+str(i)+' '+key,lambda q=q,h=h,key=key:source.compare_change(source.revenue,source.revenue_derivative,q,h)[key],refs[0][j],'sampled callback integration,not latent unrounded polynomial change')
 # Ordered duplicate shocks,including0,assembled from independent direct-model reports.
 shocks=[.1,0.,-.1,.1];ladder=source.discount_step_ladder(100.,2.,0.,shocks);test('ladder row count',lambda:len(ladder),4)
 for i,h in enumerate(shocks):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    H=Decimal(h);B=Decimal(100);E=B*((-2*H).exp()-1);A=-2*B*H;R=E-A;refs.append([100.,-0. if h==0 else f(E),-0. if h==0 else f(A),f(B+A),0. if h==0 else f(R),0. if h==0 else f(abs(R)),None if h==0 else f(abs(R)/abs(E))])
  assert refs[0]==refs[1];test('ladder shock order'+str(i),lambda i=i:ladder[i]['shock'],h)
  for j,key in enumerate(FIELDS):test('ladder'+str(i)+' '+key,lambda i=i,key=key:ladder[i][key],refs[0][j],'ordered assembly/direct independent shock reference')
 test('empty valid ladder',lambda:source.discount_step_ladder(1.,1.,.1,[]),[])
 for name,c,t,r,want in [('cash zero',0.,1.,.1,'ValueError'),('cash negative',-1.,1.,.1,'ValueError'),('negative time',1.,-1.,.1,'ValueError'),('rate NaN',1.,1.,math.nan,'ValueError'),('cash bool',True,1.,.1,'TypeError'),('time bool',1.,True,.1,'TypeError'),('rate bool',1.,1.,True,'TypeError'),('cash oversized',10**1000,1.,.1,'ValueError')]:test('empty prerequisite '+name,lambda c=c,t=t,r=r:source.discount_step_ladder(c,t,r,[]),want,'new explicit empty-ladder prerequisite policy')
 seen=[]
 def steps():
  seen.append('consumed');yield .1
 test('invalid model before consumption',lambda:source.discount_step_ladder(0.,1.,.1,steps()),'ValueError','new explicit prerequisite policy');test('invalid model consumed nothing',lambda:seen,[],'new explicit prerequisite policy');test('invalid model before steps type',lambda:source.discount_step_ladder(0.,1.,.1,None),'ValueError','new explicit prerequisite priority')
 test('valid model noniterable steps',lambda:source.discount_step_ladder(1.,1.,.1,None),'TypeError')
 consumed=[]
 def bad_steps():
  for x in [.1,True,.2]:consumed.append(x);yield x
 test('bad shock type',lambda:source.discount_step_ladder(1.,1.,.1,bad_steps()),'TypeError');test('partial consumption stops at bad shock',lambda:consumed,[.1,True]);test('NaN shock',lambda:source.discount_step_ladder(1.,1.,.1,[math.nan]),'ValueError')
 instance=RuntimeError('synthetic step iterator failure')
 def broken():
  yield 0.
  raise instance
 try:source.discount_step_ladder(1.,1.,.1,broken())
 except Exception as e:test('late iterator identity',lambda:e is instance,True)
 test('tuple ordered inputs',lambda:[x['shock'] for x in source.discount_step_ladder(1.,1.,.1,(0.,.1))],[0.,.1]);test('generator ordered inputs',lambda:[x['shock'] for x in source.discount_step_ladder(1.,1.,.1,iter([0.,.1]))],[0.,.1]);original=[0.,.1];source.discount_step_ladder(1.,1.,.1,original);test('caller list unchanged',lambda:original,[0.,.1])
 for val,want in [(True,'TypeError'),('1','TypeError'),(None,'TypeError'),(math.nan,'ValueError'),(math.inf,'ValueError'),(-1.,'ValueError'),(10**1000,'ValueError')]:
  test('revenue invalid '+repr(val),lambda val=val:source.revenue(val),want);test('derivative invalid '+repr(val),lambda val=val:source.revenue_derivative(val),want)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'ladder/revenue predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
