"""Independent complete model expectations;latent analytic baselines differ from supplied zero."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_02 as source

def observations():
 rows=[]
 def test(name,fn,want):
  try:
   a=fn();ok=(math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,want) if want==0 else math.isclose(a,want,rel_tol=5e-14,abs_tol=0))) if isinstance(want,float) else a==want
  except Exception as e:a=type(e).__name__;ok=a==want
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
 def report(z):
  f=float(z);return f if math.isfinite(f) else 'ValueError'
 def power_ref(p,a,e):
  refs=[]
  for precision in (1800,2400):
   with localcontext(Context(prec=precision)):
    P,A,E=map(Decimal,(p,a,e))
    def power(c,k):
     if c==0:return e*0.0
     if P==1:return report(c)
     amp=abs(c).ln()+k*P.ln()
     if amp>10000:return 'ValueError'
     if amp< -10000:return -0. if c<0 else 0.
     return report(c*P**k)
    refs.append([power(A,E),power(E*A,E-1),float(E)])
  assert refs[0]==refs[1]
  return refs[0]
 def linear_ref(p,a,b):
  refs=[]
  for precision in (1800,2400):
   with localcontext(Context(prec=precision)):
    P,A,B=map(Decimal,(p,a,b));Q=A-B*P
    refs.append(['ValueError']*5 if Q<=0 else [report(x) for x in (Q,-B,-B*P/Q,P*Q,A-2*B*P)])
  assert refs[0]==refs[1]
  return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.);u=math.ulp(1.)
 powers=[(20.,400.,-1.5),(1e308,1e308,-2.),(1e-308,1e-308,-2.),(1e-200,1e-200,1.),(1e200,1e-200,2.),(mx,1.,0.),(1.,1.,-0.),(1.,1e308,1e308),(2.,1.,1e308)]
 for i,x in enumerate(powers):
  want=power_ref(*x)
  for j,k in enumerate(('quantity','derivative','elasticity')):test('constant'+str(i)+' '+k,lambda x=x,k=k:source.constant_elasticity_demand(*x)[k],'ValueError' if 'ValueError' in want else want[j])
 linear=[(10.,100.,2.),(25.,100.,2.),(40.,100.,2.),(1-u,1.,1+u),(1e-308,1e-308,1-u),(1e308,1e308,.5),(mx,mx,tiny),(1.,1.,1.),(1.,1.,math.nextafter(1.,math.inf)),(tiny,1.,1.)]
 for i,x in enumerate(linear):
  want=linear_ref(*x)
  for j,k in enumerate(('quantity','derivative','elasticity','revenue','revenue_derivative')):test('linear'+str(i)+' '+k,lambda x=x,k=k:source.linear_demand(*x)[k],'ValueError' if 'ValueError' in want else want[j])
 incomes=[(50000.,5.,.7),(1e308,1e308,-2.),(1e-308,1e-308,-2.),(1e-200,1e-200,2.),(1.,1e308,1e308),(1.,1.,0.),(1.,1.,-0.)]
 # Exact analytic identity: I*Q'(I)/Q(I)=e for positive I,a,regardless of unreported Q range.
 for i,x in enumerate(incomes):test('income analytic'+str(i),lambda x=x:source.income_elasticity(*x),x[2])
 for name,fn,want in [('constant zero price',lambda:source.constant_elasticity_demand(0),'ValueError'),('constant zero scale',lambda:source.constant_elasticity_demand(1,0),'ValueError'),('constant scale before exponent',lambda:source.constant_elasticity_demand(1,True,math.nan),'TypeError'),('linear negative slope',lambda:source.linear_demand(1,100,-1),'ValueError'),('linear slope bool',lambda:source.linear_demand(1,100,True),'TypeError'),('linear NaN price',lambda:source.linear_demand(math.nan),'ValueError'),('income zero',lambda:source.income_elasticity(0),'ValueError'),('income negative scale',lambda:source.income_elasticity(1,-1),'ValueError'),('income scale before exponent',lambda:source.income_elasticity(1,True,math.nan),'TypeError'),('income infinite exponent',lambda:source.income_elasticity(1,5,math.inf),'ValueError')]:test(name,fn,want)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'model predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
