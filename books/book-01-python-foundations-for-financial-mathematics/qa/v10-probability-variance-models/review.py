"""Finite joint laws, empirical denominator assumptions and additive-horizon variance."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='47f7f67f22be55b31fa5164f2774e3d324060610';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.10-variance-and-standard-deviation.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[]
def ck(name,got,want,kind):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=(got==want if isinstance(got,str) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15)),kind=kind))
def pmf(values,weights):
 out={}
 for x,p in zip(values,weights):out[x]=out.get(x,F(0))+p
 return out
def pairvar(values,weights):return sum(p*q*(x-y)**2 for x,p in zip(values,weights) for y,q in zip(values,weights))/2
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'variance.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('variance_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 base={-20:F(1,4),5:F(1,2),30:F(1,4)}
 for a,b in itertools.product([-3,0,2],[-100,0,70]):
  d=m.transformed(base,a,b);ck(f'affine {a}/{b} variance',m.variance(d),a*a*F(625,2),'independent centered rational law;currency squared');ck(f'affine {a}/{b} SD',m.standard_deviation(d),abs(a)*math.sqrt(312.5),'SD restores currency units')
 states=list(itertools.product([-1,1],repeat=2));w=[F(1,4)]*4;X=[s[0] for s in states]
 for label,Y in [('independent',[s[1] for s in states]),('shared',X),('opposed',[-x for x in X])]:
  cov=sum(p*x*y for x,y,p in zip(X,Y,w))
  for sign in [-1,1]:
   vals=[x+sign*y for x,y in zip(X,Y)];ck(f'{label} sum sign{sign}',m.variance(pmf(vals,w)),2+2*sign*cov,'common-state covariance law,not marginal independence');ck(f'{label} pairwise oracle sign{sign}',m.variance(pmf(vals,w)),pairvar(vals,w),'independent pairwise squared-difference identity')
 # A nonlinear deterministic relation has zero covariance without independence.
 X=[-1,0,1];Y=[1,0,1];w=[F(1,3)]*3;mx=sum(p*x for x,p in zip(X,w));my=sum(p*y for y,p in zip(Y,w))
 ck('dependent zero covariance',sum(p*(x-mx)*(y-my) for x,y,p in zip(X,Y,w)),0,'Y=X squared,so independent sum-variance equality does not establish independence');ck('dependent sum variance',m.variance(pmf([x+y for x,y in zip(X,Y)],w)),F(8,9),'2/3 plus2/9 despite deterministic dependence')
 ck('nonfactorizing joint zero event',F(1,3)-F(1,3)**2,F(2,9),'P(X=0,Y=0) differs from product of marginals')
 for n in [2,3,4]:
  samples=list(itertools.product([-1,1],repeat=n));weights=[F(1,2**n)]*len(samples)
  ck(f'IID n{n} mean sample variance',sum(p*F(m.sample_variance(s)) for s,p in zip(samples,weights)),1,'exhaustive IID Rademacher sampling;unbiased under stipulated population')
  ck(f'IID n{n} mean population variance',sum(p*F(m.population_variance(s)) for s,p in zip(samples,weights)),F(n-1,n),'descriptive denominator n is biased for generating variance')
  ck(f'shared n{n} sample variance',sum(m.sample_variance([x]*n) for x in [-1,1])/2,0,'perfectly dependent observations;Bessel correction does not remove dependence bias')
 for label,values,w,want in [('IID',[sum(s) for s in itertools.product([0,1],repeat=3)],[F(1,8)]*8,F(3,4)),('shared',[0,3],[F(1,2)]*2,F(9,4))]:
  ck(label+' default count variance',m.variance(pmf(values,w)),want,'same three Bernoulli marginals;binomial independence contract');ck(label+' default count mean',m.mean(pmf(values,w)),F(3,2),'mean alone does not identify count risk')
 # Two equal periods model additive returns only;compounded wealth is a different variable.
 for label,Y,want in [('uncorrelated',[s[1] for s in states],2),('persistent',[s[0] for s in states],4),('offset',[-s[0] for s in states],0)]:
  ck(label+' additive horizon variance',m.variance(pmf([s[0]+y for s,y in zip(states,Y)],[F(1,4)]*4)),want,'sqrt-time scaling requires zero cross-period covariance and matching variance')
 for scale in [F(1,100),100]:ck('unit scale '+str(scale),m.variance(m.transformed(base,scale,0)),F(625,2)*scale**2,'return decimals/percentage points and currency conversions square units')
 prior=json.loads((here.parent/'chapter-14-variance-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F119 retained source identity');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no financial-source edit')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Finite stipulated joint laws and exact exhaustive sampling expectations;no empirical model validation,compounded-return annualization or independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert not r['failed']
