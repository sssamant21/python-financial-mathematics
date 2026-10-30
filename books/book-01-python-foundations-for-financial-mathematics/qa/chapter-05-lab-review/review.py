"""Reconstruct exact Sections5.1–5.5 listings and verify documented launch contracts."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
CONFIG={
 1:dict(files={'holdings_core.py':1,'run_holdings.py':2,'test_holdings_modules.py':3},test='test_holdings_modules.py',count=8,imports='import holdings_core, run_holdings',demos=[['run_holdings.py'],['-m','run_holdings']],stdout='Active IDs: SEC-A, SEC-C\n'),
 2:dict(files={'quantity_rules.py':0,'import_styles.py':1,'test_import_styles.py':2},test='test_import_styles.py',count=9,imports='import quantity_rules, import_styles',demos=[['import_styles.py'],['-m','import_styles']],stdout='Validated units: 12.5, 12.5, 12.5\n'),
 3:dict(files={'standard_library_lab.py':3},test='standard_library_lab.py',count=9,imports='import standard_library_lab',demos=[]),
 4:dict(files={'schedule_utils.py':0,'run_schedule.py':1,'test_schedule_utils.py':2},test='test_schedule_utils.py',count=9,imports='import schedule_utils, run_schedule',demos=[['run_schedule.py'],['-m','run_schedule']],stdout='Selected event IDs: E1, E2\n'),
 5:dict(files={'finance_lab/holdings.py':0,'finance_lab/views.py':1,'finance_lab/__init__.py':2,'finance_lab/__main__.py':3,'test_finance_lab.py':4},test='test_finance_lab.py',count=8,imports='import finance_lab, finance_lab.holdings, finance_lab.views, finance_lab.__main__',demos=[['-m','finance_lab']],stdout='Package active IDs: SEC-A, SEC-C\n')}
# Supplemental assertions consume published functions and explicit expectations;
# they are not replacement implementations or additional original test methods.
HOLDING_PROBE="""
from decimal import Decimal as D
rows=[dict(security_id='B',quantity=D(0)),dict(security_id='A',quantity=D('12.5'))]
assert capture_holdings(rows)==(('B',D(0)),('A',D('12.5')))
assert active_ids(rows)==('A',)
assert capture_holdings([])==() and active_ids([])==()
snapshot=capture_holdings(rows);rows[1]['quantity']=D(99)
assert snapshot==( ('B',D(0)),('A',D('12.5')) )
try: active_ids(rows+[dict(security_id='X',quantity=D('NaN'))])
except ValueError: pass
else: raise AssertionError('invalid later record must reject')
"""
PROBES={1:'from holdings_core import capture_holdings,active_ids\n'+HOLDING_PROBE,
5:'from finance_lab import capture_holdings,active_ids\n'+HOLDING_PROBE,
2:"""
from decimal import Decimal as D
import import_styles,quantity_rules
assert import_styles.validate_three_ways(D(0))==(D(0),D(0),D(0))
assert import_styles.validate_three_ways(D('12.5'))==(D('12.5'),)*3
assert import_styles.qr is quantity_rules
assert import_styles.validate_units is quantity_rules.checked_quantity
try: import_styles.validate_three_ways(True)
except TypeError: pass
else: raise AssertionError('bool is not exact Decimal')
""",
3:"""
import json
from datetime import date
from decimal import Decimal as D
from standard_library_lab import parse_schedule,wire_schedule
wire=wire_schedule();raw=json.dumps(wire);canonical=parse_schedule(raw)
assert [(r['event_id'],r['payment_date'],r['amount']) for r in canonical['events']]==[('E0',date(2027,1,15),D(-1000)),('E1',date(2028,2,29),D(0)),('E2',date(2028,2,29),D('1040.00'))]
assert raw==json.dumps(wire)
assert str(canonical['events'][2]['amount'])=='1040.00'
canonical['events'].clear();assert len(parse_schedule(raw)['events'])==3
# Broad Decimal lexical contract is deliberate, not a fixed-cents parser.
wire['events'][2]['amount']='1e3';assert parse_schedule(json.dumps(wire))['events'][2]['amount']==D(1000)
""",
4:"""
from datetime import date
from decimal import Decimal as D
from run_schedule import sample_schedule
from schedule_utils import normalize_schedule,events_on_or_after
source=sample_schedule();original=sample_schedule()
assert [(r['event_id'],r['amount']) for r in normalize_schedule(source)['events']]==[('E0',D(-1000)),('E1',D(0)),('E2',D(1000))]
assert [r['event_id'] for r in events_on_or_after(source,date(2028,1,15))['events']]==['E1','E2']
assert events_on_or_after(source,date(2028,1,16))==dict(schedule_id='SCH-01',currency='USD',perspective='investor',events=[])
assert source==original
"""}
def run():
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);records=[]
 for n,cfg in CONFIG.items():
  source=next((BOOK/'chapter-05').glob(f'5.{n:02}-*.md'));blocks=re.findall(r'^```python\n(.*?)^```',source.read_text(),re.M|re.S);operations=[]
  with tempfile.TemporaryDirectory(prefix=f'chapter5-{n}-') as tmp:
   folder=Path(tmp);files=[]
   for name,index in cfg['files'].items():
    p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(blocks[index]);files.append(dict(path=name,python_fence_index=index,sha256=hashlib.sha256(blocks[index].encode()).hexdigest()))
   def command(label,args,stdout=None,count=None,expected_error=None):
    r=subprocess.run([sys.executable,'-B',*args],cwd=folder,env=env,capture_output=True,text=True,timeout=60);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None
    ok=r.returncode==0
    if expected_error is not None:ok=r.returncode!=0 and r.stdout=='' and expected_error in r.stderr
    if stdout is not None:ok=ok and r.stdout==stdout and r.stderr==''
    if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M)) and not re.search(r'skipped=',log)
    operations.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_count=count,actual_count=actual,status='PASS' if ok else 'FAIL'))
   command('documented direct suite',[cfg['test']],count=cfg['count'])
   for demo in cfg['demos']:command('documented demo / module parity',demo,stdout=cfg['stdout'])
   command('fresh quiet import',['-c',cfg['imports']],stdout='')
   command('supplemental contract assertions',['-c',PROBES[n]],stdout='')
   if n==5:command('expected wrong plain-file package launch',['finance_lab/__main__.py'],expected_error='attempted relative import with no known parent package')
  records.append(dict(section=f'5.{n}',source=str(source.relative_to(BOOK)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),files=files,operations=operations))
 operations=[op for r in records for op in r['operations']];out=dict(python=platform.python_version(),platform=platform.platform(),lab_records=5,command_records=len(operations),passed=sum(x['status']=='PASS' for x in operations),failed=sum(x['status']=='FAIL' for x in operations),existing_method_invocations=sum(x['actual_count'] or 0 for x in operations),records=records)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'}));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
