"""Descriptive ACF versus population dependence, imputation and supplied costs."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='1a5045c7a3c39727737579534f7074051559aa64';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.13-statistical-pitfalls-in-financial-data.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
def acf_oracle(x):
 n=len(x);mu=sum(x)/n;den=sum(v*v for v in x)-n*mu*mu
 if not den:return None
 numerator=sum(x[i]*x[i-1] for i in range(1,n))-mu*(2*sum(x)-x[0]-x[-1])+(n-1)*mu*mu
 return numerator/den
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'statistical_pitfalls.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('pitfall_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 paths=[];native_acfs=[];constant_raw=constant_squared=0;records=[]
 for amplitude in [F(1,10),F(1,5)]:
  for signs in itertools.product([-1,1],repeat=4):
   R=[amplitude*s for s in signs];paths.append(R);values=list(map(float,R));i=len(paths)-1;ck(f'path{i} native mean',m.sample_mean(values),sum(R)/4,'native mean vs exact finite path',True);expected=acf_oracle(R)
   try:got=m.lag_one_autocorrelation(values)
   except ValueError:got=None
   ck(f'path{i} raw sample ACF',got,expected,'native centered diagnostic vs expanded raw-sum oracle',expected is not None)
   if got is None:constant_raw+=1
   else:native_acfs.append(F(str(got)))
   squared=list(map(float,[r*r for r in R]))
   try:m.lag_one_autocorrelation(squared);got_squared='numeric result'
   except ValueError:got_squared='constant rejected';constant_squared+=1
   ck(f'path{i} squared diagnostic',got_squared,'constant rejected','path has common amplitude; constant squared series is not evidence of independence')
   overlap=m.overlapping_returns(values,3)
   for j,value in enumerate(overlap):ck(f'path{i} overlap{j}',value,math.prod((1+r for r in R[j:j+3]),start=F(1))-1,'native overlap vs exact gross product',True)
   records.append(dict(returns=list(map(str,R)),native_raw_acf=str(got),native_squared_outcome=got_squared,native_overlap=overlap))
 mean0=sum(r[0] for r in paths)/32;mean_square=sum(r[0]**2 for r in paths)/32
 ck('population marginal mean',mean0,F(0),'exact common-amplitude/independent-sign law')
 ck('population marginal variance',sum(r[0]**2 for r in paths)/32,F(1,40),'exact finite law')
 ck('population adjacent raw covariance',sum(r[0]*r[1] for r in paths)/32,F(0),'independent zero-mean signs conditional on common amplitude')
 ck('population squared mean',mean_square,F(1,40),'exact finite law')
 ck('population adjacent squared covariance',sum((r[0]**2-mean_square)*(r[1]**2-mean_square) for r in paths)/32,F(9,40000),'positive shared-amplitude dependence despite zero raw covariance')
 ck('raw constant-path probability',F(constant_raw,32),F(1,8),'native diagnostic rejection frequency under specified law')
 ck('squared constant-path probability',F(constant_squared,32),F(1),'within-path constancy versus across-law dependence')
 ck('conditional native sample ACF mean',sum(native_acfs)/len(native_acfs),F(-1,4),'independent four-sign ACF pattern counts, conditional on nonconstant paths',True)
 for name,x in [('caller zero-filled',[.1,0,-.1,0]),('caller compacted',[.1,-.1,0])]:ck(name+' ACF',m.lag_one_autocorrelation(x),acf_oracle(list(map(lambda v:F(str(v)),x))),'native diagnostics of different caller missingness conventions',True)
 try:m.lag_one_autocorrelation([.1,None,-.1]);missing='accepted'
 except ValueError:missing='rejected'
 ck('missing value not silently imputed',missing,'rejected','source numeric-domain guard, not a missingness model')
 r=[.01,.01,-.01,-.01]*3+[.04,.04,-.04,-.04]*3;p_values=[.001,.003,.02,.07]+[.5]*16;R=list(map(lambda v:F(str(v)),r));squared=[v*v for v in R]
 ck('project raw ACF',m.lag_one_autocorrelation(r),acf_oracle(R),'native descriptive project metric vs expanded oracle',True)
 ck('project squared ACF',m.lag_one_autocorrelation(list(map(float,squared))),acf_oracle(squared),'native descriptive project metric vs expanded oracle',True)
 net=[float(v-F(1,1000)) for v in R];ck('hypothetical net mean',m.sample_mean(net),F(-1,1000),'native mean of caller .001 per-period cost, not measured execution costs',True)
 prior=json.loads((here.parent/'chapter-15-pitfalls-review/results.json').read_text());fixture=hashlib.sha256(json.dumps([[.2,-.5],r,p_values]).encode()).hexdigest();ck('prescribed project fixture hash',fixture,prior['project_report']['fixture_sha256'],'supplied synthetic universe/strategy/ledger lineage')
 models.append(dict(name='common random amplitude',path_weight='1/32',paths=records,marginal_variance='1/40',population_raw_covariance='0',population_squared_covariance='9/40000',nonconstant_conditional_sample_acf_mean='-1/4',scope='Amplitude .1/.2 shared across four periods, independent fair signs; explicit mixture not real returns or a fitted volatility model'))
assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256'];f219=json.loads((here.parent/'v10-selection-ledger/F219-assumption-clarification.json').read_text());assert hashlib.sha256(raw).hexdigest()==f219['candidate_source_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Finite descriptive dependence law, caller missingness/cost examples and supplied project metrics; no HAC/model/data/strategy/platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
