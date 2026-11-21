"""Remaining Section18.15 path/portfolio/risk/storage/stress arithmetic crosswalk."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='99b03b4ce334912f4731ee730d8fbdf60f06bb6a';base='books/book-01-python-foundations-for-financial-mathematics/chapter-18/';rows=[];commands=[];manifest={}
def ck(name,got,want,kind='native exact-source field'):
 ok=got==want if isinstance(want,(bool,list)) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 mods=[]
 for filename,name in [('18.06-price-path-simulation.md','paths'),('18.11-portfolio-simulation.md','portfolio'),('18.12-risk-simulation.md','risk'),('18.13-computational-performance.md','performance')]:
  raw=subprocess.check_output(['git','show',pin+':'+base+filename],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S)[0];manifest[base+filename]=dict(source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest());p=Path(tmp)/(name+'.py');p.write_text(listing);spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);mods.append(m)
 paths,portfolio,risk,performance=mods
 for name in ['paths','portfolio','risk','performance']:
  args=[sys.executable,name+'.py'];z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 args=[sys.executable,'-m','compileall','-q','.'];z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 ck('31 time step',F(1,12),1/12,'caller dimensional arithmetic')
 ck('32 log drift',F('.05')-F('.2')**2/2,F('.03'),'caller model arithmetic')
 with localcontext() as ctx:
  ctx.prec=100;x=D('.05');term=total=D(1)
  for k in range(1,100):term*=x/k;total+=term
  ck('33 GBM expectation',paths.expected_terminal(100,.05,1),total*100)
 ck('34 coarse barrier misses selected crossing',paths.observed_barrier_hit([100,100],90),False)
 ck('34 refined selected path hits barrier',paths.observed_barrier_hit([100,80,100],90),True)
 mean,var=portfolio.analytical(.1,-.05,0,0,0,.6,.4);ck('35 portfolio return',mean,F('.04'));ck('35 deterministic variance',var,0)
 mean,var=portfolio.analytical(0,0,.2,.1,.25,.6,.4);ck('36 portfolio variance',var,F(184,10000));ck('36 centered model mean',mean,0)
 ck('37 drifted first weight',F(60)*F('1.1')/104,F(33,52),'caller buy-and-hold arithmetic')
 ck('37 first weight changed',F(33,52)!=F('.6'),True,'caller buy-and-hold decision')
 ck('38 down/up loss',risk.losses_from_values(100,[80,110]),[20,-10])
 losses=[-10,0,20,40]
 ck('39 nearest rank VaR',risk.nearest_rank_var(losses,.75),20)
 ck('40 empirical ES',risk.empirical_es(losses,.75),40)
 ck('41 fractional ES',risk.empirical_es(losses,.625),F(100,3))
 v=risk.nearest_rank_var(losses,.8);ck('42 discrete VaR',v,40)
 ck('42 strict exceedance probability',F(sum(x>v for x in losses),4),0,'caller atom probability')
 ck('42 exceedance differs from nominal tail',F(sum(x>v for x in losses),4)!=F('.2'),True,'caller discrete-tail decision')
 ck('43 element storage',performance.array_bytes(100000,253,8),202400000)
 ck('43 MiB',performance.array_bytes(100000,253,8)/(2**20),F(202400000,2**20),'caller unit conversion')
 partition=[10000]*10+[1];ck('44 caller partition sum',sum(partition),100001,'caller partition arithmetic');ck('44 caller final partial batch',partition[-1],1,'caller partition arithmetic')
 stream=performance.streaming_run(100001,42);batched=performance.run_batches(100001,10000,42)
 ck('44 native batch count',batched.count,100001);ck('44 same serial stream state',batched==stream,True)
 mean,var=portfolio.analytical(-.2,-.1,0,0,0,.6,.4);ck('47 stress return',mean,F('-.16'));ck('47 stress loss',risk.losses_from_values(100,[84]),[16])
 ck('48 base USD value',F(100)*F('1.1'),110,'caller FX quote arithmetic');ck('48 new USD value',F(100)*F('1.05'),105,'caller FX quote arithmetic');ck('48 USD profit',F(100)*(F('1.05')-F('1.1')),-5,'caller FX quote arithmetic')
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),manifest=manifest,rows=rows,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='remaining Section18.15 selected exercise contracts; not full V10/book/model/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
