"""Return basis, corporate actions, positional alignment and project provenance."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='56ed4b707947235643686a472fb6e5b860199cee';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.11-financial-return-statistics.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
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
 def prices(name,values,basis,labels=None):
  actual=m.simple_returns(values);X=[F(str(v)) for v in values];expected=[(b-a)/a for a,b in zip(X,X[1:])]
  for i,(v,w) in enumerate(zip(actual,expected)):ck(name+' return'+str(i),v,w,'native price-only return vs independent exact price difference ratio',True)
  ck(name+' compounded endpoint',m.cumulative_return(actual),X[-1]/X[0]-1,'source compounding of reported returns vs endpoint, within tolerance',True)
  logs=m.log_returns(values)
  with localcontext() as c:c.prec=100;expected_log=(dec(X[-1]/X[0])).ln()
  ck(name+' log endpoint',math.fsum(logs),expected_log,'native log additivity vs independent100-digit endpoint logarithm',True)
  models.append(dict(name=name,prices=values,labels=labels,declared_basis=basis,native_returns=actual,native_logs=logs,scope='Caller-specified synthetic price basis/labels; native API consumes numbers only'))
  return actual
 raw_split=prices('raw split',[100,50],'unadjusted per-share price around hypothetical2-for-1 split',[1,2]);adjusted=prices('split-adjusted',[100,100],'caller supplied comparable per-old-share/total-value basis',[1,2])
 ck('split share-value preservation',F(2*50,100)-1,0,'supplemental share-count/corporate-action algebra, no source adapter')
 ck('split raw versus adjusted differs',raw_split!=adjusted,True,'basis matters despite valid positive numeric inputs')
 ex_div=prices('ex-dividend price-only',[100,99],'price only, hypothetical cash dividend1 separately specified',[1,2]);total_index=prices('caller total-return index',[100,100],'caller assembled total wealth with cash dividend1',[1,2]);ck('cash dividend holding-period total return',F(99+1,100)-1,0,'supplemental cash-flow convention, not native dividend processing')
 local=prices('local-currency price',[100,110],'local currency, hypothetical FX rates2 then1 base per local',[1,2]);base=prices('caller base-currency value',[200,110],'caller price×FX conversion, same declared labels',[1,2]);ck('FX product identity',(1+F(str(local[0])))*F(1,2)-1,F(str(base[0])),'native metrics of caller currency transform')
 stale=prices('stale intermediate quote',[100,100,110],'synthetic stale intermediate observation',[1,2,3]);fresh=prices('alternative intermediate quote',[100,105,110],'separate hypothetical more frequently updated path, not verified truth',[1,2,3])
 for name,r in [('stale',stale),('alternative',fresh)]:
  R=list(map(lambda v:F(str(v)),r));v=sum((a-b)**2 for i,a in enumerate(R) for b in R[i+1:])/(len(R)*(len(R)-1));ck(name+' observed-path SD',m.sample_volatility(r),root(v),'native volatility of supplied observed path, not latent-price accuracy',True)
 ck('stale path dispersion differs',m.sample_volatility(stale)>m.sample_volatility(fresh),True,'specific counterexample only; no universal direction or freshness detector')
 a=prices('asset A irregular labels',[100,110,121],'numeric values with labels1,2,4',[1,2,4]);b=prices('asset B different labels',[100,90,99],'numeric values with labels1,3,4',[1,3,4]);ck('equal return counts despite misaligned intervals',len(a)==len(b),True,'native lengths cannot prove calendar alignment')
 reordered=prices('nonchronological input',[100,121,110],'caller order labels1,4,2',[1,4,2]);ck('caller ordering changes return sequence',reordered!=a,True,'no native timestamp/order guard')
 old=prices('original source snapshot',[100,110],'caller snapshot before hypothetical correction',[1,2]);revised=prices('revised source snapshot',[100,105],'different caller snapshot, availability unspecified',[1,2]);ck('snapshot hashes differ',hashlib.sha256(json.dumps([100,110]).encode()).hexdigest()!=hashlib.sha256(json.dumps([100,105]).encode()).hexdigest(),True,'content identity, not temporal availability/authenticity')
 project_prices=[100,110,99];r=[-.04,-.01,0,.02,.08,.01];rf=[.001]*6;prior=json.loads((here.parent/'chapter-15-return-statistics-review/results.json').read_text());fixture=hashlib.sha256(json.dumps([project_prices,r,rf]).encode()).hexdigest();ck('prescribed project fixture identity',fixture,prior['project_report']['fixture_sha256'],'synthetic inputs match previous project record')
 ck('price fixture and separate risk fixture have different lengths',len(m.simple_returns(project_prices))!=len(r),True,'risk fixture intentionally supplied independently, not silently derived from prices')
 excess=[float(F(str(a))-F(str(b))) for a,b in zip(r,rf)];ck('prescribed hypothetical excess mean',m.arithmetic_mean(excess),F(9,1000),'source mean of caller arithmetic excess differences',True)
 ck('prescribed hypothetical per-period Sharpe',m.arithmetic_mean(excess)/m.sample_volatility(excess),F(9,40),'caller ratio of native metrics, no native Sharpe API',True)
 models.append(dict(name='prescribed project provenance',fixture_sha256=fixture,prices=project_prices,risk_returns=r,riskfree=rf,periods_per_year=252,prices_labels=[0,1,2],risk_labels=[1,2,3,4,5,6],calendar_dates=None,currency='fictional USD',cash_flows=None,scope='No actual dividend/split/FX/calendar/quote/revision feed or market risk-free source; risk fixture separate; per-period excess/Sharpe caller logic'))
prior=json.loads((here.parent/'chapter-15-return-statistics-review/results.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['source_sha256'];assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Supplied synthetic return-basis transformations and project lineage; source consumes positive positional prices, not corporate-action/timestamp/FX/freshness/revision adapters or independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
