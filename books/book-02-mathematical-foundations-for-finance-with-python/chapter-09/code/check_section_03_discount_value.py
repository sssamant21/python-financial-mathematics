"""Independent complete discounted-value references;shock reports remain separate."""
import math,json,sys
from decimal import Decimal,Context,localcontext,Inexact
import section_9_03 as source

def observations():
 rows=[]
 def test(name,fn,want):
  try:a=fn();ok=math.isfinite(a) and (a==0 if want==0 else math.isclose(a,want,rel_tol=5e-14,abs_tol=0)) if isinstance(want,float) else a==want
  except Exception as e:a=type(e).__name__;ok=a==want
  rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
 def reference(c,t,r):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    C,T,R=map(Decimal,(c,t,r));amplitude=C.ln()-T*R
    # exp(1000) exceeds binary64 max;exp(-2000) is below half the minimum subnormal.
    if amplitude>1000:f='ValueError'
    elif amplitude< -2000:f=0.
    else:
     f=float(C*(-T*R).exp())
     if not math.isfinite(f):f='ValueError'
    refs.append(f)
  assert refs[0]==refs[1];return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.)
 cases=[(10000.,5.,.04),(1e-308,2.,-355.),(1e308,2.,355.),(mx,0.,mx),(mx,mx,0.),(1.,mx,tiny),(1e-308,2.,355.),(1e308,2.,-355.),(1.,mx,mx),(1.,mx,-mx),(1.,1e308,1e-308),(tiny,1.,-1000.),(mx,1.,1000.),(tiny,1.,1.),(tiny,1.,.1),(mx,1.,-1e-16),(1.,-0.,-0.),(100.,1.,-.05)]
 for i,vals in enumerate(cases):test('complete value'+str(i),lambda vals=vals:source.discount_value(*vals),reference(*vals))
 controls=[('cash zero',(0.,1.,.1),'ValueError'),('cash negative',(-1.,1.,.1),'ValueError'),('negative time',(1.,-1.,.1),'ValueError'),('cash bool',(True,1.,.1),'TypeError'),('time bool',(1.,True,.1),'TypeError'),('rate bool',(1.,1.,True),'TypeError'),('cash NaN',(math.nan,1.,.1),'ValueError'),('time inf',(1.,math.inf,.1),'ValueError'),('rate inf',(1.,0.,math.inf),'ValueError'),('cash oversized',(10**1000,1.,.1),'ValueError'),('wrong type',('1',1.,.1),'TypeError'),('rate before cash domain',(0.,1.,math.nan),'ValueError')]
 for name,vals,want in controls:test(name,lambda vals=vals:source.discount_value(*vals),want)
 for label in ['trap inexact','restricted exponent']:
  with localcontext(Context(prec=2)) as ctx:
   ctx.traps[Inexact]=True
   if label=='restricted exponent':ctx.Emax=9;ctx.Emin=-9
   before=(ctx.prec,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags));test('ambient '+label,lambda:source.discount_value(1e-308,2.,-355.),reference(1e-308,2.,-355.));test('caller context '+label,lambda:(ctx.prec,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags))==before,True)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'discount-value predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
