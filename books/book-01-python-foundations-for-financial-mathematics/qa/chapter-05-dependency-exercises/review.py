"""Original offline wheel helpers with supplemental dependency exercise orchestration."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.06-*.md'))
CODE=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S)[0]
H=types.ModuleType('exact_dependency_helpers');exec(compile(CODE,str(SOURCE),'exec'),H.__dict__)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 operations=[];checks=[];artifacts=[]
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 env={k:v for k,v in os.environ.items() if not k.startswith('PIP_') and k not in {'PYTHONPATH','PYTHONHOME'}};env.update(PYTHONDONTWRITEBYTECODE='1',PIP_CONFIG_FILE=os.devnull)
 with tempfile.TemporaryDirectory(prefix='dependency-exercises-') as tmp:
  root=Path(tmp);work=root/'outside';work.mkdir();good=root/'approved';bad=root/'unavailable';good.mkdir();bad.mkdir()
  for folder,dependency in [(good,'book1-unit-demo==1.0.0'),(bad,'book1-unit-demo==2.0.0')]:
   for wheel in [H.fixture_wheel(folder,'book1-unit-demo','book1_unit_demo',H.UNIT_SOURCE),H.fixture_wheel(folder,'book1-report-demo','book1_report_demo',H.REPORT_SOURCE,dependency)]:
    with ZipFile(wheel) as archive:metadata=archive.read(next(x for x in archive.namelist() if x.endswith('/METADATA'))).decode()
    artifacts.append(dict(set=folder.name,filename=wheel.name,sha256=sha(wheel.read_bytes()),metadata=metadata))
  def command(label,python,args,*,expected=0,diagnostic=None,stdout=None):
   r=subprocess.run([str(python),*map(str,args)],cwd=work,env=env,text=True,capture_output=True,timeout=120);ok=r.returncode==expected
   if diagnostic:ok=ok and diagnostic.lower() in (r.stdout+r.stderr).lower()
   if stdout is not None:ok=ok and (r.stdout,r.stderr)==(stdout,'')
   operations.append(dict(label=label,argv=[str(python),*map(str,args)],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_returncode=expected,expected_diagnostic=diagnostic,status='PASS' if ok else 'FAIL'));return r
  target=root/'runtime';command('fresh runtime create',sys.executable,['-m','venv',target]);python=target/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
  identity=json.loads(command('E3 actual invoked interpreter',python,['-I','-c',"import json,sys;print(json.dumps(dict(executable=sys.executable,prefix=sys.prefix,base_prefix=sys.base_prefix)))"]).stdout);ck('5.6-E3','sys.executable equals invoked path',identity['executable'],str(python));ck('5.6-E3','prefix is selected runtime',Path(identity['prefix']).resolve(),target.resolve());ck('5.6-E3','prefix differs base',identity['prefix']!=identity['base_prefix'],True)
  command('runtime pip identity',python,H.pip_args('--version'))
  constraints=root/'constraints.txt';constraints.write_text('book1-unit-demo==1.0.0\n');requirements=root/'requirements.txt';requirements.write_text('book1-report-demo==1.0.0\n')
  command('E2 constraints alone are not installation request',python,H.pip_args('install','--no-index','--find-links',good,'-c',constraints),expected=1,diagnostic='at least one requirement')
  absent="from importlib.util import find_spec;assert find_spec('book1_report_demo') is None;assert find_spec('book1_unit_demo') is None"
  command('E2 no fixture installed by constraints',python,['-I','-c',absent],stdout='')
  command('E1 unavailable transitive version',python,H.pip_args('install','--no-index','--no-cache-dir','--find-links',bad,'-r',requirements),expected=1,diagnostic='book1-unit-demo==2.0.0')
  command('E1 failed resolution has no fixture imports',python,['-I','-c',absent],stdout='')
  command('E1/E2 corrected approved install with constraint',python,H.pip_args('install','--no-index','--no-cache-dir','--find-links',good,'-r',requirements,'-c',constraints))
  command('repaired declared dependencies',python,H.pip_args('check'))
  command('exact original installed behavior checks',python,['-I','-c',H.BEHAVIOR_CHECK],stdout='installed behavior passed\n')
  behavior="""
from decimal import Decimal
from pathlib import Path
import json,sys,book1_report_demo,book1_unit_demo
from importlib.metadata import version
rows=[]
for text in ['0','12.50']:
 label,value=book1_report_demo.labeled_quantity(Decimal(text))
 rows.append(dict(label=label,text=str(value),exact_decimal=type(value) is Decimal,tuple=list(value.as_tuple()[:2])+[value.as_tuple().exponent]))
print(json.dumps(dict(rows=rows,versions={name:version(name) for name in ['book1-report-demo','book1-unit-demo']},origins_owned=all(Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()) for m in [book1_report_demo,book1_unit_demo]))))
"""
  observed=json.loads(command('E5 independent installed zero/fraction expectations',python,['-I','-c',behavior]).stdout)
  ck('5.6-E5','zero/fraction label and text',[(r['label'],r['text'],r['exact_decimal']) for r in observed['rows']],[('instrument_units','0',True),('instrument_units','12.50',True)]);ck('5.6-E5','Decimal scale retained',[r['tuple'][2] for r in observed['rows']],[0,-2]);ck('5.6-E5','installed versions',observed['versions'],{'book1-report-demo':'1.0.0','book1-unit-demo':'1.0.0'});ck('5.6-E5','installed origin under selected runtime',observed['origins_owned'],True)
  command('installed freeze inventory',python,H.pip_args('freeze'))
  # E4 deliberately skip dependencies in a second owned runtime, then repair normally.
  skipped=root/'no-deps-runtime';command('E4 separate runtime create',sys.executable,['-m','venv',skipped]);other=skipped/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
  command('E4 incomplete --no-deps install',other,H.pip_args('install','--no-index','--find-links',good,'--no-deps','book1-report-demo==1.0.0'))
  command('E4 expected dependency metadata failure',other,H.pip_args('check'),expected=1,diagnostic='book1-unit-demo')
  command('E4 expected missing imported dependency',other,['-I','-c','import book1_report_demo'],expected=1,diagnostic="No module named 'book1_unit_demo'")
  command('E4 approved normal dependency repair',other,H.pip_args('install','--no-index','--find-links',good,'-r',requirements))
  command('E4 repaired metadata',other,H.pip_args('check'));command('E4 repaired exact original behavior',other,['-I','-c',H.BEHAVIOR_CHECK],stdout='installed behavior passed\n')
  for folder in [good,bad]:
   for wheel in folder.glob('*.whl'):ck('all','local artifact unchanged '+folder.name+'/'+wheel.name,sha(wheel.read_bytes()),next(x['sha256'] for x in artifacts if x['set']==folder.name and x['filename']==wheel.name))
 ck('all','owned temporary resources cleaned',root.exists(),False)
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),code_sha256=sha(CODE.encode()),unit_source_sha256=sha(H.UNIT_SOURCE.encode()),report_source_sha256=sha(H.REPORT_SOURCE.encode()),artifacts=artifacts,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','artifacts')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
