"""Independent direct 1800/2400-digit spot-curve report references."""
from decimal import Decimal,Context,localcontext,getcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_06 as m
CASES=[('ordinary',[(100.,1.),(1100.,2.)],[.035,.04]),('exp rescue',[(1e-308,2.)],[-355.]),('underflowed factor',[(1e308,1000.),(1.,0.)],[1.,0.]),('aggregate overflow',[(8e307,1.),(8e307,1.)],[0.,0.]),('aggregate derivative overflow',[(5e307,2.),(5e307,2.)],[0.,0.]),('true value overflow',[(1e308,1.),(1e308,1.)],[0.,0.]),('true derivative overflow',[(1e308,2.)],[0.]),('zero time',[(1e308,0.)],[1e308]),('large exponent product',[(1.,1e308)],[1e308]),('all amount underflow',[(1e-308,2.)],[355.]),('eligible tiny leg',[(1e-308,2.),(1.,0.)],[355.,0.]),('integer inputs',[(100,1),(1100,2)],[0,0]),('subnormal',[(math.ulp(0.),0.)],[0.]),('mixed spot',[(10.,2.),(20.,3.)],[-.1,.2]),('tiny horizon',[(1e308,1e-308)],[1.]),('zero negative rate',[(1.,0.)],[-0.])]
def reference(flows,rates,prec):
 with localcontext(Context(prec=prec)):
  V=Decimal(0);ds=[]
  for (c,t),z in zip(flows,rates):
   C,T,Z=[Decimal.from_float(float(x)) for x in (c,t,z)]
   exponent=-Z*T
   # Beyond these guards even the largest finite coefficient and t cannot
   # rescue exp(-10000); exp(10000) exceeds range even at min positive cash.
   amount=Decimal(0) if exponent < -10000 else (Decimal('Infinity') if exponent>10000 else C*exponent.exp())
   V+=amount;ds.append(-T*amount)
  try:out=[float(V),*[float(x) for x in ds],float(sum(ds,Decimal(0)))]
  except (OverflowError,ValueError):return 'ValueError'
  return out if out[0]>0 and all(math.isfinite(x) for x in out) else 'ValueError'
rows=[]
for label,f,z in CASES:
 a=reference(f,z,1800);b=reference(f,z,2400);assert a==b,(label,a,b)
 try:
  out=m.spot_curve_sensitivity(f,z);actual=[out['value'],*out['spot_derivatives'],out['parallel_first']]
 except Exception as e:actual=type(e).__name__
 fields=['value',*[f'spot_derivative_{i}' for i in range(len(f))],'parallel_first']
 for i,k in enumerate(fields):
  want=b if isinstance(b,str) else b[i];got=actual if isinstance(actual,str) else actual[i]
  ok=got==want if isinstance(want,str) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
  rows.append(dict(case=label,field=k,actual=repr(got),expected=repr(want),passed=ok))
for label,f,z,want in [('flows first',None,None,'TypeError'),('empty first',[],None,'ValueError'),('cash bool',[(True,1.)],[0.],'TypeError'),('rate bool',[(1.,1.)],[True],'TypeError'),('negative cash',[(-1.,1.)],[0.],'ValueError'),('negative years',[(1.,-1.)],[0.],'ValueError'),('nan rate',[(1.,1.)],[math.nan],'ValueError'),('infinite years',[(1.,math.inf)],[0.],'ValueError'),('large int',[(10**1000,1.)],[0.],'ValueError'),('shape',[(1.,)],[0.],'ValueError'),('short rates',[(1.,1.)],[],'ValueError'),('long rates',[(1.,1.)],[0.,0.],'ValueError')]:
 try:a=m.spot_curve_sensitivity(f,z)
 except Exception as e:a=type(e).__name__
 rows.append(dict(case=label,actual=repr(a),expected=want,passed=a==want))
f=[(100.,1.),(1100.,2.)];z=[.035,.04];fc=f.copy();zc=z.copy();a=m.spot_curve_sensitivity(f,z)
rows.append(dict(case='ownership',passed=f==fc and z==zc))
rows.append(dict(case='one shot inputs',passed=m.spot_curve_sensitivity(iter(f),iter(z))==a))
b=m.spot_curve_sensitivity(f[::-1],z[::-1]);rows.append(dict(case='paired permutation',passed=b['value']==a['value'] and b['parallel_first']==a['parallel_first'] and b['spot_derivatives']==a['spot_derivatives'][::-1]))
b=m.spot_curve_sensitivity([(2*c,t) for c,t in f],z);rows.append(dict(case='scaling',passed=all(math.isclose(x,2*y,rel_tol=5e-14,abs_tol=0.) for x,y in zip([b['value'],*b['spot_derivatives'],b['parallel_first']],[a['value'],*a['spot_derivatives'],a['parallel_first']]))))
ctx=getcontext();old=ctx.copy()
with localcontext(Context(prec=9)):
 b=m.spot_curve_sensitivity(f,z)
rows.append(dict(case='ambient precision independent',passed=b==a and ctx.prec==old.prec and ctx.flags==old.flags and ctx.traps==old.traps))
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Spot curve only; exact represented binary inputs. Selected exponent guards and fixed precision are not universal resource/accuracy proof. Spot shock and platform/independent acceptance remain open.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
