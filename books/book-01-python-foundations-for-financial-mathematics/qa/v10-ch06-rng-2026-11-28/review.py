import hashlib,json,re,subprocess,sys,tempfile,platform
from pathlib import Path
import numpy as np
here=Path(__file__).resolve().parent
root=here.parents[3]
pin="6eb128fff8b8067cdb8a2155f939628a381dca68"
path="books/book-01-python-foundations-for-financial-mathematics/chapter-06/6.13-random-number-generation.md"
raw=subprocess.check_output(["git","show",pin+":"+path],cwd=root)
fences=re.findall(r"^```python\n(.*?)^```",raw.decode(),re.M|re.S)
rows=[];commands=[]
def ck(name,ok):rows.append(dict(name=name,passed=bool(ok)))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 for name,code in zip(["random_lab.py","test_random_lab.py"],fences): (p/name).write_text(code)
 for cmd in [[sys.executable,"random_lab.py"],[sys.executable,"test_random_lab.py"],[sys.executable,"-m","compileall","-q","."]]:
  z=subprocess.run(cmd,cwd=p,capture_output=True,text=True);commands.append(dict(argv=cmd,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 sys.path.insert(0,tmp)
 from random_lab import make_rng,innovations
 for seed in [0,7,2**128-1]:
  for shape in [(1,1),(3,4),(7,2)]:
   ref=np.random.Generator(np.random.PCG64(seed)).standard_normal(shape)
   ck(f"replay {seed} {shape}",np.array_equal(innovations(make_rng(seed),*shape),ref))
  a=make_rng(seed);b=make_rng(seed)
  x=np.concatenate([innovations(a,3,2),innovations(a,4,2)])
  ck(f"contiguous chunks {seed}",np.array_equal(x,innovations(b,7,2)))
  ck(f"reseed duplicates prefix {seed}",np.array_equal(innovations(make_rng(seed),3,2),x[:3]))
  ck(f"same innovation scale {seed}",np.array_equal(.02*x,2*(.01*x)))
 # Supplemental finite law: same marginal signs, different dependence.
 for label,pairs,want in [("independent",[(-1,-1),(-1,1),(1,-1),(1,1)],.5),("shared",[(-1,-1),(1,1)],1),("offset",[(-1,1),(1,-1)],0)]:
  ck(label+" equal-weight variance",sum(((a+b)/2)**2 for a,b in pairs)/len(pairs)==want)
r=dict(pin=pin,source_sha256=hashlib.sha256(raw).hexdigest(),listing_hashes=[hashlib.sha256(s.encode()).hexdigest() for s in fences],numpy=np.__version__,python=platform.python_version(),rows=rows,commands=commands,passed=sum(x["passed"] for x in rows),failed=sum(not x["passed"] for x in rows))
(here/(sys.argv[1]+".json")).write_text(json.dumps(r,indent=2)+"\n");print(r["passed"],r["failed"]);assert not r["failed"]
