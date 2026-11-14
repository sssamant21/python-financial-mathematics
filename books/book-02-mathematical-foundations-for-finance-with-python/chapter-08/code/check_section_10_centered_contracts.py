"""Independent Decimal sampled-stencil oracles plus callback/preflight contracts."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_8_10 as source

def observations():
 rows=[]
 def test(name,fn,want):
  try:
   a=fn()
   if isinstance(want,float):ok=math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,want) if want==0 else math.isclose(a,want,rel_tol=4e-15,abs_tol=0))
   else:ok=a==want
  except Exception as e:a=type(e).__name__;ok=a==want
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
 def expected(samples,h,order):
  refs=[]
  for precision in (2200,2600):
   with localcontext(Context(prec=precision)):
    s=list(map(Decimal,samples));H=Decimal(h);x=(s[0]-s[1])/(2*H) if order==1 else (s[0]-2*s[1]+s[2])/(H*H);f=float(x);refs.append(f if math.isfinite(f) else 'ValueError')
  assert refs[0]==refs[1]
  if order==1 and samples[0]==samples[1]:return samples[0]-samples[1] # declared signed pair-zero policy
  if order==2 and refs[0]==0:return 0.0 # canonical quadratic zero policy
  return refs[0]
 tiny=math.ulp(0.);mx=sys.float_info.max
 first=[(2.,.1,((2+.1)**3,(2-.1)**3)),(0.,1e308,(1e308,-1e308)),(0.,1e-308,(1e-308,-1e-308)),(0.,mx,(1.,-1.)),(0.,tiny,(tiny,0.)),(0.,1e-308,(1e308,0.)),(0.,1.,(-0.,0.)),(0.,1.,(1e-308,1e-308)),(0.,2.,(tiny,0.))]
 second=[(2.,.1,((2+.1)**2,4.,(2-.1)**2)),(0.,1e200,(1e200,0.,1e200)),(0.,1e-200,(tiny,0.,tiny)),(0.,1.,(mx,mx,mx)),(0.,1.,(mx,-mx,mx)),(0.,2.,(mx,-mx,mx)),(0.,1e-308,(1.,0.,0.)),(0.,1.,(-0.,0.,0.)),(0.,1e200,(0.,0.,0.))]
 for order,vectors,api in [(1,first,source.centered_first),(2,second,source.centered_second)]:
  for i,(x,h,samples) in enumerate(vectors):
   nodes=(x+h,x-h) if order==1 else (x+h,x,x-h);mapping=dict(zip(nodes,samples));seen=[]
   def callback(z):seen.append(z);return mapping[z]
   test('order'+str(order)+' sampled vector'+str(i),lambda:api(callback,x,h),expected(samples,h,order));test('order'+str(order)+' callback order'+str(i),lambda:seen,list(nodes))
 for name,api,x,h in [('first nonfinite perturb',source.centered_first,1e308,1e308),('second nonfinite perturb',source.centered_second,1e308,1e308),('first unperturbing',source.centered_first,1.,tiny),('second unperturbing',source.centered_second,1.,tiny),('first negative h',source.centered_first,0.,-1.),('second zero h',source.centered_second,0.,0.)]:
  seen=[]
  def callback(z):seen.append(z);return 0.
  test(name,lambda:api(callback,x,h),'ValueError');test(name+' no callback',lambda:seen,[])
 for order,api in [(1,source.centered_first),(2,source.centered_second)]:
  test('order'+str(order)+' callable before x',lambda:api(None,math.nan,1),'TypeError')
  test('order'+str(order)+' bool step',lambda:api(lambda z:0.,0,True),'TypeError')
  for label,value,want in [('bool',True,'TypeError'),('NaN',math.nan,'ValueError'),('oversized',10**1000,'ValueError')]:
   seen=[]
   def callback(z):seen.append(z);return value
   test('order'+str(order)+' bad sample '+label,lambda:api(callback,0.,1.),want);test('order'+str(order)+' stops first '+label,lambda:seen,[1.])
  seen=[]
  def callback(z):
   seen.append(z)
   if len(seen)==2:raise RuntimeError('deliberate callback failure')
   return 1.
  test('order'+str(order)+' callback propagation',lambda:api(callback,0.,1.),'RuntimeError');test('order'+str(order)+' stop second',lambda:len(seen),2)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'centered predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
