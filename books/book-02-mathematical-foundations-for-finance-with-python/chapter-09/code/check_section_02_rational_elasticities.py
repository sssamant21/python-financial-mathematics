"""Independent Decimal complete point/arc/rate references with explicit zero policy."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_02 as source

def observations():
 rows=[]
 def test(name,fn,want):
  try:
   a=fn();ok=(math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,want) if want==0 else math.isclose(a,want,rel_tol=4e-15,abs_tol=0))) if isinstance(want,float) else a==want
  except Exception as e:a=type(e).__name__;ok=a==want
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
 def oracle(values,kind):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    d=list(map(Decimal,values))
    if kind=='point':
     x,y,s=d;z=x*s/y
    elif kind=='arc':
     a,b,c,e=d;z=(e-c)*(a+b)/((b-a)*(c+e))
    else:z=-d[0]*d[1]
    f=float(z);refs.append(f if math.isfinite(f) else 'ValueError')
  assert refs[0]==refs[1]
  # Signed exact zeros are policy checks,not unique mathematical signs.
  if kind=='point' and values[2]==0:return values[0]*values[2]/values[1]
  if kind=='arc' and values[2]==values[3]:
   a,b,c,e=map(Decimal,values);sign=1 if (a+b)*(b-a)*(c+e)>0 else -1;return math.copysign(0.,sign)
  if kind=='rate' and values[1]==0:return -values[0]*values[1]
  return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.)
 points=[(2.,8.,12.),(1e308,1e308,1e308),(1e-308,1e-308,1e-308),(tiny,mx,mx),(mx,tiny,1.),(2.,-3.,4.),(2.,-3.,-0.),(-2.,3.,0.),(1e308,1e-308,1e-308)]
 for i,x in enumerate(points):test('point vector'+str(i),lambda x=x:source.point_elasticity(*x),oracle(x,'point'))
 arcs=[(10.,12.,80.,70.),(1e308,1.5e308,1e308,.5e308),(tiny,2*tiny,tiny,3*tiny),(1.,2.,tiny,0.),(1.,2.,mx,mx),(-mx,.5*mx,80.,70.),(1.,2.,-1.,-1.),(1.,math.nextafter(1.,math.inf),1.,math.nextafter(-1.,0.))]
 for i,x in enumerate(arcs):
  test('arc vector'+str(i),lambda x=x:source.arc_elasticity(*x),oracle(x,'arc'));rev=(x[1],x[0],x[3],x[2]);test('arc reverse'+str(i),lambda x=rev:source.arc_elasticity(*x),oracle(rev,'arc'))
 for i,x in enumerate([(.04,5.),(-.02,10.),(mx,0.),(1e308,1e308),(-1e308,1e308),(tiny,tiny),(-tiny,tiny)]):test('rate vector'+str(i),lambda x=x:source.discounted_rate_elasticity(*x),oracle(x,'rate'))
 for name,fn,want in [('point zero x',lambda:source.point_elasticity(0,1,1),'ValueError'),('point zero value',lambda:source.point_elasticity(1,0,1),'ValueError'),('point NaN',lambda:source.point_elasticity(math.nan,1,1),'ValueError'),('point bool before NaN',lambda:source.point_elasticity(True,math.nan,1),'TypeError'),('point infinite value',lambda:source.point_elasticity(1,math.inf,1),'ValueError'),('arc equal x',lambda:source.arc_elasticity(1,1,80,70),'ValueError'),('arc zero x midpoint',lambda:source.arc_elasticity(-1,1,80,70),'ValueError'),('arc zero y midpoint',lambda:source.arc_elasticity(1,2,-1,1),'ValueError'),('arc bool',lambda:source.arc_elasticity(True,2,80,70),'TypeError'),('rate zero',lambda:source.discounted_rate_elasticity(0,5),'ValueError'),('rate negative years',lambda:source.discounted_rate_elasticity(.04,-1),'ValueError'),('rate bool years',lambda:source.discounted_rate_elasticity(.04,True),'TypeError')]:test(name,fn,want)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'rational elasticity predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
