"""Complete polynomial references and explicit integer-order selector policy."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_04 as source

def observations():
 rows=[]
 def test(name,fn,want,category='numeric/report contract'):
  try:a=fn();ok=math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,want) if want==0 else math.isclose(a,want,rel_tol=5e-14,abs_tol=0)) if isinstance(want,float) else a==want
  except Exception as e:a=type(e).__name__;ok=a==want
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok,category=category))
 def reference(vals,order):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    A,B,H=map(Decimal,vals);z=A*H+(B*H*H/2 if order==2 else Decimal(0));f=0. if z==0 else float(z);refs.append(f if math.isfinite(f) else 'ValueError')
  assert refs[0]==refs[1];return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.)
 cases=[(12.,12.,.1),(1.,2.,-.25),(-1e308,1e308,2.),(0.,tiny,2.),(mx,-mx,2.),(1e308,1e308,1e308),(0.,tiny,math.nextafter(2.,math.inf)),(1.,-2.,1.),(-0.,-0.,1.),(0.,1.,tiny),(0.,1e308,1e-308),(1e308,-1e308,math.nextafter(2.,0.)),(1e-308,1e-308,1e308),(-1.,-1.,0.)]
 for i,vals in enumerate(cases):
  for order in (1,2):test('complete polynomial'+str(i)+' order'+str(order),lambda vals=vals,order=order:source.taylor_change(*vals,order),reference(vals,order))
 for order in [True,False,1.,2.,'1',None]:test('selector type '+repr(order),lambda order=order:source.taylor_change(1.,2.,.1,order),'TypeError','new explicit strict built-in integer selector policy')
 for order in [0,3,-1]:test('selector domain '+repr(order),lambda order=order:source.taylor_change(1.,2.,.1,order),'ValueError','selector domain')
 controls=[(True,1.,.1,'TypeError'),(1.,True,.1,'TypeError'),(1.,1.,True,'TypeError'),(math.nan,1.,.1,'ValueError'),(1.,math.inf,.1,'ValueError'),(1.,1.,math.inf,'ValueError'),(10**1000,1.,.1,'ValueError'),('1',1.,.1,'TypeError')]
 for i,(*vals,want) in enumerate(controls):
  for order in (1,2):test('input'+str(i)+' order'+str(order),lambda vals=vals,order=order:source.taylor_change(*vals,order),want,'input contract retained')
 test('unused second remains validated',lambda:source.taylor_change(1.,math.nan,.1,1),'ValueError','input contract retained')
 test('input failure precedes bad selector',lambda:source.taylor_change(math.nan,1.,.1,None),'ValueError','validation priority retained')
 test('default equals order2',lambda:source.taylor_change(12.,12.,.1)==source.taylor_change(12.,12.,.1,2),True,'default order contract')
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'quadratic predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
