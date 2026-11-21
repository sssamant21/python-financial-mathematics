"""Exact counterexample: first two empirical moments do not determine VaR."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='278fe361a26394ce4d2c5d1e1955d804994e150a';base='books/book-01-python-foundations-for-financial-mathematics/chapter-18/';rows=[];manifest={};commands=[]
def ck(name,got,want):
 ok=got==want if isinstance(want,bool) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=got,expected=str(want),passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 mods=[]
 for filename,name in [('18.15-exercises-and-applied-problems.md','exercises'),('18.14-chapter-project-monte-carlo-financial-simulator.md','project'),('18.13-computational-performance.md','performance')]:
  raw=subprocess.check_output(['git','show',pin+':'+base+filename],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S)[0];manifest[base+filename]=dict(source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest());p=Path(tmp)/(name+'.py');p.write_text(listing);spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);mods.append(m)
 snippet,project,performance=mods
 for argv in [[sys.executable,'exercises.py'],[sys.executable,'-m','compileall','-q','.']]:
  r=subprocess.run(argv,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0
 xs=snippet.values;n=len(xs);mean=F(sum(xs),n);v=sum((F(x)-mean)**2 for x in xs)/(n-1)
 ck('exact snippet mean',snippet.mean,mean);ck('exact snippet SE',snippet.se,math.sqrt(float(v/n)))
 datasets=[[98]+[100]*6+[102],[99]*4+[101]*4];states=[]
 for i,xs in enumerate(datasets):
  stats=performance.RunningStats()
  for x in xs:stats.update(x)
  ck(str(i)+' count',stats.count,8);ck(str(i)+' mean',stats.mean,100);ck(str(i)+' M2',stats.m2,8);ck(str(i)+' variance',stats.sample_variance(),F(8,7));ck(str(i)+' SE',stats.standard_error(),math.sqrt(1/7))
  states.append(stats)
  for alpha,wantv,wante in [(.75,0 if i==0 else 1,1),(.9,2 if i==0 else 1,2 if i==0 else 1)]:
   out=project.report(xs,100,alpha);ck(str(i)+' VaR '+str(alpha),out['var_nearest_rank'],wantv);ck(str(i)+' ES '+str(alpha),out['es_fractional_tail'],wante)
 ck('same running moments within arithmetic tolerance',all(math.isclose(getattr(states[0],k),getattr(states[1],k),rel_tol=5e-14,abs_tol=1e-12) for k in ['mean','m2']),True)
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),manifest=manifest,rows=rows,commands=commands,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Exercise45 only plus exact snippet arithmetic; no complete Section18.15 acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
