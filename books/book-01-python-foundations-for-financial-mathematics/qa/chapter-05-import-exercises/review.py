"""Exact import-policy source plus explicit new callers and namespace experiments."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.02-*.md'))
FOURTH='''from decimal import Decimal
from quantity_rules import checked_quantity

def validate_fourth(value):
    return checked_quantity(value)

if __name__=='__main__':
    print('Fourth units: '+str(validate_fourth(Decimal('12.5'))))
'''
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 blocks=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S);files=dict(zip(['quantity_rules.py','import_styles.py','test_import_styles.py'],blocks));operations=[];checks=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 with tempfile.TemporaryDirectory(prefix='import-exercises-') as tmp:
  folder=Path(tmp)
  for name,code in files.items():(folder/name).write_text(code)
  supplements={'fourth_caller.py':FOURTH,'position_policy.py':'from quantity_rules import checked_quantity\ndef validate(value):\n    return checked_quantity(value)\n','order_policy.py':'from quantity_rules import checked_quantity\ndef validate(value):\n    return checked_quantity(value)\n','broken_application.py':'import missing_transitive_dependency_for_exercise_52\n'}
  for name,code in supplements.items():(folder/name).write_text(code)
  def command(label,args,*,stdout=None,count=None,error=None):
   r=subprocess.run([sys.executable,'-B',*args],cwd=folder,env=env,capture_output=True,text=True,timeout=30);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
   if error:ok=r.returncode!=0 and r.stdout=='' and error in r.stderr
   if stdout is not None:ok=ok and (r.stdout,r.stderr)==(stdout,'')
   if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M))
   operations.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_method_count=actual,expected_error=error,status='PASS' if ok else 'FAIL'));return r
  command('unchanged original suite',['test_import_styles.py'],count=9)
  command('original demo',['import_styles.py'],stdout='Validated units: 12.5, 12.5, 12.5\n');command('E1 fourth unaliased caller',['fourth_caller.py'],stdout='Fourth units: 12.5\n')
  code="""
from decimal import Decimal as D
import json,quantity_rules,import_styles
from fourth_caller import validate_fourth
from quantity_rules import checked_quantity
from quantity_rules import POLICY_LABEL
checks={}
checks['zero_equivalence']=tuple(str(x) for x in import_styles.validate_three_ways(D(0)))+(str(validate_fourth(D(0))),)
checks['fraction_equivalence']=tuple(str(x) for x in import_styles.validate_three_ways(D('12.5')))+(str(validate_fourth(D('12.5'))),)
checked_quantity='caller variable'
checks['caller_shadow']=checked_quantity
checks['qualified_still_callable']=str(quantity_rules.checked_quantity(D('2.5')))
POLICY_LABEL='local-only'
checks['local_label']=POLICY_LABEL
checks['module_label']=quantity_rules.POLICY_LABEL
quantity_rules.rows=[]
from quantity_rules import rows
rows.append('A');checks['shared_after_mutation']=list(quantity_rules.rows)
rows=['local'];checks['module_after_local_rebind']=list(quantity_rules.rows)
checks['local_after_rebind']=rows
print(json.dumps(checks))
"""
  observed=json.loads(command('E1-E4 fresh namespace probes',['-c',code]).stdout)
  expected={'zero_equivalence':['0']*4,'fraction_equivalence':['12.5']*4,'caller_shadow':'caller variable','qualified_still_callable':'2.5','local_label':'local-only','module_label':'nonnegative-units-v1','shared_after_mutation':['A'],'module_after_local_rebind':['A'],'local_after_rebind':['local']}
  for key,value in expected.items():ck('5.2-E1-E4',key,observed[key],value)
  code="""
from decimal import Decimal as D
import json
from position_policy import validate as validate_position_units
from order_policy import validate as validate_order_units
print(json.dumps(dict(position=str(validate_position_units(D(0))),order=str(validate_order_units(D('12.5'))),modules=[validate_position_units.__module__,validate_order_units.__module__],distinct_wrappers=validate_position_units is not validate_order_units)))
"""
  observed=json.loads(command('E5 named aliases',['-c',code]).stdout)
  for key,value in dict(position='0',order='12.5',modules=['position_policy','order_policy'],distinct_wrappers=True).items():ck('5.2-E5',key,observed[key],value)
  command('E6 retained missing-transitive traceback',['-c','import broken_application'],error='ModuleNotFoundError: No module named')
  command('E6 misleading fallback demonstration',['-c',"import json\ntry:\n import broken_application\nexcept ImportError:\n report=[]\nassert report==[]\nprint(json.dumps(report))"],stdout='[]\n')
  core=folder/'quantity_rules.py';original=core.read_bytes();edited=original+b'\n# Temporary E7 saved-file comparison.\n'
  try:
   core.write_bytes(edited);observed=json.loads(command('E7 compare loaded path and saved bytes',['-c',"import quantity_rules,json,hashlib;from pathlib import Path;p=Path(quantity_rules.__file__).resolve();print(json.dumps(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())))"]).stdout);ck('5.2-E7','actual loaded file',observed['path'],str(core.resolve()));ck('5.2-E7','saved file bytes',observed['sha256'],sha(edited))
  finally:core.write_bytes(original)
  ck('all','source restored unchanged',{name:sha((folder/name).read_bytes()) for name in files},{name:sha(code.encode()) for name,code in files.items()})
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),selected_files=[dict(path=name,sha256=sha(code.encode())) for name,code in files.items()],supplements=supplements,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),existing_passed_method_invocations=sum(x['actual_method_count'] or 0 for x in operations if x['status']=='PASS'),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','supplements','selected_files')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
