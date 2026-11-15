"""Independent represented affine/sample-report expectations and callback contracts."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_03 as source
FIELDS=['baseline_value','exact_change','linear_change','linear_value','signed_error','absolute_error','relative_change_error']
def observations():
 rows=[]
 def eq(a,b):
  if isinstance(b,float):return isinstance(a,(int,float)) and math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,b) if b==0 else math.isclose(a,b,rel_tol=5e-14,abs_tol=0))
  return a==b
 def test(name,fn,want):
  try:a=fn()
  except Exception as e:a=type(e).__name__
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=eq(a,want)))
 def f(z):
  a=float(z);return a if math.isfinite(a) else 'ValueError'
 def affine_ref(vals):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    V,D,H=map(Decimal,vals);refs.append(f(V+D*H))
  assert refs[0]==refs[1];return refs[0]
 u=math.ulp(1.);tiny=math.ulp(0.);mx=sys.float_info.max
 affine=[(9.,6.,.2),(1e308,-1e308,2.),(-1.,1+u,1-u),(mx,mx,1.),(0.,tiny,.5),(-0.,-0.,1.),(1.,0.,mx),(1e308,1e-308,1e308)]
 for i,vals in enumerate(affine):test('affine'+str(i),lambda vals=vals:source.linear_taylor(*vals),affine_ref(vals))
 def report_ref(y0,y1,d,h):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    V,W,D,H=map(Decimal,(y0,y1,d,h));E=W-V;A=D*H;R=E-A;vals=[V,E,A,V+A,R,abs(R),None if E==0 else abs(R)/abs(E)];out=[None if z is None else f(z) for z in vals];refs.append(['ValueError']*7 if 'ValueError' in out else out)
  assert refs[0]==refs[1];return refs[0]
 # Prespecified actual rounded callback samples,not analytic unrounded f(x+h).
 samples=[('quadratic',3.,.2,9.,(3.+.2)**2,6.),('cancelled product',1.,1-u,0.,1.,1+u),('underflowed product',1.,.5,0.,tiny,tiny),('zero exact change',1.,.125,1.,1.,2.),('collided shocked point',1.,tiny,1.,1.,1.),('exact change overflow',1.,.125,-mx,mx,0.),('linear value overflow',1.,1.,mx,mx,mx),('relative error overflow',1.,1.,0.,tiny,1.),('signed error overflow',1.,1.,0.,mx,-mx),('negative signed error',100.,5.,3000.,3097.5,20.),('negative zeros',0.,-0.,-0.,-0.,-0.)]
 for label,x,h,y0,y1,d in samples:
  want=report_ref(y0,y1,d,h)
  for j,key in enumerate(FIELDS):
   def run(x=x,h=h,y0=y0,y1=y1,d=d,key=key):
    samples=iter((y0,y1));return source.compare_change(lambda z:next(samples),lambda z:d,x,h)[key]
   test(label+' '+key,run,want[j])
 controls=[]
 def control(name,x,h,fn,df,want,expected):
  seen=[]
  def fun(z):seen.append(('f',z));return fn(z,len(seen))
  def der(z):seen.append(('d',z));return df(z)
  try:a=source.compare_change(fun,der,x,h);actual='returned'
  except Exception as e:actual=type(e).__name__
  rows.append(dict(name=name,actual=actual,expected=want,calls=[repr(z) for z in seen],expected_calls=[repr(z) for z in expected],passed=actual==want and seen==expected))
 for x,h in [(math.inf,1.),(math.nan,1.),(True,1.),(10**1000,1.),(1.,math.inf),(1.,math.nan),(1.,True),(1.,10**1000),(1e308,1e308),(-1e308,-1e308)]:
  control('preflight '+repr((x,h)),x,h,lambda z,i:1.,lambda z:0.,'TypeError' if type(x) is bool or type(h) is bool else 'ValueError',[])
 for stage in (1,2,3):
  for val in (True,None,math.nan,math.inf,10**1000):
   expected='TypeError' if val is True or val is None else 'ValueError'
   control('invalid output stage'+str(stage)+' '+repr(val),2.,.125,lambda z,i,s=stage,v=val:v if i==s else 1.,lambda z,s=stage,v=val:v if s==3 else 0.,expected,[('f',2.),('f',2.125),('d',2.)][:stage])
  for kind in (TypeError,RuntimeError):
   def fun(z,i,s=stage,k=kind):
    if i==s:raise k('callback sentinel')
    return 1.
   def der(z,s=stage,k=kind):
    if s==3:raise k('derivative sentinel')
    return 0.
   control('callback '+kind.__name__+' stage'+str(stage),2.,.125,fun,der,kind.__name__,[('f',2.),('f',2.125),('d',2.)][:stage])
 control('zero shock retains two f calls',2.,0.,lambda z,i:1.,lambda z:0.,'returned',[('f',2.),('f',2.),('d',2.)])
 for i,args in enumerate([(None,lambda z:0.,math.nan,0.),(lambda z:1.,None,math.nan,0.)]):test('callable first'+str(i),lambda args=args:source.compare_change(*args),'TypeError')
 for i,args in enumerate([(True,1.,1.),(1.,True,1.),(1.,1.,True),(math.nan,1.,1.),(1.,math.inf,1.),(1.,1.,10**1000)]):test('affine input'+str(i),lambda args=args:source.linear_taylor(*args),'TypeError' if any(type(x) is bool for x in args) else 'ValueError')
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'affine/report predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
