"""Pinned exact-source decisions, finite alternative laws and supplemental references."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='199352a9f3398bb2bdd2b2fe3eee5ec42e605a76';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.09-hypothesis-testing-foundations.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,close=False):
 ok=math.isclose(got,float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want
 rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'hypothesis_testing.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('hypothesis_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for n,critical in [(6,{0,6}),(7,{0,7}),(8,{0,8}),(9,{0,1,8,9})]:
  patterns=list(itertools.product([-1,1],repeat=n));native=[]
  for i,x in enumerate(patterns):
   reject=m.decision(m.exact_sign_test_p(list(x)),.05)=='reject H0';native.append(reject)
   ck(f'{n} path{i} rejection',reject,x.count(1) in critical,'native decision vs independent binomial critical region')
  for p in [F(1,4),F(1,2),F(3,4)]:
   weights=[p**x.count(1)*(1-p)**x.count(-1) for x in patterns]
   ck(f'{n} p{p} law mass',sum(weights),F(1),'exact alternative law')
   actual=sum(w for w,r in zip(weights,native) if r)
   expected=sum(math.comb(n,k)*p**k*(1-p)**(n-k) for k in critical)
   ck(f'{n} p{p} weighted rejection',actual,expected,'native regions weighted by alternative vs independent binomial sum')
   ck(f'{n} p{p} miss probability',sum(w for w,r in zip(weights,native) if not r),1-expected,'native finite Type II probability; null p=.5 is size not power')
   models.append(dict(n=n,positive_probability=str(p),rejection_probability=str(actual),interpretation='attained size' if p==F(1,2) else 'power under specified IID sign alternative',miss_probability=str(1-actual)))
 # Same signs, changed magnitudes: sign-test target is not a mean/cost target.
 a=[1]*8+[-1];b=[1]*8+[-100]
 ck('magnitude-invariant sign p',m.exact_sign_test_p(a),m.exact_sign_test_p(b),'native sign invariance')
 ck('positive sample mean',F(sum(a),9),F(7,9),'supplemental exact sample effect')
 ck('negative sample mean same signs',F(sum(b),9),F(-92,9),'supplemental exact sample effect')
 ck('same significant signs',m.decision(m.exact_sign_test_p(b)), 'reject H0','native median/sign inference does not imply positive mean')
 # Caller-chosen tail AFTER data, not a source one-sided p-value API.
 n=8;selected=0;fixed=0;two=0
 for i,x in enumerate(itertools.product([-1,1],repeat=n)):
  k=x.count(1);p=m.exact_sign_test_p(list(x));directional=min(F(1),F(sum(math.comb(n,j) for j in range(k,n+1)),2**n))
  chosen=m.decision(p/2,.05)=='reject H0';fixed+=directional<=F(1,20);selected+=chosen;two+=m.decision(p,.05)=='reject H0'
  oracle=min(sum(math.comb(n,j) for j in range(k+1)),sum(math.comb(n,j) for j in range(k,n+1)))<=F(2**n,20)
  ck(f'selected-tail path{i}',chosen,oracle,'caller p/2 selection vs direct directional-tail null counting')
 for name,got,want in [('fixed direction size',F(fixed,256),F(9,256)),('selected direction size',F(selected,256),F(9,128)),('two-sided size',F(two,256),F(1,128))]:ck(name,got,want,'exact caller selection null law')
 models.append(dict(n=8,fixed_one_tail_size=str(F(fixed,256)),data_chosen_one_tail_size=str(F(selected,256)),native_two_tail_size=str(F(two,256)),scope='Caller selection counterexample, no one-sided API or real-data calibration claim'))
 with localcontext() as ctx:
  ctx.prec=100
  for hurdle in [D(0),D('.005')]:
   effect=D('.02')-hurdle;t=effect/D('.01')*D(3).sqrt();p=1-abs(t)/(t*t+2).sqrt()
   native=m.one_sample_t_statistic([.01,.02,.03],float(hurdle))
   ck(f'hurdle{hurdle} t',native,t,'native statistic vs independently derived exact decimal moments',True)
   ck(f'hurdle{hurdle} mean excess',effect,D('.02')-hurdle,'supplemental effect with explicit hypothetical per-period cost')
   ck(f'hurdle{hurdle} Student decision',m.decision(float(p)), 'do not reject H0','native decision receiving supplemental df2 reference')
   ck(f'hurdle{hurdle} normal decision',m.decision(m.normal_two_sided_p(native)), 'reject H0','deliberately different normal-reference model, not a t p-value')
   models.append(dict(hurdle=str(hurdle),effect=str(effect),t_statistic=str(t),supplemental_df2_two_sided_p=str(p),native_normal_two_sided_p=m.normal_two_sided_p(native),scope='df2 closed-form distribution calculation supplemental, normal tails are a separate model; no native t CDF/calibration or measured costs'))
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Exact finite IID sign alternatives, caller post-selection law, sample cost-hurdle and supplemental df2 reference; no real data/power planning/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
