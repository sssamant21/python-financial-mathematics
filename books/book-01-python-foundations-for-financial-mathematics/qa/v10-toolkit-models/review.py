"""Finite-law CI/tail diagnostics and external project-assumption disposition."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import re,sys,subprocess,tempfile,importlib.util,json,math,hashlib,platform,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='f77f274e9f0f601ad1b950097f38be188baecae5';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.14-chapter-project-financial-statistical-analysis-toolkit.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);fences=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S);listing=fences[0];rows=[];commands=[];laws=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
def variance(x):return sum((a-b)**2 for i,a in enumerate(x) for b in x[i+1:])/(len(x)*(len(x)-1))
def sqrt(x):
 with localcontext() as c:c.prec=100;return float((D(x.numerator)/D(x.denominator)).sqrt())
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'financial_statistics_toolkit.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('toolkit',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for name,paths in [('IID signs',list(itertools.product([-1,1],repeat=4))),('shared sign',[(-1,)*4,(1,)*4])]:
  covered=0;records=[]
  for i,signs in enumerate(paths):
   X=[F(s,10) for s in signs];x=list(map(float,X));mu=sum(X)/4;sd=sqrt(variance(X));ci=m.normal_mean_ci(x);half=1.959963984540054*sd/2
   ck(f'{name} path{i} mean',m.mean(x),mu,'native mean vs exact sign count',True);ck(f'{name} path{i} SD',m.sample_sd(x),sd,'pairwise-difference variance oracle',True)
   for j,v in enumerate([float(mu)-half,float(mu)+half]):ck(f'{name} path{i} CI{j}',ci[j],v,'fixed declared critical literal; not assumed distribution coverage',True)
   actual=ci[0]<=0<=ci[1];expected=abs(sum(signs))<4
   ck(f'{name} path{i} contains true mean',actual,expected,'enumerated exact sign pattern; extreme all-equal paths miss0');covered+=actual;records.append(dict(returns=x,ci=ci,covers_zero=actual))
  expected=F(7,8) if name=='IID signs' else F(0)
  ck(name+' native CI exact-law coverage',F(covered,len(paths)),expected,'uniform finite joint law; nominal95% not a coverage guarantee')
  laws.append(dict(name=name,weight='1/'+str(len(paths)),records=records,coverage=str(F(covered,len(paths))),true_mean='0',marginal='P(R=−.1)=P(R=.1)=1/2',scope='two specified joint laws; not empirical market coverage'))
 # Exact future strict exceedance probability for a disclosed four-point IID law.
 levels=[F(-1,5),F(-1,10),F(1,10),F(1,5)];exceeds=0;tail_records=[]
 for i,history in enumerate(itertools.product(levels,repeat=4)):
  tail=m.historical_tail(list(map(float,history)),.05);minimum=min(history)
  ck(f'tail history{i} count',tail['tail_count'],1,'ceil(.05*4)=1')
  ck(f'tail history{i} VaR',tail['var'],-minimum,'independent minimum rank under disclosed finite law',True);ck(f'tail history{i} ES',tail['es'],-minimum,'one-point worst-tail average',True)
  below=sum(v < F(str(-tail['var'])) for v in levels);exceeds+=below;tail_records.append(dict(history=list(map(str,history)),native_tail=tail,next_strict_exceedance_count=below))
 ck('IID future strict exceedance probability',F(exceeds,4**5),F(49,512),'sum_j p_j*P(R>r_j)^4=(81+16+1)/1024; ties excluded')
 ck('strict exceedance differs from requested .05',F(exceeds,4**5)!=F(1,20),True,'estimator rank/count is not a predictive calibration guarantee')
 laws.append(dict(name='IID four-point tails',levels=list(map(str,levels)),history_weight='1/256',next_weight='1/4',strict_exceedance=str(F(exceeds,1024)),records=tail_records,scope='fixed estimator/strict-tie convention; not a fitted distribution or predictive validation'))
 x=[-2,-1,1,2];y=[1+2*v for v in x];fit=m.ols(x,y)
 for k,v in dict(alpha=1,beta=2,r2=1,sse=0).items():ck('observational OLS '+k,fit[k],v,'same observable sample for X=U,Y=1+2X or X=U,Y=1+2U',True)
 ck('external intervention X=3 direct-model mean',F(7),7,'supplemental structural equation, no native causal API')
 ck('external intervention X=3 common-cause mean',sum(F(1+2*u) for u in x)/4,1,'supplemental U remains unchanged under do(X=3); identical observational fit does not identify mechanism')
 prior=json.loads((here.parent/'chapter-15-toolkit-review/results.json').read_text());ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F140/previous62 predicates and19 baseline failures retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source modification')
r=dict(pin=pin,source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),rows=rows,laws=laws,commands=commands,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Exact selected finite-law diagnostics; native CI/tail/OLS execution separate from probability-law aggregation and conceptual causal/project/data readiness review; no model/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
