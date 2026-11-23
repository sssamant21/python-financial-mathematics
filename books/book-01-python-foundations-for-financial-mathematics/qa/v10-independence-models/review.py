"""Independence constructors versus pairwise/mutual/conditional/joint-law assumptions."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='ff67ac399441099d09200fd6cd26f65390cb32a3';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.05-independence.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'independence.py';path.write_text(listing);spec=importlib.util.spec_from_file_location('independence_lab',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,path.name],[sys.executable,'-m','compileall','-q',path.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 a={(1,0),(1,1)};b={(0,1),(1,1)}
 for pa,pb in itertools.product([F(0),F(1,50),F(3,100),F(1,2),F(99,100),F(1)],repeat=2):
  w=m.bernoulli_joint(pa,pb);label=f'{pa}/{pb}';ck(label+' mass',sum(w.values()),F(1),'exact external product-model normalization');ck(label+' marginal A',m.p(w,a),pa,'declared constructor probabilities',True);ck(label+' marginal B',m.p(w,b),pb,'declared constructor probabilities',True);ck(label+' joint',m.p(w,a&b),pa*pb,'constructor imposes independence,does not infer it',True);ck(label+' independence',m.independent(w,a,b),True,'finite product-model equality');ck(label+' union',m.at_least_one_independent([pa,pb]),pa+pb-pa*pb,'external two-event inclusion-exclusion',True)
 for name,space in [('IID',list(itertools.product([0,1],repeat=3))),('XOR',[(0,0,0),(0,1,1),(1,0,1),(1,1,0)])]:
  w={x:F(1,len(space)) for x in space};events=[{x for x in space if x[i]} for i in range(3)]
  for i,event in enumerate(events):ck(name+' marginal'+str(i),m.p(w,event),.5,'declared equal-atom finite law')
  for i,j in itertools.combinations(range(3),2):ck(f'{name} pair{i}{j}',m.independent(w,events[i],events[j]),True,'pairwise exact independence');ck(f'{name} joint{i}{j}',m.p(w,events[i]&events[j]),.25,'each pair has four equally weighted states')
  triple=set.intersection(*events);union=set.union(*events);actual_triple=F(1,8) if name=='IID' else F(0);actual_union=F(7,8) if name=='IID' else F(3,4)
  ck(name+' triple',m.p(w,triple),actual_triple,'mutual equality needs higher-order intersection',True);ck(name+' actual union',m.p(w,union),actual_union,'external atom enumeration',True);ck(name+' assumed independent union',m.at_least_one_independent([.5]*3),F(7,8),'assumption-based helper accepts marginals,not a joint distribution',True);records.append(dict(name=name,triple=str(actual_triple),actual_union=str(actual_union),assumed_union='7/8'))
 for q in [F(0),F(3,5000),F(1,100),F(1,50)]:
  pa,pb=F(1,50),F(3,100);w={(0,0):1-pa-pb+q,(1,0):pa-q,(0,1):pb-q,(1,1):q};label='loan q'+str(q);ck(label+' A',m.p(w,a),pa,'same loan marginal',True);ck(label+' B',m.p(w,b),pb,'same loan marginal',True);ck(label+' independent',m.independent(w,a,b),q==pa*pb,'joint default varies within admissible marginals');ck(label+' actual union',m.p(w,a|b),pa+pb-q,'external exact loan joint law',True);ck(label+' assumed union',m.at_least_one_independent([pa,pb]),F(247,5000),'product assumption fixed at.0494',True)
 # Zero covariance does not identify independence: X=-1,0,1;Y=X².
 space=[(-1,1),(0,0),(1,1)];w={x:F(1,3) for x in space};EX=sum(F(x,3) for x,y in space);EY=sum(F(y,3) for x,y in space);cov=sum(F(x*y,3) for x,y in space)-EX*EY;A={x for x in space if x[0]==0};B={x for x in space if x[1]==0};ck('nonlinear covariance',cov,F(0),'external exact moment arithmetic,no native covariance API');ck('nonlinear A',m.p(w,A),F(1,3),'finite event mass',True);ck('nonlinear B',m.p(w,B),F(1,3),'finite event mass',True);ck('nonlinear not independent',m.independent(w,A,B),False,'joint1/3 differs from product1/9')
 # Independent conditionally on a common regime,dependent after mixing.
 w={}
 for regime,p in [(0,F(1,10)),(1,F(9,10))]:
  for x,y in itertools.product([0,1],repeat=2):w[(regime,x,y)]=F(1,2)*(p if x else 1-p)*(p if y else 1-p)
 A={x for x in w if x[1]};B={x for x in w if x[2]}
 for regime,rate in [(0,F(1,10)),(1,F(9,10))]:
  given={x for x in w if x[0]==regime};ck('regime A'+str(regime),m.conditional(w,A,given),rate,'external conditional Bernoulli model',True);ck('regime B'+str(regime),m.conditional(w,B,given),rate,'external conditional Bernoulli model',True);ck('regime joint'+str(regime),m.conditional(w,A&B,given),rate*rate,'within-regime independence',True)
 ck('mixed dependence',m.independent(w,A,B),False,'common latent regime changes joint law');ck('mixed joint',m.p(w,A&B),F(41,100),'exact regime mixture',True);ck('mixed union',m.p(w,A|B),F(59,100),'marginals.5 do not imply union.75',True);ck('mixed assumed union',m.at_least_one_independent([.5,.5]),.75,'independent helper has no regime information')
 rare=F(1,10**80);w={'rare':rare,'usual':1-rare};ck('rare exact dependence',m.independent(w,{'rare'},{'rare'}),False,'positive probability differs from squared probability');ck('rare opt-in tolerance',m.independent(w,{'rare'},{'rare'},1e-12),True,'approximate tolerance may hide dependence;not model validation')
 def outcome(fn):
  try:return fn()
  except Exception as e:return type(e).__name__
 for label,fn in [('unknown label',lambda:m.independent(w,{'missing'},{'rare'})),('empty union list',lambda:m.at_least_one_independent([])),('bool tolerance',lambda:m.independent(w,{'rare'},{'rare'},True))]:ck(label,outcome(fn),'ValueError','existing domain contract')
 prior=json.loads((here.parent/'chapter-14-independence-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F114 six failures/41 predicates/24 answers/eight tasks retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,model_records=records,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Finite independence/joint-law/model-assumption crosswalk;no actual dependence/calibration,platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
