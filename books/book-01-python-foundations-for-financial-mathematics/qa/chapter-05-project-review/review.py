"""Exact project verifier and same retained wheel in two fresh installed runtimes."""
import argparse,hashlib,json,os,platform,re,shutil,subprocess,sys,tempfile
from fractions import Fraction
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.12-*.md'))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 parser=argparse.ArgumentParser();parser.add_argument('--builder',type=Path,required=True);args=parser.parse_args();builder=args.builder.absolute();operations=[];checks=[]
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 def ck(label,actual,expected):checks.append(dict(label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 def command(label,argv,cwd,*,count=None,expected_json=None,error=None,quiet=False):
  r=subprocess.run([str(x) for x in argv],cwd=cwd,env=env,capture_output=True,text=True,timeout=300);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
  if error:ok=r.returncode!=0 and r.stdout=='' and error in r.stderr
  if quiet:ok=ok and r.stdout==r.stderr==''
  if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M)) and not re.search(r'skipped=',log)
  if expected_json is not None:
   try:ok=ok and json.loads(r.stdout)==expected_json and not r.stderr
   except json.JSONDecodeError:ok=False
  operations.append(dict(label=label,argv=[str(x) for x in argv],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_count=count,actual_count=actual,expected_error=error,status='PASS' if ok else 'FAIL'))
  if not ok:raise RuntimeError('Failed operation '+label+'; see results on exit')
  return r
 text=SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);files={name:blocks[i] for name,i in {'src/financial_inflows/__init__.py':0,'src/financial_inflows/core.py':1,'src/financial_inflows/cli.py':2,'src/financial_inflows/__main__.py':3,'tests/test_inflows.py':4,'verify_package.py':5}.items()}
 for lang,name in [('toml','pyproject.toml'),('markdown','README.md'),('gitignore','.gitignore')]:files[name]=re.findall(r'^```'+lang+r'\n(.*?)^```',text,re.M|re.S)[0]
 fixtures=re.findall(r'^```json\n(.*?)^```',text,re.M|re.S);files['fixtures/inflows.json'],files['fixtures/settings.json']=fixtures[:2]
 versions=None;artifact=None
 try:
  with tempfile.TemporaryDirectory(prefix='book1-project-review-') as tmp:
   root=Path(tmp);project=root/'project';project.mkdir();outside=root/'orchestration';outside.mkdir()
   versions=json.loads(command('builder identity',[builder,'-I','-c',"import json,platform;from importlib.metadata import version;print(json.dumps(dict(python=platform.python_version(),pip=version('pip'),setuptools=version('setuptools'))))"],outside).stdout);ck('exact backend',versions['setuptools'],'84.0.0')
   if versions['setuptools']!='84.0.0':raise RuntimeError('Declared exact builder required')
   for name,contents in files.items():p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(contents)
   verifier=command('exact project verifier',[builder,project/'verify_package.py'],outside,count=8);ck('verifier cleanup status','Temporary wheel and runtime removed' in verifier.stdout,True)
   command('retained build',[builder,'-m','pip','--isolated','wheel','.', '--no-index','--no-deps','--no-build-isolation','--wheel-dir','dist'],project)
   wheels=list((project/'dist').glob('*.whl'));ck('one retained wheel',len(wheels),1);wheel=wheels[0];raw=wheel.read_bytes();artifact=dict(filename=wheel.name,bytes=len(raw),sha256=sha(raw))
   artifacts=HERE/'artifacts';artifacts.mkdir(exist_ok=True);retained=artifacts/wheel.name;retained.write_bytes(raw)
   with ZipFile(wheel) as archive:
    names=archive.namelist();ck('core included','financial_inflows/core.py' in names,True);ck('fixtures/tests source-side only',any(n.startswith(('tests/','fixtures/')) for n in names),False)
   inputs=project/'fixtures/inflows.json';config=project/'fixtures/settings.json';amounts=[Fraction(r['amount']) for r in json.loads(inputs.read_bytes())];scaled=sum(amounts)*100;q,r=divmod(scaled.numerator,scaled.denominator);cents=q+int(2*r>scaled.denominator or (2*r==scaled.denominator and q%2==1));ck('independent fixture cents',cents,3001)
   expected=dict(currency='USD',count=2,total=f'{cents//100}.{cents%100:02d}',method='sum_then_round',rounding='ROUND_HALF_EVEN')
   for name in ['runtime-a','runtime-b']:
    target=root/name;command(name+' create',[builder,'-m','venv',target],outside);scripts=target/('Scripts' if os.name=='nt' else 'bin');python=scripts/('python.exe' if os.name=='nt' else 'python');work=root/(name+'-outside');work.mkdir();shutil.copyfile(project/'tests/test_inflows.py',work/'test_inflows.py')
    command(name+' exact retained wheel install',[python,'-m','pip','--isolated','install','--no-index','--no-deps',retained],work);command(name+' pip check',[python,'-m','pip','check'],work)
    origin=json.loads(command(name+' installed origin',[python,'-I','-c',"import json,sysconfig,sys;from pathlib import Path;import financial_inflows;origin=Path(financial_inflows.__file__).resolve();purelib=Path(sysconfig.get_path('purelib')).resolve();assert purelib in origin.parents;print(json.dumps(dict(origin=str(origin),purelib=str(purelib),prefix=sys.prefix)))"],work).stdout);ck(name+' external origin',Path(origin['origin']).is_relative_to(target.resolve()),True)
    command(name+' source tests installed externally',[python,'-I','-m','unittest','discover','-s',work,'-v'],work,count=8)
    module=command(name+' module CLI',[python,'-I','-m','financial_inflows','--input',inputs,'--config',config],work,expected_json=expected)
    console=scripts/('financial-inflows.exe' if os.name=='nt' else 'financial-inflows');entry=command(name+' console CLI',[console,'--input',inputs,'--config',config],work,expected_json=expected);ck(name+' CLI byte parity',module.stdout,entry.stdout)
    command(name+' missing arguments',[python,'-I','-m','financial_inflows'],work,error='--input');bad=work/'malformed.json';bad.write_bytes(b'[');command(name+' malformed input',[python,'-I','-m','financial_inflows','--input',bad,'--config',config],work,error='JSONDecodeError');command(name+' quiet import',[python,'-I','-c','import financial_inflows,financial_inflows.cli'],work,quiet=True)
    ck(name+' retained bytes unchanged',sha(retained.read_bytes()),artifact['sha256'])
   ck('all supplied project files unchanged',{name:sha((project/name).read_bytes()) for name in files},{name:sha(contents.encode()) for name,contents in files.items()})
  ck('owned temporary resources removed',root.exists(),False)
 finally:
  out=dict(python=platform.python_version(),platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),selected_files=[dict(path=name,sha256=sha(contents.encode())) for name,contents in files.items()],builder=versions,artifact=artifact,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),existing_method_invocations=sum(x['actual_count'] or 0 for x in operations),operations=operations,checks=checks)
  (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','selected_files','artifact','builder')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
