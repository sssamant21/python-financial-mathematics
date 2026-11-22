"""Historical-tail sampling and same-sample strategy-selection finite laws."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='d0162ccb04b8a3fd97fe3928de6a5c1a597f1ab7';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.11-financial-return-statistics.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):
 ok=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want
 rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=ok))
def dec(x):return D(x.numerator)/D(x.denominator)
def root(x):
 with localcontext() as c:c.prec=100;return dec(x).sqrt()
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'financial_return_statistics.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('return_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 p=F(1,10);bad=F(-1,2);good=F(1,50);n=6;patterns=list(itertools.product([0,1],repeat=n));weights=[];cache=[]
 for i,z in enumerate(patterns):
  k=sum(z);weight=p**k*(1-p)**(n-k);weights.append(weight);r=[bad if v else good for v in z];values=list(map(float,r));entry=dict(bad_count=k,weight=str(weight),returns=list(map(str,r)),metrics={})
  for alpha,count in [(F(1,20),1),(F(1,4),2)]:
   # Closed binary-order formula: kth return is bad iff bad_count>=count.
   v=-bad if k>=count else -good;e=-(bad*min(k,count)+good*(count-min(k,count)))/count
   actual_v=m.historical_var(values,float(alpha));actual_e=m.historical_expected_shortfall(values,float(alpha))
   ck(f'path{i} alpha{alpha} VaR',actual_v,v,'source signed nearest-rank left-return quantile vs binary count identity',True)
   ck(f'path{i} alpha{alpha} ES',actual_e,e,'source ceil-count ES vs exact binary tail sum',True)
   entry['metrics'][str(alpha)]=dict(var=str(actual_v),es=str(actual_e))
  cache.append(entry)
 ck('exact IID training-law mass',sum(weights),1,'exact finite law')
 miss=sum(w for z,w in zip(patterns,weights) if sum(z)==0);q=(1-p)**n
 ck('no observed bad return probability',miss,q,'finite training enumeration vs binomial zero count')
 expected_single_var=(-bad)*(1-q)-good*q
 native_var=sum(w*F(c['metrics']['1/20']['var']) for c,w in zip(cache,weights));native_es=sum(w*F(c['metrics']['1/20']['es']) for c,w in zip(cache,weights))
 ck('expected native 5pct VaR',native_var,expected_single_var,'exact path weighted estimator vs closed binary-law formula',True)
 ck('expected native 5pct ES',native_es,expected_single_var,'ceil-one ES shares minimum under this selected n/alpha',True)
 # Future observation independent of training; loss strictly above fitted signed threshold.
 future_exceed=sum(w*(p if F(c['metrics']['1/20']['var'])<F(1,2) else 0) for c,w in zip(cache,weights))
 ck('single-fit future strict exceedance',future_exceed,p*q,'independent future law, no actual forecast/backtest')
 count2_es=sum(math.comb(n,k)*p**k*(1-p)**(n-k)*(-(bad*min(k,2)+good*(2-min(k,2)))/2) for k in range(n+1))
 ck('expected native 25pct ceil-two ES',sum(w*F(c['metrics']['1/4']['es']) for c,w in zip(cache,weights)),count2_es,'native weighted tail mean vs independent binomial-count sum',True)
 selected_no_bad=selected_var=selected_exceed=F(0);total_pair_weight=F(0)
 for a,wa in zip(cache,weights):
  for b,wb in zip(cache,weights):
   w=wa*wb;va=F(a['metrics']['1/20']['var']);vb=F(b['metrics']['1/20']['var']);chosen=min(va,vb);total_pair_weight+=w;selected_var+=w*chosen
   if chosen < F(1,2):selected_no_bad+=w;selected_exceed+=w*p
 expected_selection=1-(1-q)**2
 ck('two-strategy independent training-law mass',total_pair_weight,1,'caller pair law')
 ck('selected no-loss appearance probability',selected_no_bad,expected_selection,'caller picks lower same-sample VaR vs closed independent-law formula')
 ck('selected expected empirical VaR',selected_var,F(1,2)*(1-expected_selection)-good*expected_selection,'cached native metrics under caller selection',True)
 ck('selected future strict exceedance',selected_exceed,p*expected_selection,'independent future bad-return law of selected identical strategies')
 ck('selection raises chance of missing bad tail',selected_no_bad>miss,True,'exact comparative sampling law')
 models.append(dict(name='binary return law',training_paths=64,paired_strategy_training_paths=4096,n=n,bad_probability=str(p),bad_return=str(bad),good_return=str(good),population_5pct_loss_quantile='1/2',population_fractional_5pct_ES='1/2',no_bad_training_probability=str(q),mean_native_5pct_VaR=str(native_var),mean_native_5pct_ES=str(native_es),single_future_strict_exceedance=str(future_exceed),selected_no_bad_probability=str(selected_no_bad),selected_mean_empirical_VaR=str(selected_var),selected_future_strict_exceedance=str(selected_exceed),expected_25pct_ceil_two_ES=str(count2_es),paths=cache,scope='IID training signs with declared probabilities, independent identical strategies and independent future observation; exact enumeration not PRNG, actual strategy search, universal calibration or real data'))
prior=json.loads((here.parent/'chapter-15-return-statistics-review/results.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['source_sha256'];assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Historical-tail count/estimator instability and caller strategy selection under explicit finite binary law; upstream return basis/alignment/project provenance remain unfinished')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);print({k:v for k,v in models[0].items() if k not in ['paths','scope']});assert result['failed']==0
