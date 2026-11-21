"""Selected project report/risk/stream integration; deterministic exact oracles."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform,itertools
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='ce38a04197aef40afd31e54adbb8d0bdadc588a3';base='books/book-01-python-foundations-for-financial-mathematics/chapter-18/';rows=[];commands=[];manifest={}
def ck(name,got,want,kind):
 ok=got==want if isinstance(want,(list,bool)) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=ok))
def risk(losses,alpha):
 # Atom masses/CDF and upper-tail probability, distinct from sorted observation-equivalents.
 atoms={x:F(losses.count(x),len(losses)) for x in set(losses)};cdf=F(0)
 for var,p in sorted(atoms.items()):
  cdf+=p
  if cdf>=alpha:break
 tail=sum(p for x,p in atoms.items() if x>var);es=(sum(x*p for x,p in atoms.items() if x>var)+var*(1-alpha-tail))/(1-alpha)
 return var,es
with tempfile.TemporaryDirectory() as tmp:
 modules=[]
 for file,name in [('18.14-chapter-project-monte-carlo-financial-simulator.md','project'),('18.12-risk-simulation.md','risk'),('18.13-computational-performance.md','performance')]:
  path=base+file;raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S)[0];manifest[path]=dict(source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest());p=Path(tmp)/(name+'.py');p.write_text(listing);spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);modules.append(m)
 project,risk_source,performance=modules
 for args in [[sys.executable,'project.py'],[sys.executable,'-m','compileall','-q','.']]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for i,values in enumerate(itertools.product([80,100,120],repeat=4)):
  losses=[100-x for x in values];mean=F(sum(values),4);variance=sum((F(x)-mean)**2 for x in values)/3
  ck(str(i)+' loss conversion',project.losses_from_values(100,values),losses,'native list vs caller subtraction')
  for alpha in [.625,.75,.96]:
   report=project.report(iter(values),100,alpha);v,e=risk(losses,F(str(alpha)));expected=dict(count=4,mean_terminal=mean,sample_sd=math.sqrt(float(variance)),standard_error_mean=math.sqrt(float(variance/4)),loss_frequency=F(sum(x>0 for x in losses),4),alpha=alpha,var_nearest_rank=v,es_fractional_tail=e)
   for key,want in expected.items():ck(str(i)+' '+str(alpha)+' '+key,report[key],want,'project field vs independent atom/moment oracle')
   for key,got in [('var_nearest_rank',risk_source.nearest_rank_var(losses,alpha)),('es_fractional_tail',risk_source.empirical_es(losses,alpha))]:ck(str(i)+' '+str(alpha)+' sibling '+key,report[key],got,'native sibling agreement, not independent oracle')
 for count in [20,101,1000]:
  values=project.sample_values(count,42);report=project.report(values,100,.75);stream=performance.streaming_run(count,42)
  ck('stream count '+str(count),report['count'],stream.count,'native project/stream agreement');ck('stream mean '+str(count),report['mean_terminal'],stream.mean,'native project/stream agreement');ck('stream SE '+str(count),report['standard_error_mean'],stream.standard_error(),'native project/stream agreement')
prior=json.loads((root/'books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-project-review/results.json').read_text());identity=prior.get('source_sha256');assert identity==next(iter(manifest.values()))['source_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),manifest=manifest,prior_project_source_identity=identity,rows=rows,commands=commands,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='81 deterministic length-four paths; selected serial project/risk/stream agreement; no IID coverage/model/integration acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
