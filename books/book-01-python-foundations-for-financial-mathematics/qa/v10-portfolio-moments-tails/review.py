"""Zero correlation andequalportfolio variance do notdetermine jointtail risk."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import subprocess,re,tempfile,importlib.util,json,math,sys,hashlib,platform,itertools
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='ad0f11b8eb295b0c062256a47d869044b874aa77';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.11-portfolio-simulation.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(listing)==1;rows=[];commands=[];cases=[]
def ck(name,got,want,kind='source summary'):
 ok=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=str(got) if isinstance(got,F) else got,expected=str(want),kind=kind,passed=ok))
def rootq(x):
 with localcontext() as c:c.prec=120;return (Decimal(x.numerator)/Decimal(x.denominator)).sqrt()
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'portfolio_simulation.py';p.write_text(listing[0]);spec=importlib.util.spec_from_file_location('portfolio_reference',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  r=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0
 a=F(2,5);marginal=[-a,*([F(0)]*6),a];independent=list(itertools.product(marginal,repeat=2));dependent=[pair for pair in itertools.product([-a,a],repeat=2) for _ in range(4)]+[(F(0),F(0))]*48
 analytical=m.analytical(0,0,.2,.2,0,.5,.5);ck('native analytical mean',analytical[0],0,'analytical source');ck('native analytical variance',analytical[1],F(1,50),'analytical source')
 for name,pairs,loss,severe,crossfourth in [('independent',independent,F(13,64),F(1,64),F(1,625)),('same_abs_dependent',dependent,F(1,16),F(1,16),F(4,625))]:
  n=len(pairs);portfolio=[(x+y)/2 for x,y in pairs];data=[(float(x),float(y),float(rp)) for (x,y),rp in zip(pairs,portfolio)];result=m.summarize(data,100)
  facts={'mean1':sum(x for x,y in pairs)/n,'mean2':sum(y for x,y in pairs)/n,'variance1':sum(x*x for x,y in pairs)/n,'variance2':sum(y*y for x,y in pairs)/n,'covariance':sum(x*y for x,y in pairs)/n,'portfolio_variance':sum(x*x for x in portfolio)/n,'cross_fourth_moment':sum(x*x*y*y for x,y in pairs)/n}
  for k,w in [('mean1',0),('mean2',0),('variance1',F(1,25)),('variance2',F(1,25)),('covariance',0),('portfolio_variance',F(1,50)),('cross_fourth_moment',crossfourth)]:ck(name+' '+k,facts[k],w,'exact finite-model moment')
  var=F(1,50)*F(n,n-1);expected=dict(count=64,mean_return=0,return_sd=rootq(var),mean_terminal=100,standard_error_terminal=100*rootq(var/n),loss_frequency=loss,paths_with_asset_return_below_minus_one=0)
  for k,w in expected.items():ck(name+' '+k,result[k],w)
  tail=F(sum(x< -F(3,10) for x in portfolio),n);ck(name+' caller severe loss frequency',tail,severe,'caller tail indicator');cases.append(dict(name=name,rows=data,summary=result,moments={k:str(v) for k,v in facts.items()},severe_return_threshold='-3/10',severe_loss_frequency=str(tail)))
result=dict(pin=pin,source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing[0].encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,cases=cases,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='finitecaller jointlaws,notsourceGaussian sampler/independence/validSEcertification')
(here/((sys.argv[1] if len(sys.argv)>1 else 'first')+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],failed=result['failed'])));assert result['failed']==0
