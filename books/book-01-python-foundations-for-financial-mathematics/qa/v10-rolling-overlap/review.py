"""Finite IID rolling-mean overlap covariance and output-position timing."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='56ed4b707947235643686a472fb6e5b860199cee';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.12-rolling-statistics.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'rolling_statistics.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('rolling_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 triples=[];pairs=[]
 for i,x in enumerate(itertools.product([-1,1],repeat=4)):
  a=m.rolling_mean(list(x),3);b=m.rolling_mean(list(x),2);triples.append(a);pairs.append(b)
  for j,w in enumerate([F(x[0]+x[1]+x[2],3),F(x[1]+x[2]+x[3],3)]):ck(f'path{i} overlapping mean{j}',a[j],w,'native trailing mean vs exact window sum',True)
  for j in range(3):ck(f'path{i} pair mean{j}',b[j],F(x[j]+x[j+1],2),'native trailing mean vs exact two-point sum',True)
 def covariance(values,i,j):
  a=[F(v[i]) for v in values];b=[F(v[j]) for v in values];ma=sum(a)/len(a);mb=sum(b)/len(b);return sum((x-ma)*(y-mb) for x,y in zip(a,b))/len(a)
 ck('three-window first variance',covariance(triples,0,0),F(1,3),'native means weighted over exact IID signs vs coefficient variance',True)
 ck('three-window second variance',covariance(triples,1,1),F(1,3),'native means weighted over exact IID signs vs coefficient variance',True)
 ck('adjacent three-window covariance',covariance(triples,0,1),F(2,9),'two shared independent observations each coefficient1/3',True)
 ck('nonoverlap pair covariance',covariance(pairs,0,2),F(0),'disjoint-window independence under declared IID signs',True)
 ck('adjacent pair covariance',covariance(pairs,0,1),F(1,4),'one shared observation each coefficient1/2',True)
 values=[1,2,3,4];means=m.rolling_mean(values,2);mutated=m.rolling_mean([1,2,3,400],2)
 ck('future perturbation preserves earlier means',means[:2],mutated[:2],'caller cutoff index, not timestamp availability')
 ck('last-only perturbation effect',mutated[-1]-means[-1],198,'source trailing-window dependency')
 ck('native means paired to supplied end labels',list(zip([1,2,8,10][1:],means)),[(2,1.5),(8,2.5),(10,3.5)],'caller end-label mapping of native array; no timestamp guard')
 ck('lag is one output position',m.lagged_signal(means),[None,1.5,2.5],'native positional lag, not elapsed/trading-time execution')
 models.append(dict(name='four independent fair signs',paths=16,weight='1/16',underlying_variance=1,three_window_covariance='2/9',three_window_variance='1/3',three_window_correlation='2/3',adjacent_two_window_covariance='1/4',disjoint_two_window_covariance='0',native_three_means=triples,native_two_means=pairs,scope='Exact finite IID law; correlation2/3 is caller covariance ratio, not a native rolling-correlation call'))
 models.append(dict(name='irregular labels and output mapping',source_labels=[1,2,8,10],window=2,end_labels=[2,8,10],source_means=means,lagged=m.lagged_signal(means),scope='Caller labels only; native arrays have no calendar/availability/execution guarantee'))
prior=json.loads((here.parent/'chapter-15-rolling-review/results.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['source_sha256'];assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Selected rolling-mean overlap and positional timing under finite IID signs; rolling SD/correlation/compounded and broader selection/data/execution contracts unfinished')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
