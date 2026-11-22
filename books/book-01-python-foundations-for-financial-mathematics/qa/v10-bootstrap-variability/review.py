"""Native finite-replicate bootstrap versus exact conditional multinomial laws."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform,itertools,random
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='cdf2679391b0060db8465c0de08c09c632d658e6';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.08-confidence-intervals.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];cases=[];exact_laws={}
def ck(name,got,want,kind):
 ok=got==want if isinstance(want,bool) or kind.startswith('exact ') else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=ok))
def bounds(counts,B):
 def rank(index):
  total=0
  for j,n in enumerate(counts):
   total+=n
   if index<total:return F(2*j,3)
  raise RuntimeError('rank')
 def quantile(prob):
  h=(B-1)*prob;lo=h.numerator//h.denominator;hi=math.ceil(h)
  return rank(lo) if lo==hi else (hi-h)*rank(lo)+(h-lo)*rank(hi)
 return quantile(F(1,40)),quantile(F(39,40))
# Exact conditional B27 distribution over multinomial replicate category counts.
D=27**27
for k,weights in [(1,[8,12,6,1]),(2,[1,6,12,8])]:
 total=0;covered={p:0 for p in [F(1,10),F(1,2),F(9,10)]}
 for n0 in range(28):
  for n1 in range(28-n0):
   for n2 in range(28-n0-n1):
    ns=[n0,n1,n2,27-n0-n1-n2];multi=math.comb(27,n0)*math.comb(27-n0,n1)*math.comb(27-n0-n1,n2);numerator=multi*math.prod(w**n for w,n in zip(weights,ns));total+=numerator;lo,hi=bounds(ns,27)
    for p in covered:
     if lo<=2*p<=hi:covered[p]+=numerator
 ck('conditional k'+str(k)+' exact probability mass',F(total,D),F(1),'exact multinomial law')
 exact_laws[k]={p:F(v,D) for p,v in covered.items()}
 q=F(weights[0],27);closed=1-(1-q)**27-27*q*(1-q)**26-q**27;ck('conditional k'+str(k)+' rare-target binomial identity',exact_laws[k][F(1,10)],closed,'exact independent binomial count identity')
for p in [F(1,10),F(1,2),F(9,10)]:ck('conditional reflection p'+str(p),exact_laws[1][p],exact_laws[2][1-p],'exact reflected law')
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'confidence_intervals.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('confidence_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 designs=[(values,27,seed) for values in itertools.product([0,2],repeat=3) for seed in range(32)]+[(values,B,seed) for values in [(0,0,2),(0,2,2)] for B in [54,216] for seed in range(32)]
 for i,(values,B,seed) in enumerate(designs):
  native=m.bootstrap_percentile_ci(list(values),replicates=B,alpha=.05,seed=seed);rng=random.Random(seed);counts=[0]*4;indices=[]
  for _ in range(B):
   selected=rng.choices(range(3),k=3);indices.append(selected);successes=sum(values[j]==2 for j in selected);counts[successes]+=1
  lo,hi=bounds(counts,B)
  for side,want in enumerate([lo,hi]):ck(str(i)+' native endpoint'+str(side),native[side],want,'native endpoint vs histogram-rank replay')
  ck(str(i)+' histogram count',sum(counts),B,'exact replay count')
  for p in [F(1,10),F(1,2),F(9,10)]:ck(str(i)+' mean-target membership p'+str(p),native[0]<=float(2*p)<=native[1],lo<=2*p<=hi,'native membership vs rational histogram ranks')
  cases.append(dict(values=values,replicates=B,seed=seed,native_interval=native,histogram=counts,oracle_interval=[str(lo),str(hi)],index_replay_sha256=hashlib.sha256(json.dumps(indices).encode()).hexdigest()))
summaries=[]
for p in [F(1,10),F(1,2),F(9,10)]:
 exact=3*p*(1-p)**2*exact_laws[1][p]+3*p*p*(1-p)*exact_laws[2][p];selected=[]
 for seed in range(32):
  covered=F(0)
  for c in cases:
   if c['replicates']==27 and c['seed']==seed:
    k=sum(x==2 for x in c['values']);weight=p**k*(1-p)**(3-k)
    if c['native_interval'][0]<=float(2*p)<=c['native_interval'][1]:covered+=weight
  selected.append(covered)
 summaries.append(dict(p=str(p),exact_IID_resample_B27_coverage=str(exact),exact_IID_resample_B27_coverage_float=float(exact),fixed_seed_grid_average=float(sum(selected)/32),fixed_seed_grid_min=float(min(selected)),fixed_seed_grid_max=float(max(selected)),scope='32 deterministic seeds are not independent statistical replications or a PRNG/coverage acceptance test'))
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,cases=cases,conditional_exact_laws={str(k):{str(p):str(v) for p,v in law.items()} for k,law in exact_laws.items()},summaries=summaries,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Exact hypothetical IID-resample B27 law plus native deterministic seed-grid arithmetic replay; not independent RNG/nominal coverage certification')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);print(summaries);assert result['failed']==0
