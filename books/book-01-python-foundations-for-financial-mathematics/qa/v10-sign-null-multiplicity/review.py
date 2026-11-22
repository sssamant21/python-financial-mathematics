"""Exact fair-sign null rejection and caller multiple-test dependence models."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='7108ac9f0776faa84bb1b024276023900e20b66f';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.09-hypothesis-testing-foundations.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind):rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=got==want))
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'hypothesis_testing.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('hypothesis_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for n,expected_size in [(6,F(1,32)),(7,F(1,64)),(8,F(1,128)),(9,F(5,128))]:
  patterns=list(itertools.product([-1,1],repeat=n));deviations=[abs(sum(x)) for x in patterns];rejects=bonferroni=0;hist={}
  for i,values in enumerate(patterns):
   # Direct finite fair-sign tail counting, not the source binomial-tail sum.
   p=F(sum(d>=abs(sum(values)) for d in deviations),2**n);actual=m.exact_sign_test_p(list(values));native=m.decision(actual,.05);adjusted=m.decision(actual,.05/20)
   ck(str(n)+' path'+str(i)+' exact p',F(actual),p,'native exact p vs enumerated null deviation tail')
   ck(str(n)+' path'+str(i)+' rejection',native,'reject H0' if p<=F(1,20) else 'do not reject H0','native decision vs exact threshold')
   ck(str(n)+' path'+str(i)+' caller Bonferroni threshold',adjusted,'reject H0' if p<=F(1,400) else 'do not reject H0','native decision with caller threshold, not multiplicity API')
   rejects+=native=='reject H0';bonferroni+=adjusted=='reject H0';hist[str(p)]=hist.get(str(p),0)+1
  size=F(rejects,2**n);ck(str(n)+' exact size',size,expected_size,'native weighted rejection vs closed binomial critical region');ck(str(n)+' selected Bonferroni size',F(bonferroni,2**n),F(0),'native weighted caller-threshold region')
  models.append(dict(n=n,paths=2**n,exact_null_size=str(size),null_p_histogram=hist,family_tests=20,caller_expected_false_count=str(20*size),caller_independent_family_any_false=str(1-(1-size)**20),caller_independent_family_any_false_float=float(1-(1-size)**20),caller_perfectly_dependent_family_any_false=str(size),caller_perfectly_dependent_expected_false_count=str(20*size),caller_Bonferroni_size_per_test='0',scope='Fair independent signs within each test. Family independence/perfect dependence are separate hypothetical laws, not implemented family APIs or real-data assumptions.'))
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Exact finite fair-sign n6..9 null regions and caller multiplicity models; no real-data null/power/model/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);print([(x['n'],x['exact_null_size'],x['caller_independent_family_any_false_float']) for x in models]);assert result['failed']==0
