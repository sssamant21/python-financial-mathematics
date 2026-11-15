"""Independent complete value/derivative/normalization and whole-report policy."""
import math,json,sys
from decimal import Decimal,Context,localcontext,Inexact
import section_9_04 as source
FIELDS=['value','first','second','duration','convexity']
def observations():
 rows=[]
 def eq(a,b):
  if isinstance(b,float):return isinstance(a,(int,float)) and math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,b) if b==0 else math.isclose(a,b,rel_tol=5e-14,abs_tol=0))
  return a==b
 def test(name,a,want,category='complete report contract'):rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=eq(a,want),category=category))
 def report(z):
  a=float(z);return a if math.isfinite(a) else 'ValueError'
 def reference(vals):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    C,T,R=map(Decimal,vals);amp=C.ln()-T*R
    if amp>1000 or amp< -2000:out=['ValueError']*5
    else:
     B=C*(-T*R).exp();first=math.copysign(0.,-math.copysign(1.,vals[1])) if T==0 else report(-T*B);out=[report(B),first,report(T*T*B),float(T),report(T*T)]
     if out[0]==0 or 'ValueError' in out:out=['ValueError']*5
    refs.append(out)
  assert refs[0]==refs[1],(vals,refs);return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.)
 cases=[(10000.,5.,.04),(1e-308,2.,-355.),(1e308,1e-308,0.),(1.,1e308,0.),(1e-308,2.,355.),(tiny,1.,1.),(tiny,0.,mx),(mx,0.,mx),(mx,1.,0.),(mx,2.,0.),(1.,1e154,0.),(1.,1.35e154,0.),(1e308,1e-308,1e308),(1e-308,1e154,0.),(1e-308,1.35e154,0.),(1.,mx,mx),(1.,mx,-mx),(100.,-0.,-0.),(100.,2.,-.05),(1e-308,mx,mx)]
 for i,vals in enumerate(cases):
  want=reference(vals)
  try:a=source.single_cash_flow(*vals)
  except Exception as e:a=type(e).__name__
  for j,key in enumerate(FIELDS):test('single'+str(i)+' '+key,a if isinstance(a,str) else a[key],want[j])
 controls=[('zero cash',(0.,1.,.1),'ValueError'),('negative cash',(-1.,1.,.1),'ValueError'),('negative time',(1.,-1.,.1),'ValueError'),('cash bool',(True,1.,.1),'TypeError'),('time bool',(1.,True,.1),'TypeError'),('rate bool',(1.,1.,True),'TypeError'),('cash None',(None,1.,.1),'TypeError'),('cash Decimal',(Decimal(1),1.,.1),'TypeError'),('time text',(1.,'1',.1),'TypeError'),('cash NaN',(math.nan,1.,.1),'ValueError'),('time inf',(1.,math.inf,.1),'ValueError'),('rate inf',(1.,0.,math.inf),'ValueError'),('cash oversized',(10**1000,1.,.1),'ValueError'),('rate validated before cash domain',(0.,1.,True),'TypeError')]
 for name,vals,want in controls:
  try:a=source.single_cash_flow(*vals)
  except Exception as e:a=type(e).__name__
  test(name,a,want,'input/domain policy retained')
 want=reference((1e-308,2.,-355.))[0]
 for label in ['inexact trap','restricted exponent']:
  with localcontext(Context(prec=2)) as ctx:
   ctx.traps[Inexact]=True
   if label=='restricted exponent':ctx.Emax=9;ctx.Emin=-9
   before=(ctx.prec,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags))
   try:a=source.single_cash_flow(1e-308,2.,-355.)['value']
   except Exception as e:a=type(e).__name__
   test('ambient '+label,a,want);test('caller context '+label,(ctx.prec,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags))==before,True,'context isolation')
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'single-report predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
