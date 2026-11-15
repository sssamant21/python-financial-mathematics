"""Independent high-precision sampled quotients, callback and preflight contracts."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_07 as m
FIELDS=('left_difference','right_difference','centered_difference');rows=[]
def add(label,field,got,want,kind='contract'):
 ok=got==want if isinstance(want,(str,list,bool)) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=label,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
CASES=[('linear',0.,1.,0.,-1.,1.),('call kink',100.,2.,0.,0.,2.),('identity huge step',0.,1e308,0.,-1e308,1e308),('numerator overflow rescue',0.,1e308,1e308,-1e308,1e308),('smallest step',0.,math.ulp(0.),0.,-math.ulp(0.),math.ulp(0.)),('tiny quotient',0.,1e308,0.,-math.ulp(0.),math.ulp(0.)),('unequal rounded grid',1.,math.ulp(1.),1.,1.-math.ulp(1.),1.+math.ulp(1.)),('asymmetric samples',2.,.1,4.,3.61,4.41),('constant',1.,.5,7.,7.,7.),('true quotient overflow',0.,1e-308,1e308,0.,0.),('opposite true quotient overflow',0.,math.ulp(0.),0.,1.,-1.),('tiny finite outputs',0.,1.,0.,-1e-308,1e-308),('integer callback values',0.,1.,0,-2,2),('negative sampled quotients',0.,1.,0.,1.,-1.)]
def ref(vals,h,precision):
 with localcontext(Context(prec=precision)):
  A,B,C=[Decimal.from_float(float(v)) for v in vals];H=Decimal.from_float(h)
  out=[float((A-B)/H),float((C-A)/H),float((C-B)/(H*2))]
  return out if all(math.isfinite(x) for x in out) else 'ValueError'
for label,x,h,a,b,c in CASES:
 want=ref((a,b,c),h,1800);assert want==ref((a,b,c),h,2400);trace=[];points=[x,x-h,x+h];values=[a,b,c]
 def fn(v):trace.append(v);return values[points.index(v)]
 try:actual=m.difference_report(fn,x,h)
 except Exception as e:actual=type(e).__name__
 for i,k in enumerate(FIELDS):add(label,k,actual if isinstance(actual,str) else actual[k],want if isinstance(want,str) else want[i],'range-policy' if isinstance(want,str) else 'numerical')
 add(label,'callback order',trace,points)
for label,x,h,want,kind in [('zero step',0.,0.,'ValueError','contract'),('negative step',0.,-1.,'ValueError','contract'),('nan point',math.nan,1.,'ValueError','contract'),('bool point',True,1.,'TypeError','contract'),('bool step',0.,True,'TypeError','contract'),('infinite step',0.,math.inf,'ValueError','contract'),('infinite point',math.inf,1.,'ValueError','contract'),('huge integer point',10**1000,1.,'ValueError','contract'),('rounded plus point',1.,2**-53,'ValueError','contract'),('rounded both points',1e308,1.,'ValueError','contract'),('positive endpoint overflow',1e308,1e308,'ValueError','grid-policy'),('negative endpoint overflow',-1e308,1e308,'ValueError','grid-policy')]:
 trace=[]
 def fn(v):trace.append(repr(v));return 1.
 try:a=m.difference_report(fn,x,h)
 except Exception as e:a=type(e).__name__
 add(label,'preflight',a,want,kind);add(label,'no callback',trace,[],kind)
try:a=m.difference_report(None,True,True)
except Exception as e:a=type(e).__name__
add('callable before numeric input','preflight',a,'TypeError')
for phase in range(3):
 for value,want in [(True,'TypeError'),(math.nan,'ValueError'),(math.inf,'ValueError'),(10**1000,'ValueError')]:
  trace=[]
  def fn(x):trace.append(x);return value if len(trace)-1==phase else 0.
  try:a=m.difference_report(fn,0.,1.)
  except Exception as e:a=type(e).__name__
  add(f'bad callback phase{phase} value{str(value)[:10]}','rejection',a,want);add(f'bad callback phase{phase} value{str(value)[:10]}','short circuit',trace,[0.,-1.,1.][:phase+1])
for phase in range(3):
 trace=[];original=RuntimeError('callback sentinel')
 def fn(x):
  trace.append(x)
  if len(trace)-1==phase:raise original
  return 0.
 try:m.difference_report(fn,0.,1.);same=False
 except Exception as e:same=e is original
 add('original exception phase'+str(phase),'identity',same,True);add('original exception phase'+str(phase),'short circuit',trace,[0.,-1.,1.][:phase+1])
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Sampled quotient contracts at rounded x-h/x+h with nominal represented h denominators; not analytic derivative convergence. Finite endpoint/output policies explicit. Callback order and original exception identity retained. Scenario, physical zero-spot interpretation, resource/platform/independent acceptance remain open; zero signs numeric only.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
