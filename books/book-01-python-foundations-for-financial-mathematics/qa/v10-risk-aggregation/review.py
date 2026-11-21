"""Equal-weight empirical VaR/ES underanexplicitjointlosslaw;notmarketcalibration."""
from pathlib import Path
from fractions import Fraction as F
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform,itertools
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='4e4dba9e89d0448ab378b6c6a1d8735bec198942';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.12-risk-simulation.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(listing)==1;rows=[];commands=[];cases=[]
def ck(name,got,want,kind='source numeric'):
 ok=got==want if type(want)in(bool,list) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=ok))
def reference(atoms,alpha):
 cumulative=F(0);var=None
 for x,p in sorted(atoms.items()):
  cumulative+=p
  if cumulative>=alpha:var=x;break
 above=sum(p for x,p in atoms.items() if x>var);numerator=sum(x*p for x,p in atoms.items() if x>var)+var*(1-alpha-above)
 return var,numerator/(1-alpha)
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'risk_simulation.py';p.write_text(listing[0]);spec=importlib.util.spec_from_file_location('risk_reference',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 paired=list(itertools.product([0]*24+[100],repeat=2));A=[x for x,y in paired];B=[y for x,y in paired];S=[x+y for x,y in paired];datasets={'A':(A,100,{F(0):F(24,25),F(100):F(1,25)}),'B':(B,100,{F(0):F(24,25),F(100):F(1,25)}),'combined':(S,200,{F(0):F(576,625),F(100):F(48,625),F(200):F(1,625)})}
 for name,(losses,initial,atoms) in datasets.items():
  terminals=[initial-x for x in losses];ck(name+' loss conversion',m.losses_from_values(initial,terminals),losses,'source list equality');ck(name+' loss frequency',m.loss_frequency(losses),sum(p for x,p in atoms.items() if x>0));result=[]
  for alpha in [.9,.95,.96,.99]:
   exact=F(str(alpha));v,e=reference(atoms,exact);gotv=m.nearest_rank_var(losses,alpha);gote=m.empirical_es(losses,alpha);ck(name+' VaR '+str(alpha),gotv,v);ck(name+' ES '+str(alpha),gote,e);ck(name+' reverse VaR '+str(alpha),m.nearest_rank_var(list(reversed(losses)),alpha),v,'source permutation');ck(name+' reverse ES '+str(alpha),m.empirical_es(list(reversed(losses)),alpha),e,'source permutation');result.append(dict(alpha=alpha,native_var=gotv,native_es=gote,exact_var=str(v),exact_es=str(e)))
  cases.append(dict(name=name,initial=initial,scenario_count=len(losses),atoms={str(x):str(p) for x,p in atoms.items()},levels=result))
 for i,alpha in enumerate([.9,.95,.96,.99]):
  av=cases[0]['levels'][i];bv=cases[1]['levels'][i];sv=cases[2]['levels'][i]
  ck('selected ES subadditivity '+str(alpha),sv['native_es']<=av['native_es']+bv['native_es'],True,'caller aggregate decision')
  ck('selected VaR non-subadditivity '+str(alpha),sv['native_var']>av['native_var']+bv['native_var'],alpha in [.95,.96],'caller aggregate decision')
result=dict(pin=pin,source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing[0].encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,cases=cases,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='625exactequal-weightjointstates,notsimulatedIIDpaths,ESuncertainty/modelapprovalorweightedAPI')
(here/((sys.argv[1] if len(sys.argv)>1 else 'first')+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],failed=result['failed'],level95=[r['levels'][1] for r in cases])));assert result['failed']==0
