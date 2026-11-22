"""Pinned return statistics under finite IID/common/alternating increment laws."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='c4e5392d416b692c8737b9e03629397624219802';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.11-financial-return-statistics.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):
 ok=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want
 rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=ok))
def dec(x):return D(x.numerator)/D(x.denominator)
def root(x):
 with localcontext() as c:c.prec=100;return dec(x).sqrt()
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'financial_return_statistics.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('return_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 laws=[('IID signs',list(itertools.product([-1,1],repeat=4)),F(1,25),F(1,100)),('common sign',[(s,s,s,s) for s in [-1,1]],F(4,25),F(0)),('alternating sign',[(s,-s,s,-s) for s in [-1,1]],F(0),F(1,75))]
 for name,signs,true_sum_var,expected_sample_var in laws:
  paths=[[F(1,50)+F(s,10) for s in z] for z in signs];weight=F(1,len(paths));records=[];means=[];variances=[];annual_squares=[];compounds=[]
  for i,R in enumerate(paths):
   values=list(map(float,R));mu=sum(R)/4;v=sum((R[j]-R[k])**2 for j in range(4) for k in range(j+1,4))/12;gross=math.prod((1+r for r in R),start=F(1));compound=gross-1
   with localcontext() as c:c.prec=100;geometric=dec(gross).sqrt().sqrt()-1
   actual=dict(mean=m.arithmetic_mean(values),sample_variance=str(m.exact_sample_variance(values)),sample_vol=m.sample_volatility(values),annualized_vol=m.annualized_volatility(values,4),compound=m.cumulative_return(values),geometric=m.geometric_mean(values))
   ck(f'{name} path{i} mean',actual['mean'],mu,'source mean vs exact finite law path',True)
   ck(f'{name} path{i} variance',F(actual['sample_variance']),v,'source centered variance vs independent pairwise identity')
   ck(f'{name} path{i} sample SD',actual['sample_vol'],root(v),'source SD vs independent pairwise variance/root',True)
   ck(f'{name} path{i} four-period scaling',actual['annualized_vol'],root(4*v),'source algebraic annualization, not process validity',True)
   ck(f'{name} path{i} compound',actual['compound'],compound,'source wealth product vs exact represented returns',True)
   ck(f'{name} path{i} geometric',actual['geometric'],geometric,'source log-based growth vs independent nested square roots',True)
   means.append(F(str(actual['mean'])));variances.append(F(actual['sample_variance']));annual_squares.append(F(actual['annualized_vol'])**2);compounds.append(F(actual['compound']));records.append(dict(returns=list(map(str,R)),source=actual))
  ck(name+' law mass',weight*len(paths),1,'exact finite process law')
  for j in range(4):
   mean=sum(p[j] for p in paths)*weight;var=sum((p[j]-mean)**2 for p in paths)*weight
   ck(f'{name} marginal{j} mean',mean,F(1,50),'same marginal mean across dependence laws')
   ck(f'{name} marginal{j} variance',var,F(1,100),'same marginal variance across dependence laws')
  sums=[sum(p) for p in paths];sum_mean=sum(sums)*weight;sum_variance=sum((s-sum_mean)**2 for s in sums)*weight
  ck(name+' sum mean',sum_mean,F(2,25),'exact additive horizon mean, not compounded return')
  ck(name+' sum sampling variance',sum_variance,true_sum_var,'independent covariance law for sum of four increments')
  ck(name+' mean native sample variance',sum(variances)*weight,expected_sample_var,'native estimator expectation under exact process law')
  ck(name+' mean native scaled variance',sum(annual_squares)*weight,4*expected_sample_var,'native annualized SD squared, weighted exactly then compared',True)
  ck(name+' native linearized mean',4*sum(means)*weight,F(2,25),'caller linear annual-mean convention using native means')
  if name=='IID signs':expected_compound=F(51,50)**4-1
  elif name=='common sign':expected_compound=((F(28,25)**4+F(23,25)**4)/2)-1
  else:expected_compound=(F(28,25)*F(23,25))**2-1
  ck(name+' expected native compounded return',sum(compounds)*weight,expected_compound,'native compounded paths weighted vs closed joint-law gross-product expectation',True)
  ck(name+' linear mean differs from expected compounding',F(2,25)!=expected_compound,True,'linear mean convention is not realized/expected compounded growth')
  models.append(dict(name=name,paths=records,exact_path_weight=str(weight),period_count=4,periods_per_year=4,marginal_mean='1/50',marginal_variance='1/100',true_additive_sum_variance=str(sum_variance),expected_native_sample_variance=str(expected_sample_var),expected_native_scaled_variance=str(4*expected_sample_var),linearized_mean='2/25',expected_compounded_return=str(expected_compound),scope='Four artificial equal periods form one hypothetical year; exact dependence laws, not actual daily/calendar/252-session data or PRNG evidence.'))
prior=json.loads((here.parent/'chapter-15-return-statistics-review/results.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['source_sha256'];assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Annualization/sample-moment/compounding assumptions under three explicit finite return laws; no real-data scaling, compounded-volatility approximation, tail/model or independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
