"""Exact selected rank laws, sign transformation and exposure-weight assumptions."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,subprocess,tempfile,importlib.util,json,math,hashlib,platform,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='3394dadd805cd683c35c4e1232df2b7a1b01aff9';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.02-mean-median-and-quantiles.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
def oracle(x,p):
 ordered=sorted(x);h=(len(x)-1)*p;i=h.numerator//h.denominator;w=h-i
 return ordered[i] if not w else ordered[i]*(1-w)+ordered[i+1]*w
with tempfile.TemporaryDirectory() as tmp:
 pth=Path(tmp)/'mean_median_quantiles.py';pth.write_text(listing);spec=importlib.util.spec_from_file_location('quantiles',pth);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,pth.name],[sys.executable,'-m','compileall','-q',pth.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 levels=[F(-1,5),F(-1,10),F(1,10),F(1,5)];probs=[F(1,20),F(1,4),F(1,2),F(3,4),F(19,20)];type7breaches=nearestbreaches=0
 for i,history in enumerate(itertools.product(levels,repeat=3)):
  x=list(map(float,history));o=sorted(history);quantiles={}
  for p in probs:
   q=m.quantile_type7(x,float(p));nr=m.nearest_rank_quantile(x,float(p));want=oracle(history,p);rank=(3*p.numerator+p.denominator-1)//p.denominator
   ck(f'history{i} p{p} type7',q,want,'independent rational barycentric order-statistic oracle',True);ck(f'history{i} p{p} nearest',nr,o[rank-1],'independent integer ceiling rank',True)
   loss=m.quantile_type7([-100000*v for v in x],float(1-p));ck(f'history{i} p{p} type7 loss map',loss,-100000*want,'type7 negative scale reflects probability, displayed-decimal policy',True)
   quantiles[str(p)]=dict(type7=q,nearest=nr)
   if p==F(1,20):type7breaches+=sum(v<F(str(q)) for v in levels);nearestbreaches+=sum(v<F(str(nr)) for v in levels)
  records.append(dict(returns=list(map(str,history)),quantiles=quantiles))
 ck('type7 future strict breach probability',F(type7breaches,256),F(39,128),'exact IID four-point law:sum_z[U(z)^3+3p(z)U(z)^2]/4;small.05 interpolation stays below next level')
 ck('nearest future strict breach probability',F(nearestbreaches,256),F(9,64),'exact IID law:sum_z U(z)^3/4;strict ties excluded')
 x=[0,10,20,30];ck('type7 negative-scale identity',m.quantile_type7([-v for v in x],.75),-m.quantile_type7(x,.25),'linear quantile interpolation preserves reflection')
 ck('nearest-rank reflection can differ',m.nearest_rank_quantile([-v for v in x],.75)!=-m.nearest_rank_quantile(x,.25),True,'ceil rank at discrete boundary does not obey naive negative reflection')
 values=[.02,.08];weights=[F(3,4),F(1,4)];gross=sum(w*(1+F(str(v))) for w,v in zip(weights,values));end_weights=[w*(1+F(str(v)))/gross for w,v in zip(weights,values)]
 for label,w in [('start',weights),('ending',end_weights),('rescaled',[10*v for v in weights])]:ck('source weighted '+label,m.weighted_mean(values,list(map(float,w))),sum(F(str(v))*q for v,q in zip(values,w))/sum(w),'native arithmetic of caller exposures,not timestamp/portfolio validation',True)
 ck('ending differs from beginning exposures',m.weighted_mean(values,list(map(float,end_weights)))!=m.weighted_mean(values,list(map(float,weights))),True,'different caller weight semantics;no native holdings adapter')
 original=[-.04,-.01,0,.02,.08];stress=[-.04,-.01,0,.02,.28];trim=[.01,.02,.03,.20]
 ck('stress mean change',m.arithmetic_mean(stress)-m.arithmetic_mean(original),F(1,25),'replacement changes mean4 percentage points',True);ck('stress median unchanged',m.median(stress),m.median(original),'order statistic robustness for this fixture,not arbitrary contamination')
 ck('trimmed location',m.trimmed_mean(trim,1),F(1,40),'caller one-per-side selection',True);ck('untrimmed location retained',m.arithmetic_mean(trim),F(13,200),'unadjusted estimate remains distinct',True)
 ck('project type7 loss95',m.quantile_type7([-100000*v for v in original],.95),3400,'native transformed finite sample,not forecast',True)
 prior=json.loads((here.parent/'chapter-15-quantiles-review/results.json').read_text())
 ck('prior source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'prior F128 evidence retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),rows=rows,commands=commands,law=dict(levels=list(map(str,levels)),history_weight='1/64',next_weight='1/4',histories=records,type7_strict_breach='39/128',nearest_strict_breach='9/64'),exposure_model=dict(begin=list(map(str,weights)),end=list(map(str,end_weights)),gross=str(gross),scope='same-period hypothetical buy-hold exposures,not native corporate-action/calendar/holdings integration'),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected rank/selection/exposure law;source outputs separate from external next-draw probabilities;no data/model/platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
