"""Independent complete-discount/normalization/shock references and exact unit mapping."""
import math,json,sys
from decimal import Decimal,Context,localcontext
import section_9_01 as source

def observations():
 rows=[];units=[]
 def test(name,fn,want,rtol=5e-14):
  try:
   a=fn();ok=(math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,want) if want==0 else math.isclose(a,want,rel_tol=rtol,abs_tol=0))) if isinstance(want,float) else a==want
  except Exception as e:a=type(e).__name__;ok=a==want
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
 def refs(c,r,t,h=None):
  out=[]
  for precision in (1800,2400):
   with localcontext(Context(prec=precision)):
    C,R,T=map(Decimal,(c,r,t));E=-R*T
    if h is None:coeff=[C,-T*C];exps=[E,E]
    else:H=Decimal(h);coeff=[-C*T*H];exps=[E]
    a=[]
    for k,e in zip(coeff,exps):
     if k==0:z=k
     elif e>10000:z=Decimal('Infinity').copy_sign(k)
     elif e< -10000:z=Decimal(0).copy_sign(k)
     else:z=k*e.exp()
     f=float(z);a.append(f if math.isfinite(f) else 'ValueError')
    if h is None:
     if t==0:a[1]=-t*c
     for z in [T,-R*T]:
      f=float(z);a.append(f if math.isfinite(f) else 'ValueError')
     if r==0 or t==0:a[3]=-r*t
    else:
     z=C*((-(R+H)*T).exp()-E.exp());f=float(z);a.append(f if math.isfinite(f) else 'ValueError')
     if h==0 or t==0:a=[-0.*c*t*h]*2
    out.append(a)
  assert out[0]==out[1],out
  return out[0]
 vectors=[(10000.,.04,5.),(1e-300,-1.,710.),(1e300,1.,750.),(1e-200,0.,1e200),(1.,0.,1e-200),(1.,1.,1000.),(1e308,-1.,1000.),(2.,.1,0.),(1.,1e308,1e308)]
 for i,(c,r,t) in enumerate(vectors):
  want=refs(c,r,t);test('value vector'+str(i),lambda:source.discounted_value(c,r,t),want[0])
  for j,k in enumerate(('value','absolute','normalized_rate','elasticity')):test('sensitivity'+str(i)+' '+k,lambda k=k:source.discounted_sensitivity(c,r,t)[k],'ValueError' if 'ValueError' in want else want[j])
 shocks=[(10000.,.04,5.,.0001),(1e-300,-1.,710.,.001),(1e300,1.,750.,-.001),(1.,0.,1e200,1e-200),(1e-200,0.,1e200,1e-200),(1e308,-1.,1000.,0.),(1.,0.,2.,1.),(1e308,0.,1000.,-1.)]
 for i,(c,r,t,h) in enumerate(shocks):
  want=refs(c,r,t,h)
  for j,k in enumerate(('first_order','exact')):test('shock'+str(i)+' '+k,lambda k=k:source.discounted_shock(c,r,t,h)[k],'ValueError' if 'ValueError' in want else want[j])
 for h in (.0001,.0004,.01):
  want=refs(10000.,.04,5.,h)
  for j,k in enumerate(('first_order','exact')):test('exact printed unit/shock '+repr(h)+' '+k,lambda k=k:source.discounted_shock(10000,.04,5,h)[k],want[j])
 for name,fn,want in [('zero C domain',lambda:source.discounted_value(0,0,0),'ValueError'),('negative T',lambda:source.discounted_value(1,0,-1),'ValueError'),('rate first',lambda:source.discounted_sensitivity('x',True,math.nan),'TypeError'),('shock invalid',lambda:source.discounted_shock(1,0,1,True),'TypeError'),('nonfinite rate at T0',lambda:source.discounted_value(1,math.inf,0),'ValueError'),('oversized C',lambda:source.discounted_value(10**1000,0,0),'ValueError')]:test(name,fn,want)
 with localcontext(Context(prec=100)):
  r=Decimal('.04');relative=Decimal('.01');delta=r*relative
  for name,a,w in [('E10 relative delta',str(delta),'0.0004'),('E10 relative new rate',str(r+delta),'0.0404'),('E10 percentage-point new rate',str(r+Decimal('.01')),'0.05'),('E10 relative value linear effect',str(-Decimal(5)*delta),'-0.0020'),('E7 basis point',str(Decimal(1)/10000),'0.0001')]:units.append(dict(name=name,actual=a,expected=w,passed=a==w,scope='Supplemental exact unit arithmetic;not an invented source conversion API'))
 return dict(source_predicates=rows,supplemental_unit_predicates=units)
if __name__=='__main__':
 d=observations();print(json.dumps(d,indent=2));print(len(d['source_predicates']),'source predicates;',sum(not x['passed'] for x in d['source_predicates']),'failed;',len(d['supplemental_unit_predicates']),'supplemental units');assert all(x['passed'] for x in d['source_predicates']+d['supplemental_unit_predicates'])
