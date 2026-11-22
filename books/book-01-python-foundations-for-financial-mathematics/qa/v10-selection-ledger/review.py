"""Outcome-retention and declared multiplicity ledger, with pinned native sign tests."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='aad482ca16bd3c011c402f4ce92ff216170123e4';paths=['books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.13-statistical-pitfalls-in-financial-data.md','books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.09-hypothesis-testing-foundations.md'];rows=[];commands=[];manifest={};models=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
with tempfile.TemporaryDirectory() as tmp:
 modules=[]
 for i,p in enumerate(paths):
  raw=subprocess.check_output(['git','show',pin+':'+p],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];manifest[p]=dict(source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest());f=Path(tmp)/('source'+str(i)+'.py');f.write_text(listing);spec=importlib.util.spec_from_file_location('pinned_source'+str(i),f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);modules.append(m)
  z=subprocess.run([sys.executable,f.name],cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=[sys.executable,f.name],returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 z=subprocess.run([sys.executable,'-m','compileall','-q','.'],cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=[sys.executable,'-m','compileall','-q','.'],returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 p,h=modules;full=[];retained=[];selected_full=[]
 for i,x in enumerate(itertools.product([-.1,.1],repeat=4)):
  expected=sum(F(str(v)) for v in x)/4;actual=p.sample_mean(list(x));full.append(F(str(actual)));ck('retention path'+str(i)+' full mean',actual,expected,'native sample mean vs exact full universe',True);keep=[v>0 for v in x]
  if any(keep):
   value=p.survivor_mean(list(x),keep);ck('retention path'+str(i)+' selected mean',value,F(1,10),'native supplied positive-only retention changes estimand',True);retained.append(F(str(value)));selected_full.append(expected)
  else:
   try:p.survivor_mean(list(x),keep);got=False
   except ValueError:got=True
   ck('retention all-excluded rejects',got,True,'native empty retained universe policy')
 ck('unconditional full mean expectation',sum(full)/16,F(0),'exact fair-sign universe law')
 ck('nonempty retention probability',F(len(retained),16),F(15,16),'conditional selection law')
 ck('full mean conditional on nonempty selection',sum(selected_full)/15,F(1,150),'explicit conditioning changes population mean')
 ck('selected-only conditional mean',sum(retained)/15,F(1,10),'outcome-retention estimand distinct from full/conditional means')
 n=6;patterns=list(itertools.product([-1,1],repeat=n));deviations=[abs(sum(x)) for x in patterns];rejects=0
 for i,x in enumerate(patterns):
  expected=F(sum(v>=abs(sum(x)) for v in deviations),64);actual=h.exact_sign_test_p(list(x));decision=h.decision(actual,.05)
  ck('null path'+str(i)+' p',F(actual),expected,'native exact sign p vs enumerated null deviation tail')
  ck('null path'+str(i)+' decision',decision,'reject H0' if abs(sum(x))==6 else 'do not reject H0','independent two-extreme-path critical region');rejects+=decision=='reject H0'
 q=F(rejects,64);ck('attained false rejection probability',q,F(1,32),'native weighted exact-null rejection region')
 ck('twenty expected false rejections',20*q,F(5,8),'linear expectation from attained marginal probabilities, not nominal level')
 full_threshold=p.bonferroni_threshold(.05,20);partial_threshold=p.bonferroni_threshold(.05,10)
 ck('complete declared ledger threshold',full_threshold,.0025,'native helper vs exact .05/20')
 ck('underreported ledger threshold',partial_threshold,.005,'native helper can only use supplied count')
 ck('ledger diagnostic full count decision',h.decision(.003,full_threshold),'do not reject H0','caller ledger sensitivity, supplied p is hypothetical')
 ck('ledger diagnostic hidden trials decision',h.decision(.003,partial_threshold),'reject H0','caller ledger sensitivity, not actual calibrated p-value')
 models.append(dict(name='retention law',paths=16,unconditional_weight='1/16',unconditional_full_mean='0',nonempty_selection_probability='15/16',conditional_full_mean='1/150',conditional_selected_mean='1/10',scope='Four independent fair±.1 observations; positive-only retention supplied by caller, not a historical membership reconstruction'))
 models.append(dict(name='exact-null/ledger law',sign_paths=64,attained_size=str(q),expected_false_count_20=str(20*q),native_complete_threshold=full_threshold,native_underreported_threshold=partial_threshold,scope='Independent signs within each null test; expected count needs no across-test independence. Hypothetical .003 diagnostic is not a real test/strategy acceptance.'))
prior=json.loads((here.parent/'chapter-15-pitfalls-review/results.json').read_text());assert manifest[paths[0]]['source_sha256']==prior['source_sha256'];assert manifest[paths[0]]['listing_sha256']==prior['listing_sha256'];old=json.loads((here.parent/'v10-power-selection/F218-assumption-clarification.json').read_text());assert manifest[paths[1]]['listing_sha256']==old['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),manifest=manifest,rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Selected retention/declared-ledger contracts and finite null law; timestamp/ACF/outlier/cost/project-data/model/platform/independent boundaries remain unfinished')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
