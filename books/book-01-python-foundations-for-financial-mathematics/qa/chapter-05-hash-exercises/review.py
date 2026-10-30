"""Original offline wheel/hash helpers plus explicit exercise and retained-input probes."""
import hashlib,json,os,platform,re,shutil,subprocess,sys,tempfile,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
def source(n):
 p=next((BOOK/'chapter-05').glob(f'5.{n:02}-*.md'));code=re.findall(r'^```python\n(.*?)^```',p.read_text(),re.M|re.S)[0];return p,code
P6,C6=source(6);P8,C8=source(8)
H=types.ModuleType('pip_dependency_lab');sys.modules[H.__name__]=H;exec(compile(C6,str(P6),'exec'),H.__dict__)
Q=types.ModuleType('exact_repeatability_helpers');exec(compile(C8,str(P8),'exec'),Q.__dict__)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 checks=[];operations=[];records={};specs={};env={k:v for k,v in os.environ.items() if not k.startswith('PIP_') and k not in {'PYTHONPATH','PYTHONHOME'}};env.update(PIP_CONFIG_FILE=os.devnull,PYTHONDONTWRITEBYTECODE='1')
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 bundle=HERE/'evidence-bundle';bundle.mkdir(exist_ok=True);wheelstore=bundle/'approved-wheels';wheelstore.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='hash-exercises-') as tmp:
  root=Path(tmp);work=root/'outside';work.mkdir();wheels=root/'wheels';wheels.mkdir()
  unit=H.fixture_wheel(wheels,'book1-unit-demo','book1_unit_demo',H.UNIT_SOURCE);report=H.fixture_wheel(wheels,'book1-report-demo','book1_report_demo',H.REPORT_SOURCE,'book1-unit-demo==1.0.0');approved={p.name:Q.digest(p) for p in [unit,report]}
  reportline=f'book1-report-demo==1.0.0 --hash=sha256:{approved[report.name]}\n';unitline=f'book1-unit-demo==1.0.0 --hash=sha256:{approved[unit.name]}\n'
  specs={'complete':reportline+unitline,'missing-transitive':reportline,'wrong-report-hash':'book1-report-demo==1.0.0 --hash=sha256:'+('0'*64)+'\n'+unitline}
  for name,text in specs.items():(root/(name+'.txt')).write_text(text);(bundle/(name+'.txt')).write_text(text)
  for p in [unit,report]:shutil.copyfile(p,wheelstore/p.name)
  # Original BEHAVIOR still runs unchanged; separate new file-bound probe consumes exact bytes.
  assert Q.BEHAVIOR.count('input_text = "12.50"')==1
  app='import hashlib\n'+Q.BEHAVIOR.replace('input_text = "12.50"',"input_raw=Path(sys.argv[1]).read_bytes()\ninput_text=input_raw.decode('utf-8')").replace('"input": input_text,', '"input": input_text, "input_sha256":hashlib.sha256(input_raw).hexdigest(), "application_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),')
  application=bundle/'application_probe.py';application.write_text(app);data=bundle/'input.txt';data.write_bytes(b'12.50')
  expected={'versions':{'book1-report-demo':'1.0.0','book1-unit-demo':'1.0.0'},'input':'12.50','output':['instrument_units','12.50']};expected_file=dict(expected,input_sha256=sha(b'12.50'),application_source_sha256=sha(app.encode()))
  def command(label,python,args,*,expected_code=0,diagnostics=()):
   r=subprocess.run([str(python),*map(str,args)],cwd=work,env=env,capture_output=True,text=True,timeout=120);log=(r.stdout+r.stderr).lower();ok=r.returncode==expected_code and all(token.lower() in log for token in diagnostics);operations.append(dict(label=label,argv=[str(python),*map(str,args)],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_returncode=expected_code,diagnostics=list(diagnostics),status='PASS' if ok else 'FAIL'));return r
  for name,bad_spec in [('a','missing-transitive'),('b','wrong-report-hash')]:
   target=root/('runtime-'+name);command('fresh runtime '+name,sys.executable,['-m','venv',target]);python=Q.interpreter(target)
   command('E1 missing transitive hash' if name=='a' else 'E2 incorrect approved report hash',python,Q.install_arguments(wheels,root/(bad_spec+'.txt')),expected_code=1,diagnostics=('hash','book1-unit-demo') if name=='a' else ('hash','book1-report-demo'))
   command('failed attempt has no fixture imports '+name,python,['-I','-c',"from importlib.util import find_spec;assert find_spec('book1_report_demo') is None;assert find_spec('book1_unit_demo') is None"])
   command('complete approved specification retry '+name,python,Q.install_arguments(wheels,root/'complete.txt'));command('pip check '+name,python,H.pip_args('check'))
   original=json.loads(command('unchanged original behavior '+name,python,['-I','-c',Q.BEHAVIOR]).stdout);ck('5.8-E5','independent known result '+name,original,expected)
   bound=json.loads(command('E3 file-bound application '+name,python,['-I',application.resolve(),data.resolve()]).stdout);ck('5.8-E3','consumed input/source digests and known result '+name,bound,expected_file)
   pip=command('runtime pip evidence '+name,python,H.pip_args('--version')).stdout.strip();runtime=json.loads(command('runtime identity '+name,python,['-I','-c',"import sys,json;print(json.dumps(dict(executable=sys.executable,prefix=sys.prefix,base_prefix=sys.base_prefix)))"]).stdout)
   ck('5.8-E5','owned runtime prefix '+name,Path(runtime['prefix']).resolve(),target.resolve());records[name]=dict(result=original,file_result=bound,pip=pip,runtime=runtime)
  ck('5.8-E5','selected invariant outputs agree',records['a']['file_result'],records['b']['file_result']);ck('5.8-E5','runtime prefixes deliberately differ',records['a']['runtime']['prefix']!=records['b']['runtime']['prefix'],True);ck('5.8-E5','pip location strings legitimately differ',records['a']['pip']!=records['b']['pip'],True)
  for p in [unit,report]:ck('all','approved wheel unchanged '+p.name,Q.digest(p),approved[p.name]);ck('all','retained approved bytes '+p.name,sha((wheelstore/p.name).read_bytes()),approved[p.name])
  ck('5.8-E2','wrong hash not approved',approved[report.name]!='0'*64,True);ck('all','complete specification unchanged',(root/'complete.txt').read_text(),specs['complete'])
 manifest=dict(schema_version=1,scope='Synthetic same-runtime installation/selected behavior; not independent financial acceptance',source_revision='28af429b',application=dict(path='application_probe.py',sha256=sha(application.read_bytes()),kind='supplemental file-bound caller of installed original fixture'),input=dict(path='input.txt',sha256=sha(data.read_bytes()),encoding='UTF-8',quantity_unit='instrument_units'),requirements=dict(path='complete.txt',sha256=sha(specs['complete'].encode())),approved_wheels=[dict(path='approved-wheels/'+name,sha256=digest) for name,digest in approved.items()],sources=[dict(path=str(p.relative_to(BOOK)),sha256=sha(p.read_bytes()),selected_code_sha256=sha(code.encode())) for p,code in [(P6,C6),(P8,C8)]],orchestration_sha256=sha(Path(__file__).read_bytes()),python=platform.python_version(),implementation=platform.python_implementation(),platform=platform.platform(),results=records)
 (bundle/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');ck('all','owned temporary resources cleaned',root.exists(),False)
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,sources=manifest['sources'],command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','sources')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
