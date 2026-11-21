"""Finite paired-unit uncertainty laws, Exercise46; boundary observation,49."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform,itertools
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='3a9dddb78f225bef1cd59241f28ea8d5e0a87744';base='books/book-01-python-foundations-for-financial-mathematics/chapter-18/';rows=[];commands=[];manifest={};laws=[]
def ck(name,got,want,kind):
 ok=got==want if isinstance(want,bool) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 mods=[]
 for filename,name in [('18.08-monte-carlo-estimation.md','estimation'),('18.10-confidence-and-simulation-error.md','confidence')]:
  raw=subprocess.check_output(['git','show',pin+':'+base+filename],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S)[0];manifest[base+filename]=dict(source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest());p=Path(tmp)/(name+'.py');p.write_text(listing);spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);mods.append(m)
 estimation,confidence=mods
 for args in [[sys.executable,'estimation.py'],[sys.executable,'confidence.py'],[sys.executable,'-m','compileall','-q','.']]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for name,atoms,cov,var_d in [('positive',[(90,90),(110,110)],100,0),('negative',[(90,110),(110,90)],-100,400),('independent',list(itertools.product([90,110],repeat=2)),0,200)]:
  count=len(atoms);paths=list(itertools.product(atoms,repeat=3));p=F(1,len(paths));exact_mse=F(0);native_se2=0.0;naive_se2=0.0
  ck(name+' exact covariance',sum(F((a-100)*(b-100),count) for a,b in atoms),cov,'exact caller joint-law moment')
  ck(name+' exact difference variance',sum(F((a-b)**2,count) for a,b in atoms),var_d,'exact caller joint-law moment')
  for i,path in enumerate(paths):
   A=[x for x,y in path];B=[y for x,y in path];D=[x-y for x,y in path]
   stats=[]
   for label,xs in [('A',A),('B',B),('D',D)]:
    mean=F(sum(xs),3);v=sum((F(x)-mean)**2 for x in xs)/2;got=estimation.estimate_mean(xs);stats.append(got)
    for key,want in [('count',3),('mean',mean),('sample_sd',math.sqrt(float(v))),('standard_error',math.sqrt(float(v/3)))]:ck(name+' '+str(i)+' '+label+' '+key,got[key],want,'native summary vs exact centered moments')
   exact_mse+=p*F(sum(D),3)**2;native_se2+=float(p)*stats[2]['standard_error']**2;naive_se2+=float(p)*(stats[0]['standard_error']**2+stats[1]['standard_error']**2)
  ck(name+' exact paired mean variance',exact_mse,F(var_d,3),'exact weighted IID-pair enumeration')
  ck(name+' expected native paired SE squared',native_se2,F(var_d,3),'weighted native estimate vs exact model')
  ck(name+' expected naive independent SE squared',naive_se2,F(200,3),'weighted caller misuse reference')
  laws.append(dict(name=name,atoms=atoms,paths=len(paths),pair_units=3,covariance=cov,difference_variance=var_d,paired_mean_variance=str(F(var_d,3)),naive_independent_variance=str(F(200,3))))
 # A fixed zero-event observation is not a claim that Bernoulli p=0.
 lo,hi=confidence.wilson_interval(0,100)
 ck('zero-event Wilson lower',lo,0,'native boundary interval')
 ck('zero-event Wilson upper',hi,F('1.96')**2/(100+F('1.96')**2),'native boundary interval vs score root')
 for probability in [F(1,100),F(1,20),F(1,4)]:
  mass=(1-probability)**100;ck('no-event mass positive p'+str(probability),mass>0,True,'exact caller binomial mass');laws.append(dict(bernoulli_p=str(probability),zero_events_probability=str(mass)))
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),manifest=manifest,rows=rows,laws=laws,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Exercises46/49 finite IID-pair and boundary counterexamples; not normal-interval coverage or independent/model acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
