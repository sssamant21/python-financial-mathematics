"""Conditional probability,base rates,selection and regime mixture assumptions."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='534485e5c34a2e8892aa85ec6471d24daa08681c';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.04-conditional-probability.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def p(w,a):return sum((F(str(w[x])) for x in a),F(0))/sum(F(str(v)) for v in w.values())
def outcome(fn):
 try:return fn()
 except Exception as e:return type(e).__name__
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'conditioning.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('conditioning_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 space=['00','01','10','11'];events=[set(space[i] for i in range(4) if mask&(1<<i)) for mask in range(16)]
 for name,weights in [('positive',[.72,.08,.15,.05]),('zero atoms',[.5,0.,0.,.5])]:
  w=dict(zip(space,weights))
  for i,a in enumerate(events):
   for j,b in enumerate(events):
    den=p(w,b);ck(f'{name} conditional{i},{j}',outcome(lambda:m.conditional(w,a,b)),float(p(w,a&b)/den) if den else 'ValueError','exact normalized atom ratio,zero conditioning undefined',bool(den))
 for prior,sensitivity,false_positive in itertools.product([0.,.001,.01,.1,.5,1.],[0.,.5,.9,1.],[0.,.05,.5,1.]):
  P,S,Q=map(lambda x:F(str(x)),(prior,sensitivity,false_positive));joint=P*S;evidence=joint+(1-P)*Q;want=float(joint/evidence) if evidence else 'ValueError';label=f'{prior}/{sensitivity}/{false_positive}';ck('Bayes '+label,outcome(lambda:m.bayes(prior,sensitivity,false_positive)),want,'independent exact two-class joint/evidence law',bool(evidence));w={'positive_true':float(joint),'negative_true':float(P-joint),'positive_false':float((1-P)*Q),'negative_false':float((1-P)*(1-Q))};ck('joint-table posterior '+label,outcome(lambda:m.conditional(w,{'positive_true','negative_true'},{'positive_true','positive_false'})),want,'explicit external joint-table construction cross-check;no prior inferred from signal',bool(evidence))
  if sensitivity==.9 and false_positive==.05:records.append(dict(prior=prior,sensitivity=sensitivity,false_positive=false_positive,posterior=want))
 for prior,sensitivity,false_positive in [(1e-300,1e-300,0.),(1e-300,1e-300,1e-300)]:
  P,S,Q=map(lambda x:F(str(x)),(prior,sensitivity,false_positive));want=float(P*S/(P*S+(1-P)*Q));got=m.bayes(prior,sensitivity,false_positive);ck('tiny positive evidence '+str(false_positive),got,want,'exact rational evidence before reporting;zero absolute tolerance for tiny posterior' if want<1e-100 else 'exact rational positive evidence',False if want<1e-100 else True)
 # Conditioning on A or B in an independent fair two-bit model changes dependence.
 w=dict(zip(space,[.25]*4));a={'10','11'};b={'01','11'};selected=a|b
 ck('unselected joint',m.prob(w,a&b),.25,'external independent joint model');pa=m.conditional(w,a,selected);pb=m.conditional(w,b,selected);joint=m.conditional(w,a&b,selected);ck('selected A',pa,F(2,3),'caller conditions on union',True);ck('selected B',pb,F(2,3),'caller conditions on union',True);ck('selected joint',joint,F(1,3),'caller conditions on union',True);ck('selected dependence gap',joint-pa*pb,-F(1,9),'external product comparison,not a source causal/independence API',True)
 ck('original regime mix',m.total_probability([(.2,.25),(.8,.1)]),.13,'matched exhaustive disjoint mixture');ck('changed regime mix',m.total_probability([(.8,.25),(.2,.1)]),.22,'same conditional rates,different target population')
 for name,mixture,want in [('A',[(.1,.1),(.9,.6)],.55),('B',[(.9,.2),(.1,.7)],.25)]:ck('aggregate reversal '+name,m.total_probability(mixture),want,'external case mix:A lower risk within each stratum but greater aggregate risk',True)
 ck('single-pass mixture',m.total_probability(iter([(.2,.25),(.8,.1)])),.13,'actual source consumes one-pass input once;prior F113 contract retained')
 for label,fn,want in [('unknown numerator',lambda:m.conditional(w,{'missing'},a),'ValueError'),('zero evidence',lambda:m.bayes(0.,1.,0.),'ValueError'),('nonempty zero given',lambda:m.conditional({'a':1.,'b':0.},{'a'},{'b'}),'ValueError')]:ck(label,outcome(fn),want,'conditional domain,not evidence of model validity')
 prior=json.loads((here.parent/'chapter-14-conditional-probability-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F113 six failures/33 predicates/24 answers/ten tasks retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,base_rate_records=records,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected finite conditioning/selection/base-rate/regime assumptions;no actual calibration,causality,platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
