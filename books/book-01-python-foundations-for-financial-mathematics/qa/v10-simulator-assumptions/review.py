"""Integrated simulator source versus finite model/replay/uncertainty assumptions."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from random import Random
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='fa4f0ff5ab47be843c18525195fed5c2041b7f72';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.16-chapter-project-financial-probability-simulator.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);fences=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S);listing,driver=fences;rows=[];commands=[]
def ck(name,got,want,kind,tol=F(1,10**13)):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=(got==want if isinstance(got,(str,list,bool)) else abs(F(got)-F(want))<=tol),tolerance=str(tol),kind=kind))
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'financial_probability_simulator.py';path.write_text(listing);runpath=Path(tmp)/'run_simulator.py';runpath.write_text(driver);spec=importlib.util.spec_from_file_location('simulator_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,runpath.name],[sys.executable,'-m','compileall','-q',path.name,runpath.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=90);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 outcomes=[-20,5,30];weights=[.25,.5,.25];n=256;seed=512;rng=Random(seed);ref=[-20 if (u:=rng.random())<.25 else 5 if u<.75 else 30 for _ in range(n)];draws=m.simulate(outcomes,weights,n,seed);ck('actual256 scenario replay',draws,ref,'independent uniform CDF bands')
 mu=F(sum(ref),n);sv=sum((F(x)-mu)**2 for x in ref)/(n-1);summary=m.summarize(draws)
 with localcontext() as ctx:
  ctx.prec=90;sd=(D(sv.numerator)/D(sv.denominator)).sqrt();se=sd/D(n).sqrt()
  ck('actual summary mean',summary['mean'],mu,'integer outcome sums');ck('actual summary sample SD',summary['sample_sd'],F(sd),'independent90digit rational centered variance root');ck('actual summary SE',summary['se'],F(se),'IID plug-in only,not model uncertainty')
 ck('actual loss frequency',summary['loss_probability'],F(sum(x<0 for x in ref),n),'explicit negative-outcome event counts')
 sorted_ref=sorted(ref)
 for p,key in [(F(1,20),'p05'),(F(19,20),'p95')]:
  pos=(n-1)*p;low=pos.numerator//pos.denominator;alpha=pos-low;want=(1-alpha)*sorted_ref[low]+alpha*sorted_ref[math.ceil(pos)];ck('actual empirical '+key,summary[key],want,'exact declared linear interpolation,not population tail certainty')
 for shock in [-25.,0.,2.]:
  stressed=m.paired_stress(draws,shock);ck('actual paired payoffs '+str(shock),stressed,[float(x+shock) for x in ref],'fixed additive model,not changed scenario probabilities')
  ck('actual shifted mean '+str(shock),m.summarize(stressed)['mean'],mu+F(shock),'finite exact payoff arithmetic for these ordinary values')
 ck('sub-ULP rounded payoff stress',m.paired_stress([1e16,1e16],1.),[1e16,1e16],'rounded output payoffs need not retain sub-ULP additive difference;no exact-shift guarantee')
 rng=Random(513);bootstrap_means=[F(sum(ref[math.floor(rng.random()*n)] for _ in range(n)),n) for _ in range(128)];bm=sum(bootstrap_means)/128;bv=sum((x-bm)**2 for x in bootstrap_means)/127
 with localcontext() as ctx:ctx.prec=90;want=(D(bv.numerator)/D(bv.denominator)).sqrt()
 ck('actual128 bootstrap SE',m.bootstrap_mean_se(draws,128,513),F(want),'independent uniform-index means and rational sample variance root')
 ck('bootstrap cannot leave empirical support',all(-20<=x<=30 for x in bootstrap_means),True,'no resample creates unobserved extreme outcomes')
 rng=Random(514);counts=[sum(rng.random()<.25 for _ in range(4)) for _ in range(256)];ck('actual256 independent-loan counts',m.default_count_simulation(4,.25,256,514),counts,'separate Bernoulli threshold replay')
 paths=list(itertools.product([0,1],repeat=4));ps=[math.prod(F(1,4) if x else F(3,4) for x in s) for s in paths];means=sum(p*sum(s) for p,s in zip(ps,paths));variance=sum(p*(sum(s)-means)**2 for p,s in zip(ps,paths));ck('IID count mean',means,1,'exhaustive product-law paths');ck('IID count variance',variance,F(3,4),'independent default assumption')
 ck('shared-marginal count mean',F(1,4)*4,1,'external common shock keeps same marginal PD');ck('shared-marginal count variance',F(1,4)*(4-1)**2+F(3,4)*(0-1)**2,3,'external correlated count law,not implemented by native IID helper')
 config={'seed':seed,'trials':n,'outcomes':outcomes,'probabilities':weights,'prng':'random.Random'};canonical=json.dumps(config,sort_keys=True,separators=(',',':'));manifest=m.manifest(seed,n,outcomes,weights);ck('full base config hash',manifest['sha256'],hashlib.sha256(canonical.encode()).hexdigest(),'independent canonical JSON bytes')
 ck('payoff values bound by manifest',m.manifest(seed,n,[-18,7,32],weights)['sha256']!=manifest['sha256'],True,'base distribution included,unlike narrower14.15 manifest')
 ck('manifest omits experiment parameters','bootstrap_repetitions' not in manifest['configuration'] and 'additive_shock' not in manifest['configuration'],True,'driver/bootstrap/stress/source/runtime evidence still required')
 prior=json.loads((here.parent/'chapter-14-simulator-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F125 retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),driver_sha256=hashlib.sha256(driver.encode()).hexdigest(),rows=rows,commands=commands,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Actual exact-source tests/driver and finite model/replay/provenance assumptions;no calibrated dependence,tiny-weight/cross-runtime/production or independent certification')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert not r['failed']
