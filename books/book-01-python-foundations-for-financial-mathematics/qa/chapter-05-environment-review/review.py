"""Exact offline source workflows, raw expected failures and scoped Linux manual setup."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
CHAPTER=BOOK/'chapter-05'
NAMES={6:'pip_dependency_lab.py',7:'virtual_environment_lab.py',8:'reproducibility_lab.py'}
STAGES={6:['ENVIRONMENT:','INSTALL:','INVENTORY:','BROKEN STATE:','REPAIR:','CLEANUP:','PASS: temporary environment cleaned up'],7:['IDENTITY:','ISOLATION:','INDEPENDENCE:','RECREATE:','REBUILD:','PASS: both temporary environments cleaned up'],8:['SETUP:','FIRST INSTALL:','NEGATIVE CHECK:','SECOND INSTALL:','PASS: two local installs verified and temporary resources cleaned up']}
def run():
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);records=[];checks=[]
 def ck(id,label,actual,expected):checks.append(dict(id=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 with tempfile.TemporaryDirectory(prefix='book1-environment-review-') as tmp:
  root=Path(tmp)
  for n,name in NAMES.items():
   source=next(CHAPTER.glob(f'5.{n:02}-*.md'));code=re.findall(r'^```python\n(.*?)^```',source.read_text(),re.M|re.S)[0];(root/name).write_text(code)
   records.append(dict(section=f'5.{n}',source=str(source.relative_to(BOOK)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),file=name,code_sha256=hashlib.sha256(code.encode()).hexdigest()))
  for record in records:
   n=int(record['section'].split('.')[1]);trace=HERE/f'5-{n}-children.json'
   r=subprocess.run([sys.executable,'-B',str(HERE/'trace_source.py'),str(root/record['file']),str(trace)],cwd=root,env=env,capture_output=True,text=True,timeout=300)
   record.update(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,trace=trace.name);ck(record['section'],'source exit',r.returncode,0);ck(record['section'],'source stderr',r.stderr,'')
   offsets=[r.stdout.find(stage) for stage in STAGES[n]];ck(record['section'],'all expected stages ordered',all(x>=0 for x in offsets) and offsets==sorted(offsets),True)
   children=json.loads(trace.read_text());negative=[x for x in children if x['returncode']!=0];record['child_records']=len(children)
   ck(record['section'],'nonzero children count',len(negative),1 if n in (6,8) else 0)
   if n==6:
    diagnostic=''.join((x['stdout'] or '')+(x['stderr'] or '') for x in negative).lower();ck('5.6','missing dependency identified','book1-unit-demo' in diagnostic,True);ck('5.6','expected pip check exit',[x['returncode'] for x in negative],[1])
    # The unchanged original requires install/check/behavior repair before cleanup.
    ck('5.6','repair followed failure',r.stdout.find('REPAIR:')>r.stdout.find('BROKEN STATE:'),True)
   if n==8:
    diagnostic=''.join((x['stdout'] or '')+(x['stderr'] or '') for x in negative).lower();ck('5.8','hash failure identified','hash' in diagnostic and 'book1' in diagnostic,True);ck('5.8','expected rejection exit',[x['returncode'] for x in negative],[1]);ck('5.8','approved retry follows rejection',r.stdout.find('SECOND INSTALL:')>r.stdout.find('NEGATIVE CHECK:'),True)
    start=r.stdout.find('{\n');stop=r.stdout.rfind('\nPASS:')
    if r.returncode!=0:continue
    evidence=json.loads(r.stdout[start:stop]);record['source_evidence']=evidence;ck('5.8','independent unit fixture expectation',evidence['result'],dict(versions={'book1-report-demo':'1.0.0','book1-unit-demo':'1.0.0'},input='12.50',output=['instrument_units','12.50']));ck('5.8','input text hash',evidence['input_sha256'],hashlib.sha256(b'12.50').hexdigest())
  # Ordinary import uses same-directory Section5.6 helper; no environment setup on import.
  r=subprocess.run([sys.executable,'-B','-c','import pip_dependency_lab,virtual_environment_lab,reproducibility_lab'],cwd=root,env=env,capture_output=True,text=True,timeout=30);records.append(dict(section='imports',returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));ck('imports','quiet helper/source imports',(r.returncode,r.stdout,r.stderr),(0,'',''))
  # Manual Linux Section5.7.4 pattern, explicitly separate from no-pip automated marker lab.
  environment=root/'manual-venv';r=subprocess.run([sys.executable,'-B','-m','venv',str(environment)],cwd=root,env=env,capture_output=True,text=True,timeout=120);manual=dict(create_returncode=r.returncode,create_stdout=r.stdout,create_stderr=r.stderr);ck('5.7-manual','create venv',r.returncode,0)
  python=environment/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
  inspect="import json,sys,sysconfig;print(json.dumps(dict(executable=sys.executable,prefix=sys.prefix,base_prefix=sys.base_prefix,purelib=sysconfig.get_path('purelib'),isolated=sys.flags.isolated)))"
  r=subprocess.run([str(python),'-I','-c',inspect],cwd=root,env=env,capture_output=True,text=True,timeout=30);manual['inspect']=dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr);info=json.loads(r.stdout);ck('5.7-manual','reported executable',info['executable'],str(python));ck('5.7-manual','prefix',Path(info['prefix']).resolve(),environment.resolve());ck('5.7-manual','base differs',info['prefix']!=info['base_prefix'],True);ck('5.7-manual','purelib owned',Path(info['purelib']).resolve().is_relative_to(environment.resolve()),True)
  r=subprocess.run([str(python),'-m','pip','--version'],cwd=root,env=env,capture_output=True,text=True,timeout=30);manual['pip']=dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr);ck('5.7-manual','explicit interpreter pip',r.returncode,0)
 out=dict(python=platform.python_version(),platform=platform.platform(),source_workflows=3,predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),records=records,manual=manual,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('records','manual','checks')}));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
