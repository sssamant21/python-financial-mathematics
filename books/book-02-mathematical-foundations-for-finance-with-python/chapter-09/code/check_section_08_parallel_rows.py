"""Complete facade rows and reported-error flags from direct latent references."""
from decimal import Decimal,Context,localcontext
from pathlib import Path
import math,json,sys,hashlib
import section_9_08 as m
NUMERIC=('exact_change','linear_change','quadratic_change','linear_error','quadratic_error','absolute_linear_error','absolute_quadratic_error','exact_value','linear_value','quadratic_value','shock_bp','shock_decimal')
FIELDS=NUMERIC+('linear_within_tolerance','quadratic_within_tolerance')
CASES=[('ordinary',[(100.,1.),(1100.,2.)],.04,50.,.25),('negative shock',[(100.,1.),(1100.,2.)],.04,-50.,.25),('zero shock',[(100.,1.),(1100.,2.)],.04,0.,0.),('direct tiny endpoint',[(1.,1.)],0.,500000.,.25),('latent baseline leg',[(1e-308,2.),(1.,0.)],355.,-3550000.,0.),('tiny latent errors',[(1e308,1.)],0.,1e-196,0.),('tiny horizon',[(1e308,1e-308)],0.,10000.,0.),('baseline unused derivative gate',[(1e308,2.)],0.,0.,0.),('true row value overflow',[(1e308,1.)],0.,-10000.,.25),('true change overflow',[(1e308,1.)],0.,-20000.,.25),('zero time large rate/shift',[(1e308,0.)],1e308,1e308,0.),('basispoint conversion underflow',[(1.,1.)],0.,math.ulp(0.),0.),('reported value underflow allowed',[(1.,1.)],0.,1e8,.25),('integer inputs',[(100,1),(1100,2)],0,25,0),('linear value cancellation',[(1e308,1.)],0.,10000.,0.)]
def reference(flows,rate,bp,tol,prec):
 with localcontext(Context(prec=prec)):
  R=Decimal.from_float(float(rate));h=float(bp)/10000.;H=Decimal.from_float(h);V=A=B=Decimal(0);parts=[]
  def amount(C,x):
   if C==0:return Decimal(0)
   if x>10000:return Decimal('Infinity')
   return Decimal(0) if x < -10000 else C*x.exp()
  for c,t in flows:
   C,T=[Decimal.from_float(float(x)) for x in (c,t)];v=amount(C,-R*T);V+=v;A-=T*v;B+=T*T*v;parts.append((C,T,v))
  if V==0:return 'ValueError'
  base=[float(x) for x in (V,A,B,-A/V,B/V)]
  if base[0]<=0 or not all(math.isfinite(x) for x in base):return 'ValueError'
  shifted=sum((amount(C,-T*(R+H)) for C,T,v in parts),Decimal(0));E=shifted-V;L=A*H;Q=L+B*H*H/2
  vals=[float(x) for x in (E,L,Q,E-L,E-Q,abs(E-L),abs(E-Q),shifted,V+L,V+Q)]+[float(bp),h]
  if not all(math.isfinite(x) for x in vals):return 'ValueError'
  return dict(zip(FIELDS,vals+[vals[5]<=float(tol),vals[6]<=float(tol)]))
a=reference([(100.,1.),(1100.,2.)],.04,50.,.25,2400);boundary=a['absolute_quadratic_error']
for label,tol in [('equal reported error',boundary),('just below reported error',math.nextafter(boundary,0.)),('just above reported error',math.nextafter(boundary,math.inf))]:CASES.append((label,[(100.,1.),(1100.,2.)],.04,50.,tol))
rows=[]
def add(case,field,got,want,kind='contract'):
 ok=got==want if isinstance(want,(str,bool,list)) else isinstance(got,float) and math.isfinite(got) and math.isclose(got,want,rel_tol=5e-14,abs_tol=0.)
 rows.append(dict(case=case,field=field,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
for label,f,r,bp,tol in CASES:
 a=reference(f,r,bp,tol,1800);b=reference(f,r,bp,tol,2400);assert a==b
 try:actual=m.parallel_report(f,r,[bp],tol)['scenarios'][0]
 except Exception as e:actual=type(e).__name__
 for key in FIELDS:add(label,key,actual if isinstance(actual,str) else actual[key],b if isinstance(b,str) else b[key],'range/prerequisite-policy' if isinstance(b,str) else 'flag/report' if key.endswith('tolerance') else 'numerical')
for label,f,r,grid,tol,want in [('flows first',None,True,None,True,'TypeError'),('empty first',[],True,None,True,'ValueError'),('bad rate',[(1.,1.)],True,[],None,'TypeError'),('negative tolerance',[(1.,1.)],0.,[],-1.,'ValueError'),('boolean tolerance',[(1.,1.)],0.,[],True,'TypeError'),('infinite tolerance',[(1.,1.)],0.,[],math.inf,'ValueError'),('boolean bp',[(1.,1.)],0.,[True],None,'TypeError'),('infinite bp',[(1.,1.)],0.,[math.inf],None,'ValueError'),('oversized bp',[(1.,1.)],0.,[10**1000],None,'ValueError')]:
 try:a=m.parallel_report(f,r,grid,tol)
 except Exception as e:a=type(e).__name__
 add(label,'rejection',a,want)
f=[(100.,1.),(1100.,2.)];fc=f.copy();grid=[-25.,0.,25.,25.];gc=grid.copy();a=m.parallel_report(f,.04,grid)
add('ownership','inputs',f==fc and grid==gc,True);add('grid order and duplicates','bps',[x['shock_bp'] for x in a['scenarios']],grid);add('duplicate rows','same',a['scenarios'][2]==a['scenarios'][3],True);add('absent tolerance flags','schema',all('linear_within_tolerance' not in x and 'quadratic_within_tolerance' not in x for x in a['scenarios']),True);add('all numeric fields finite','values',all(math.isfinite(x[k]) for x in a['scenarios'] for k in NUMERIC),True)
b=m.parallel_report(iter(f),.04,iter(grid));add('one-shot facade inputs','report',a==b,True)
original=RuntimeError('grid sentinel')
def late():
 yield 0.
 raise original
try:m.parallel_report(f,.04,late());same=False
except Exception as e:same=e is original
add('late grid exception identity','same object',same,True)
trace=[]
def tracked():trace.append('consumed');yield 0.
try:m.parallel_report([(1e308,2.)],0.,tracked())
except ValueError:pass
add('baseline gate before grid','not consumed',trace,[])
a=m.parallel_report(f,.04,[0.],0.)['scenarios'][0];add('flag bool types','schema',type(a['linear_within_tolerance'])is bool and type(a['quadratic_within_tolerance'])is bool,True)
raw=Path(m.__file__).read_bytes();d=dict(source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),reference_precisions=[1800,2400],relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Parallel facade only. Full baseline eligibility retained; h is reported finite float bp/10000. Shifted rate latent R+H. Values/errors computed before float conversion; flags compare reported absolute errors to reported tolerance. Exact shifted value zero underflow allowed; Taylor values may be negative. Spot numerics/resource/platform/model/independent approval remain open; zero signs numeric only.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'])))
assert d['failed']==0
