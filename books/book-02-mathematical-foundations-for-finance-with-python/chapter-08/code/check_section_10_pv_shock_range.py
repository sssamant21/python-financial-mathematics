"""Independent high-precision references for exact assessment PV/shock calls."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_8_10 as source

def observations():
 rows=[]
 def test(name,fn,want):
  try:
   actual=fn()
   if isinstance(want,str):ok=False
   elif want==0:ok=actual==0 and math.copysign(1,actual)==math.copysign(1,want)
   else:ok=math.isfinite(actual) and math.isclose(actual,want,rel_tol=5e-14,abs_tol=0)
  except Exception as e:actual=type(e).__name__;ok=actual==want
  rows.append(dict(name=name,actual=repr(actual),expected=repr(want),passed=ok))
 def refs(c,r,t,h=None):
  out=[]
  for precision in (1300,1800):
   with localcontext(Context(prec=precision)):
    C,R,T=map(Decimal,(c,r,t));exponent=-R*T
    if h is None:coeff=[C,-T*C,T*T*C];es=[exponent]*3
    else:
     H=Decimal(h);g=T*H;coeff=[-C*g,C*g*(g/2-1)];es=[exponent]*2
     # Independent complete difference of exponential levels at high precision.
     if C==0 or T==0 or H==0:exact=Decimal('-0') if not (math.copysign(1,c)*math.copysign(1,t)*math.copysign(1,h)<0) else Decimal(0)
     elif max(exponent,-(R+H)*T)>10000:exact=Decimal('Infinity')
     else:exact=C*((-(R+H)*T).exp()-exponent.exp())
    a=[]
    for k,e in zip(coeff,es):
     if k==0:value=k
     elif e>10000:value=Decimal('Infinity').copy_sign(k)
     elif e< -10000:value=Decimal(0).copy_sign(k)
     else:value=k*e.exp()
     f=float(value);a.append(f if math.isfinite(f) else 'ValueError')
    if h is None and (c==0 or t==0):a[1]=-0.0
    if h is not None:
     if c==0 or t==0 or h==0:a[0]=-0.0*c*t*h;a[1]=0.0  # stated sum/zero reporting convention
     f=float(exact);a.append(f if math.isfinite(f) else 'ValueError')
    out.append(a)
  assert out[0]==out[1],(out,c,r,t,h)
  return out[0]
 pv=[(10000.,.04,5.),(1e-300,-1.,710.),(1e300,1.,750.),(1e-200,0.,1e200),(1.,0.,1e-200),(0.,-1e308,1e308),(1e308,-1.,1000.),(1.,1e308,1e308),(2.,.1,0.)]
 for i,(c,r,t) in enumerate(pv):
  want=refs(c,r,t);test('PV'+str(i),lambda:source.present_value(c,r,t),want[0])
  for j in range(3):
   expected='ValueError' if 'ValueError' in want else want[j]
   test('PV tuple'+str(i)+' field'+str(j),lambda j=j:source.pv_rate_derivatives(c,r,t)[j],expected)
 shocks=[(10000.,.04,5.,.001),(1e-300,-1.,710.,.001),(1e300,1.,750.,-.001),(1.,0.,1e200,1e-200),(1e-200,0.,1e200,1e-200),(1.,0.,2.,1.),(1e308,0.,1.,1e-308),(2.,.1,0.,.1),(0.,-1e308,1e308,.1)]
 for i,(c,r,t,h) in enumerate(shocks):
  want=refs(c,r,t,h)
  for j,key in enumerate(('first_order','second_order','exact')):
   expected='ValueError' if 'ValueError' in want else want[j]
   test('shock'+str(i)+' '+key,lambda k=key:source.pv_rate_shock(c,r,t,h)[k],expected)
 for name,fn,want in [('negative amount',lambda:source.present_value(-1,0,1),'ValueError'),('negative years',lambda:source.pv_rate_derivatives(1,0,-1),'ValueError'),('years validation first',lambda:source.pv_rate_derivatives('x',0,True),'TypeError'),('shock validation first',lambda:source.pv_rate_shock('x',0,1,True),'TypeError'),('nonfinite rate',lambda:source.present_value(0,math.inf,1),'ValueError'),('oversized amount',lambda:source.present_value(10**1000,0,0),'ValueError')]:test(name,fn,want)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'PV/shock predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
