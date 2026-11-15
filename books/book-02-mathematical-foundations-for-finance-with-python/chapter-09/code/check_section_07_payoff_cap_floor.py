"""Exact rational payoff/one-sided secants; explicit finite payment policy."""
from fractions import Fraction
from pathlib import Path
import math,json,sys,hashlib
import section_9_07 as m
rows=[]
def add(label,field,actual,expected):
 ok=actual==expected if isinstance(expected,(str,bool)) else isinstance(actual,float) and math.isfinite(actual) and math.isclose(actual,expected,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=label,field=field,actual=repr(actual),expected=repr(expected),passed=ok))
def safe(fn,*args):
 try:return fn(*args)
 except Exception as e:return type(e).__name__
for s,k in [(98.,100.),(100.,100.),(102.,100.),(1.,2.),(2.,1.),(1e308,1.),(1.,1e308),(1e308,1e308),(math.nextafter(100.,0.),100.),(math.nextafter(100.,math.inf),100.),(math.ulp(0.),math.ulp(0.)),(1e-308,2e-308)]:
 S,K=map(Fraction,(s,k));h=min(x for x in [S/2,abs(S-K)/2,K/2] if x>0)
 for name,fn,slopes,pay in [('call',m.call_payoff,m.call_slopes,lambda x:max(x-K,0)),('put',m.put_payoff,m.put_slopes,lambda x:max(K-x,0))]:
  val=pay(S);left=(val-pay(S-h))/h;right=(pay(S+h)-val)/h;actual=slopes(s,k)
  for field,got,want in [('value',fn(s,k),float(val)),('left',actual['left'],float(left)),('right',actual['right'],float(right)),('differentiable',actual['differentiable'],left==right)]:add(f'{name} S={s} K={k}',field,got,want)
CAPS=[('below',.01,1000.,.02,.05),('floor',.02,1000.,.02,.05),('inside',.03,1000.,.02,.05),('cap',.05,1000.,.02,.05),('above',.06,1000.,.02,.05),('negative floor',-.1,1000.,-.05,.05),('negative interior',-.03,1000.,-.05,.05),('negative cap',0.,1000.,-.05,-.01),('zero rate',0.,1000.,-.01,.01),('large finite',1.,1e308,0.,2.),('positive overflow',1e308,1e308,0.,1e308),('negative overflow',-1e308,1e308,-1e308,0.),('subnormal underflow',.5,math.ulp(0.),0.,1.),('integer inputs',3,1000,2,5),('adjacent floor',math.nextafter(.02,0.),1000.,.02,.05),('adjacent cap',math.nextafter(.05,math.inf),1000.,.02,.05)]
for label,r,n,a,c in CAPS:
 R,N,A,C=[Fraction(float(x)) for x in (r,n,a,c)]
 def pay(x):return N*min(max(x,A),C)
 value=pay(R)
 try:fv=float(value)
 except OverflowError:fv=math.inf
 if not math.isfinite(fv):expected='ValueError'
 else:
  h=min(x/2 for x in [C-A,abs(R-A),abs(R-C)] if x>0);left=(value-pay(R-h))/h;right=(pay(R+h)-value)/h;expected=(fv,float(left),float(right),left==right)
 val=safe(m.capped_floored_payment,r,n,a,c);sl=safe(m.cap_floor_slopes,r,n,a,c)
 for i,key in enumerate(['value','left','right','differentiable']):
  actual=val if i==0 else sl if isinstance(sl,str) else sl[key]
  add(label,key,actual,expected if isinstance(expected,str) else expected[i])
for name,fn,args,want in [('call bool',m.call_payoff,(True,1.),'TypeError'),('put negative spot',m.put_payoff,(-1.,1.),'ValueError'),('zero strike',m.call_slopes,(1.,0.),'ValueError'),('negative strike',m.put_slopes,(1.,-1.),'ValueError'),('nan spot',m.call_payoff,(math.nan,1.),'ValueError'),('huge int',m.put_payoff,(10**1000,1.),'ValueError'),('cap bool rate',m.capped_floored_payment,(True,1.,0.,1.),'TypeError'),('cap bool notional',m.cap_floor_slopes,(.5,True,0.,1.),'TypeError'),('cap zero notional',m.capped_floored_payment,(.5,0.,0.,1.),'ValueError'),('cap negative notional',m.cap_floor_slopes,(.5,-1.,0.,1.),'ValueError'),('equal thresholds',m.capped_floored_payment,(.5,1.,1.,1.),'ValueError'),('reversed thresholds',m.cap_floor_slopes,(.5,1.,1.,0.),'ValueError'),('infinite floor',m.capped_floored_payment,(.5,1.,-math.inf,1.),'ValueError'),('nan cap',m.cap_floor_slopes,(.5,1.,0.,math.nan),'ValueError'),('huge notional',m.capped_floored_payment,(.5,10**1000,0.,1.),'ValueError'),('nan rate before domain',m.cap_floor_slopes,(math.nan,0.,1.,0.),'ValueError')]:add(name,'rejection',safe(fn,*args),want)
for fn,expected in [(m.call_payoff,0.),(m.put_payoff,1.)]:add('domain boundary payoff only '+fn.__name__,'value',fn(0.,1.),expected)
add('payoff identity selected','identity',m.call_payoff(102.,100.)-m.put_payoff(102.,100.),2.)
add('cap scale selected','value',m.capped_floored_payment(.03,2000.,.02,.05),2*m.capped_floored_payment(.03,1000.,.02,.05))
add('cap branch continuity exact thresholds','value',m.capped_floored_payment(.02,1000.,.02,.05),20.)
add('cap upper continuity exact thresholds','value',m.capped_floored_payment(.05,1000.,.02,.05),50.)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Selected payoff and cap/floor only. Finite payment result is an explicit new report-range policy; slopes retain full payment eligibility. Exact rational neighboring secants are algebraic references, not finite-difference approximation acceptance. Spot-zero left-extension interpretation, difference/scenario contracts, resources/platform/independent approval remain open; zero signs numerical only.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
