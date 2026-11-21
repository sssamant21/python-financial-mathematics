"""Exact selected streaming moments and draw-order contracts; no speedup claim."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,math,hashlib,platform,itertools,random
if not __debug__: raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3]
pin='477083a59f74be60e5e5766f4cd9ec5c8b1656b9'
path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.13-computational-performance.md'
raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root)
listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S)[0]
rows=[];commands=[]
def ck(name,got,want,kind):
 ok=got==want if isinstance(want,bool) else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12)
 rows.append(dict(name=name,actual=got,expected=str(want),kind=kind,passed=ok))
def compare(name,stats,xs):
 n=len(xs);mean=F(sum(xs),n);m2=sum((F(x)-mean)**2 for x in xs);v=m2/(n-1)
 for key,want in [('count',n),('mean',mean),('m2',m2),('sample_variance',v),('standard_error',math.sqrt(float(v/n)))]:
  got=getattr(stats,key);ck(name+' '+key,got() if callable(got) else got,want,'native field vs exact raw moments')
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'simulation_performance.py';p.write_text(listing)
 spec=importlib.util.spec_from_file_location('performance_reference',p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for i,xs in enumerate(itertools.product([80,100,120],repeat=5)):
  s=m.RunningStats()
  for x in xs:s.update(x)
  compare('enumerated path '+str(i),s,xs)
 for n in [2,3,10,11,101,1003]:
  rng=random.Random(42);u=[rng.random() for _ in range(n)];xs=[80 if z<.25 else 100 if z<.75 else 120 for z in u]
  direct=m.streaming_run(n,42);compare('seed42 N'+str(n),direct,xs)
  for batch in [1,2,10,11,100,2000]:
   batched=m.run_batches(n,batch,42);ck('N'+str(n)+' B'+str(batch)+' stream state',batched==direct,True,'exact same-order native state')
   compare('N'+str(n)+' B'+str(batch),batched,xs)
 ck('binary64 element bytes',m.array_bytes(100000,253,8),202400000,'native storage arithmetic')
 ck('binary32 element bytes',m.array_bytes(100000,253,4),101200000,'native storage arithmetic')
 ck('MiB conversion',m.array_bytes(100000,253,8)/(2**20),F(202400000,2**20),'caller unit conversion')
 ck('partial batch arithmetic',101//10+(101%10>0),11,'caller partition arithmetic')
prior=json.loads((root/'books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-performance-review/results.json').read_text())
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),prior_identity_fields={k:v for k,v in prior.items() if 'sha' in k},python=platform.python_version(),platform=platform.platform(),rows=rows,commands=commands,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='243 deterministic five-observation paths; selected same-generator ordered batches; not timing/memory/parallel/NumPy or statistical acceptance')
(here/((sys.argv[1] if len(sys.argv)>1 else 'first')+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
