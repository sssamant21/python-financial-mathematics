"""Complete sampled-ratio references and actual callback consumption contracts."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_02 as source

def observations():
 rows=[]
 def compare(a,b):
  if isinstance(b,float):return isinstance(a,(int,float)) and math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,b) if b==0 else math.isclose(a,b,rel_tol=5e-14,abs_tol=0))
  return a==b
 def test(name,x,h,fn,expected,expected_calls):
  seen=[]
  def callback(z):seen.append(z);return fn(z,len(seen))
  try:a=source.centered_elasticity(callback,x,h)
  except Exception as e:a=type(e).__name__
  ok=compare(a,expected) and seen==expected_calls
  rows.append(dict(name=name,x=repr(x),step=repr(h),actual=repr(a),expected=repr(expected),calls=[repr(z) for z in seen],expected_calls=[repr(z) for z in expected_calls],passed=ok))
 def ref(x,h,ys):
  vals=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    X,H,Y,U,D=map(Decimal,(x,h,*ys));z=X*(U-D)/(2*H*Y)
    f=float(z);vals.append(f if math.isfinite(f) else 'ValueError')
  assert vals[0]==vals[1]
  return vals[0]
 # y=f(x),up=f(fl(x+h)),down=f(fl(x-h));reference is sampled nominal-2h formula.
 samples=[('ordinary quadratic',2.,.125,(4.,2.125**2,1.875**2)),('sum difference overflow',1.,1e308,(1.,1e308,-1e308)),('derivative underflow',1e308,1e307,(1.,1e-308,0.)),('normalization overflow',1e308,1e307,(1e-308,1e-308,0.)),('derivative overflow rescued',1e-308,5e-309,(1e308,1e308,-1e308)),('negative x',-2.,.125,(4.,(-1.875)**2,(-2.125)**2)),('zero difference',2.,.125,(3.,3.,3.)),('final overflow',1.,.125,(math.ulp(0.),1.,-1.)),('negative final underflow',1e-308,5e-309,(1e308,0.,math.ulp(0.))),('large denominator finite difference',1.,1e308,(1.,1.,-1.)),('subnormal x linear',math.ulp(0.),math.ulp(0.),(math.ulp(0.),2*math.ulp(0.),0.))]
 for name,x,h,ys in samples:
  test(name,x,h,lambda z,i,ys=ys:ys[i-1],ref(x,h,ys),[x,x+h,x-h])
 for x,h in [(0.,.1),(math.inf,.1),(math.nan,.1),(True,.1),(10**1000,.1),(1.,0.),(1.,-1.),(1.,True),(1.,math.inf),(1.,math.nan),(1.,10**1000),(1.,math.ulp(0.)),(1e308,1e308),(-1e308,1e308)]:
  expected='TypeError' if type(x) is bool or type(h) is bool else 'ValueError'
  test('preflight '+repr((x,h)),x,h,lambda z,i:1.,expected,[])
 # Callback invocation order retained:central,plus,minus;stop at first raised/invalid output.
 for stage in (1,2,3):
  for value in (True,None,math.inf,math.nan,10**1000):
   expected='TypeError' if value is True or value is None else 'ValueError'
   test('bad sample stage'+str(stage)+' '+repr(value),2.,.125,lambda z,i,v=value,s=stage:v if i==s else 1.,expected,[2.,2.125,1.875][:stage])
  for exc in (TypeError,RuntimeError):
   def fail(z,i,s=stage,k=exc):
    if i==s:raise k('deliberate callback error')
    return 1.
   test('callback '+exc.__name__+' stage'+str(stage),2.,.125,fail,exc.__name__,[2.,2.125,1.875][:stage])
 test('zero center preserves three evaluations',2.,.125,lambda z,i:0. if i==1 else 1.,'ValueError',[2.,2.125,1.875])
 try:source.centered_elasticity(None,math.nan,0)
 except Exception as e:a=type(e).__name__
 rows.append(dict(name='callable validation precedes numeric input',actual=a,expected='TypeError',passed=a=='TypeError'))
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'centered predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
