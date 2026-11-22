"""Four exact manuscript listings sharing the toolkit CSV; external integration oracle."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import re,sys,subprocess,tempfile,importlib.util,json,math,hashlib,platform
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='4d32cafb9c9d97c9d3d3b4b81d3ef387bfd71ec4';book='books/book-01-python-foundations-for-financial-mathematics';rows=[];commands=[];sources={};mods={}
def ck(name,got,want,kind,approx=False):
 ok=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want
 rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=ok))
def sqrt(x):
 with localcontext() as c:c.prec=100;return float((D(x.numerator)/D(x.denominator)).sqrt())
def variance(x):return sum((a-b)**2 for i,a in enumerate(x) for b in x[i+1:])/(len(x)*(len(x)-1))
def rejects(fn):
 try:fn()
 except ValueError:return 'ValueError'
 return 'accepted'
with tempfile.TemporaryDirectory() as tmp:
 for num,name in [('11','returns'),('12','rolling'),('13','pitfalls'),('14','financial_statistics_toolkit')]:
  path=next((root/book/'chapter-15').glob('15.'+num+'-*.md')).relative_to(root).as_posix();raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);fences=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S);listing=fences[0];p=Path(tmp)/(name+'.py');p.write_text(listing);spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);mods[num]=m;sources[num]=dict(path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest())
  z=subprocess.run([sys.executable,p.name],cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=[sys.executable,p.name],returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
  if num=='14':
   csv=re.findall(r'^```csv\n(.*?)^```',raw.decode(),re.M|re.S)[0];(Path(tmp)/'prices.csv').write_text(csv);(Path(tmp)/'csv_usage.py').write_text(fences[1])
 for args in [[sys.executable,'csv_usage.py'],[sys.executable,'-m','compileall','-q','.']]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 ret,rolling,pit,kit=[mods[n] for n in ['11','12','13','14']];dates,asset,bench=kit.load_prices_csv(Path(tmp)/'prices.csv');ck('dates match exact fixture',dates,['2026-01-05','2026-01-06','2026-01-07','2026-01-08','2026-01-09'],'native loader vs source CSV')
 # Oracle uses exact price ratios, then declared displayed-decimal report boundary.
 for label,prices in [('asset',asset),('benchmark',bench)]:
  exact_returns=[F(prices[i],prices[i-1])-1 for i in range(1,len(prices))]
  for mod in [ret,kit]:
   for i,v in enumerate(mod.simple_returns(prices)):ck(f'{label} {mod.__name__} return{i}',v,exact_returns[i],'source returns vs rational endpoint ratio',True)
 a=kit.simple_returns(asset);b=kit.simple_returns(bench);A=list(map(lambda v:F(str(v)),a));B=list(map(lambda v:F(str(v)),b));n=len(A);ma=sum(A)/n;mb=sum(B)/n;va=variance(A);vb=variance(B);cov=(sum(x*y for x,y in zip(A,B))-sum(A)*sum(B)/n)/(n-1);slope=cov/vb;alpha=ma-slope*mb;report=kit.report(asset,bench,2)
 expectations={'observations':n,'mean_return':ma,'volatility':sqrt(va),'cumulative_return':math.prod((1+x for x in A),start=F(1))-1,'correlation':float(cov)/sqrt(va*vb)}
 for k,v in expectations.items():ck('report '+k,report[k],v,'native report vs independent pairwise/raw-product oracle',True)
 for k,v in {'alpha':alpha,'beta':slope,'sse':(n-1)*(va-cov*cov/vb),'r2':cov*cov/(va*vb)}.items():ck('regression '+k,report['regression'][k],v,'native OLS vs covariance identities, SSE from explained sum of squares',True)
 half=1.959963984540054*sqrt(va/n)
 for i,v in enumerate([float(ma)-half,float(ma)+half]):ck('CI endpoint'+str(i),report['normal_ci_approx'][i],v,'declared normal critical literal; no normal-model coverage claim',True)
 ordered=sorted(A);ck('tail count',report['historical_tail']['tail_count'],1,'ceil(.05*4)=1');ck('signed VaR',report['historical_tail']['var'],-ordered[0],'independent sorted rank',True);ck('signed ES',report['historical_tail']['es'],-ordered[0],'one-point tail mean',True)
 ck('cross mean return',ret.arithmetic_mean(a),kit.mean(a),'same supplied return vector',True);ck('cross sample volatility',ret.sample_volatility(a),kit.sample_sd(a),'same supplied return vector',True);ck('cross cumulative',ret.cumulative_return(a),kit.compounded(a),'same supplied return vector',True);ck('cross pitfall mean',pit.sample_mean(a),ma,'shared fixture vs independent rational mean',True)
 for w in [1,2,3,4]:
  oracle=[sum(A[i:i+w])/w for i in range(n-w+1)]
  for name,values in [('rolling',rolling.rolling_mean(a,w)),('toolkit',kit.rolling_mean(a,w))]:
   ck(f'{name} w{w} length',len(values),n-w+1,'window ending positions')
   for i,v in enumerate(values):ck(f'{name} w{w} mean{i}',v,oracle[i],'native means vs independent exact slices',True)
  for i,v in enumerate(rolling.rolling_compounded_return(a,w)):ck(f'rolling compound w{w} i{i}',v,math.prod((1+x for x in A[i:i+w]),start=F(1))-1,'native window product vs exact gross product',True)
  if w>=2:
   for i,v in enumerate(rolling.rolling_sample_std(a,w)):ck(f'rolling SD w{w} i{i}',v,sqrt(variance(A[i:i+w])),'independent pairwise-difference variance',True)
   for i,v in enumerate(pit.overlapping_returns(a,w)):ck(f'pitfall overlap w{w} i{i}',v,rolling.rolling_compounded_return(a,w)[i],'same positional windows across source modules',True)
 for scale_a,scale_b in [(10,1),(1,10),(10,10)]:
  transformed=kit.report([x*scale_a for x in asset],[x*scale_b for x in bench],2)
  ck(f'positive currency/unit scaling {scale_a},{scale_b}',transformed,report,'identical returns under integer positive price rescaling; no FX/adjustment adapter')
 for tail in [.05,.25,.5,.75]:
  t=kit.historical_tail(a,tail);k=math.ceil(F(str(tail))*n)
  ck(f'tail {tail} count',t['tail_count'],k,'same shared sample/discrete rank')
  ck(f'tail {tail} VaR cross',t['var'],ret.historical_var(a,tail),'same declared signed rank',True);ck(f'tail {tail} ES cross',t['es'],ret.historical_expected_shortfall(a,tail),'same declared worst-k mean',True)
 # Numeric-only API cannot detect mismatched session labels; do not invent joins.
 shifted=bench[1:]+bench[:1];shift_report=kit.report(asset,shifted)
 ck('same-length mispaired benchmark accepted',shift_report['observations'],4,'native length check; caller-shifted benchmark is NOT aligned-data acceptance')
 ck('mispaired correlation differs',shift_report['correlation']!=report['correlation'],True,'positional-pair sensitivity')
 ck('native report has no timestamp field','dates' in report,False,'metadata remains external caller provenance')
 for name,fn in [('rolling',lambda:rolling.rolling_correlation([1,1,1],[1,2,3],3)),('toolkit',lambda:rejects(lambda:kit.pearson([1,1,1],[1,2,3])))]:ck(name+' constant dependence',fn(),[None] if name=='rolling' else 'ValueError','different documented missing/undefined contracts; adapter required')
 ck('constant-return combined report fails',rejects(lambda:kit.report([100,200,400,800],[100,200,400,800])),'ValueError','native report is fail-fast, not a partial-report API')
 prior=json.loads((here.parent/'chapter-15-toolkit-review/results.json').read_text());ck('toolkit prior whole-source identity',sources['14']['source_sha256'],prior['source_sha256'],'F140 corrected manuscript retained');ck('toolkit prior listing identity',sources['14']['listing_sha256'],prior['listing_sha256'],'prior failures/62 predicates retained');fixture_sha=hashlib.sha256(csv.encode()).hexdigest()
r=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),sources=sources,fixture_sha256=fixture_sha,dates=dates,prices=dict(asset=asset,benchmark=bench),report=report,rows=rows,commands=commands,python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected four-section shared synthetic fixture, arithmetic/report/undefined contracts. External orchestrator, no native timestamp join/model/platform/bookwide integration acceptance.')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
