"""Exact manuscript source,events and numeric controls;local synthetic handlers only."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,math,logging
from fractions import Fraction
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.10-logging.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];commands=[];rows=[];events=[]
def test(name,fn,want,tol=0):
 try:a=fn();ok=math.isclose(a,want,rel_tol=0,abs_tol=tol) if tol else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),absolute_tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'financial_logging.py';src.write_text(code)
 quiet='import logging;before=(list(logging.getLogger().handlers),logging.getLogger().level);import financial_logging;assert before==(list(logging.getLogger().handlers),logging.getLogger().level)'
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','financial_logging']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import/root state',[sys.executable,'-c',quiet]),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('logging_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 class Capture(logging.Handler):
  def __init__(self):super().__init__();self.records=[]
  def emit(self,r):self.records.append(dict(level=r.levelname,message=r.getMessage(),exception_info=r.exc_info is not None))
 def observe(name,runid,flows,rate):
  logger=m.LOGGER;old=(list(logger.handlers),logger.level,logger.propagate,logger.disabled);handler=Capture();logger.handlers=[handler];logger.setLevel(logging.INFO);logger.propagate=False;logger.disabled=False
  try:a=m.run_calculation(runid,flows,rate)
  except Exception as e:a=type(e).__name__
  finally:logger.handlers,logger.level,logger.propagate,logger.disabled=old
  events.append(dict(name=name,actual=repr(a),records=handler.records));return a,handler.records
 for name,flows,rate in [('zero NPV',[-100,110],.1),('negative rate',[0,95],-.05),('negative flow',[0,-110],.1),('zero rate',[0,100],0),('ordinary',[5,-7,9],-.1)]:
  ref=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction()));a,logs=observe(name,'run_1',flows,rate);test(name,lambda a=a:a,ref,1e-10);test(name+' start/completion',lambda logs=logs:[x['message'].split()[0] for x in logs],['calculation_started','calculation_completed'])
 for name,flows,rate in [('empty',[],0),('bool',[True],0),('string',['private_raw_value'],0),('NaN',[math.nan],0),('infinite rate',[1],math.inf),('boundary',[1],-1),('oversized flow',[10**1000],0),('oversized rate',[1],10**1000)]:
  a,logs=observe(name,'run_1',flows,rate);test(name+' category',lambda a=a:a,'ValueError');test(name+' logged rejection',lambda logs=logs:[(x['level'],x['message'].split()[0],x['message'].split()[-1]) for x in logs],[('INFO','calculation_started','run_id=run_1'),('WARNING','calculation_rejected','category=invalid_input')])
 for name,flows,rate in [('exponential overflow',[0]*1000+[1],-.9),('sum overflow',[1e308,1e308],0)]:
  a,logs=observe(name,'run_1',flows,rate);test(name+' category',lambda a=a:a,'ArithmeticError');test(name+' log',lambda logs=logs:[(x['level'],x['message'].split()[0]) for x in logs],[('INFO','calculation_started'),('ERROR','calculation_failed')])
 for runid in ['', 'bad\nline','x'*33,'private secret',True]:
  a,logs=observe('runid '+repr(runid),runid,[1],0);test('runid rejected '+repr(runid),lambda a=a:a,'ValueError');test('invalid runid emits nothing '+repr(runid),lambda logs=logs:logs,[])
 for runid in ['x','A'*32,'run-1_2']:
  a,logs=observe('valid runid',runid,[1],0);test('valid runid '+runid,lambda a=a:a,1.)
 a,logs=observe('private numeric sentinel','run_1',[987654321.123],.123456789);test('no raw numeric/result sentinel',lambda:all('987654321' not in x['message'] and '0.123456789' not in x['message'] for x in logs),True)
 test('no raw text sentinel',lambda:all('private_raw_value' not in x['message'] for e in events for x in e['records']),True);test('no emitted exception info',lambda:not any(x['exception_info'] for e in events for x in e['records']),True)
 def broken():
  yield 1
  raise RuntimeError('private iterator error')
 a,logs=observe('unknown iterator failure','run_1',broken(),0);test('unknown failure propagates',lambda:a,'RuntimeError');test('unknown failure only start',lambda:[x['message'].split()[0] for x in logs],['calculation_started'])
 original=[-100,110];m.calculate_npv(original,.1);test('caller unchanged',lambda:original,[-100,110])
 test('generator accepted',lambda:m.calculate_npv(iter([-100,110]),.1),0,1e-10)
d=dict(candidate_based_on='c7d5060fc6bf7a8f01f7a91dd6651b7bccb25e1c',selected_revision=REV,python=sys.version,manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,actual_event_records=events,existing_unique_methods=12,method_invocations=36,new_historical_unique_methods=0,limits='Local synthetic handler events/input/ordinary NPV only;no persistence,delivery,privacy/compliance,all-range NPV,platform or independent acceptance. F28/F32/F209 and broader gaps open.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;5 commands');assert all(x['passed'] for x in rows) and all(x['returncode']==0 for x in commands)
