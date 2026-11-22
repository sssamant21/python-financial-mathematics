"""Section15.1 measurement/sampling/ordering assumptions using exact source."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import subprocess,tempfile,importlib.util,json,sys,re,hashlib,math,platform,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='8e2cd8aee2f7497e8da34be3f86c22ce28da3c85';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.01-descriptive-statistics.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
def rootq(x):
 with localcontext() as c:c.prec=100;return float((D(x.numerator)/D(x.denominator)).sqrt())
def oracle(values):
 x=[F(str(v)) for v in values];n=len(x);o=sorted(x);pair=sum(((a-b)**2 for i,a in enumerate(x) for b in x[i+1:]),F(0));v=pair/n**2;s=pair/(n*(n-1)) if n>1 else None
 return dict(count=n,mean=sum(x)/n,median=o[n//2] if n%2 else (o[n//2-1]+o[n//2])/2,minimum=o[0],maximum=o[-1],range=o[-1]-o[0],population_variance=v,population_sd=rootq(v),sample_variance=s,sample_sd=None if s is None else rootq(s),negative_fraction=F(sum(v<0 for v in x),n))
def rejects(fn):
 try:fn()
 except ValueError:return 'ValueError'
 return 'accepted'
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'descriptive_statistics.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('descriptive',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 fixtures=[('declared decimal',[.02,-.01,.03,0]),('percent units',[2,-1,3,0]),('shifted decimal',[.03,0,.04,.01]),('missing omitted',[.02,-.01,.03]),('caller zero-filled',[.02,-.01,.03,0]),('untrimmed extreme',[.01,.02,.03,.20]),('caller trimmed',[.02,.03]),('one observation',[.02])]
 reports={}
 for name,x in fixtures:
  actual=m.describe(x);reports[name]=actual
  for k,v in oracle(x).items():ck(name+' '+k,actual[k],v,'native summary vs pairwise/raw-order rational oracle',v is not None)
 for field in ['mean','median','minimum','maximum','range','population_sd','sample_sd']:ck('unit x100 '+field,reports['percent units'][field],100*reports['declared decimal'][field],'numeric scale only, not economic unit validation',True)
 for field in ['population_variance','sample_variance']:ck('unit x10000 '+field,reports['percent units'][field],10000*reports['declared decimal'][field],'variance units square',True)
 ck('negative fraction unit invariant',reports['percent units']['negative_fraction'],reports['declared decimal']['negative_fraction'],'same sign counts')
 for field in ['population_variance','sample_variance','population_sd','sample_sd']:ck('shift invariant '+field,reports['shifted decimal'][field],reports['declared decimal'][field],'constant shift does not change dispersion',True)
 ck('missing None rejected',rejects(lambda:m.describe([.02,None,-.01])),'ValueError','native missing policy, no imputation')
 ck('zero-fill changes mean',reports['missing omitted']['mean']!=reports['caller zero-filled']['mean'],True,'different caller observation sets/estimands')
 ck('describe accepts below−100% numeric observation',m.describe([-2,.1])['count'],2,'generic finite numeric summary is not unlevered-return domain acceptance')
 ck('compound rejects below−100%',rejects(lambda:m.compounded_return([-2,.1])),'ValueError','explicit unlevered simple-return contract')
 # Same empirical multiset, distinct temporal account paths. Source has no drawdown API.
 perms=sorted(set(itertools.permutations([F(-1,10)]*2+[F(1,10)]*2)));drawdowns=[];perm_records=[];base=m.describe(list(map(float,perms[0])))
 for i,x in enumerate(perms):
  values=list(map(float,x));ck('permutation'+str(i)+' whole summary',m.describe(values),base,'native summary discards order')
  ck('permutation'+str(i)+' cumulative',m.compounded_return(values),F(-199,10000),'exact product independent of order',True)
  ck('permutation'+str(i)+' geometric',m.geometric_mean_return(values),math.sqrt(.99)-1,'same gross-product geometric mean',True)
  wealth=F(1);peak=F(1);dd=F(0);wealth_path=[]
  for j,v in enumerate(x):
   wealth*=1+v;peak=max(peak,wealth);dd=max(dd,1-wealth/peak);wealth_path.append(str(wealth));ck(f'permutation{i} source prefix{j}',m.compounded_return(values[:j+1]),wealth-1,'native prefix product vs external account wealth',True)
  drawdowns.append(dd);perm_records.append(dict(returns=list(map(str,x)),wealth=wealth_path,external_max_drawdown=str(dd)))
 ck('external min drawdown',min(drawdowns),F(1,10),'exact temporal peak-to-wealth oracle');ck('external max drawdown',max(drawdowns),F(19,100),'summary equality does not establish equal temporal risk')
 models.append(dict(name='six orderings',paths=perm_records,scope='source summaries/products and supplemental account/drawdown calculation; no native temporal-risk field'))
 variances=[];sds=[];law=[]
 for i,x in enumerate(itertools.product([-.1,.1],repeat=2)):
  native=m.describe(list(x));ref=oracle(x)
  for field in ['mean','sample_variance','sample_sd','negative_fraction']:ck(f'IID pair{i} '+field,native[field],ref[field],'exact four-path fair-sign law',True)
  variances.append(F(str(native['sample_variance'])));sds.append(native['sample_sd']);law.append(dict(returns=x,summary=native))
 ck('IID expected sample variance',sum(variances)/4,F(1,100),'unbiased variance under this exact IID law')
 ck('IID expected sample SD',sum(sds)/4,rootq(F(1,50))/2,'sample SD not unbiased population SD.1',True)
 models.append(dict(name='two IID fair signs',path_weight='1/4',population_variance='1/100',population_sd='1/10',records=law,expected_sample_variance='1/100',expected_sample_sd='sqrt(1/50)/2',scope='explicit law, not arbitrary bias correction or real IID acceptance'))
 prior=json.loads((here.parent/'chapter-15-descriptive-review/results.json').read_text())
 ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'prior corrected source/failures retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source modification')
 ck('project no date field','date' in reports['declared decimal'],False,'native summary has no metadata/provenance contract')
r=dict(pin=pin,source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),rows=rows,commands=commands,fixtures=fixtures,reports=reports,models=models,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected descriptive measurement/order/finite-sampling assumptions; no data authenticity, forecasting, model/platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
