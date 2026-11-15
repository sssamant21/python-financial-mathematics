"""Execute pinned manuscript fences against independent rational annuity sums.

Run with Python from any directory in a git checkout containing the pin.
This source contract batch does not install or accept an updated wheel.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal
import subprocess,sys,json,re,math,hashlib,platform
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
PIN='a112900d53216e81f73c0ee9223621c951fd7e96'
BASE='books/book-01-python-foundations-for-financial-mathematics/chapter-21/'
p=BASE+'21.07-loan-module.md';text=subprocess.check_output(['git','show',PIN+':'+p],cwd=ROOT,text=True)
blocks=re.findall(r'```python\n(.*?)\n```',text,re.S);assert len(blocks)==4
scope={};exec(compile(blocks[0],p,'exec'),scope);fn=scope['level_payment'];rows=[]
def add(label,ok,**data):rows.append(dict(case=label,passed=bool(ok),**data))
# The oracle discounts each payment as an exact rational. It does not use
# the implementation's log1p/expm1 denominator or its annuity quotient.
for principal in [1.,1000.,1e-200,1e200]:
 for rate,n in [(0.,12),(.1,1),(.1,2),(1e-12,12),(.01,360),(1.,1200),(1e-308,12),(math.ulp(0.),12)]:
  L,R=map(Fraction,(principal,rate));v=Fraction(1,1)/(1+R);power=v;total=Fraction(0)
  for _ in range(n):total+=power;power*=v
  exact=L/total;want=float(exact);got=fn(principal,rate,n)
  add(f'annuity sum L={principal} r={rate} n={n}',math.isclose(got,want,rel_tol=5e-14,abs_tol=0.),actual=got,expected=want)
for label,args in [('integer principal',(1000,.1,2)),('bool principal',(True,.1,2)),('decimal principal',(Decimal('1000'),.1,2)),('zero principal',(0.,.1,2)),('negative principal',(-1.,.1,2)),('nan principal',(math.nan,.1,2)),('inf principal',(math.inf,.1,2)),('integer rate',(1000.,0,2)),('bool rate',(1000.,True,2)),('decimal rate',(1000.,Decimal('.1'),2)),('negative rate',(1000.,-.01,2)),('over cap rate',(1000.,1.01,2)),('nan rate',(1000.,math.nan,2)),('inf rate',(1000.,math.inf,2)),('bool periods',(1000.,.1,True)),('float periods',(1000.,.1,2.)),('zero periods',(1000.,.1,0)),('over cap periods',(1000.,.1,1201)),('result overflow',(1e308,1.,1)),('zero rate underflow',(math.ulp(0.),0.,1200)),('positive rate underflow',(math.ulp(0.),1e-12,1200))]:
 try:got=fn(*args);kind='returned'
 except Exception as e:kind=type(e).__name__
 add(label,kind=='ValueError',actual=kind,expected='ValueError')
for r,n in [(0.,12),(.01,360),(.1,2),(1.,1200)]:
 a=fn(1000.,r,n);add(f'scale r={r} n={n}',math.isclose(fn(2000.,r,n),2*a,rel_tol=5e-14,abs_tol=0.))
for n in [1,2,360,1200]:add(f'rate monotonic n={n}',fn(1000.,0.,n)<fn(1000.,.01,n)<fn(1000.,1.,n))
for r in [0.,.01,.1]:add(f'term monotonic r={r}',fn(1000.,r,12)>fn(1000.,r,24)>fn(1000.,r,48))
print('source numerical contracts; integration cap is reviewed separately')
d=dict(source_revision=PIN,source_path=p,source_blob=subprocess.check_output(['git','rev-parse',PIN+':'+p],cwd=ROOT,text=True).strip(),source_fence_sha256=hashlib.sha256(blocks[0].encode()).hexdigest(),python=sys.version,platform=platform.platform(),oracle='Exact Fraction sum of n individual discounted payments; divide principal by sum; no log/expm1 oracle.',relative_tolerance=5e-14,absolute_tolerance=0.,source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),new_historical_unique_methods=0,limits='Source numerical contract batch only. No new formal workflow/answer records, wheel installation, model/platform/release/independent acceptance. Earlier 48-method source checkpoint remains separate; 1200 loan periods exceed 1000-payment cashflow integration cap. Rounding/final payoff/fees/APR excluded.')
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
