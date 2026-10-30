"""Original schedule utilities and explicitly supplemental cutoff/count/adapter tasks."""
import copy,hashlib,json,os,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from datetime import date,datetime
from decimal import Decimal as D
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
def load(n,index=0):
 p=next((BOOK/'chapter-05').glob(f'5.{n:02}-*.md'));blocks=re.findall(r'^```python\n(.*?)^```',p.read_text(),re.M|re.S);m=types.ModuleType('source_'+str(n));exec(compile(blocks[index],str(p),'exec'),m.__dict__);return m,p,blocks
U,P4,B4=load(4);P,P3,B3=load(3,3)
SECOND='''from datetime import date
from decimal import Decimal
import schedule_utils

def sample_eur():
    return dict(schedule_id='SCH-EUR',currency='EUR',perspective='investor',events=[
        dict(event_id='E-PAY',payment_date=date(2027,1,15),amount=Decimal('-100')),
        dict(event_id='E-ZERO',payment_date=date(2028,2,29),amount=Decimal('0')),
        dict(event_id='E-RECEIVE',payment_date=date(2028,2,29),amount=Decimal('109.5'))])

def main():
    result=schedule_utils.events_on_or_after(sample_eur(),date(2028,2,29))
    print(result['currency']+' selected IDs: '+', '.join(r['event_id'] for r in result['events']))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
'''
def events_before(value,cutoff):
 """Strictly before cutoff, all input validated; retain empty wrapper, fresh owned rows."""
 if type(cutoff) is not date:raise TypeError('exact date cutoff required')
 result=U.normalize_schedule(value)
 result['events']=[row for row in result['events'] if row['payment_date']<cutoff]
 return result

def count_events(value):
 """Return validated event cardinality with metadata; not a money or settled count."""
 result=U.normalize_schedule(value)
 return dict(schedule_id=result['schedule_id'],currency=result['currency'],perspective=result['perspective'],event_count=len(result['events']))

def adapt_canonical(value):
 """5.3 canonical fields already match5.4; delegate full validation and fresh sorting."""
 return U.normalize_schedule(value)

def run():
 checks=[];commands=[]
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,kind,fn):
  try:fn();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,'rejection',actual,kind)
 sample=dict(schedule_id='SCH-01',currency='USD',perspective='investor',events=[dict(event_id='E2',payment_date=date(2028,1,15),amount=D(1000)),dict(event_id='E0',payment_date=date(2027,1,15),amount=D(-1000)),dict(event_id='E1',payment_date=date(2028,1,15),amount=D(0))]);saved=copy.deepcopy(sample)
 for changes,kind in [({'event_id':1},'TypeError'),({'extra':1},'ValueError')]:
  bad=copy.deepcopy(sample);bad['events'][0].update(changes);before=copy.deepcopy(bad);err('5.4-E1',kind,lambda bad=bad:U.normalize_schedule(bad));ck('5.4-E1','failed input preserved',bad,before)
 for cutoff,ids in [(date(2026,1,1),[]),(date(2027,1,15),[]),(date(2028,1,15),['E0']),(date(2028,1,16),['E0','E1','E2'])]:ck('5.4-E2','exclusive cutoff '+str(cutoff),[r['event_id'] for r in events_before(sample,cutoff)['events']],ids)
 empty=dict(schedule_id='EMPTY',currency='EUR',perspective='investor',events=[]);ck('5.4-E2','empty identity',events_before(empty,date(2028,1,1)),empty)
 for cutoff in [None,'2028-01-15',datetime(2028,1,15)]:err('5.4-E2','TypeError',lambda cutoff=cutoff:events_before(sample,cutoff))
 bad=copy.deepcopy(sample);bad['events'][0]['amount']=D('NaN');err('5.4-E2','ValueError',lambda:events_before(bad,date(2026,1,1)))
 out=events_before(sample,date(2029,1,1));out['events'][0]['amount']=D(99);ck('5.4-E2','output ownership',sample,saved)
 reverse=copy.deepcopy(sample);reverse['events'].reverse();ck('5.4-E4','order invariant',U.normalize_schedule(reverse),U.normalize_schedule(sample));ck('5.4-E4','canonical IDs',[r['event_id'] for r in U.normalize_schedule(sample)['events']],['E0','E1','E2']);ck('5.4-E4','original order intact',[r['event_id'] for r in sample['events']],['E2','E0','E1'])
 ck('5.4-E5','all events including zero',count_events(sample),dict(schedule_id='SCH-01',currency='USD',perspective='investor',event_count=3));ck('5.4-E5','empty count',count_events(empty),dict(schedule_id='EMPTY',currency='EUR',perspective='investor',event_count=0));bad=copy.deepcopy(sample);bad['events'][0]['event_id']='E0';err('5.4-E5','ValueError',lambda:count_events(bad))
 canonical=P.parse_schedule(json.dumps(P.wire_schedule()));before=copy.deepcopy(canonical);adapted=adapt_canonical(canonical)
 ck('5.4-E6','matching wrapper fields',set(canonical),{'schedule_id','currency','perspective','events'});ck('5.4-E6','matching event fields',[set(x) for x in canonical['events']],[{'event_id','payment_date','amount'}]*3)
 ck('5.4-E6','explicit canonical values',[(r['event_id'],r['payment_date'],r['amount']) for r in adapted['events']],[('E0',date(2027,1,15),D(-1000)),('E1',date(2028,2,29),D(0)),('E2',date(2028,2,29),D('1040.00'))]);ck('5.4-E6','parent identity',(adapted['schedule_id'],adapted['currency'],adapted['perspective']),('SCH-01','USD','investor'));ck('5.4-E6','exact scalar types',[(type(r['payment_date']) is date,type(r['amount']) is D) for r in adapted['events']],[(True,True)]*3);adapted['events'][0]['amount']=D(99);ck('5.4-E6','adapter ownership',canonical,before)
 bad=copy.deepcopy(canonical);bad['extra']=1;err('5.4-E6','ValueError',lambda:adapt_canonical(bad))
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 with tempfile.TemporaryDirectory(prefix='utility-exercises-') as tmp:
  folder=Path(tmp)
  for name,code in zip(['schedule_utils.py','run_schedule.py','test_schedule_utils.py'],B4):(folder/name).write_text(code)
  (folder/'eur_runner.py').write_text(SECOND)
  for label,args,stdout,count in [('exact source suite',['test_schedule_utils.py'],None,9),('original caller',['run_schedule.py'],'Selected event IDs: E1, E2\n',None),('E3 second EUR caller',['eur_runner.py'],'EUR selected IDs: E-RECEIVE, E-ZERO\n',None),('quiet source and EUR imports',['-c','import schedule_utils,run_schedule,eur_runner'],'',None)]:
   r=subprocess.run([sys.executable,'-B',*args],cwd=folder,env=env,capture_output=True,text=True,timeout=30);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
   if stdout is not None:ok=ok and (r.stdout,r.stderr)==(stdout,'')
   if count:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M))
   commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_method_count=actual,status='PASS' if ok else 'FAIL'))
 ck('all','source input unchanged',sample,saved)
 sources=[dict(source=str(p.relative_to(BOOK)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),code_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in blocks]) for p,blocks in [(P4,B4),(P3,B3)]]
 result=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),existing_methods=sum(x['actual_method_count'] or 0 for x in commands if x['status']=='PASS'),sources=sources,supplement_second_runner=SECOND,checks=checks,commands=commands)
 (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('checks','commands','sources','supplement_second_runner')}));return bool(result['failed'] or result['command_failed'])
if __name__=='__main__':raise SystemExit(run())
