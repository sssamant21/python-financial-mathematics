"""Local-window compounding versus account wealth, window policies and project timing."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='5c543db206151d5be9eb609a6e5e4fb5fe5e377b';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.12-rolling-statistics.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'rolling_statistics.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('rolling_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for i,R in enumerate(itertools.product([F(-1),F(0),F(1,10)],repeat=4)):
  for w in [2,3]:
   got=m.rolling_compounded_return(list(map(float,R)),w)
   for j,v in enumerate(got):ck(f'path{i} w{w} end{j+w}',v,math.prod((1+r for r in R[j:j+w]),start=F(1))-1,'native local-window return vs exact fresh-capital gross product',True)
 r=[.1,-1,.1,.1];local=m.rolling_compounded_return(r,2);global_wealth=[];wealth=F(1)
 for v in r:wealth*=1+F(str(v));global_wealth.append(str(wealth))
 ck('bankruptcy local first window',local[0],-1,'native local window includes total loss')
 ck('bankruptcy local second window',local[1],-1,'native local window includes total loss')
 ck('later fresh-capital local window',local[2],F(21,100),'native local window after loss is excluded',True)
 ck('supplemental global account stays zero',global_wealth,['11/10','0','0','0'],'exact global account convention, not native account API')
 values=[1,1,1,9];rolling=m.rolling_mean(values,3);expanding=[m.rolling_mean(values[:j],j)[0] for j in range(1,5)]
 ck('fixed rolling final mean',rolling[-1],F(11,3),'native fixed-window excludes earliest observation',True)
 ck('caller expanding-prefix final mean',expanding[-1],3,'source full-prefix means assembled by caller')
 ck('expanding prefix path',expanding,[1.,1.,1.,3.],'caller expanding assembly, no exported expanding API')
 lag=m.lagged_signal(rolling);ck('compressed output lag',lag,[None,1.],'native output-position lag')
 A=[.01]*10+[.01,-.01]*5+[.04,-.04]*5;B=[.005,-.005]*5+[.02,-.02]*10;prior=json.loads((here.parent/'chapter-15-rolling-review/results.json').read_text());fixture=hashlib.sha256(json.dumps([A,B]).encode()).hexdigest();ck('prescribed project fixture hash',fixture,prior['project_report']['fixture_sha256'],'synthetic project provenance')
 for w in [5,10,20]:
  base=m.rolling_mean(A,w);changed=m.rolling_mean(A[:20]+[99]*10,w);end_labels=list(range(w,31));cut=sum(e<=20 for e in end_labels)
  ck('project future exclusion w'+str(w),base[:cut],changed[:cut],'native trailing-array cutoff; caller availability labels')
  ck('project first full-window label w'+str(w),list(zip(end_labels,base))[0][0],w,'caller full-window end mapping')
 models.append(dict(name='local/global wealth distinction',returns=r,native_local_windows=local,supplemental_global_wealth=global_wealth,scope='A fresh unit of wealth at each local window versus one unlevered account starting before the loss. No replenishment/global-account API or bankruptcy recovery claim.'))
 models.append(dict(name='window/project policy',fixed_window=3,rolling_means=rolling,caller_expanding=expanding,project_fixture_sha256=fixture,project_labels=list(range(1,31)),dates=None,mean_cutoff_label=20,scope='Warm-up/end labels supplied externally. EWMA recursion remains conceptual with no native implementation; actual calendars, publication delay, orders and costs unaccepted.'))
assert hashlib.sha256(raw).hexdigest()==prior['source_sha256'];assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Selected local-window/account and window/project assumptions; global account/expanding assembly/timestamp maps are caller oracles, no financial execution/model/platform acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
