"""21.1 source contract checks;reuse prior documented suite by exact fence hash."""
from pathlib import Path
import subprocess,sys,re,tempfile,importlib,json,hashlib,math,platform,dataclasses
from fractions import Fraction
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
path=BOOK/'chapter-21/21.01-capstone-architecture.md';rel=str(path.relative_to(ROOT));raw=subprocess.check_output(['git','show',REV+':'+rel],cwd=ROOT,text=True) if REV else path.read_text();f=re.findall(r'```python\n(.*?)\n```',raw,re.S);assert len(f)==2
prior=json.loads((BOOK/'qa/chapter-21-architecture-resume/suite-results.json').read_text());hashes=[hashlib.sha256(c.encode()).hexdigest() for c in f];assert hashes==prior['fence_sha256'];assert all(c['returncode']==0 for c in prior['commands'])
rows=[];commands=[]
def check(name,fn,want,tol=0.):
 try:a=fn();ok=isinstance(a,float) and math.isfinite(a) and math.isclose(a,want,rel_tol=5e-14,abs_tol=tol) if isinstance(want,float) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),absolute_tolerance=tol,relative_tolerance=5e-14 if isinstance(want,float) else None,passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 for name,code in zip(['capstone_architecture.py','test_capstone_architecture.py'],f):(p/name).write_text(code)
 sys.path.insert(0,tmp);m=importlib.import_module('capstone_architecture');R=m.ValuationRequest
 for i,(cash,rate) in enumerate([(110.,.1),(110.,0.),(95.,-.05),(-110.,.1),(0.,.1),(100.,.05),(100.,.1),(100.,10.),(math.ulp(0.),1.),(-0.,.1)]):
  want=float(Fraction(cash)/(1+Fraction(rate)));check('independent represented-input PV '+str(i),lambda c=cash,r=rate:m.present_value_one_period(c,r),want,1e-10 if abs(want)>1 else 0.)
 for name,request in [('not request',None),('integer payment',R(100,.1,'USD')),('bool payment',R(True,.1,'USD')),('nan payment',R(math.nan,.1,'USD')),('inf payment',R(math.inf,.1,'USD')),('integer rate',R(100.,0,'USD')),('bool rate',R(100.,True,'USD')),('nan rate',R(100.,math.nan,'USD')),('inf rate',R(100.,math.inf,'USD')),('boundary rate',R(100.,-1.,'USD')),('below rate',R(100.,-2.,'USD')),('blank label',R(100.,.1,' ')),('empty label',R(100.,.1,'')),('None label',R(100.,.1,None)),('nonstring label',R(100.,.1,123))]:check(name,lambda q=request:m.evaluate(q),'ValueError')
 for name,fn in [('public payment type',lambda:m.present_value_one_period(100,.1)),('public rate type',lambda:m.present_value_one_period(100.,True)),('public boundary',lambda:m.present_value_one_period(100.,-1.)),('overflow',lambda:m.evaluate(R(1e308,-.5,'USD')))]:check(name,fn,'ValueError')
 q=R(110.,.1,'  XYZ  ');before=dataclasses.asdict(q);res=m.evaluate(q)
 check('preserved metadata tuple',lambda:(res.currency,res.payment,res.rate,res.convention,res.model),('  XYZ  ',110.,.1,'one effective period','pv-one-v1'))
 check('caller request unchanged',lambda:dataclasses.asdict(q),before)
 check('request normal reassignment rejected',lambda:setattr(q,'payment',0.),'FrozenInstanceError');check('result normal reassignment rejected',lambda:setattr(res,'amount',0.),'FrozenInstanceError')
 check('positive rate direction',lambda:m.present_value_one_period(100.,.05)>m.present_value_one_period(100.,.1),True);check('negative rate direction',lambda:m.present_value_one_period(-100.,.05)<m.present_value_one_period(-100.,.1),True)
 check('scaling',lambda:m.present_value_one_period(220.,.1),200.,1e-10)
 if not REV:
  for label,args in [('optimized reference suite',['-O','-m','unittest','-v','test_capstone_architecture']),('quiet import root state',['-c','import logging;before=(list(logging.getLogger().handlers),logging.getLogger().level);import capstone_architecture;assert before==(list(logging.getLogger().handlers),logging.getLogger().level)'])]:
   argv=[sys.executable]+args;z=subprocess.run(argv,cwd=p,capture_output=True,text=True);commands.append(dict(label=label,argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 sys.path.pop(0)
d=dict(selected_revision=REV,source_path=rel,python=sys.version,platform=platform.platform(),fence_sha256=hashes,source_predicates=rows,new_commands=commands,reused_evidence='../chapter-21-architecture-resume/suite-results.json',reused_revision=prior['source_revision'],reused_commands=3,reused_methods=12,current_new_method_invocations=12 if not REV else 0,existing_unique_methods=12,new_historical_unique_methods=0,limits='Exact source contracts plus explicitly reused earlier execution;frozen dataclasses are not durable audit evidence. All-range numerical,installed-artifact,model/platform/security/release/independent acceptance open. F28/F32 and other findings retained.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates',len(commands),'new commands;3 prior commands verified by unchanged fence hashes');assert all(x['passed'] for x in rows) and all(x['returncode']==0 for x in commands)
