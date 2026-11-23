"""Finite repeated-sample coverage,bootstrap and sampling-design assumptions."""
from pathlib import Path
from fractions import Fraction as F
from random import Random
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='d4729bfb7c23362138d9a0b92eee0d231b80c961';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.14-sampling-with-python.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);fences=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S);listing=fences[1];rows=[];commands=[];records=[]
def ck(name,got,want,kind,tol=F(1,10**14)):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=(got==want if isinstance(got,(str,list,bool)) else abs(F(got)-F(want))<=tol),tolerance=str(tol),kind=kind))
def var(values):
 mean=sum(values,F(0))/len(values);return sum((x-mean)**2 for x in values)/len(values)
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'sampling.py';path.write_text(listing);example=Path(tmp)/'replacement.py';example.write_text(fences[0]);spec=importlib.util.spec_from_file_location('sampling_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,example.name],[sys.executable,'-m','compileall','-q',path.name,example.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for n,wantcov in [(2,F(1,2)),(3,F(3,4)),(4,F(7,8))]:
  samples=list(itertools.product([0,1],repeat=n));means=[F(sum(s),n) for s in samples];coverage=0;mean_variances=F(0)
  for i,sample in enumerate(samples):
   ck(f'IID n{n} sample{i} mean',m.avg(sample),means[i],'exact enumerated fair-Bernoulli paths')
   lower,upper=m.mean_interval(sample);coverage+=lower<=.5<=upper;mean_variances+=F(m.se(sample))**2/len(samples)
  ck(f'IID n{n} exact mean variance',var(means),F(1,4*n),'independent finite-sampling distribution')
  ck(f'IID n{n} mean estimated SE squared',mean_variances,F(1,4*n),'unbiased sample variance divided by n',F(1,10**14))
  ck(f'IID n{n} approximate interval coverage',F(coverage,len(samples)),wantcov,'actual source interval repeated coverage;small discrete samples do not attain95percent')
  records.append(dict(n=n,coverage=str(F(coverage,len(samples))),true_mean_variance=str(var(means))))
 data=[0,0,1];resamples=list(itertools.product(range(3),repeat=3));bootmeans=[F(sum(data[i] for i in s),3) for s in resamples]
 ck('conditional bootstrap mean',sum(bootmeans)/27,F(1,3),'exhaustive empirical resampling distribution')
 ck('conditional bootstrap mean variance',var(bootmeans),F(2,27),'empirical population variance2/9 divided by3')
 ck('original SE squared',m.se(data)**2,F(1,9),'sample variance correction makes plug-in SE differ from finite conditional bootstrap',F(1,10**14))
 for x in [0,1]:
  ck('shared cluster estimated SE '+str(x),m.se([x]*4),0,'dependent sample can hide true common-shock uncertainty')
  ck('shared cluster bootstrap constant '+str(x),m.bootstrap([x]*4,16,9),[float(x)]*16,'ordinary IID bootstrap cannot recover unobserved cluster variation')
 ck('shared cluster true mean variance',var([F(0),F(1)]),F(1,4),'external shared-Bernoulli sampling law,not divided by4')
 pop=[0,1,2,3];without=[F(a+b,2) for a,b in itertools.permutations(pop,2)];withrep=[F(a+b,2) for a,b in itertools.product(pop,repeat=2)]
 ck('without replacement variance',var(without),F(5,12),'finite population correction(4-2)/(4-1)')
 ck('with replacement variance',var(withrep),F(5,8),'population variance5/4 divided by2;different sampling designs')
 rng=Random(411);want=[-20 if (u:=rng.random())<.25 else 5 if u<.75 else 30 for _ in range(256)]
 ck('actual weighted256 replay',m.draw([-20,5,30],[1,2,1],256,411),want,'separate CDF-band replay of native draws')
 ck('scaled relative weights replay',m.draw([-20,5,30],[1e307,2e307,1e307],256,411),want,'moderate ratios with very large finite weight scale;not arbitrarily rare weights')
 rng=Random(133);sample=[-20,5,30];boot=[sum(sample[math.floor(rng.random()*3)] for _ in range(3))/3 for _ in range(128)]
 ck('actual128 bootstrap mean replay',m.bootstrap(sample,128,133),boot,'separate uniform-index resampling,not confidence calibration')
 ck('bootstrap support limitation',all(-20<=x<=30 for x in boot),True,'empirical resamples cannot generate unseen outcomes')
 for p,want in [(0,-20),(.25,F(-15,2)),(.5,5),(.75,F(35,2)),(1,30)]:ck('interpolated empirical quantile '+str(p),m.quantile(sample,p),want,'declared sorted index(n-1)p convention,not a population quantile')
 prior=json.loads((here.parent/'chapter-14-sampling-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F123 retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),illustration_sha256=hashlib.sha256(fences[0].encode()).hexdigest(),rows=rows,commands=commands,coverage_records=records,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Finite IID/cluster/design/bootstrap assumptions and actual weighted/bootstrap replay;no empirical data fit,dependence-aware bootstrap or platform acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert not r['failed']
