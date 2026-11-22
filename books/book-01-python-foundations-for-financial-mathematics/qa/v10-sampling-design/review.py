"""Finite-design/FPC/census/bootstrap conditional sampling crosswalk, exact fence."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='0e5b5fc323732073c2164acbad2e30507e13a883';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.07-sampling-and-estimation.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records={}
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def mean(xs):return sum(map(F,xs))/len(xs)
def variance(xs):
 n=len(xs);return sum((F(a)-F(b))**2 for a,b in itertools.combinations(xs,2))/F(n*(n-1))
def popvar(xs):return sum((F(a)-F(b))**2 for a,b in itertools.combinations(xs,2))/F(len(xs)**2)
def sqrt(x):
 with localcontext() as ctx:ctx.prec=100;return float((D(x.numerator)/D(x.denominator)).sqrt())
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'sampling.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('sampling_lab',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 population=[0,1,2,3];wor=list(itertools.combinations(population,2));wr=list(itertools.product(population,repeat=2));mu=F(3,2)
 for name,samples,target in [('without replacement',wor,F(5,12)),('with replacement',wr,F(5,8))]:
  estimates=[];variances=[]
  for i,sample in enumerate(samples):
   v=list(sample);got=m.sample_mean(v);ck(f'{name}{i} mean',got,mean(v),'source on external exhaustive index design',True);ck(f'{name}{i} sample variance',m.sample_variance(v),variance(v),'independent pairwise-distance variance oracle',True);se=m.standard_error_mean(v);ck(f'{name}{i} SE',se,sqrt(variance(v)/2),'pairwise-distance/100-digit square root',True)
   estimates.append(F(str(got)));variances.append(se*se)
  ck(name+' design mean',mean(estimates),mu,'uniform finite model exact enumeration')
  ck(name+' design variance',popvar(estimates),target,'external exact law,not native uncertainty API')
  if name=='without replacement':
   corrected=mean([F(str(v*m.finite_population_correction(2,4)**2)) for v in variances]);ck('expected corrected WOR variance',corrected,target,'expectation of estimated VARIANCE,not unbiased SE',True)
  else:
   ck('expected uncorrected WR variance',float(mean([F(str(v)) for v in variances])),target,'iid-replacement law',True);ck('incorrectly FPC-adjusted WR variance',float(mean([F(str(v*m.finite_population_correction(2,4)**2)) for v in variances])),F(5,16),'counterexample:wrong design correction halves estimated variance',True)
  records[name]=dict(samples=samples,mean=str(mu),variance=str(target))
 ck('population variance N',popvar(population),F(5,4),'independent pairwise finite law');ck('population variance N-1',variance(population),F(5,3),'independent pairwise sample convention')
 ck('FPC sample convention',m.finite_population_correction(2,4),sqrt(F(1,2)),'multiplier on n-1 sample SD/sqrt(n)',True)
 ck('known-population convention',sqrt(popvar(population)*F(4-2,4-1)/2),sqrt(F(5,12)),'external known N-denominator population SD convention',True)
 census=m.sample_without_replacement(population,4,19);ck('census units',sorted(census),population,'native sample without replacement');ck('census mean',m.sample_mean(census),mu,'exact finite target',True);ck('census FPC',m.finite_population_correction(4,4),0.,'finite target census');ck('census corrected SE',m.standard_error_mean(census)*m.finite_population_correction(4,4),0.,'no finite-frame sampling uncertainty');ck('census uncorrected SE positive',m.standard_error_mean(census)>0,True,'future/measurement uncertainty not assessed')
 selected=[2,3];estimate=m.sample_mean(selected);ck('selected mean',estimate,F(5,2),'external eligibility restriction',True);ck('selected frame FPC',m.finite_population_correction(2,2),0.,'census of wrong frame');ck('selected target bias',F(str(estimate))-mu,F(1),'external full-frame target');ck('selected target MSE',(F(str(estimate))-mu)**2,F(1),'zero local design variance plus squared bias')
 values=[1,1,2,2];duplicate_seed=None
 for seed in range(32):
  units=m.sample_without_replacement(list(range(4)),2,seed);v=m.sample_without_replacement(values,2,seed);ck(f'unit identity{seed}',len(set(units)),2,'unit positions remain distinct');ck(f'value mapping{seed}',v,[values[i] for i in units],'same native draw on duplicated values')
  if len(set(v))<2:duplicate_seed=seed
 ck('duplicate values observed',duplicate_seed is not None,True,'without replacement does not mean distinct values');ck('exact duplicate-value probability',F(sum(values[a]==values[b] for a,b in itertools.combinations(range(4),2)),6),F(1,3),'external six equally likely unit subsets')
 bootstrap=[]
 for i,indices in enumerate(itertools.product(range(4),repeat=4)):
  v=[population[j] for j in indices];got=m.sample_mean(v);ck(f'conditional resample{i}',got,mean(v),'source mean on external exhaustive empirical resampling,not PRNG bootstrap replay',True);bootstrap.append(F(str(got)))
 ck('conditional bootstrap mean',mean(bootstrap),mu,'all256 equally likely resamples');ck('conditional bootstrap variance',popvar(bootstrap),F(5,16),'empirical N-denominator variance divided by n');ck('original iid variance estimate',m.standard_error_mean(population)**2,F(5,12),'n-1 estimate differs from finite empirical resampling variance',True)
 draws=m.bootstrap_means(population,128,11);ck('native bootstrap count',len(draws),128,'actual native seeded bootstrap');ck('native bootstrap replay',m.bootstrap_means(population,128,11),draws,'reproducibility,not uncertainty calibration');ck('native bootstrap SE',m.bootstrap_standard_error(population,128,11),sqrt(variance([F(str(x)) for x in draws])),'independent pairwise variance of native reported128 means',True)
 records['native_bootstrap']=dict(seed=11,replicates=128,means=draws,scope='conditional finite Monte Carlo,not population representativeness or coverage proof')
 prior=json.loads((here.parent/'chapter-15-sampling-estimation-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F133 nine baseline failures/34 predicates retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'unchanged source;24 answers/ten tasks/historical totals retained')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,designs=records,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected finite sampling/FPC/conditional bootstrap assumptions;no PRNG uniformity,real inclusion,dependence,platform,independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
