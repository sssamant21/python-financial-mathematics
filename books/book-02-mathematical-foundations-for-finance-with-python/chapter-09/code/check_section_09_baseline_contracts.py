"""Independent complete project baseline fields and normalized references."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_09 as m
FIELDS=('value','first','second','duration','convexity','terms')
CASES=[('ordinary',[(120.,.5),(120.,1.),(120.,2.),(1120.,3.)],.04),('factor rescued',[(1e-308,2.)],-355.),('tiny horizon',[(1e308,1e-308)],0.),('tiny baseline normalization',[(1e-308,1e-100)],0.),('subnormal ratios',[(math.ulp(0.),.5)],0.),('subnormal weighted ratios',[(math.ulp(0.),.5),(math.ulp(0.),1.)],0.),('large horizon normalized range',[(1e-308,1e155)],0.),('zero time huge rate',[(1e308,0.)],1e308),('baseline underflow',[(1e-308,2.)],355.),('true value overflow',[(1e308,0.),(1e308,0.)],0.),('true first overflow',[(1e308,2.)],0.),('integer inputs',[(100,1),(1100,2)],0),('small discounted amount',[(1e-308,1e100)],1e-100),('mixed time zero',[(100.,0.),(100.,2.)],.04)]
def reference(flows,rate,prec):
 with localcontext(Context(prec=prec)):
  R=Decimal.from_float(float(rate));V=A=B=Decimal(0);terms=[]
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];x=-R*T
   if x>10000:return 'ValueError'
   v=Decimal(0) if x < -10000 else C*x.exp();terms.append(float(v));V+=v;A-=T*v;B+=T*T*v
  if V==0:return 'ValueError'
  vals=[float(x) for x in (V,A,B,-A/V,B/V)]
  if vals[0]<=0 or not all(math.isfinite(x) for x in vals+terms):return 'ValueError'
  return dict(zip(FIELDS,vals+[terms]))
rows=[]
def add(case,field,got,want,kind='contract'):
 if isinstance(want,str) or type(want)is bool:ok=got==want
 elif isinstance(want,list):ok=isinstance(got,list) and len(got)==len(want) and all(type(a)is float and math.isfinite(a) and math.isclose(a,b,rel_tol=5e-14,abs_tol=0.) for a,b in zip(got,want))
 else:ok=type(got)is float and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
for label,f,r in CASES:
 a=reference(f,r,1800);b=reference(f,r,2400);assert a==b
 try:got=m.baseline(f,r)
 except Exception as e:got=type(e).__name__
 for k in FIELDS:add(label,k,got if isinstance(got,str) else got[k],b if isinstance(b,str) else b[k],'range policy' if isinstance(b,str) else 'numerical')
for label,f,r,want in [('none',None,0.,'TypeError'),('empty',[],0.,'ValueError'),('zero cash',[(0.,1.)],0.,'ValueError'),('negative time',[(1.,-1.)],0.,'ValueError'),('bool cash',[(True,1.)],0.,'TypeError'),('nan cash',[(math.nan,1.)],0.,'ValueError'),('bool rate',[(1.,1.)],True,'TypeError'),('nan rate',[(1.,1.)],math.nan,'ValueError'),('huge rate',[(1.,1.)],10**1000,'ValueError'),('flow priority',[],True,'ValueError')]:
 try:a=m.baseline(f,r)
 except Exception as e:a=type(e).__name__
 add(label,'rejection',a,want)
f=[(100.,1.),(1100.,2.)];copy=f.copy();a=m.baseline(f,.04);b=m.baseline(iter(f),.04)
add('one-shot flow','same',a==b,True);add('ownership','unchanged',f==copy,True);add('schema','keys',set(a)==set(FIELDS),True);b=m.baseline(f[::-1],.04);add('permutation','five numeric fields',all(math.isclose(a[k],b[k],rel_tol=5e-14,abs_tol=0.) for k in FIELDS[:-1]),True);add('terms preserve order','same',b['terms']==a['terms'][::-1],True)
b=m.baseline([(2*c,t) for c,t in f],.04);add('scale','fields',all(math.isclose(b[k],(2*a[k] if k in FIELDS[:3] else a[k]),rel_tol=5e-14,abs_tol=0.) for k in FIELDS[:-1]),True)
sentinel=RuntimeError('flow sentinel')
def late():yield(1.,1.);raise sentinel
try:m.baseline(late(),.04);same=False
except Exception as e:same=e is sentinel
add('late iterator exception','identity',same,True)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Complete project baseline six-field scope; latent normalization before conversion,finite positive reported value and all finite fields required. Selected Decimal resources,scenario/bounds/project facades and independent/platform/release approval remain open;numeric zero without sign policy.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
