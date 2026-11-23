"""Finite paired-sampling,covariance feasibility and dependence assumptions."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='f0af8925838af1a123848be1b3774c45c009bb29';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.11-covariance-and-correlation.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[]
def ck(name,got,want,kind):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=(got==want if isinstance(got,(str,bool)) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15)),kind=kind))
def paircov(x,y):return sum((a-b)*(c-d) for a,c in zip(x,y) for b,d in zip(x,y))/F(2*len(x)**2)
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'covariance.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('cov_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 X=[-2,0,2]
 for i,Y in enumerate(itertools.permutations([-3,0,3])):
  cov=paircov(X,Y);vx=paircov(X,X);vy=paircov(Y,Y);rho=float(cov)/math.sqrt(float(vx*vy))
  ck(f'pairing{i} covariance',m.population_covariance(X,Y),cov,'exact pairwise-difference oracle;identical marginals,changed pairing')
  ck(f'pairing{i} correlation',m.correlation(X,Y),rho,'independent pairwise covariance normalizer')
  for a,c in itertools.product([-2,1,3],[-3,2]):
   xx=[a*x+7 for x in X];yy=[c*y-5 for y in Y];ck(f'pairing{i} scales{a}/{c} covariance',m.population_covariance(xx,yy),a*c*cov,'fixed deterministic units/shift contract');ck(f'pairing{i} scales{a}/{c} correlation',m.correlation(xx,yy),(1 if a*c>0 else -1)*rho,'nonzero deterministic scales reverse sign iff product negative')
 for label,states in [('independent',list(itertools.product([-1,1],repeat=2))),('shared',[(-1,-1),(1,1)]),('opposed',[(-1,1),(1,-1)])]:
  truecov=paircov([x for x,y in states],[y for x,y in states])
  for n in [2,3]:
   samples=list(itertools.product(states,repeat=n));weight=F(1,len(samples));sample_sum=population_sum=F(0)
   for sample in samples:
    x,y=zip(*sample);sample_sum+=weight*F(m.sample_covariance(x,y));population_sum+=weight*F(m.population_covariance(x,y))
   ck(f'{label} IIDpaired n{n} sample expectation',sample_sum,truecov,'exhaustive IID draws of paired vectors;within-pair independence unnecessary')
   ck(f'{label} IIDpaired n{n} population expectation',population_sum,F(n-1,n)*truecov,'descriptive denominator bias under stipulated sampling')
  ck(label+' shared-time sample expectation',sum(m.sample_covariance([x]*3,[y]*3) for x,y in states)/len(states),0,'perfect dependence across observation times breaks unbiasedness except zero target')
 # Identical zero correlation does not identify joint downside probability.
 for label,x,y,tail in [('independent',[-1,-1,1,1],[-1,1,-1,1],F(1,4)),('exclusive',[-1,1,0,0],[0,0,-1,1],0)]:
  ck(label+' zero correlation',m.correlation(x,y),0,'different finite laws with zero linear association')
  ck(label+' joint negative event',F(sum(a<0 and b<0 for a,b in zip(x,y)),len(x)),tail,'external tail-event enumeration;not inferred from Pearson correlation')
 # All three pairwise2x2 matrices pass,but their common3x3 matrix is infeasible.
 for pair in ['12','13','23']:ck('pairwise bound '+pair,m.portfolio_variance([1,1],[1,1],F(-9,10)),F(1,5),'pairwise helper only validates its supplied two-asset matrix')
 ck('three-asset proposed equal-weight variance',F(3)+6*F(-9,10),F(-12,5),'supplemental negative quadratic form proves non-PSD;not a source3asset validation')
 for w in [F(1,2),F(3,2),F(-1,2)]:
  for cov in [F(-1),F(0),F(1)]:ck(f'signed weights{w}/{1-w} cov{cov}',m.portfolio_variance([w,1-w],[1,1],cov),w*w+(1-w)**2+2*w*(1-w)*cov,'fixed weights may be short/leveraged;lower correlation need not reduce variance when weight product negative')
 ck('date alignment hidden by lengths',m.correlation([1,2,3],[3,1,2]),F(-1,2),'synthetic permutation passes length checks;caller must align timestamps,no real data claim')
 prior=json.loads((here.parent/'chapter-14-covariance-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F120 retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no financial source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Finite stipulated paired-state laws/exhaustive IID sampling and conceptual matrix/timestamp limits;no market calibration/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert not r['failed']
