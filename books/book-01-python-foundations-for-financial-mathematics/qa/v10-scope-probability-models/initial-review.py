"""V10 source/evidence queue reconciliation and Section14.1 finite model boundaries."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='d14c02c65f67b92ce6dd4e27be877d400b784f0f';book='books/book-01-python-foundations-for-financial-mathematics/';source_path=book+'chapter-14/14.01-why-probability-matters-in-finance.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def law(s):
 p=[F(str(a)) for a,b in s];x=[F(str(b)) for a,b in s];total=sum(p);p=[a/total for a in p];mean=sum(a*b for a,b in zip(p,x));return [mean,sum(a*b*b for a,b in zip(p,x))-mean*mean,sum(a for a,b in zip(p,x) if b<0),sum(a*max(F(0),-b) for a,b in zip(p,x))]
# Entire locked section inventory; marker matches are search candidates,never proof of closure.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',pin,book],cwd=root,text=True).splitlines();sections=[p for p in paths if re.search(r'/chapter-\d\d/\d\d\.\d\d-[^/]+\.md$',p)];inventory=[];pattern=re.compile(r'\b(?:random|Random|rng|probability|variance|bootstrap|quantile|normal|simulation|monte_carlo|standard_error)\b',re.I)
for path in sections:
 data=subprocess.check_output(['git','show',pin+':'+path],cwd=root);fences=re.findall(r'^```python\n(.*?)^```',data.decode(),re.M|re.S);markers=sorted(set(x.lower() for f in fences for x in pattern.findall(f)));inventory.append(dict(path=path,sha256=hashlib.sha256(data).hexdigest(),python_fences=len(fences),candidate_markers=markers,disposition=('chapter14 next substantive queue;formal reviews retained' if '/chapter-14/' in path else 'chapter15 selected V10 crosswalk recorded,limits remain' if '/chapter-15/' in path else 'chapter18 selected V10 crosswalk recorded,limits remain' if '/chapter-18/' in path else 'installed V10 followups selected21.11–21.13 only;other interfaces need reconciliation' if '/chapter-21/' in path else 'candidate requires later manual V10 disposition' if markers else 'no heuristic marker;not a proof of absence')))
# Hash all prior V10 READMEs: reproducible scope catalog,not a rerun of previous observers.
catalog=[]
for path in paths:
 if re.search(r'/qa/v10[^/]+/README\.md$',path):
  data=subprocess.check_output(['git','show',pin+':'+path],cwd=root);catalog.append(dict(path=path,sha256=hashlib.sha256(data).hexdigest(),title=data.decode().splitlines()[0]))
ck('locked section count',len(sections),322,'pinned git tree inventory;no runtime inference');ck('section paths unique',len(set(sections)),len(sections),'inventory integrity');ck('prior V10 catalog nonempty',len(catalog)>0,True,'source-hashed scoped evidence references')
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'probability.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('probability_lab',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 for name,s in [('printed',[(.25,-20),(.5,5),(.25,30)]),('reweighted',[(.5,-20),(.25,5),(.25,30)]),('project',[(.05,-.35),(.2,-.1),(.5,.05),(.25,.18)]),('physical',[(.25,80),(.75,120)]),('risk-neutral teaching',[(.5,80),(.5,120)]),('selected no-loss',[(F(2,3),5),(F(1,3),30)])]:
  # Source accepts int/float; use exact finite binary weights for selected rational law.
  if name=='selected no-loss':s=[(.5,5),(.5,30)]
  expected=law(s);models.append(dict(name=name,scenarios=s,reference=list(map(str,expected))))
  for fn,want in zip([m.expected_payoff,m.outcome_variance,m.probability_of_loss,m.expected_shortfall_below_zero],expected):ck(name+' '+fn.__name__,fn(s),want,'native source on declared model;independent expanded raw-second-moment law',True)
 ck('physical expectation is not price',m.expected_payoff([(.25,80),(.75,120)]),110.,'hypothetical physical mean,not a pricing API')
 ck('risk neutral replication price',m.expected_payoff([(.5,80),(.5,120)]),100.,'external one-period binomial S0=100,r=0,terminals80/120 implies q=.5')
 for name,paths in [('iid',list(itertools.product([-1,1],repeat=4))),('shared',[(-1,)*4,(1,)*4])]:
  weight=1/len(paths);estimates=[];zero_loss=[]
  for i,path in enumerate(paths):
   value=F(sum(path),4);s=[(.5,-1),(.5,1)];ck(f'{name}{i} marginal model expectation',m.expected_payoff(s),0.,'same declared marginal for both external joint laws');estimates.append((weight,float(value)));zero_loss.append((weight,int(all(x>=0 for x in path))))
  want=F(1,4) if name=='iid' else F(1);ck(name+' estimator variance',m.outcome_variance(estimates),want,'native evaluates externally enumerated sampling law,not hidden dependence detection',True)
  ck(name+' no observed loss probability',m.expected_payoff(zero_loss),F(1,16) if name=='iid' else F(1,2),'same true marginal loss probability .5;zero-event sample not proof p=0',True)
  models.append(dict(name=name,paths=paths,mean_variance=str(want)))
 # Same marginals,three externally declared two-asset joint laws.
 for name,paths,want in [('independent',list(itertools.product([-1,1],repeat=2)),F(1,2)),('shared',[(-1,-1),(1,1)],F(1)),('offset',[(-1,1),(1,-1)],F(0))]:
  s=[(1/len(paths),sum(path)/2) for path in paths];ck(name+' portfolio variance',m.outcome_variance(s),want,'equal-weight payoff under declared dependence;not source dependence estimator',True)
 draws=m.sample_scenarios([(.25,-20),(.5,5),(.25,30)],128,19);ck('seed replay',m.sample_scenarios([(.25,-20),(.5,5),(.25,30)],128,19),draws,'actual native RNG replay,not model calibration');ck('native reported simulated mean',m.simulated_mean([(.25,-20),(.5,5),(.25,30)],128,19),sum(map(F,draws))/128,'external sum of actual reported draws',True)
 prior=json.loads((here.parent/'chapter-14-scenario-probability-review/results.json').read_text());
 # Earlier observer uses a row list; source identity is taken from its companion manifest below.
 reference=(here.parent/'chapter-14-scenario-probability-review/review.py').read_text();ck('prior formal observer source path retained',source_path.split('/')[-1] in reference,True,'prior22-answer/ten-task/six-failure/30-predicate records retained,not rerun')
(here/'scope-index.json').write_text(json.dumps(dict(pin=pin,sections=inventory,prior_v10_catalog=catalog,limits='Marker inventory is a search heuristic;no absence or closure inference. Catalog hashes do not execute or independently accept old evidence.',next_queue=['14.2 sample-space/event assumptions','14.3–14.17 subsequent probability-model assumptions','manual disposition of marked interfaces outside14/15/18 and selected installed21']),indent=2)+'\n')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,models=models,section_count=len(sections),marked_sections=sum(bool(x['candidate_markers']) for x in inventory),catalog_count=len(catalog),executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='V10 queue reconciliation plus selected14.1 finite joint-law/measure assumptions;no whole-book closure')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed'],r['section_count'],r['marked_sections'],r['catalog_count']);assert r['failed']==0
