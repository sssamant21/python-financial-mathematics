"""Complete project scenario rows from independent original-input references."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_09 as m
NUM=('shock_bp','shock_decimal','exact_change','linear_change','quadratic_change','exact_value','linear_error','quadratic_error','absolute_linear_error','absolute_quadratic_error','linear_bound','quadratic_bound');FIELDS=NUM+('linear_bound_pass','quadratic_bound_pass')
CASES=[('ordinary plus',[(120.,.5),(120.,1.),(120.,2.),(1120.,3.)],.04,100.),('ordinary minus',[(120.,.5),(120.,1.),(120.,2.),(1120.,3.)],.04,-100.),('zero shock',[(100.,1.),(1100.,2.)],.04,0.),('tiny direct endpoint',[(1.,1.)],0.,500000.),('tiny latent errors',[(1e308,1.)],0.,1e-196),('rescued vanished leg',[(1e-308,2.),(1.,0.)],355.,-3550000.),('baseline factor rescued',[(1e-308,2.)],-355.,0.),('latent cubic moment',[(1e100,1e100)],0.,1e-196),('subnormal report fields',[(1e-308,1e154)],0.,1e-150),('finite shifted-rate gate',[(1.,0.)],sys.float_info.max,sys.float_info.max),('zero time large rate',[(1e308,0.)],1e308,1e308),('bp underflow',[(1.,1.)],0.,math.ulp(0.)),('value overflow',[(1e308,1.)],0.,-10000.),('true change overflow',[(1e308,1.)],0.,-20000.),('baseline overflow',[(1e308,0.),(1e308,0.)],0.,0.),('integer inputs',[(100,1),(1100,2)],0,25),('exact value underflow',[(1.,1.)],0.,1e8),('baseline underflow gate',[(1e-308,2.)],355.,-3550000.)]
def reference(flows,rate,bp,prec):
 with localcontext(Context(prec=prec)):
  R=Decimal.from_float(float(rate));h=float(bp)/10000.;H=Decimal.from_float(h)
  if not math.isfinite(float(rate)+h):return 'ValueError'
  V=A=B=Decimal(0);parts=[]
  def amount(C,x):
   if x>10000:return Decimal('Infinity')
   return Decimal(0) if x < -10000 else C*x.exp()
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];v=amount(C,-R*T);V+=v;A-=T*v;B+=T*T*v;parts.append((C,T,v))
  if V==0:return 'ValueError'
  baseline=[float(x) for x in (V,A,B,-A/V,B/V)]
  if baseline[0]<=0 or not all(math.isfinite(x) for x in baseline):return 'ValueError'
  S=sum((amount(C,-(R+H)*T) for C,T,v in parts),Decimal(0));E=S-V;L=A*H;Q=L+B*H*H/2;low=min(R,R+H)
  b1=sum((T*T*amount(C,-low*T)*H*H/2 for C,T,v in parts),Decimal(0));b2=sum((T*T*T*amount(C,-low*T)*abs(H)**3/6 for C,T,v in parts),Decimal(0))
  vals=[float(bp),h]+[float(x) for x in (E,L,Q,S,E-L,E-Q,abs(E-L),abs(E-Q),b1,b2)]
  if not all(math.isfinite(x) for x in vals):return 'ValueError'
  allowance=1e-12*max(1.,abs(baseline[0]));return dict(zip(FIELDS,vals+[vals[8]<=vals[10]+allowance,vals[9]<=vals[11]+allowance]))
rows=[]
def add(case,field,actual,expected,kind='contract'):
 ok=actual==expected if isinstance(expected,(str,bool)) else type(actual)is float and math.isfinite(actual) and math.isclose(actual,expected,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(actual),expected=repr(expected),kind=kind,passed=ok))
for label,f,r,bp in CASES:
 a=reference(f,r,bp,1800);b=reference(f,r,bp,2400);assert a==b
 try:got=m.scenario(f,r,bp)
 except Exception as e:got=type(e).__name__
 for k in FIELDS:add(label,k,got if isinstance(got,str) else got[k],b if isinstance(b,str) else b[k],'range policy' if isinstance(b,str) else 'flag policy' if k.endswith('_pass') else 'numerical')
for label,f,r,bp,want in [('none',None,0.,0.,'TypeError'),('empty',[],0.,0.,'ValueError'),('zero cash',[(0.,1.)],0.,0.,'ValueError'),('negative time',[(1.,-1.)],0.,0.,'ValueError'),('bool rate',[(1.,1.)],True,0.,'TypeError'),('inf rate',[(1.,1.)],math.inf,0.,'ValueError'),('bool shock',[(1.,1.)],0.,True,'TypeError'),('inf shock',[(1.,1.)],0.,math.inf,'ValueError'),('huge shock',[(1.,1.)],0.,10**1000,'ValueError'),('flow priority',[],True,True,'ValueError')]:
 try:a=m.scenario(f,r,bp)
 except Exception as e:a=type(e).__name__
 add(label,'rejection',a,want)
f=[(100.,1.),(1100.,2.)];copy=f.copy();a=m.scenario(f,.04,50.);b=m.scenario(iter(f),.04,50.);add('one shot','same',a==b,True);add('ownership','unchanged',f==copy,True);add('schema','keys',set(a)==set(FIELDS),True);b=m.scenario(f[::-1],.04,50.);add('permutation','numeric',all(math.isclose(a[k],b[k],rel_tol=5e-14,abs_tol=0.) for k in NUM),True);add('flag bool types','types',all(type(a[k])is bool for k in FIELDS[-2:]),True);add('zero shock controls','zeros',all(m.scenario(f,.04,0.)[k]==0. for k in NUM if k not in ('exact_value',)),True)
sentinel=RuntimeError('flow sentinel')
def late():yield(1.,1.);raise sentinel
try:m.scenario(late(),.04,50.);same=False
except Exception as e:same=e is sentinel
add('late iterator','identity',same,True)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Selected complete scenario rows. Full baseline gate and finite reported shifted-rate sum gate retained;latent exact R+H drives endpoint/bounds. Flags compare reported errors/bounds plus existing reported baseline rounding allowance. No latent bound-certification/resource/platform/model/independent approval;numeric zeros no sign policy.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
