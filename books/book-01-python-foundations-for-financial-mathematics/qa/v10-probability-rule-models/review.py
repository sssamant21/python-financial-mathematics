"""Probability-rule model assumptions,conditioning/independence/tolerance/partition contracts."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='9197db12d407f4adf756ba48d263121caeb0e88a';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.03-probability-rules.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def p(w,a):return sum((F(str(w[x])) for x in a),F(0))/sum(F(str(v)) for v in w.values())
def outcome(fn):
 try:return fn()
 except Exception as e:return type(e).__name__
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'rules.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('rules_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 space=['normal_ok','normal_default','stress_ok','stress_default'];events=[set(space[i] for i in range(4) if mask&(1<<i)) for mask in range(16)]
 laws=[('credit',[.72,.08,.15,.05]),('independent',[.64,.16,.16,.04]),('zero atoms',[.5,0.,0.,.5])]
 for name,weights in laws:
  w=dict(zip(space,weights));models.append(dict(name=name,weights=w))
  for i,a in enumerate(events):
   for j,b in enumerate(events):
    joint=p(w,a&b);den=p(w,b);gap=abs(joint-p(w,a)*den);ck(f'{name} independent{i},{j}',m.independent(w,a,b),gap==0,'exact normalized atom equality,not a sampled test or causal conclusion');ck(f'{name} conditional{i},{j}',outcome(lambda:m.conditional_probability(w,a,b)),float(joint/den) if den else 'ValueError','independent rational joint/conditioning mass;zero denominator undefined',bool(den))
 w=dict(zip(space,laws[0][1]));stress=set(space[2:]);default={space[1],space[3]};gap=F(3,125)
 for tol in [0.,.01,.024,.03]:ck('independence tolerance '+str(tol),m.independent(w,stress,default,tol),gap<=F(str(tol)),'declared approximate equality threshold,not model proof')
 ck('exact dependence gap',p(w,stress&default)-p(w,stress)*p(w,default),gap,'supplied joint law')
 ck('default given stress',m.conditional_probability(w,default,stress),F(1,4),'conditional event/direction explicit',True);ck('stress given default',m.conditional_probability(w,stress,default),F(5,13),'inverse conditional differs',True)
 for i,a in enumerate(events):
  total=sum(F(str(m.conditional_probability(w,a,{s})))*F(str(m.probability(w,{s}))) for s in space);ck(f'total-probability event{i}',total,p(w,a),'external assembly from native conditionals over exhaustive disjoint singletons',True)
  for s in space:
   want=p(w,{s}&a)/p(w,a) if p(w,a) else None
   ck(f'Bayes event{i} state{s}',outcome(lambda:m.conditional_probability(w,{s},a)),float(want) if want is not None else 'ValueError','rational posterior;identity is within declared model',want is not None)
 normal=set(space[:2]);omitted=m.conditional_probability(w,default,normal)*m.probability(w,normal);overlap=omitted+m.conditional_probability(w,default,default)*m.probability(w,default)
 ck('omitted partition mass',omitted,F(2,25),'caller omits stress block;result.08 is not full.13',True);ck('overlapping blocks double-count',overlap,F(21,100),'caller adds normal/default blocks which overlap',True)
 zero=dict(zip(space,laws[2][1]));ck('nonempty zero conditioning',outcome(lambda:m.conditional_probability(zero,{space[0]},{space[1]})),'ValueError','undefined despite valid nonempty label set');ck('zero event independence',m.independent(zero,{space[1]},{space[0]}),True,'probability-zero event satisfies equality;not disjointness/model validation')
 for label,fn,want in [('unknown conditioning',lambda:m.conditional_probability(w,default,{'missing'}),'ValueError'),('bool tolerance',lambda:m.independent(w,default,stress,True),'ValueError'),('negative tolerance',lambda:m.independent(w,default,stress,-.1),'ValueError')]:ck(label,outcome(fn),want,'source domain validation')
 prior=json.loads((here.parent/'chapter-14-probability-rules-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F112 nine initial failures/40 predicates/24 answers/ten tasks retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change or new historical totals')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,models=models,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected finite conditioning/Bayes/partition/tolerance assumptions;not data calibration,independent/platform acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
