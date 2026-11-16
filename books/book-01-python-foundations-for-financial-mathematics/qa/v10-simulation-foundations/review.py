"""Exact pinned Section18.1 plus exhaustive four-draw IID/dependent model references.
Usage: python THIS first|replay
"""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,itertools,math
from fractions import Fraction as F
here=Path(__file__).resolve().parent;root=here.parents[3];pin='3a7a9f6df3ca6210ebe50504ed8f7324b5057320';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.01-simulation-fundamentals.md';stem=sys.argv[1]
raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);code=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S)[0];rows=[];paths=[];commands=[]
def check(name,actual,want,kind='source summary',atol=1e-12):
 ok=math.isclose(float(actual),float(want),rel_tol=5e-14,abs_tol=atol)
 rows.append(dict(name=name,kind=kind,actual=actual,independent_expected=str(want),absolute_tolerance=atol,relative_tolerance=5e-14,passed=ok));assert ok,name
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);s=t/'simulation_fundamentals.py';s.write_text(code)
 for argv in [[sys.executable,s.name],[sys.executable,'-m','compileall','-q',s.name]]:
  z=subprocess.run(argv,cwd=t,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 spec=importlib.util.spec_from_file_location('exact_simulation',s);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for bits in itertools.product((0,1),repeat=4):
  k=sum(bits);sample=[90+20*b for b in bits];mean=F(90)+5*k;variance=F(400*k*(4-k),12);se2=variance/4
  summary=m.summarize(sample,100)
  for key,want in [('count',4),('mean',mean),('loss_frequency',F(4-k,4))]:check(str(bits)+' '+key,summary[key],want)
  check(str(bits)+' sample_sd squared',summary['sample_sd']**2,variance,atol=1e-11)
  check(str(bits)+' standard_error squared',summary['standard_error']**2,se2,atol=1e-11)
  exact_cover=(mean-100)**2<=F(49,25)**2*se2
  actual_cover=abs(summary['mean']-100)<=1.96*summary['standard_error']
  rows.append(dict(name=str(bits)+' supplemental 1.96 interval eligibility',kind='caller interval comparison',actual=actual_cover,independent_expected=exact_cover,passed=actual_cover==exact_cover));assert actual_cover==exact_cover
  paths.append(dict(bits=bits,up_count=k,probability='1/16',sample=sample,source_summary=summary,exact_mean=str(mean),exact_sample_variance=str(variance),exact_se_squared=str(se2),normal_plugin_interval_covers=exact_cover))
 # Exact probability-weighted distribution of the estimator,not another MonteCarlo run.
 W=F(1,16);mean=sum((F(x['exact_mean'])*W for x in paths),F(0));variance=sum(((F(x['exact_mean'])-100)**2*W for x in paths),F(0));s2=sum((F(x['exact_sample_variance'])*W for x in paths),F(0));e2=sum((F(x['exact_se_squared'])*W for x in paths),F(0));zero=sum((W for x in paths if F(x['exact_se_squared'])==0),F(0));coverage=sum((W for x in paths if x['normal_plugin_interval_covers']),F(0))
 for name,actual,want in [('E mean',mean,F(100)),('variance of mean',variance,F(25)),('E sample variance',s2,F(100)),('E estimated SE squared',e2,F(25)),('probability zero estimated SE',zero,F(1,8)),('finite normal-plugin coverage',coverage,F(7,8))]:check(name,float(actual),want,'supplemental exhaustive IID distribution',0)
 # Perfect dependence retains the same one-draw marginal,not the IIDjoint law.
 dependent=[]
 for value in (90,110):
  summary=m.summarize([value]*4,100);check('dependent '+str(value)+' reported SE',summary['standard_error'],0,'source summary under supplied dependent sample',0);dependent.append(dict(sample=[value]*4,probability='1/2',summary=summary))
 check('dependent estimator variance',float(sum((F(x['summary']['mean']-100)**2/2 for x in dependent),F(0))),100,'supplemental dependent joint model',0)
 assert s.read_text()==code
result=dict(source_revision=pin,source_path=path,source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,rows=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),iid_paths=paths,dependent_paths=dependent,model='N4;values90/110;IID probabilities1/16perpath;dependent comparison90x4/110x4probability1/2each',limits='Actualsource summary fields,exhaustive model references andcaller1.96interval kept distinct. No sourceCI API,random-generator quality,allNcoverage,real-worldIID or independent acceptance.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(len(rows),'predicates;',len(paths),'IIDpaths;coverage',coverage,'zeroSE',zero)
