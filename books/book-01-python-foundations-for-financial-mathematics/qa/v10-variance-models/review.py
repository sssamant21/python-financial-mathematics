"""Identical marginal variances under different temporal/cross-asset joint laws."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import subprocess,tempfile,importlib.util,json,sys,re,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='f19f4218adbf94b9e6c33e5b5e8ae2a1d3024e9d';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.03-variance-and-standard-deviation.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];laws=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def sqrt(x):
 with localcontext() as c:c.prec=100;return float((D(x.numerator)/D(x.denominator)).sqrt())
def variance(x):
 n=len(x);return sum(((a-b)**2 for i,a in enumerate(x) for b in x[i+1:]),F(0))/n**2
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'variance_standard_deviation.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('variance_lab',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 models=[('IID',list(itertools.product([-1,1],repeat=4)),F(1,100),F(1,25)),('shared',[[-1]*4,[1]*4],F(0),F(4,25)),('alternating',[[-1,1,-1,1],[1,-1,1,-1]],F(1,75),F(0))]
 for name,signs,expected_s2,expected_horizon_var in models:
  paths=[[F(s,10) for s in ss] for ss in signs];estimated=[];sums=[];records=[]
  for i,x in enumerate(paths):
   native=list(map(float,x));v=variance(x);ss=4*v;expected_mean=sum(x)/4
   for ddof in [0,1]:
    result=m.moments(native,ddof);var=ss/(4-ddof)
    expect=dict(count=4,mean=expected_mean,sum_squared_deviations=ss,variance=var,standard_deviation=sqrt(var),ddof=ddof)
    for k,want in expect.items():ck(f'{name} path{i} ddof{ddof} '+k,result[k],want,'native report vs exact pairwise variance',True)
    if ddof==1:estimated.append(F(str(result['variance'])))
   for tau in [F(0),F(1,20)]:
    downside=sum((min(F(0),v-tau)**2 for v in x),F(0))/4
    ck(f'{name} path{i} downside {tau}',m.downside_deviation(native,float(tau)),sqrt(downside),'all-n lower partial moment,not conditional-negative-only SD',True)
   sums.append(sum(x));records.append(dict(returns=list(map(str,x)),sum=str(sum(x)),native_sample_variance=result['variance']))
  ck(name+' expected native sample variance',sum(estimated)/len(estimated),expected_s2,'finite-law expectation depends on joint sampling design',True)
  horizon_var=variance(sums);ck(name+' true horizon-sum variance',horizon_var,expected_horizon_var,'external exact joint law,not a native forecast')
  ck(name+' same marginal variance',sum(x[0]**2 for x in paths)/len(paths),F(1,100),'same daily marginal law,mean0')
  ck(name+' source square-root4 scaling',m.scaled_volatility(.1,4),.2,'source applies supplied uncorrelated-variance assumption',True)
  ck(name+' actual horizon SD',sqrt(horizon_var),sqrt(expected_horizon_var),'IID .2,shared .4,alternating0;different dependence laws',True)
  laws.append(dict(name=name,path_weight='1/'+str(len(paths)),paths=records,expected_sample_variance=str(expected_s2),horizon_sum_variance=str(horizon_var),scope='four-day arithmetic return sum;not compounded wealth variance or an accepted process model'))
 # Cross-asset covariance is equally a joint-law input,not implied by marginals.
 for name,pairs,cov in [('independent',list(itertools.product([F(-1,10),F(1,10)],repeat=2)),F(0)),('same',[(F(-1,10),F(-1,10)),(F(1,10),F(1,10))],F(1,100)),('opposite',[(F(-1,10),F(1,10)),(F(1,10),F(-1,10))],F(-1,100))]:
  portfolio=[(a+b)/2 for a,b in pairs];want=variance(portfolio)
  ck(name+' portfolio variance',m.portfolio_variance(.5,.01,.5,.01,float(cov)),want,'native covariance formula vs explicit finite portfolio outcomes',True)
  ck(name+' supplied covariance',sum(a*b for a,b in pairs)/len(pairs),cov,'external joint-law covariance')
 prior=json.loads((here.parent/'chapter-15-variance-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'prior corrected source/failure records retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,laws=laws,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected finite joint laws;native arithmetic distinct from external sampling/forecast assumptions;no platform/model/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
