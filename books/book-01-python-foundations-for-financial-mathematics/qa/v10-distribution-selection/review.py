"""Distribution assumptions,rate mixtures and units;selected exact native contracts."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from random import Random
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='4a72e39aea1dd8c330c76f1eecc595994a3cb152';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.12-common-probability-distributions.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,tol=0):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=(got==want if isinstance(got,(str,list,bool)) else abs(F(got)-F(want))<=tol),tolerance=str(tol),kind=kind))
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'distributions.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('distribution_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for n,p in itertools.product(range(5),[F(0),F(1,4),F(1,2),F(1)]):
  masses=[F(0)]*(n+1)
  for s in itertools.product([0,1],repeat=n):masses[sum(s)]+=math.prod(p if x else 1-p for x in s)
  for k,want in enumerate(masses):ck(f'binomial{n}/{p}/{k}',m.binomial_pmf(k,n,p),want,'exhaustive independent binary paths;decimal-text/Fraction source inputs',F(1,10**15))
  ck(f'binomial support{n}/{p}',m.binomial_pmf(n+1,n,p),0,'bounded trial count,unlike Poisson')
 with localcontext() as ctx:
  ctx.prec=100
  for rate in [1,2,3]:
   mass=(-D(rate)).exp()
   for k in range(9):
    if k:mass*=D(rate)/k
    ck(f'Poisson{rate}/{k}',m.poisson_pmf(k,rate),F(mass),'100digit independent forward recurrence;ordinary-rate selected accuracy',F(2,10**14))
  mixed_zero=((D(-1).exp()+D(-3).exp())/2);single_zero=D(-2).exp()
  ck('Poisson mixture zero probability',(m.poisson_pmf(0,1)+m.poisson_pmf(0,3))/2,F(mixed_zero),'caller supplies equal regime probabilities,not a single-rate process',F(2,10**14))
  ck('mixture differs from mean-rate zero mass',mixed_zero>single_zero,True,'same mean2 does not identify Poisson law')
  for label,mean,var in [('single rate',F(2),F(2)),('rate mixture',(F(1)+F(3))/2,(F(1)+F(3))/2+((F(1)-2)**2+(F(3)-2)**2)/2)]:
   ck(label+' mean',mean,2,'external conditional moment law');ck(label+' variance',var,2 if label=='single rate' else 3,'E[lambda]+Var(lambda),regime rates1/3 equally likely');models.append(dict(label=label,mean=str(mean),variance=str(var)))
  for hours in [0,F(1,2),2,4]:
   want=1-(-D(hours.numerator if isinstance(hours,F) else hours)/D(hours.denominator if isinstance(hours,F) else 1)/2).exp();ck('exponential hours '+str(hours),m.exponential_cdf(hours,F(1,2)),F(want),'constant hazard per hour,100digit CDF oracle',F(1,10**15));ck('exponential minutes '+str(hours),m.exponential_cdf(hours*60,F(1,120)),F(want),'rate/time reciprocal unit conversion',F(1,10**15))
  # External geometric law counts trials including success;CDF at integer k matches exponential grid when p=1-exp(-lambda*delta).
  survival=D(-1).exp()
  for k in [1,2,4]:ck('grid waiting CDF '+str(k),m.exponential_cdf(k,1),F(1-survival**k),'external geometric p=1-exp(-1),constant independent per-grid hazard;no geometric source helper',F(1,10**15))
 for x,want in [(-1,0),(0,0),(2,F(1,5)),(5,F(1,2)),(10,1),(11,1)]:
  ck('uniform years '+str(x),m.uniform_cdf(x,0,10),want,'interval-length law with endpoint clipping',F(1,10**15));ck('uniform months '+str(x),m.uniform_cdf(x*12,0,120),want,'positive affine time conversion',F(1,10**15))
 rng=Random(912);want=[sum(rng.random()<.25 for _ in range(4)) for _ in range(256)];actual=m.simulate_defaults(4,F(1,4),256,912);ck('actual256 seeded replay',actual,want,'separate uniform-draw replay,not calibration');ck('actual256 support',all(0<=x<=4 and type(x)==int for x in actual),True,'observed support only')
 # Identical default marginals can have count law unlike native IID binomial.
 ck('shared four-loan all-default mass',F(1,4),F(1,4),'external shared-indicator law');ck('IID four-loan all-default mass',m.binomial_pmf(4,4,F(1,4)),F(1,256),'native product-law assumption')
 prior=json.loads((here.parent/'chapter-14-distribution-survey-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F121 retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no financial source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,models=models,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected finite count/rate-mixture and waiting/units assumptions;no empirical fitting,extreme-Poisson or arbitrarily rare simulation validation;normal/lognormal detail continues14.13 and marked interfaces')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert not r['failed']
