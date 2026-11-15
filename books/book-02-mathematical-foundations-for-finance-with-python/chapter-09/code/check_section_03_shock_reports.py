"""Independent direct endpoint/change/error references for complete shock reports."""
import math,json,sys
from decimal import Decimal,Context,localcontext,Inexact
import section_9_03 as source
FIELDS=['baseline_value','exact_change','linear_change','linear_value','signed_error','absolute_error','relative_change_error']
def observations():
 rows=[]
 def eq(a,b):
  if isinstance(b,float):return isinstance(a,(int,float)) and math.isfinite(a) and (a==0 and math.copysign(1,a)==math.copysign(1,b) if b==0 else math.isclose(a,b,rel_tol=5e-14,abs_tol=0))
  return a==b
 def test(name,a,b):rows.append(dict(name=name,actual=repr(a),expected=repr(b),passed=eq(a,b)))
 def report(z):
  a=float(z);return a if math.isfinite(a) else 'ValueError'
 def reference(vals):
  refs=[]
  for prec in (1800,2400):
   with localcontext(Context(prec=prec)):
    C,T,R,H=map(Decimal,vals)
    def value(exponent):
     amp=C.ln()+exponent
     if amp>1000:return 'ValueError'
     # Only selected extreme endpoints are replaced by0;bounded-away normalized cases below.
     if exponent< -20000:return Decimal(0)
     return C*exponent.exp()
    B=value(-T*R)
    if B=='ValueError':out=['ValueError']*7
    elif T==0 or H==0:
     zero=math.copysign(0.,-math.copysign(1.,vals[1])*math.copysign(1.,vals[3]));out=[report(B),zero,zero,report(B),0.,0.,None]
    else:
     S=value(-T*(R+H))
     if S=='ValueError':out=['ValueError']*7
     else:
      E=S-B;A=-T*B*H;error=E-A;out=[report(B),report(E),report(A),report(B+A),report(error),report(abs(error)),report(abs(error)/abs(E))]
      if 'ValueError' in out:out=['ValueError']*7
    refs.append(out)
  assert refs[0]==refs[1],(vals,refs);return refs[0]
 mx=sys.float_info.max;tiny=math.ulp(0.)
 cases=[(10000.,5.,.04,.001),(10000.,5.,.04,-.001),(1e-308,2.,355.,-355.),(1e308,2.,355.,1e-308),(1e308,1e308,0.,0.),(mx,0.,mx,mx),(100.,5.,.04,-0.),(tiny,tiny,0.,tiny),(1.,1e308,0.,1e-308),(1e-308,1e308,0.,1.),(1.,mx,mx,-mx),(1.,mx,mx,0.),(1.,1e308,0.,1.),(1e308,2.,-355.,0.),(1.,1.,0.,-1000.),(1e-308,1e308,0.,1e308),(1e308,1.,0.,-1.),(1e-308,1e308,0.,1e-308),(1e-308,1.,1000.,-1700.),(mx,tiny,0.,tiny)]
 for i,vals in enumerate(cases):
  want=reference(vals)
  try:actual=source.discount_shock(*vals)
  except Exception as e:actual=type(e).__name__
  for j,key in enumerate(FIELDS):test('shock'+str(i)+' '+key,actual if isinstance(actual,str) else actual[key],want[j])
 controls=[('zero cash',(0.,1.,.1,.1),'ValueError'),('negative cash',(-1.,1.,.1,.1),'ValueError'),('negative time',(1.,-1.,.1,.1),'ValueError'),('cash bool',(True,1.,.1,.1),'TypeError'),('time bool',(1.,True,.1,.1),'TypeError'),('rate bool',(1.,1.,True,.1),'TypeError'),('shock bool',(1.,1.,.1,True),'TypeError'),('cash NaN',(math.nan,1.,.1,.1),'ValueError'),('time inf',(1.,math.inf,.1,.1),'ValueError'),('rate inf',(1.,0.,math.inf,.1),'ValueError'),('shock inf',(1.,0.,.1,math.inf),'ValueError'),('cash oversized',(10**1000,1.,.1,.1),'ValueError'),('wrong cash type',('1',1.,.1,.1),'TypeError'),('shock checked before cash domain',(0.,1.,.1,True),'TypeError')]
 for name,vals,want in controls:
  try:a=source.discount_shock(*vals)
  except Exception as e:a=type(e).__name__
  test(name,a,want)
 want=reference((1e-308,2.,355.,-355.))[1]
 for label in ['inexact trap','restricted exponent']:
  with localcontext(Context(prec=2)) as ctx:
   ctx.traps[Inexact]=True
   if label=='restricted exponent':ctx.Emax=9;ctx.Emin=-9
   before=(ctx.prec,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags))
   try:a=source.discount_shock(1e-308,2.,355.,-355.)['exact_change']
   except Exception as e:a=type(e).__name__
   test('ambient '+label,a,want);test('caller context '+label,(ctx.prec,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags))==before,True)
 return rows
if __name__=='__main__':
 rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'shock-report predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
