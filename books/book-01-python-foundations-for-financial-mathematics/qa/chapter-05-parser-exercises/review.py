"""Original schedule parser plus explicit scalar grammar, character limit and exporter."""
import copy,hashlib,io,json,platform,re,subprocess,sys,tempfile,types,os
from pathlib import Path
from datetime import date,datetime
from decimal import Decimal as D
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.03-*.md'))
BLOCKS=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S)
M=types.ModuleType('original_schedule_parser');exec(compile(BLOCKS[3],str(SOURCE),'exec'),M.__dict__)

def finite_amount(value):
 """Separate signed numeric domain: exact finite Decimal, zero allowed."""
 if type(value) is not D:raise TypeError('exact Decimal required')
 if not value.is_finite():raise ValueError('finite amount required')
 return value

def strict_amount(text):
 """ASCII signed ordinary decimal; no exponents/underscores, padding or leading zeros."""
 if type(text) is not str:raise TypeError('exact string required')
 if re.fullmatch(r'[+-]?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?',text) is None:raise ValueError('strict decimal spelling required')
 return finite_amount(D(text))

def limited_parse(payload,*,maximum_chars=4096):
 """Limit decoded string characters before calling unchanged JSON schedule parser."""
 if type(payload) is not str:raise TypeError('exact payload string required')
 if type(maximum_chars) is not int:raise TypeError('exact integer limit required')
 if maximum_chars<1:raise ValueError('positive limit required')
 if len(payload)>maximum_chars:raise ValueError('payload character limit exceeded')
 return M.parse_schedule(payload)

def export_schedule(value):
 """Narrow canonical investor schedule to explicit wire strings, no floats/lossy extras."""
 if type(value) is not dict:raise TypeError('exact canonical dictionary required')
 if set(value)!={'schedule_id','currency','perspective','events'}:raise ValueError('canonical fields required')
 sid=M.checked_text(value['schedule_id'],'schedule_id');currency=M.checked_text(value['currency'],'currency')
 if currency not in {'USD','EUR'}:raise ValueError('unsupported currency')
 if M.checked_text(value['perspective'],'perspective')!='investor':raise ValueError('investor perspective required')
 if type(value['events']) is not list:raise TypeError('exact events list required')
 rows=[]
 for row in value['events']:
  if type(row) is not dict:raise TypeError('exact event dictionary required')
  if set(row)!={'event_id','payment_date','amount'}:raise ValueError('canonical event fields required')
  eid=M.checked_text(row['event_id'],'event_id');payment=row['payment_date'];amount=finite_amount(row['amount'])
  if type(payment) is not date:raise TypeError('exact date required')
  rows.append(dict(event_id=eid,payment_date=payment.isoformat(),amount=str(amount)))
 wire=json.dumps(dict(schedule_id=sid,currency=currency,events=rows),ensure_ascii=False,allow_nan=False)
 M.parse_schedule(wire) # complete original identity/schema validation before return
 return wire

def run():
 checks=[]
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,kind,fn):
  try:fn();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,'rejection',actual,kind)
 wire=M.wire_schedule();raw=json.dumps(wire);baseline=M.parse_schedule(raw)
 bad=copy.deepcopy(wire);bad['events'][0]['extra']=1;err('5.3-E1','ValueError',lambda:M.parse_schedule(json.dumps(bad)))
 for text,expected in [('0',D(0)),('-0.00',D('-0.00')),('+12.50',D('12.50')),('-1000',D(-1000)),('0.125',D('.125'))]:ck('5.3-E2','strict lexical acceptance '+text,strict_amount(text).as_tuple(),expected.as_tuple())
 for text in ['1e3','1_000','NaN','Infinity',' 1','1 ','01','.5','1.','١٢'] :err('5.3-E2','ValueError',lambda text=text:strict_amount(text))
 err('5.3-E2','TypeError',lambda:strict_amount(1))
 for value in [D('NaN'),D('sNaN'),D('Infinity'),D('-Infinity')]:err('5.3-E2','ValueError',lambda value=value:finite_amount(value))
 for value in [None,True,1,1.0,'1']:err('5.3-E2','TypeError',lambda value=value:finite_amount(value))
 ck('5.3-E2','signed finite numeric domain',finite_amount(D('-2.5')),D('-2.5'))
 ck('5.3-E2','original broad grammar unchanged',M.parse_schedule(json.dumps(dict(wire,events=[dict(wire['events'][0],amount='1e3')])) )['events'][0]['amount'],D(1000))
 ck('5.3-E3','exact character boundary',limited_parse(raw,maximum_chars=len(raw)),baseline);err('5.3-E3','ValueError',lambda:limited_parse(raw,maximum_chars=len(raw)-1))
 original=M.parse_schedule;calls=[]
 def counted(payload):calls.append(payload);return original(payload)
 M.parse_schedule=counted
 try:err('5.3-E3','ValueError',lambda:limited_parse('{'*4097));ck('5.3-E3','oversized invalid JSON never decoded',calls,[])
 finally:M.parse_schedule=original
 for limit,kind in [(True,'TypeError'),(0,'ValueError'),(-1,'ValueError')]:err('5.3-E3',kind,lambda limit=limit:limited_parse(raw,maximum_chars=limit))
 unicode_raw=json.dumps(dict(wire,schedule_id='SCH-é'),ensure_ascii=False);ck('5.3-E3','character count distinct from UTF8 bytes',len(unicode_raw.encode('utf-8'))>len(unicode_raw),True);ck('5.3-E3','unicode at character boundary',limited_parse(unicode_raw,maximum_chars=len(unicode_raw))['schedule_id'],'SCH-é')
 commands=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 with tempfile.TemporaryDirectory(prefix='parser-exercises-') as tmp:
  folder=Path(tmp);source=folder/'standard_library_lab.py';source.write_text(BLOCKS[3]);intro=folder/'intro.py';intro.write_text('\n'.join(BLOCKS[:3]))
  for label,filename,count in [('exact original suite',source,9),('three exact introductory blocks in order',intro,None)]:
   r=subprocess.run([sys.executable,'-B',str(filename)],cwd=folder,env=env,text=True,capture_output=True,timeout=30);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0 and (actual==count and bool(re.search(r'^OK\s*$',log,re.M)) if count else r.stdout==r.stderr=='');commands.append(dict(label=label,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,method_count=actual,status='PASS' if ok else 'FAIL'))
  path=folder/'malformed.json';path.write_text('{"schedule_id":"SCH-é",',encoding='utf-8');saved=path.read_bytes();err('5.3-E4','JSONDecodeError',lambda:M.read_schedule(path));ck('5.3-E4','valid UTF8 read preserved',path.read_bytes(),saved)
 bad=copy.deepcopy(wire);bad['events'][-1]['payment_date']='2027-02-29';bad_text=json.dumps(bad);saved=bad_text;err('5.3-E5','ValueError',lambda:M.parse_schedule(bad_text));ck('5.3-E5','input text unchanged',bad_text,saved);ck('5.3-E5','earlier source event intact',json.loads(bad_text)['events'][0],wire['events'][0])
 before=copy.deepcopy(baseline);encoded=export_schedule(baseline);ck('5.3-E6','typed round trip',M.parse_schedule(encoded),baseline);ck('5.3-E6','amount scale retained',json.loads(encoded)['events'][2]['amount'],'1040.00');ck('5.3-E6','canonical source unchanged',baseline,before)
 special=copy.deepcopy(baseline);special['events'][0]['amount']=D('-0.00');special['events'][1]['amount']=D('1E+3');special['events'][2]['amount']=D('0.12345678901234567890');decoded=M.parse_schedule(export_schedule(special));ck('5.3-E6','exact Decimal tuples without floats',[r['amount'].as_tuple() for r in decoded['events']],[r['amount'].as_tuple() for r in special['events']])
 empty=dict(schedule_id='EMPTY',currency='EUR',perspective='investor',events=[]);ck('5.3-E6','empty identity round trip',M.parse_schedule(export_schedule(empty)),empty)
 for changes,kind in [({'payment_date':datetime(2028,2,29)},'TypeError'),({'amount':1.25},'TypeError'),({'amount':D('Infinity')},'ValueError'),({'extra':1},'ValueError')]:
  bad=copy.deepcopy(baseline);bad['events'][0].update(changes);err('5.3-E6',kind,lambda bad=bad:export_schedule(bad))
 bad=copy.deepcopy(baseline);bad['events'][1]['event_id']='E0';err('5.3-E6','ValueError',lambda:export_schedule(bad))
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,source=str(SOURCE.relative_to(BOOK)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),code_sha256=[hashlib.sha256(code.encode()).hexdigest() for code in BLOCKS],command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),existing_methods=sum(x['method_count'] or 0 for x in commands if x['status']=='PASS'),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),commands=commands,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('commands','checks','code_sha256')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
