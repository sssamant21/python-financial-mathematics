"""Eight Section5.1 prompts: exact source, new caller, deliberate mutation and restore."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.01-*.md'))
SECOND='''from decimal import Decimal
import holdings_core

def sample_holdings():
    return [dict(security_id='Q',quantity=Decimal(0)),dict(security_id='Z',quantity=Decimal('2.5')),dict(security_id='Y',quantity=Decimal(4))]

def main():
    rows=sample_holdings()
    print('Second IDs: '+', '.join(holdings_core.active_ids(rows)))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
'''
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 blocks=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S);files=dict(zip(['holdings_core.py','run_holdings.py','test_holdings_modules.py'],blocks[1:4]));operations=[];checks=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 def ck(label,actual,expected):checks.append(dict(label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 with tempfile.TemporaryDirectory(prefix='module-exercises-') as tmp:
  folder=Path(tmp)
  for name,code in files.items():(folder/name).write_text(code)
  (folder/'second_runner.py').write_text(SECOND)
  def command(label,args,*,stdout=None,count=None,negative=False):
   r=subprocess.run([sys.executable,'-B',*args],cwd=folder,env=env,capture_output=True,text=True,timeout=30);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
   if negative:ok=r.returncode==1 and actual==1 and 'FAILED (failures=1)' in r.stderr and 'Active IDs: SEC-A, SEC-C' in r.stderr
   else:
    if stdout is not None:ok=ok and (r.stdout,r.stderr)==(stdout,'')
    if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M))
   operations.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_method_count=actual,expected_negative=negative,status='PASS' if ok else 'FAIL'))
  command('baseline exact original suite',['test_holdings_modules.py'],count=8)
  command('E1 original runner',['run_holdings.py'],stdout='Active IDs: SEC-A, SEC-C\n');command('E1 second caller',['second_runner.py'],stdout='Second IDs: Z, Y\n')
  spy="""
import copy,holdings_core,run_holdings,second_runner
original=holdings_core.active_ids;records=[]
def checked(rows):
 before=copy.deepcopy(rows);result=original(rows);assert rows==before;records.append(before);return result
holdings_core.active_ids=checked
try:run_holdings.main();second_runner.main()
finally:holdings_core.active_ids=original
assert [r['security_id'] for r in records[0]]==['SEC-B','SEC-A','SEC-C']
assert [r['security_id'] for r in records[1]]==['Q','Z','Y']
assert [str(r['quantity']) for r in records[0]]==['0','12.5','3']
assert [str(r['quantity']) for r in records[1]]==['0','2.5','4']
"""
  command('E1 observe caller inputs preserved',['-c',spy],stdout='Active IDs: SEC-A, SEC-C\nSecond IDs: Z, Y\n')
  probe="""
from decimal import Decimal as D
import copy,holdings_core
from test_holdings_modules import sample_holdings
for row,kind in [(dict(security_id=1,quantity=D(0)),TypeError),(dict(security_id='A',quantity=D(0),extra=1),ValueError)]:
 before=copy.deepcopy(row)
 try:holdings_core.capture_holdings([row])
 except kind:pass
 else:raise AssertionError('schema/type should reject')
 assert row==before
source=sample_holdings();before=copy.deepcopy(source)
assert holdings_core.active_ids(list(reversed(source)))==('SEC-C','SEC-A')
assert source==before
"""
  command('E2/E5 rejection and reverse order',['-c',probe],stdout='')
  # E3: preserve normal script output, but move its display responsibility outside main.
  line='    print("Active IDs: " + ", ".join(ids))\n';assert files['run_holdings.py'].count(line)==1
  mutant=files['run_holdings.py'].replace(line,'').replace('if __name__ == "__main__":','print("Active IDs: SEC-A, SEC-C")\n\nif __name__ == "__main__":')
  (HERE/'mutation.json').write_text(json.dumps(dict(original_sha256=sha(files['run_holdings.py'].encode()),mutant_sha256=sha(mutant.encode()),mutant_source=mutant,reason='Deliberate E3 top-level print moves visible application work outside main.'),indent=2)+'\n')
  (folder/'run_holdings.py').write_text(mutant)
  command('E3 expected existing quiet-import test failure',['-m','unittest','test_holdings_modules.ModuleTests.test_fresh_import_is_quiet','-v'],negative=True)
  (folder/'run_holdings.py').write_text(files['run_holdings.py']);command('E3 restored exact suite',['test_holdings_modules.py'],count=8)
  cache="""
import holdings_core,subprocess,sys
from pathlib import Path
path=Path(holdings_core.__file__);before=path.read_bytes();original=holdings_core
try:
 path.write_bytes(before+b'\\nEDIT_VISIBLE=True\\n')
 import holdings_core as again
 assert again is original and not hasattr(again,'EDIT_VISIBLE')
 r=subprocess.run([sys.executable,'-B','-c','import holdings_core;assert holdings_core.EDIT_VISIBLE is True'],capture_output=True,text=True)
 assert (r.returncode,r.stdout,r.stderr)==(0,'','')
finally:path.write_bytes(before)
"""
  command('E6 cached import versus fresh interpreter',['-c',cache],stdout='')
  command('E4 import definitions still execute',['-c',"import run_holdings,holdings_core;assert callable(run_holdings.main);assert callable(holdings_core.active_ids);assert holdings_core.Decimal.__name__=='Decimal'"],stdout='')
  ck('original source bytes restored',{name:sha((folder/name).read_bytes()) for name in files},{name:sha(code.encode()) for name,code in files.items()})
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),selected_files=[dict(path=name,sha256=sha(code.encode())) for name,code in files.items()],supplement_second_runner=SECOND,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),passed_original_method_invocations=sum(x["actual_method_count"] or 0 for x in operations if not x["expected_negative"] and x["status"]=="PASS"),expected_negative_method_invocations=sum(x["actual_method_count"] or 0 for x in operations if x["expected_negative"]),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','selected_files','supplement_second_runner')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
