"""Original cash/spot references for complete nonparallel facade reports."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import json,math,hashlib,sys
import section_9_08 as m
KEYS=('baseline_value','exact_change','linear_change','quadratic_change','linear_error','quadratic_error','absolute_linear_error','absolute_quadratic_error')
CASES=[('ordinary',[(100.,1.),(1100.,2.)],[.035,.04],[10.,-20.]),('zero',[(100.,1.),(1100.,2.)],[.035,.04],[0.,0.]),('finite baseline factor overflow',[(1e-308,2.)],[-355.],[0.]),('rescued endpoint',[(1e308,1000.)],[1.],[-10000.]),('lost leg',[(1e-308,2.),(1.,0.)],[355.,0.],[-3550000.,0.]),('opposite shocks',[(100.,1.),(100.,1.)],[0.,0.],[500.,-500.]),('tiny errors',[(1e308,1.)],[0.],[1e-196]),('tiny time',[(1e308,1e-308)],[0.],[10000.]),('baseline underflow gate',[(1e-308,2.)],[355.],[-3550000.]),('baseline overflow gate',[(1e308,1.)],[-1.],[10000.]),('scenario overflow',[(1e308,1.)],[0.],[-20000.]),('unused derivative no gate',[(1e308,2.)],[0.],[0.]),('zero time',[(1e308,0.)],[1e308],[1e308]),('bp conversion underflow',[(1.,1.)],[0.],[math.ulp(0.)]),('integer inputs',[(100,1),(1100,2)],[0,0],[25,-25]),('large positive shock',[(1.,1.)],[0.],[1e8])]
def reference(flows,rates,bps,prec):
 with localcontext(Context(prec=prec)):
  V=S=L=B=Decimal(0)
  def amt(C,x):
   if x>10000:return Decimal('Infinity')
   return Decimal(0) if x < -10000 else C*x.exp()
  for (cash,time),rate,bp in zip(flows,rates,bps):
   C,T,R,H=[Decimal.from_float(float(x)) for x in (cash,time,rate,float(bp)/10000.)];v=amt(C,-R*T);V+=v;S+=amt(C,-(R+H)*T);L-=T*v*H;B+=T*T*v*H*H/2
  fv=float(V)
  if not math.isfinite(fv) or fv<=0:return 'ValueError'
  E=S-V;Q=L+B;values=[float(x) for x in (V,E,L,Q,E-L,E-Q,abs(E-L),abs(E-Q))]
  return 'ValueError' if not all(math.isfinite(x) for x in values) else dict(zip(KEYS,values))
rows=[]
def add(case,field,actual,expected,kind='contract'):
 ok=actual==expected if isinstance(expected,(str,bool,list)) else type(actual)is float and math.isfinite(actual) and math.isclose(actual,expected,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(actual),expected=repr(expected),kind=kind,passed=ok))
for label,f,r,bp in CASES:
 a=reference(f,r,bp,1800);b=reference(f,r,bp,2400);assert a==b
 try:got=m.spot_scenario(f,r,bp)
 except Exception as e:got=type(e).__name__
 for key in KEYS:add(label,key,got if isinstance(got,str) else got[key],b if isinstance(b,str) else b[key],'range policy' if isinstance(b,str) else 'numerical')
for label,f,r,bp,want in [('empty',[],[],[],'ValueError'),('none flow',None,[],[],'TypeError'),('missing rate',[(1.,1.)],[],[0.],'ValueError'),('extra shock',[(1.,1.)],[0.],[0.,0.],'ValueError'),('bool rate',[(1.,1.)],[True],[0.],'TypeError'),('nan rate',[(1.,1.)],[math.nan],[0.],'ValueError'),('bool shock',[(1.,1.)],[0.],[True],'TypeError'),('huge shock',[(1.,1.)],[0.],[10**1000],'ValueError'),('zero cash',[(0.,1.)],[0.],[0.],'ValueError'),('negative time',[(1.,-1.)],[0.],[0.],'ValueError')]:
 try:got=m.spot_scenario(f,r,bp)
 except Exception as e:got=type(e).__name__
 add(label,'rejection',got,want)
f=[(100.,1.),(1100.,2.)];r=[.035,.04];bp=[10.,-20.];copy=(f.copy(),r.copy(),bp.copy());a=m.spot_scenario(f,r,bp);b=m.spot_scenario(iter(f),iter(r),iter(bp))
add('one-shot vectors','report',a==b,True);add('ownership','inputs',(f,r,bp)==copy,True);add('rate metadata','rates',a['spot_rates'],r);add('shock metadata','bp',a['shock_bp'],bp);add('exact schema','keys',sorted(a),sorted(list(KEYS)+['model','spot_rates','shock_bp']));add('permutation','same numeric fields',all(math.isclose(a[k],m.spot_scenario(f[::-1],r[::-1],bp[::-1])[k],rel_tol=5e-14,abs_tol=0.) for k in KEYS),True)
for kind in ('rate','shock'):
 sentinel=RuntimeError(kind+' sentinel')
 def late():yield 0.;raise sentinel
 try:m.spot_scenario(f,late() if kind=='rate' else r,late() if kind=='shock' else bp);same=False
 except Exception as e:same=e is sentinel
 add('late '+kind+' exception','identity',same,True)
add('spot value no derivative eligibility gate','zero changes',all(m.spot_scenario([(1e308,2.)],[0.],[0.])[k]==0. for k in KEYS[1:]),True)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Selected original-cash/spot complete report fields. Positive reported baseline gate retained; no unused derivative gate. Reported bp conversion preserved. Fixed precision/resource and independent model/platform/release acceptance open; numeric zeros no sign policy.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
