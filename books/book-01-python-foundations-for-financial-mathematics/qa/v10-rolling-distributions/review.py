"""Finite rolling SD/correlation/compounded-window laws and caller window selection."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='e29f14d85ecbdf6bde690da001b06d61fa191865';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.12-rolling-statistics.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):
 ok=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want
 rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=ok))
def root(x):
 with localcontext() as c:c.prec=100;return (D(x.numerator)/D(x.denominator)).sqrt()
def corr(a,b):
 # Pairwise difference identity, independent of native centered products.
 xx=sum((a[i]-a[j])**2 for i in range(3) for j in range(i+1,3));yy=sum((b[i]-b[j])**2 for i in range(3) for j in range(i+1,3))
 if not xx or not yy:return None
 xy=sum((a[i]-a[j])*(b[i]-b[j]) for i in range(3) for j in range(i+1,3));return root(F(xy*xy,xx*yy))*(1 if xy>=0 else -1)
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'rolling_statistics.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('rolling_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 patterns=list(itertools.product([-1,1],repeat=4));stds=[];compounds=[];path_records=[]
 for i,x in enumerate(patterns):
  sd=m.rolling_sample_std(list(x),3);r=[F(v,10) for v in x];comp=m.rolling_compounded_return(list(map(float,r)),3);stds.append(sd);compounds.append(comp)
  for j in range(2):
   w=x[j:j+3];variance=F(sum((w[a]-w[b])**2 for a in range(3) for b in range(a+1,3)),6);gross=math.prod((1+v for v in r[j:j+3]),start=F(1))
   ck(f'path{i} SD{j}',sd[j],root(variance),'native SD vs independent pairwise variance',True)
   ck(f'path{i} compound{j}',comp[j],gross-1,'native compounded-window value vs exact gross product',True)
  path_records.append(dict(signs=x,native_SD=sd,native_compounds=comp))
 undefined=[0,0];correlations=[]
 for i,x in enumerate(patterns):
  for k,y in enumerate(patterns):
   actual=m.rolling_correlation(list(x),list(y),3);correlations.append(actual)
   for j in range(2):
    expected=corr(x[j:j+3],y[j:j+3]);ck(f'pair{i},{k} correlation{j}',actual[j],expected,'native window correlation vs pairwise-difference oracle',expected is not None);undefined[j]+=actual[j] is None
 means=[sum(F(v[j])**2 for v in stds)/16 for j in range(2)]
 for j in range(2):ck(f'expected rolling sample variance{j}',means[j],F(1),'exact IID law, native SD squared then weighted',True)
 covariance=sum((F(v[0])**2-means[0])*(F(v[1])**2-means[1]) for v in stds)/16
 ck('adjacent rolling sample variance covariance',covariance,F(1,9),'exact joint indicator probability5/8 times16/9 minus1',True)
 for j in range(2):ck(f'undefined correlation probability{j}',F(undefined[j],256),F(7,16),'one or both independent three-sign windows constant:1−(3/4)^2')
 compmeans=[sum(F(str(v[j])) for v in compounds)/16 for j in range(2)]
 for j in range(2):ck(f'expected rolling compounded return{j}',compmeans[j],F(0),'independent gross-factor expectation1')
 compcov=sum((F(str(v[0]))-compmeans[0])*(F(str(v[1]))-compmeans[1]) for v in compounds)/16
 ck('adjacent compounded return covariance',compcov,F(201,10000),'two shared gross factors: (1+.1²)^2−1')
 selected=sum(min(F(v[0])**2,F(v[1])**2) for v in stds)/16
 ck('caller lower-window selected variance expectation',selected,F(5,6),'both windows nonconstant probability5/8×4/3; selection below unconditional mean1',True)
 models.append(dict(name='four IID fair signs',path_weight='1/16',paths=path_records,expected_sample_variance='1',adjacent_sample_variance_covariance='1/9',independent_x_y_pair_weight='1/256',undefined_window_correlation_probability='7/16',adjacent_compounded_return_covariance='201/10000',caller_selected_variance_expectation='5/6',scope='SD/correlation use signs±1; compounded-return example uses±.1. All laws hypothetical, not real financial processes or confidence calibration.'))
prior=json.loads((here.parent/'chapter-15-rolling-review/results.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['source_sha256'];assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Rolling SD/correlation/compounded finite-law assumptions and caller window selection; project/window/timing/model/platform/independent boundaries remain unfinished')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
