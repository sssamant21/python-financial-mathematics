"""Chapter14 applied A/B/C source/finite-model/provenance assumption crosswalk."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from random import Random
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='61c06b7c9114d0d45bcdb2ddfe08e8bce44a75a6';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.17-exercises-and-applied-problems.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records=[]
def ck(name,got,want,kind,tol=F(1,10**13)):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=(got==want if isinstance(got,(str,list,bool)) else abs(F(got)-F(want))<=tol),tolerance=str(tol),kind=kind))
def phi(z):
 z=D(z);term=total=z
 for k in range(1,201):term*=-(z*z/2)*D(2*k-1)/(D(k)*D(2*k+1));total+=term
 assert abs(z)<=4 and abs(term)<D('1e-100')
 return D('.5')+total/(2*D('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')).sqrt()
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'chapter14.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('chapter14_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 # Screening example is caller joint-table reasoning,not a source Bayes API.
 for prevalence in [F(1,50),F(1,10)]:
  tp=F(9,10)*prevalence;fp=F(1,20)*(1-prevalence);ck('screen posterior '+str(prevalence),tp/(tp+fp),F(18,67) if prevalence==F(1,50) else F(2,3),'external fixed sensitivity/false-positive law,base rate changes target')
 masses=[F(0)]*11
 for states in itertools.product([0,1],repeat=10):masses[sum(states)]+=math.prod(F(1,10) if x else F(9,10) for x in states)
 for k,want in enumerate(masses):ck('A native binomial mass '+str(k),m.binomial_pmf(k,10,.1),want,'exhaustive independent Bernoulli product paths')
 ck('A IID mean',sum(k*p for k,p in enumerate(masses)),1,'exact count law');ck('A IID variance',sum(p*(k-1)**2 for k,p in enumerate(masses)),F(9,10),'independence/homogeneity contract')
 ck('A shared indicator variance',F(1,10)*(10-1)**2+F(9,10)*(0-1)**2,9,'same marginal PD,external common-shock law,not native correlated-default API')
 rng=Random(42);counts=[sum(rng.random()<.1 for _ in range(10)) for _ in range(20000)];ck('A supplemental zero count',counts.count(0),6960,'actual extension loop stated in manuscript,not exact-source lab API');ck('A supplemental one count',counts.count(1),7766,'same extension');ck('A supplemental mean',F(sum(counts),20000),F(10017,10000),'observed seed42 result,not model validation')
 for n in [1000,20000]:
  rng=Random(42);ref=[-20 if (u:=rng.random())<.25 else 5 if u<.75 else 30 for _ in range(n)];sample=m.sample_scenarios([-20,5,30],[.25,.5,.25],n,42);ck('B actual sample replay '+str(n),sample,ref,'independent CDF-band replay')
  mu=F(sum(ref),n);sv=sum((F(x)-mu)**2 for x in ref)/(n-1);got=m.summarize(sample)
  with localcontext() as ctx:ctx.prec=90;sd=(D(sv.numerator)/D(sv.denominator)).sqrt();se=sd/D(n).sqrt()
  ck('B actual mean '+str(n),got[0],mu,'exact integer outcome sums');ck('B actual SD '+str(n),got[1],F(sd),'90digit rational centered root');ck('B actual SE '+str(n),got[2],F(se),'IID plug-in,not model uncertainty')
  for p,want in [(.05,-20),(.95,30)]:ck('B actual empirical tail '+str(n)+'/'+str(p),m.empirical_quantile(sample,p),want,'interpolated observed ranks,not universal population quantiles')
  stressed=m.sample_scenarios([-18,7,32],[.25,.5,.25],n,42);ck('B paired stress replay '+str(n),stressed,[x+2 for x in ref],'same scenario map/seed with fixed additive outcome shift')
  if n==1000:
   bootstrap=m.bootstrap_means(sample,500,43);rng=Random(43);ref_boot=[sum(ref[math.floor(rng.random()*n)] for _ in range(n))/n for _ in range(500)];ck('B actual500 bootstrap means',bootstrap,ref_boot,'independent uniform-index replay');ck('B bootstrap support',all(-20<=x<=30 for x in bootstrap),True,'resampling cannot add unseen outcomes')
  records.append(dict(n=n,seed=42,mean=str(mu),estimated_se=got[2],source_sha256=hashlib.sha256(raw).hexdigest(),bootstrap_seed=43 if n==1000 else None,bootstrap_repetitions=500 if n==1000 else None,stress_shift=2))
 with localcontext() as ctx:
  ctx.prec=110;ck('C return loss probability',m.normal_cdf(0,.01,.02),F(phi(D('-.5'))),'independent integrated normal-density series',F(2,10**14));lo,hi=D(-4),D(4)
  for _ in range(280):
   mid=(lo+hi)/2
   if phi(mid)<D('.05'):lo=mid
   else:hi=mid
  q=(lo+hi)/2;rq=D('.01')+D('.02')*q;loss=-100000*rq;ck('C CDF at independent return quantile',m.normal_cdf(float(rq),.01,.02),F(1,20),'source CDF at external independently inverted normal threshold',F(2,10**14));ck('C loss convention equivalence',F(loss),F(100000)*(F(D('.02'))*(-F(q))-F(D('.01'))),'external loss minus exposure times return;no native VaR helper');records.append(dict(normal_return_quantile=str(rq),unfloored_loss_quantile=str(loss),model='stipulated normal one-period returns,not calibrated'))
 prior=json.loads((here.parent/'chapter-14-applied-answers-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F126 retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,applied_records=records,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Applied A/B/C selected model/source/replay assumptions;no real credit calibration,normal-tail validation or independent chapter/V10 approval')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert not r['failed']
