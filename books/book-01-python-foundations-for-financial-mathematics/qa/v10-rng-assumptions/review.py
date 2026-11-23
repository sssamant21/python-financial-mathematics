"""Source replay/state and finite CRN/antithetic/provenance assumptions."""
from pathlib import Path
from fractions import Fraction as F
from random import Random
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='50191124b93345af6b74ccc971d94b86edbad98f';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.15-random-number-generation-and-reproducibility.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);fences=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S);listing=fences[1];rows=[];commands=[]
def ck(name,got,want,kind,tol=F(1,10**14)):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=(got==want if isinstance(got,(str,list,bool)) else abs(F(got)-F(want))<=tol),tolerance=str(tol),kind=kind))
def variance(x):
 mu=sum(x)/len(x);return sum((v-mu)**2 for v in x)/len(x)
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'rng_lab.py';path.write_text(listing);example=Path(tmp)/'uniform_example.py';example.write_text(fences[0]);spec=importlib.util.spec_from_file_location('rng_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,example.name],[sys.executable,'-m','compileall','-q',path.name,example.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 state=m.random.getstate();rng=Random(905);ref=[rng.random() for _ in range(256)];actual=m.uniform_draws(256,905)
 ck('actual256 uniform replay',actual,ref,'independent local state initialized once,not restarted each draw');ck('global state unchanged by uniform',m.random.getstate()==state,True,'source local RNG isolates shared module state')
 ck('prefix preserved with longer count',m.uniform_draws(300,905)[:256],actual,'same algorithm/state/call sequence on this runtime')
 rng=Random(905);rng.random();shifted=[rng.random() for _ in range(256)];ck('inserted draw shifts stream',shifted[:255],actual[1:],'draw-order contract,not model change')
 ck('cloned seed is duplicated experiment',m.uniform_draws(256,905),actual,'identical state is not independent parallel stream')
 rng=Random(906);norm=[rng.gauss(.01,.02) for _ in range(128)];ck('actual128 normal replay',m.normal_draws(128,906,.01,.02),norm,'replay only,not normality/calibration proof');ck('global state unchanged by normal',m.random.getstate()==state,True,'local RNG only')
 rng=Random(907);ref=[-20 if (u:=rng.random())<.25 else 5 if u<.75 else 30 for _ in range(256)];base=m.scenario_draws([-20,5,30],[1,2,1],256,907);ck('actual256 scenario replay',base,ref,'external CDF band assignment')
 ck('relative scale draw invariance',m.scenario_draws([-20,5,30],[2,4,2],256,907),base,'exact moderate ratios,not arbitrarily rare weights')
 for n in [1,7,256]:
  for shock in [-.02,0.,.02,1e-300]:ck(f'paired constant shift {n}/{shock}',m.paired_mean_difference(n,907,shock),shock,'exact represented common-input differences;zero Monte Carlo variation in stipulated additive shift',F(0))
 u=[F(1,8),F(3,8),F(5,8),F(7,8)];v=variance(u);independent=[x-y for x in u for y in u]
 ck('independent difference variance',variance(independent),2*v,'finite product uniform-grid law')
 ck('positive CRN covariance difference variance',variance([x-x for x in u]),0,'perfect positive pairing reduces variance')
 ck('negative CRN covariance difference variance',variance([x-(1-x) for x in u]),4*v,'negative pairing increases variance versus independent streams')
 ck('monotone antithetic average variance',variance([(x+1-x)/2 for x in u]),0,'g(u)=u,negative covariance')
 g=[(x-F(1,2))**2 for x in u];ck('nonmonotone antithetic average variance',variance([((x-F(1,2))**2+(1-x-F(1,2))**2)/2 for x in u]),variance(g),'g(u)=(u-.5)^2 yields identical pair,not variance reduction')
 ck('independent nonmonotone average variance',variance([(x+y)/2 for x in g for y in g]),variance(g)/2,'independent comparator reveals antithetic penalty')
 manifest=m.manifest(907,256,[1,2,1]);canonical=json.dumps({'seed':907,'n':256,'weights':[1,2,1],'generator':'random.Random'},sort_keys=True,separators=(',',':'),allow_nan=False)
 ck('canonical payload hash',manifest['sha256'],hashlib.sha256(canonical.encode()).hexdigest(),'independent canonical JSON bytes')
 ck('scaled weights change identity',m.manifest(907,256,[2,4,2])['sha256']!=manifest['sha256'],True,'byte identity is different despite identical probability law')
 shifted=m.scenario_draws([-18,7,32],[1,2,1],256,907);ck('payoff shift actual mean difference',m.mean(shifted)-m.mean(base),2,'payoff data omitted by narrow source manifest')
 ck('same narrow manifest for different payoff fixture',m.manifest(907,256,[1,2,1])['sha256'],manifest['sha256'],'seed/count/weights/generator hash does not bind payoff values/runtime/source')
 ck('global state still unchanged',m.random.getstate()==state,True,'all source local-generator probes')
 prior=json.loads((here.parent/'chapter-14-rng-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F124 retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),illustration_sha256=hashlib.sha256(fences[0].encode()).hexdigest(),rows=rows,commands=commands,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Actual seeded/state/provenance checks and external finite CRN/antithetic laws;not independence,cryptographic,parallel-substream,rare-tail or cross-runtime validation')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert not r['failed']
