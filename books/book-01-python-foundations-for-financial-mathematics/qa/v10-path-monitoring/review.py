"""Pinned source calls; caller-controlled coarse/fine grid coupling. Run with first or replay."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from decimal import Decimal,localcontext
here=Path(__file__).resolve().parent;root=here.parents[3]
pin='c539a0d935facc2a11c510516c7fa3b23271806f';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.06-price-path-simulation.md'
raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(listing)==1
rows=[];commands=[];cases=[]
def check(name,actual,expected):
 ok=actual==expected if isinstance(expected,(bool,list,dict)) else math.isclose(float(actual),float(expected),rel_tol=5e-14,abs_tol=1e-12)
 rows.append(dict(name=name,actual=actual,expected=str(expected),passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'price_path_simulation.py';p.write_text(listing[0])
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=90);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('paths_reference',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);original=m.random.Random
 def controlled(steps,draws,horizon=1):
  trace=[]
  class Fixed:
   def __init__(self,seed):self.values=iter(draws)
   def normalvariate(self,mu,sigma):trace.append([mu,sigma]);return next(self.values)
  m.random.Random=Fixed
  try:out=m.simulate_paths(100,.02,.2,horizon,steps,2,7)
  finally:m.random.Random=original
  check('standard draw contract '+str((steps,draws,horizon)),trace,[[0,1]]*len(draws));check('RNG restored',m.random.Random is original,True)
  return out
 for amplitude in [.5,1.,1.5]:
  fine=controlled(2,[amplitude,-amplitude,-amplitude,amplitude]);coarse=controlled(1,[0.,0.])
  with localcontext() as ctx:
   ctx.prec=120;ideal=Decimal('.02').sqrt();scale=Decimal(str(float(ideal)));a=Decimal(str(amplitude));expected=[Decimal(100)*(scale*a).exp(),Decimal(100)*(-scale*a).exp()]
  for i in range(2):
   check('fine midpoint '+str((amplitude,i)),fine[i][1],expected[i]);check('terminal coupling '+str((amplitude,i)),fine[i][-1],coarse[i][-1]);check('coarse terminal100',coarse[i][-1],100)
  check('fine lower95 hits '+str(amplitude),[m.observed_barrier_hit(p,95) for p in fine],[False,True]);check('coarse lower95 hits '+str(amplitude),[m.observed_barrier_hit(p,95) for p in coarse],[False,False])
  check('terminal summary fine',m.summarize_terminal(fine),dict(count=2,mean=100,standard_error=0.0));check('terminal summary coarse',m.summarize_terminal(coarse),dict(count=2,mean=100,standard_error=0.0))
  cases.append(dict(amplitude=amplitude,fine=fine,coarse=coarse,ideal_scale=str(ideal),reported_scale=str(scale),fine_observed_hits=sum(m.observed_barrier_hit(p,95) for p in fine),coarse_observed_hits=sum(m.observed_barrier_hit(p,95) for p in coarse)))
 # Same dimensionless increments when sigma^2*T/steps is equal: horizon4/steps8 vs horizon1/steps2.
 long=controlled(8,[1.,-1.]*8,4);short=controlled(2,[1.,-1.]*2,1)
 for i in range(2):
  check('equal dt midpoint '+str(i),long[i][1],short[i][1]);check('long terminal cancellation '+str(i),long[i][-1],100)
 check('grid count is not path count',[len(long),len(long[0]),len(short),len(short[0])],[2,9,2,3])
prior=json.loads((here.parent/'chapter-18-paths-review/results.json').read_text())
# Record prior schema without guessing its hash-key name; compare its retained source text hash where available.
sha=hashlib.sha256(listing[0].encode()).hexdigest()
result=dict(pin=pin,source=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=sha,python=platform.python_version(),platform=platform.platform(),rows=rows,cases=cases,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Controlled coupling, not random-law, IID uncertainty or continuous-monitoring validation')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['passed','failed','listing_sha256']}));assert result['failed']==0 and all(c['returncode']==0 for c in commands)
