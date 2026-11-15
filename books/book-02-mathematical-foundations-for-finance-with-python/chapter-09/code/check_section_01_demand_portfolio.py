"""Independent high-precision complete power/portfolio references and domain controls."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_01 as source

def observations():
 rows=[]
 def test(name,fn,want):
  try:
   a=fn();ok=(math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,want) if want==0 else math.isclose(a,want,rel_tol=5e-14,abs_tol=0))) if isinstance(want,float) else a==want
  except Exception as e:a=type(e).__name__;ok=a==want
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
 def demand_ref(p,a,e):
  refs=[]
  for precision in (1800,2400):
   with localcontext(Context(prec=precision)):
    P,A,E=map(Decimal,(p,a,e))
    def power(c,k):
     if c==0:return e*0.0
     if P==1:z=c
     else:
      amplitude=abs(c).ln()+k*P.ln()
      if amplitude>10000:return 'ValueError'
      if amplitude< -10000:return -0. if c<0 else 0.
      z=c*(P**k)
     f=float(z);return f if math.isfinite(f) else 'ValueError'
    refs.append([power(A,E),power(E*A,E-1),float(E)])
  assert refs[0]==refs[1],refs
  return refs[0]
 def portfolio_ref(n,p,b):
  refs=[]
  for precision in (1800,2400):
   with localcontext(Context(prec=precision)):
    N,P,B=map(Decimal,(n,p,b));V=N*P+B
    if V<=0:refs.append(['ValueError']*3);continue
    f=float(V);el=float(N*P/V) if n!=0 else n*0.0;refs.append([f if math.isfinite(f) else 'ValueError',n,el])
  assert refs[0]==refs[1]
  return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.)
 demand=[(20.,400.,-1.5),(1e-308,1e-308,-2.),(1e308,1e308,-2.),(1e-200,1e-200,2.),(1e-200,1e-200,1.),(1e200,1e-200,2.),(mx,1.,0.),(1.,1e308,1e308),(2.,1.,1e308),(1.,1.,-0.)]
 for i,(p,a,e) in enumerate(demand):
  want=demand_ref(p,a,e);test('demand quantity'+str(i),lambda:source.demand_quantity(p,a,e),want[0])
  for j,k in enumerate(('quantity','absolute','elasticity')):test('demand sensitivity'+str(i)+' '+k,lambda k=k:source.demand_sensitivity(p,a,e)[k],'ValueError' if 'ValueError' in want else want[j])
 portfolios=[(20.,50.,1000.),(mx,2.,mx),(mx,tiny,0.),(tiny,tiny,0.),(0.,mx,100.),(1e308,1e-308,1.),(1e-308,1e308,1e308),(1.,mx,mx),(0.,1.,0.),(-0.,1.,5.)]
 for i,(n,p,b) in enumerate(portfolios):
  want=portfolio_ref(n,p,b)
  for j,k in enumerate(('value','absolute','elasticity')):test('portfolio'+str(i)+' '+k,lambda k=k:source.portfolio_sensitivity(n,p,b)[k],'ValueError' if 'ValueError' in want else want[j])
 for name,fn,want in [('demand zero price',lambda:source.demand_quantity(0),'ValueError'),('demand zero scale',lambda:source.demand_quantity(1,0),'ValueError'),('demand negative price',lambda:source.demand_sensitivity(-1),'ValueError'),('demand bool exponent',lambda:source.demand_sensitivity(1,400,True),'TypeError'),('demand exponent before scale',lambda:source.demand_sensitivity(1,True,math.nan),'ValueError'),('portfolio negative shares',lambda:source.portfolio_sensitivity(-1,1,0),'ValueError'),('portfolio zero price',lambda:source.portfolio_sensitivity(1,0,1),'ValueError'),('portfolio negative cash',lambda:source.portfolio_sensitivity(1,1,-1),'ValueError'),('portfolio bool shares',lambda:source.portfolio_sensitivity(True,1,0),'TypeError'),('portfolio nonfinite price',lambda:source.portfolio_sensitivity(0,math.inf,1),'ValueError')]:test(name,fn,want)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'demand/portfolio predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
