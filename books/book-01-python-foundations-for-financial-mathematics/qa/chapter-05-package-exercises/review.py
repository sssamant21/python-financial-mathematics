"""Exact local package baseline, explicit extensions, and relative/absolute variants."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.05-*.md'))
COUNT='''

def count_holdings(value: object) -> int:
    """Count validated aggregate holdings including zero, not monetary units."""
    return len(capture_holdings(value))
'''
DISPLAY='''from .views import active_ids

def format_active_ids(value):
    """Presentation only; no printing, I/O or valuation."""
    return 'Package active IDs: '+', '.join(active_ids(value))
'''
REPORTS='''from .summary import count_report
'''
SUMMARY='''from ..views import count_holdings

def count_report(value):
    """Nested teaching report: cardinality only, no money total."""
    return dict(holding_count=count_holdings(value))
'''
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 blocks=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S);files=dict(zip(['finance_lab/holdings.py','finance_lab/views.py','finance_lab/__init__.py','finance_lab/__main__.py','test_finance_lab.py'],blocks));operations=[];checks=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 with tempfile.TemporaryDirectory(prefix='package-exercises-') as tmp:
  folder=Path(tmp)
  for name,code in files.items():p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
  def command(label,args,*,stdout=None,count=None,error=None):
   r=subprocess.run([sys.executable,'-B',*args],cwd=folder,env=env,capture_output=True,text=True,timeout=30);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
   if error:ok=r.returncode!=0 and r.stdout=='' and error in r.stderr
   if stdout is not None:ok=ok and (r.stdout,r.stderr)==(stdout,'')
   if count:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M))
   operations.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_method_count=actual,expected_error=error,status='PASS' if ok else 'FAIL'));return r
  command('exact original baseline suite',['test_finance_lab.py'],count=8)
  extended=dict(files);extended['finance_lab/views.py']+=COUNT
  # Keep original wildcard exports stable; new public view has an explicit facade import.
  extended['finance_lab/__init__.py']+='\nfrom .views import count_holdings as count_holdings\n'
  extended['finance_lab/__main__.py']=extended['finance_lab/__main__.py'].replace('from .views import active_ids','from .display import format_active_ids').replace('print("Package active IDs: " + ", ".join(active_ids(source)))','print(format_active_ids(source))')
  extended.update({'finance_lab/display.py':DISPLAY,'finance_lab/reports/__init__.py':REPORTS,'finance_lab/reports/summary.py':SUMMARY})
  for name,code in extended.items():p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
  command('unchanged original tests against extended relative package',['test_finance_lab.py'],count=8)
  probe="""
from decimal import Decimal as D
import copy,json,sys
import finance_lab
from finance_lab import count_holdings
from finance_lab.views import count_holdings as implementation
checks={'view_identity':count_holdings is implementation,'display_not_initialized':'finance_lab.display' not in sys.modules}
from finance_lab.display import format_active_ids
checks['helper_not_facade']=not hasattr(finance_lab,'format_active_ids')
source=[dict(security_id='B',quantity=D(0)),dict(security_id='A',quantity=D('12.5'))];before=copy.deepcopy(source)
checks['all_count']=count_holdings(source);checks['empty_count']=count_holdings([]);checks['display']=format_active_ids(source);checks['source_unchanged']=source==before
for row,kind,label in [(dict(security_id=1,quantity=D(0)),TypeError,'numeric_id'),(dict(security_id='A',quantity=D(0),extra=1),ValueError,'extra_field')]:
 try:finance_lab.capture_holdings([row])
 except kind:checks[label]=True
 else:checks[label]=False
import finance_lab.holdings as holdings
checks['explicit_implementation_import']=holdings.capture_holdings is finance_lab.capture_holdings
namespace={};exec('from finance_lab import *',namespace);checks['wildcard_names']=sorted(k for k in namespace if not k.startswith('_'))
checks['new_explicit_view_not_wildcard']='count_holdings' not in namespace
import finance_lab.reports,finance_lab.reports.summary
checks['subpackage_name']=finance_lab.reports.__name__;checks['nested_module']=finance_lab.reports.summary.__name__;checks['nested_report']=finance_lab.reports.count_report(source);checks['nested_empty']=finance_lab.reports.summary.count_report([])
try:count_holdings(source+[dict(security_id='BAD',quantity=D('NaN'))])
except ValueError:checks['full_validation']=True
else:checks['full_validation']=False
print(json.dumps(checks))
"""
  observed=json.loads(command('E1-E3/E5/E7 package API probes',['-c',probe]).stdout)
  expected=dict(view_identity=True,display_not_initialized=True,helper_not_facade=True,all_count=2,empty_count=0,display='Package active IDs: A',source_unchanged=True,numeric_id=True,extra_field=True,explicit_implementation_import=True,wildcard_names=['active_ids','capture_holdings'],new_explicit_view_not_wildcard=True,subpackage_name='finance_lab.reports',nested_module='finance_lab.reports.summary',nested_report={'holding_count':2},nested_empty={'holding_count':0},full_validation=True)
  for label,value in expected.items():ck('5.5-E1-E7',label,observed[label],value)
  command('extended -m package caller',['-m','finance_lab'],stdout='Package active IDs: SEC-A, SEC-C\n')
  command('relative views plain-file failure',['finance_lab/views.py'],error='attempted relative import with no known parent package')
  absolute=extended['finance_lab/views.py'].replace('from .holdings import capture_holdings','from finance_lab.holdings import capture_holdings');(folder/'finance_lab/views.py').write_text(absolute)
  command('absolute internal import variant suite',['test_finance_lab.py'],count=8);command('absolute variant -m package',['-m','finance_lab'],stdout='Package active IDs: SEC-A, SEC-C\n');command('absolute variant plain file missing discoverable parent',['finance_lab/views.py'],error="No module named 'finance_lab'")
  (folder/'finance_lab/views.py').write_text(extended['finance_lab/views.py']);ck('5.5-E4','restored extended relative view',sha((folder/'finance_lab/views.py').read_bytes()),sha(extended['finance_lab/views.py'].encode()))
  ck('all','original core validation unchanged',sha((folder/'finance_lab/holdings.py').read_bytes()),sha(files['finance_lab/holdings.py'].encode()))
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),original_files=[dict(path=name,sha256=sha(code.encode())) for name,code in files.items()],extended_files=extended,absolute_variant_sha256=sha(absolute.encode()),command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),existing_method_invocations=sum(x['actual_method_count'] or 0 for x in operations if x['status']=='PASS'),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','original_files','extended_files')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
