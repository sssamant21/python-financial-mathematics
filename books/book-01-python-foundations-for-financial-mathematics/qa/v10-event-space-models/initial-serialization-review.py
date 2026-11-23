"""Finite event algebra versus joint-law/partition/sample-space assumptions."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='3938c931d4abccfc314e197e1ed2f75afe0acca4';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-14/14.02-sample-spaces-and-events.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def probability(w,event):return sum(F(str(w[s])) for s in event)/sum(map(lambda x:F(str(x)),w.values()))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'events.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('event_lab',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 axes=[['up','down'],['pay','default']];space=m.sample_space(*axes);expected=(('up','pay'),('up','default'),('down','pay'),('down','default'));ck('ordered product labels',space,expected,'independent explicit outcome tuple;no probability assignment implied')
 weights=dict(zip(expected,[.5,.1,.2,.2]));events=[frozenset(space[i] for i in range(4) if mask&(1<<i)) for mask in range(16)]
 for i,a in enumerate(events):
  complement=frozenset(s for s in space if s not in a);ck(f'event{i} probability',m.probability(weights,a),probability(weights,a),'exact normalized atom sum',True);ck(f'event{i} complement',m.complement(space,a),complement,'membership oracle');ck(f'event{i} complement probability',m.probability(weights,complement),1-probability(weights,a),'declared full finite universe',True)
  for j,b in enumerate(events):
   union=frozenset(s for s in space if s in a or s in b);intersection=frozenset(s for s in space if s in a and s in b)
   ck(f'pair{i},{j} union',m.union(a,b),union,'membership rather than source set-operator implementation');ck(f'pair{i},{j} intersection',m.intersection(a,b),intersection,'membership oracle');ck(f'pair{i},{j} disjoint',m.disjoint(a,b),not any(s in a and s in b for s in space),'set disjointness,not probabilistic independence');ck(f'pair{i},{j} inclusion-exclusion',m.probability(weights,m.union(a,b)),probability(weights,a)+probability(weights,b)-probability(weights,intersection),'external rational law',True)
 # Same abstract product labels admit different joint probabilities.
 for name,w in [('independent',[.25,.25,.25,.25]),('shared',[.5,0.,0.,.5]),('offset',[0.,.5,.5,0.])]:
  law=dict(zip(space,w));a=m.event(space,lambda s:s[0]=='down');b=m.event(space,lambda s:s[1]=='default');ck(name+' marginal A',m.probability(law,a),.5,'caller-supplied joint law');ck(name+' marginal B',m.probability(law,b),.5,'same marginals');joint=m.probability(law,m.intersection(a,b));ck(name+' joint',joint,{'independent':.25,'shared':.5,'offset':0.}[name],'product sample-space construction does not impose independence');records.append(dict(name=name,weights=w,joint=joint))
 zero={space[0]:1.,space[1]:0.,space[2]:0.,space[3]:0.};ck('nonempty zero-mass event',m.probability(zero,{space[1]}),0.,'zero probability need not mean empty event');ck('zero-mass event overlaps itself',m.disjoint({space[1]},{space[1]}),False,'set disjointness differs from a probability-zero intersection')
 # Refinement preserves default event mass but identifies additional severity outcomes.
 fine={'no default':.75,'default recovery high':.2,'default recovery low':.05};default={'default recovery high','default recovery low'};coarse={'no default':.75,'default':.25};ck('coarse/fine default probability',m.probability(fine,default),m.probability(coarse,{'default'}),'consistent pushforward of an externally defined refinement');ck('low recovery mass',m.probability(fine,{'default recovery low'}),.05,'coarse binary event has no native severity field')
 ck('supplied partial universe complement',m.complement(['up','flat'],{'up'}),frozenset({'flat'}),'complement is relative to caller universe;missing down is not detected');ck('event union permits unrecognized labels',m.union({'up'},{'missing'}),frozenset({'up','missing'}),'raw set operations do not validate a universe')
 def exception(fn):
  try:fn()
  except ValueError:return 'ValueError'
  return 'accepted'
 ck('probability rejects unknown union label',exception(lambda:m.probability({'up':.5,'down':.5},m.union({'up'},{'missing'}))),'ValueError','probability validates supplied distribution membership')
 selected={'up':.625,'down':.375};full={'up':.5,'flat':.2,'down':.3};ck('full down mass',m.probability(full,{'down'}),.3,'full declared universe');ck('conditioned down mass',m.probability(selected,{'down'}),F(3,8),'external selection excludes flat and renormalizes,changes question',True)
 prior=json.loads((here.parent/'chapter-14-sample-spaces-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F111 five initial failures/34 predicates/24 answers/ten tasks retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,models=records,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected finite event/model/partition assumptions;not actual market completeness,calibration,independent/platform acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
