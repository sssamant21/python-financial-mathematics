"""Exact finite-law source CI membership, distinct from nominal coverage approval."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform,itertools
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='31f4962bb9efee1a6e09d65c72a59187f0ce14c4';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.08-confidence-intervals.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S);assert len(listing)==1;rows=[];commands=[];cases=[];coverage=[]
def ck(name,got,want,kind):
 ok=got==want if isinstance(want,bool) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'confidence_intervals.py';p.write_text(listing[0]);spec=importlib.util.spec_from_file_location('confidence_source',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for i,values in enumerate(itertools.product([0,2],repeat=3)):
  k=sum(x==2 for x in values);mean=F(2*k,3);se2=F(sum((F(x)-mean)**2 for x in values),6);intervals={}
  for name,critical,fn in [('normal',F('1.96'),m.normal_approx_mean_ci),('t_df2',F('4.30265273'),m.t_mean_ci)]:
   got=fn(list(values),float(critical));intervals[name]=got
   with localcontext() as ctx:
    ctx.prec=100;center=D(mean.numerator)/D(mean.denominator);half=(D(se2.numerator)/D(se2.denominator)).sqrt()*(D(critical.numerator)/D(critical.denominator));expected=[center-half,center+half]
    for side in [0,1]:ck(str(i)+' '+name+' endpoint'+str(side),got[side],expected[side],'native endpoint vs independent exact moments/root')
  original=m.random.Random;created=[]
  class Exhaustive:
   def __init__(self,seed):self.samples=iter(itertools.product(range(3),repeat=3));self.calls=0;created.append(self)
   def choices(self,seq,k):self.calls+=1;return [seq[j] for j in next(self.samples)]
  try:m.random.Random=Exhaustive;boot=m.bootstrap_percentile_ci(list(values),replicates=27,alpha=.05,seed=42)
  finally:m.random.Random=original
  oracle=[(F(0),F(0)),(F(0),F(47,30)),(F(13,30),F(2)),(F(2),F(2))][k];intervals['exhaustive27_type7']=boot
  for side in [0,1]:ck(str(i)+' exhaustive bootstrap endpoint'+str(side),boot[side],oracle[side],'native controlled resamples vs independent rank counts')
  ck(str(i)+' exact index-resample count',created[0].calls,27,'controlled dependency count')
  cases.append(dict(values=values,k=k,mean=str(mean),se_squared=str(se2),intervals=intervals))
 for prob in [F(1,10),F(1,2),F(9,10)]:
  target=2*prob;mass=F(0);covered={name:F(0) for name in ['normal','t_df2','exhaustive27_type7']}
  for i,c in enumerate(cases):
   k=c['k'];weight=prob**k*(1-prob)**(3-k);mass+=weight;mean=F(c['mean']);se2=F(c['se_squared'])
   for name in covered:
    lo,hi=c['intervals'][name];native=lo<=float(target)<=hi
    if name=='exhaustive27_type7':bounds=[(F(0),F(0)),(F(0),F(47,30)),(F(13,30),F(2)),(F(2),F(2))][k];expected=bounds[0]<=target<=bounds[1]
    else:critical=F('1.96') if name=='normal' else F('4.30265273');expected=(mean-target)**2<=critical**2*se2
    ck('p'+str(prob)+' path'+str(i)+' '+name+' membership',native,expected,'native CI membership vs exact score/rank decision')
    if native:covered[name]+=weight
  ck('p'+str(prob)+' law probability mass',mass,1,'exact joint-law arithmetic')
  expected_standard=1-prob**3-(1-prob)**3;expected_boot=(3*prob*(1-prob)**2 if prob==F(1,10) else 3*prob**2*(1-prob) if prob==F(9,10) else F(3,4))
  for name,got in covered.items():ck('p'+str(prob)+' '+name+' exact coverage',got,expected_boot if name=='exhaustive27_type7' else expected_standard,'weighted native membership vs independent binomial mass')
  coverage.append(dict(p=str(prob),target_mean=str(target),iid_coverage={k:str(v) for k,v in covered.items()},perfectly_dependent_three_same_draws_coverage='0'))
 # Under perfect dependence, only all-zero/all-two samples occur; all intervals collapse and exclude 2p.
 for prob in [F(1,10),F(1,2),F(9,10)]:
  for name in cases[0]['intervals']:
   actual=sum((1-prob if i==0 else prob) for i in [0,7] if cases[i]['intervals'][name][0]<=float(2*prob)<=cases[i]['intervals'][name][1]);ck('dependent p'+str(prob)+' '+name+' coverage',actual,0,'same marginals, different sampling design')
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing[0].encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,cases=cases,coverage=coverage,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Exact n3 finite IID/dependent laws; controlled27-index-resample type7 intervals; not native PRNG/large-B/t-normal model coverage approval')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);print(coverage);assert result['failed']==0
