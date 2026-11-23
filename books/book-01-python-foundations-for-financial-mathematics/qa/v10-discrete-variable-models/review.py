"""Finite discrete PMF/binomial/CDF/count dependence and severity assumptions."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='d2e0b72758c3bb81321b0786021d28ff70ed25d0';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.07-discrete-random-variables.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def enumerate_counts(probabilities):
 n=len(probabilities);d={k:F(0) for k in range(n+1)}
 for bits in itertools.product([0,1],repeat=n):
  weight=F(1)
  for bit,p in zip(bits,probabilities):weight*=p if bit else 1-p
  d[sum(bits)]+=weight
 return d
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'discrete_variables.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('dv_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for n,p in itertools.product(range(7),[F(0),F(1,10),F(1,2),F(9,10),F(1)]):
  expected=enumerate_counts([p]*n);got=m.binomial_pmf(n,p);label=f'n{n}p{p}';ck(label+' PMF',got,expected,'external Bernoulli-sequence enumeration,not comb/power source formula');mean=sum(k*v for k,v in expected.items());var=sum(expected[a]*expected[b]*(a-b)**2 for a,b in itertools.combinations(expected,2));ck(label+' mean',m.expectation(got),mean,'independent count-state weighted sum',True);ck(label+' variance',m.variance(got),var,'weighted pairwise-distance oracle',True)
  for threshold in [F(k,2) for k in range(-2,2*n+3)]:
   cdf=sum(v for k,v in expected.items() if k<=threshold);tail=sum(v for k,v in expected.items() if k>threshold);left=m.cdf(got,threshold);right=m.tail_probability(got,threshold);ck(label+' CDF'+str(threshold),left,cdf,'CDF includes threshold atom',True);ck(label+' strict tail'+str(threshold),right,tail,'tail is strictly greater than threshold',True);ck(label+' complement'+str(threshold),left+right,1,'reported finite CDF/tail complement',True)
 independent=enumerate_counts([F(1,2)]*6);heterogeneous=enumerate_counts([F(0),F(1,10),F(1,5),F(4,5),F(9,10),F(1)]);shared={0:F(1,2),6:F(1,2)};cases=[('IID',independent,F(3,2),F(7,64)),('heterogeneous',heterogeneous,F(1,2),F(9,625)),('shared shock',shared,F(9),F(1,2))]
 for name,d,var,tail in cases:
  ck(name+' count mean',m.expectation(d),3.,'same expected count does not identify count dispersion');ck(name+' count variance',m.variance(d),var,'declared heterogeneous/independent or common-shock law',True);ck(name+' count strict tail4',m.tail_probability(d,4),tail,'fixed count threshold with different joint/default-rate assumptions',True);records.append(dict(name=name,mean='3',variance=str(var),tail_gt4=str(tail)))
 low=enumerate_counts([F(1,10)]*4);high=enumerate_counts([F(9,10)]*4);mixture={k:(low[k]+high[k])/2 for k in low};ck('regime mixture mean',m.expectation(mixture),2.,'conditionally independent defaults mixed over a common regime');ck('regime mixture variance',m.variance(mixture),F(73,25),'E[Var]+Var[E]=.36+2.56',True);ck('regime mixture tail3',m.tail_probability(mixture,3),F(3281,10000),'mixture of exact all-default event probabilities',True)
 for name,d,var,tail in cases:
  loss={1000*k:v for k,v in d.items()};ck(name+' fixed-loss mean',m.expectation(loss),3000.,'external fixed1000-loss-per-default mapping,not random severity');ck(name+' fixed-loss variance',m.variance(loss),var*1000000,'loss units square,requiring fixed identical exposure/severity',True)
 d=m.binomial_pmf(4,.5);draws=m.sample(d,128,19);ck('native sample replay',m.sample(d,128,19),draws,'actual seed/runtime replay,not binomial calibration');ck('native sample count',len(draws),128,'actual native sampler');ck('native sample support',all(x in d for x in draws),True,'reported support only,no frequency/rare-tail claim')
 prior=json.loads((here.parent/'chapter-14-discrete-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F116 seven failures/48 predicates/24 answers/ten tasks retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,count_model_records=records,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected finite PMF/binomial/CDF/count/severity assumptions;not actual default calibration,rare-tail sampling,platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
