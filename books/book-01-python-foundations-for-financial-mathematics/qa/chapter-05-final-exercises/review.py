"""Install retained original wheel; exercise an explicitly modified owned copy."""
import hashlib,json,os,platform,re,shutil,subprocess,sys
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-05/5.12-chapter-project-reusable-financial-python-package.md'
WHEEL=BOOK/'qa/chapter-05-project-review/artifacts/book1_financial_inflows-0.1.0-py3-none-any.whl'

def sha(raw):return hashlib.sha256(raw).hexdigest()

def run():
    operations=[];checks=[]
    env={k:v for k,v in os.environ.items() if k not in ('PYTHONPATH','PYTHONHOME')};env['PYTHONDONTWRITEBYTECODE']='1'
    def ck(label,actual,expected):checks.append(dict(label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
    text=SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
    names=['__init__.py','core.py','cli.py','__main__.py']
    with ZipFile(WHEEL) as archive:
        ck('retained original wheel matches current four exact source listings',
           {name:archive.read('financial_inflows/'+name) for name in names},
           {name:blocks[i].encode() for i,name in enumerate(names)})
    baseline_wheel_sha=sha(WHEEL.read_bytes())
    expected_artifact=json.loads((BOOK/'qa/chapter-05-project-review/results.json').read_text())['artifact']['sha256']
    ck('retained wheel digest matches previously recorded artifact',baseline_wheel_sha,expected_artifact)
    with TemporaryDirectory(prefix='final-package-exercises-') as tmp:
        root=Path(tmp);outside=root/'outside';outside.mkdir();target=root/'runtime'
        def command(label,args,*,count=None,error=None,expected_json=None):
            r=subprocess.run(list(map(str,args)),cwd=outside,env=env,capture_output=True,text=True,timeout=60)
            found=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(found[0]) if len(found)==1 else None;ok=r.returncode==0
            if error:ok=r.returncode!=0 and r.stdout=='' and error in r.stderr
            if count:ok=ok and actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
            if expected_json is not None:
                try:ok=ok and json.loads(r.stdout)==expected_json and r.stderr==''
                except ValueError:ok=False
            operations.append(dict(label=label,args=list(map(str,args)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_error=error,actual_method_count=actual,status='PASS' if ok else 'FAIL'))
            return r
        command('fresh runtime creation',[sys.executable,'-m','venv',target])
        python=target/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        command('original retained wheel offline install',[python,'-m','pip','--isolated','install','--no-index','--no-deps',WHEEL])
        command('original pip check',[python,'-m','pip','check'])
        identity=command('original installed origin',[python,'-I','-c',"import json,sysconfig,financial_inflows;from pathlib import Path;p=Path(financial_inflows.__file__).resolve();purelib=Path(sysconfig.get_path('purelib')).resolve();assert purelib in p.parents;print(json.dumps(dict(origin=str(p),purelib=str(purelib))))"])
        package=Path(json.loads(identity.stdout)['origin']).parent
        ck('installed package lives in owned runtime',package.is_relative_to(target.resolve()),True)
        (outside/'test_inflows.py').write_text(blocks[4]);shutil.copyfile(HERE/'import_probe.py',outside/'import_probe.py')
        command('original eight-method installed suite',[python,'-I','-m','unittest','discover','-s',outside,'-v'],count=8)
        probe=command('E4 original fresh quiet and application-file-denied import',[python,'-I',outside/'import_probe.py'])
        observed=json.loads(probe.stdout);ck('original quiet stdout/stderr',(observed['stdout'],observed['stderr']),('',''))
        facade=package/'__init__.py';original_facade=facade.read_bytes();core=package/'core.py';original_core=core.read_bytes()
        mutant=original_facade+b'\nfrom pathlib import Path\nPath("application-marker.txt").read_bytes()\n'
        (outside/'application-marker.txt').write_text('synthetic application data')
        facade.write_bytes(mutant)
        command('E4 intentional read mutant must be detected',[python,'-I',outside/'import_probe.py'],error='APPLICATION_FILE_ACCESS')
        facade.write_bytes(original_facade)
        command('E4 restored original import',[python,'-I',outside/'import_probe.py'])
        ck('E4 original facade restored',facade.read_bytes(),original_facade)
        # The following is a modified installed COPY in this disposable runtime,
        # not a rebuilt wheel or a published 0.1.0 distribution.
        for name in ['reports.py','result_types.py']:shutil.copyfile(HERE/name,package/name)
        extended_facade=original_facade.decode().replace("__all__ = ['analyze']","from .reports import inflow_count\n\n__all__ = ['analyze', 'inflow_count']")
        assert extended_facade!=original_facade.decode()
        facade.write_text(extended_facade)
        typed_core=original_core.decode().replace('def analyze(data_raw: bytes, config_raw: bytes) -> dict:', 'from .result_types import AnalyzeResult\n\ndef analyze(data_raw: bytes, config_raw: bytes) -> AnalyzeResult:')
        assert typed_core!=original_core.decode();core.write_text(typed_core)
        command('supplemental copy original eight-method suite',[python,'-I','-m','unittest','discover','-s',outside,'-v'],count=8)
        command('supplemental copy fresh guarded import',[python,'-I',outside/'import_probe.py'])
        shutil.copyfile(HERE/'extension_probe.py',outside/'extension_probe.py')
        extended=command('E1/E6 supplemental API/type/runtime contracts',[python,'-I',outside/'extension_probe.py'])
        extended_checks=json.loads(extended.stdout);checks.extend(extended_checks)
        fixture_blocks=re.findall(r'^```json\n(.*?)^```',text,re.M|re.S)
        for name,code in zip(['inflows.json','settings.json'],fixture_blocks[:2]):
            (outside/name).write_text(code)
        command('supplemental copy module CLI schema',[python,'-I','-m','financial_inflows','--input',outside/'inflows.json','--config',outside/'settings.json'],expected_json=dict(currency='USD',count=2,total='30.01',method='sum_then_round',rounding='ROUND_HALF_EVEN'))
        ck('retained original wheel bytes unchanged',sha(WHEEL.read_bytes()),baseline_wheel_sha)
        mutations=dict(intentional_read_facade=mutant.decode(),extended_facade=extended_facade,typed_core=typed_core)
    ck('owned runtime and source-copy removed',root.exists(),False)
    output=dict(python=platform.python_version(),platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),wheel_sha256=baseline_wheel_sha,exercise_records=6,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),original_method_invocations=sum(x['actual_method_count'] or 0 for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),mutations=mutations,operations=operations,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('operations','checks','mutations')}))
    return bool(output['failed'] or output['command_failed'])

if __name__=='__main__':raise SystemExit(run())
