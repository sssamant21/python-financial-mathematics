"""Structural requirement contracts;prior valuation evidence is mapped,not approval."""
from pathlib import Path
import sys,subprocess,tempfile,importlib,re,json,hashlib,platform,dataclasses
from fractions import Fraction
from decimal import Decimal,localcontext,Context
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-21/21.02-requirements-and-assumptions.md';raw=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();f=re.findall(r'```python\n(.*?)\n```',raw,re.S);assert len(f)==2
prior=json.loads((BOOK/'qa/chapter-21-requirements-resume/suite-results.json').read_text());digests=[hashlib.sha256(c.encode()).hexdigest() for c in f];assert digests==prior['fence_sha256'];assert all(c['returncode']==0 for c in prior['commands'])
arch=json.loads((BOOK/'qa/chapter-21-architecture-review/results.json').read_text());ap=BOOK/'chapter-21/21.01-capstone-architecture.md';assert arch['fence_sha256']==[hashlib.sha256(c.encode()).hexdigest() for c in re.findall(r'```python\n(.*?)\n```',ap.read_text(),re.S)]
assert all(x['passed'] for x in arch['source_predicates']);rows=[];commands=[];limits=[]
def check(name,fn,want):
 try:a=fn();ok=a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for name,code in zip(['requirements_check.py','test_requirements_check.py'],f):(t/name).write_text(code)
 sys.path.insert(0,tmp);m=importlib.import_module('requirements_check')
 def record(**kw):
  fields=dict(identifier='R-SYNTH',statement='Synthetic structural probe only',criterion='not an authentic acceptance record',method='structural check');fields.update(kw);return m.Requirement(**fields)
 check('default not_run valid',lambda:m.validate_requirement(record()),None)
 for status in ['not_run','blocked','passed','failed']:
  q=record(status=status,evidence='synthetic-only' if status in ('passed','failed') else '')
  check('valid status '+status,lambda q=q:m.validate_requirement(q),None);check('readiness '+status,lambda q=q:m.ready_for_review([q]),status=='passed')
 for field in ['identifier','statement','criterion','method']:
  for value in ['',None,True]:check(field+' rejects '+repr(value),lambda f=field,v=value:m.validate_requirement(record(**{f:v})),'ValueError')
 for label,kw in [('unknown status',dict(status='approved')),('bool status',dict(status=True)),('nonstring evidence',dict(evidence=None)),('passed blank',dict(status='passed',evidence=' ')),('failed blank',dict(status='failed',evidence=''))]:check(label,lambda kw=kw:m.validate_requirement(record(**kw)),'ValueError')
 for label,qs in [('empty',[]),('tuple',(record(),)),('None',None),('invalid later',[record(),record(status='failed',evidence='')])]:check('container '+label,lambda qs=qs:m.ready_for_review(qs),'ValueError')
 q=record();copy=dataclasses.asdict(q);m.ready_for_review([q]);check('caller record unchanged',lambda:dataclasses.asdict(q),copy);check('normal frozen reassignment',lambda:setattr(q,'status','passed'),'FrozenInstanceError')
 fake=record(status='passed',evidence='synthetic-not-authentic-evidence');limits.append(dict(name='documented structural gate permits unauthenticated evidence strings',actual=m.ready_for_review([fake]),status='Documented design limitation;not financial/model acceptance.'))
 limits.append(dict(name='duplicate identifiers not validated',actual=m.ready_for_review([fake,fake]),status='No uniqueness contract;separate design observation,not failed financial case.'))
 if not REV:
  for label,args in [('optimized reference suite',['-O','-m','unittest','-v','test_requirements_check']),('quiet import/root state',['-c','import logging;before=(list(logging.getLogger().handlers),logging.getLogger().level);import requirements_check;assert before==(list(logging.getLogger().handlers),logging.getLogger().level)'])]:
   argv=[sys.executable]+args;z=subprocess.run(argv,cwd=t,capture_output=True,text=True);commands.append(dict(label=label,argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 sys.path.pop(0)
with localcontext(Context(prec=80)):
 monthly=(Decimal(28)/25)**(Decimal(1)/12)-1
 supplemental=dict(name='independent effective monthly rate',actual=str(monthly),printed_percent='0.948879',passed=abs(monthly*100-Decimal('.948879'))<Decimal('.0000005'))
d=dict(selected_revision=REV,python=sys.version,platform=platform.platform(),fence_sha256=digests,source_predicates=rows,new_commands=commands,reused_documented_commands=3,reused_structural_probe_commands=1,reused_requirements_source_revision=prior['source_revision'],reused_valuation_evidence='../chapter-21-architecture-review/results.json',reused_valuation_predicates=36,design_observations=limits,supplemental_arithmetic=supplemental,existing_unique_methods=12,new_method_invocations=12 if not REV else 0,reused_method_invocations=12,new_historical_unique_methods=0,limits='Bookkeeping source execution and mapped prior valuation evidence;not evidence authentication,owner/independent acceptance,operational store,full toolkit,installed artifact,security/platform/release acceptance. F28/F32 and other findings remain.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'structural source predicates;2design observations;1supplemental monthly reference;',len(commands),'newcommands;3documented commands reused');assert all(x['passed'] for x in rows) and supplemental['passed'] and all(x['returncode']==0 for x in commands)
