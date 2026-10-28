"""Reconstruct Chapter 5 labs; run local suites and offline environment workflows.

Package verification uses the published exact backend requirement. No dependency
is downloaded, and a missing backend is recorded as BLOCKED rather than bypassed.
"""
import ast,hashlib,json,os,pathlib,re,subprocess,sys
from importlib.metadata import version,PackageNotFoundError
src=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True);results=[]
config={
1:{'files':{'holdings_core.py':1,'run_holdings.py':2,'test_holdings_modules.py':3},'test':'test_holdings_modules','demo':['run_holdings.py']},
2:{'files':{'quantity_rules.py':0,'import_styles.py':1,'test_import_styles.py':2},'test':'test_import_styles','demo':['import_styles.py']},
3:{'files':{'standard_library_lab.py':3},'test':'standard_library_lab'},
4:{'files':{'schedule_utils.py':0,'run_schedule.py':1,'test_schedule_utils.py':2},'test':'test_schedule_utils','demo':['run_schedule.py']},
5:{'files':{'finance_lab/holdings.py':0,'finance_lab/views.py':1,'finance_lab/__init__.py':2,'finance_lab/__main__.py':3,'test_finance_lab.py':4},'test':'test_finance_lab','demo':['-m','finance_lab']},
6:{'files':{'pip_dependency_lab.py':0},'workflow':['pip_dependency_lab.py']},
7:{'files':{'environment_lab.py':0},'workflow':['environment_lab.py']},
8:{'files':{'repeatability_lab.py':0},'workflow':['repeatability_lab.py']},
9:{'files':{'financial_layout/__init__.py':0,'financial_layout/quantities.py':1,'financial_layout/__main__.py':2,'tests/test_layout.py':3},'testdir':'tests','demo':['-m','financial_layout','--input','fixtures/holdings.json']},
10:{'files':{'configuration.py':0,'config_demo.py':1,'test_configuration.py':2},'test':'test_configuration','demo':['config_demo.py','--config','development.json']},
11:{'files':{'research.py':0,'test_research.py':1},'test':'test_research','demo':['research.py','--input','inflows.json','--config','settings.json','--output','report.json']},
12:{'files':{'src/financial_inflows/__init__.py':0,'src/financial_inflows/core.py':1,'src/financial_inflows/cli.py':2,'src/financial_inflows/__main__.py':3,'tests/test_inflows.py':4,'verify_package.py':5}}
}
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)

def write(folder,name,text):
 p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def execute(folder,label,args,timeout=300):
 proc=subprocess.run([sys.executable,*args],cwd=folder,env=env,capture_output=True,text=True,timeout=timeout)
 log=proc.stdout+proc.stderr;write(folder,label+'.log',log)
 count=re.search(r'Ran (\d+) tests? in',log)
 return {'operation':label,'command':[sys.executable,*args],'returncode':proc.returncode,'test_count':int(count.group(1)) if count else None,'unittest_ok':bool(re.search(r'^OK\s*$',log,re.M)),'skipped':bool(re.search(r'skipped=',log)),'log':str(folder.relative_to(out)/(label+'.log'))}
for f in sorted(src.glob('5.*.md')):
 n=int(f.name.split('.')[1][:2])
 if n not in config:continue
 text=f.read_text();blocks=[m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',text)];folder=out/f.stem;folder.mkdir(exist_ok=True);cfg=config[n]
 for name,i in cfg['files'].items():ast.parse(blocks[i]);write(folder,name,blocks[i])
 if n==8:
  dep=next(src.glob('5.06-*.md')).read_text();code=re.search(r'(?ms)^```python\n(.*?)^```\s*$',dep).group(1);write(folder,'pip_dependency_lab.py',code)
 fixtures={9:['fixtures/holdings.json'],10:['development.json'],11:['inflows.json','settings.json'],12:['fixtures/inflows.json','fixtures/settings.json']}
 if n in fixtures:
  jb=[m.group(1) for m in re.finditer(r'(?ms)^```json\n(.*?)^```\s*$',text)]
  for name,code in zip(fixtures[n],jb):write(folder,name,code)
 if n==12:
  for lang,name in [('toml','pyproject.toml'),('markdown','README.md'),('gitignore','.gitignore')]:write(folder,name,re.search(r'(?ms)^```'+lang+r'\n(.*?)^```\s*$',text).group(1))
 ops=[]
 if 'test' in cfg:ops.append(execute(folder,'tests',['-W','error::FutureWarning','-m','unittest','-v',cfg['test']]))
 if 'testdir' in cfg:ops.append(execute(folder,'tests',['-W','error::FutureWarning','-m','unittest','discover','-s',cfg['testdir'],'-v']))
 if 'demo' in cfg:ops.append(execute(folder,'demo',['-W','error::FutureWarning',*cfg['demo']]))
 if 'workflow' in cfg:ops.append(execute(folder,'workflow',cfg['workflow']))
 if n==12:
  try:backend=version('setuptools')
  except PackageNotFoundError:backend=None
  if backend=='84.0.0':ops.append(execute(folder,'package',['verify_package.py']))
  else:
   ops.append(execute(folder,'backend-prerequisite',['verify_package.py']))
   ops[-1]['status']='BLOCKED';ops[-1]['reason']=f'Published verifier requires setuptools 84.0.0; current builder has {backend}. No cached exact wheel found; no dependency downloaded.'
 ops.append(execute(folder,'compile',['-m','compileall','-q','.']))
 results.append({'file':f.name,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'operations':ops})
 print(f.name,[(x['operation'],x.get('status',x['returncode']),x['test_count']) for x in ops],flush=True)
f=src/'solutions/5.13-solutions-and-reference-implementations.md'
folder=out/'5.13-installed-package-extension';folder.mkdir(exist_ok=True)
import shutil
base=out/'5.12-chapter-project-reusable-financial-python-package'
for name in ('src','fixtures','tests'):
 shutil.copytree(base/name,folder/name,dirs_exist_ok=True)
for name in ('pyproject.toml','README.md','verify_package.py'):
 shutil.copyfile(base/name,folder/name)
block=re.search(r'(?ms)^```python\n(.*?)^```\s*$',f.read_text()).group(1)
p=folder/'tests/test_inflows.py';text=p.read_text();marker="if __name__ == '__main__':"
if text.count(marker)!=1:raise ValueError('expected one main guard')
p.write_text(text.replace(marker,block+'\n\n'+marker))
p=folder/'verify_package.py';p.write_text(p.read_text().replace('PASS: 8 installed tests;','PASS: 12 installed tests;'))
try:backend=version('setuptools')
except PackageNotFoundError:backend=None
op=execute(folder,'package' if backend=='84.0.0' else 'backend-prerequisite',['verify_package.py'])
if backend!='84.0.0':op.update(status='BLOCKED',reason=f'Exact published builder backend 84.0.0 unavailable; found {backend}. Extension installed tests not run.')
ops=[op,execute(folder,'compile',['-m','compileall','-q','.'])]
results.append({'file':str(f.relative_to(src)),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'operations':ops})
print(str(f.relative_to(src)),[(x['operation'],x.get('status',x['returncode']),x['test_count']) for x in ops],flush=True)

(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
(out/'all-checks.log').write_text(''.join('\n===== '+r['file']+' / '+op['operation']+' =====\n'+(out/op['log']).read_text() for r in results for op in r['operations']))
if any(op['returncode'] and op.get('status')!='BLOCKED' for r in results for op in r['operations']):sys.exit(1)
if any(op.get('status')=='BLOCKED' for r in results for op in r['operations']):sys.exit(2)
