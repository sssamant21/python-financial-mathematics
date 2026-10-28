"""Reconstruct Chapter 5.12 and companion projects; verify regular installed wheels.

Usage: python run_package_checks.py CHAPTER05_DIR NEW_OUTPUT_DIR BUILDER_PYTHON
The builder must already have pip and setuptools exactly 84.0.0.
"""
import ast,hashlib,json,pathlib,re,subprocess,sys,os
source=pathlib.Path(sys.argv[1]).resolve();output=pathlib.Path(sys.argv[2]).resolve();builder=pathlib.Path(sys.argv[3]).resolve()
if output.exists():raise SystemExit('Choose a new output directory; existing evidence will not be overwritten.')
output.mkdir(parents=True)
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
info=subprocess.run([str(builder),'-I','-c','import json,platform;from importlib.metadata import version;print(json.dumps({"python":platform.python_version(),"pip":version("pip"),"setuptools":version("setuptools")}))'],env=env,text=True,capture_output=True,check=True,timeout=30)
versions=json.loads(info.stdout)
if versions['setuptools']!='84.0.0':raise SystemExit('Builder requires setuptools exactly 84.0.0')
f=next(source.glob('5.12-*.md'));text=f.read_text();blocks=[m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',text)]
files={name:blocks[i] for name,i in {'src/financial_inflows/__init__.py':0,'src/financial_inflows/core.py':1,'src/financial_inflows/cli.py':2,'src/financial_inflows/__main__.py':3,'tests/test_inflows.py':4,'verify_package.py':5}.items()}
for lang,name in [('toml','pyproject.toml'),('markdown','README.md')]:files[name]=re.search(r'(?ms)^```'+lang+r'\n(.*?)^```\s*$',text).group(1)
fixtures=[m.group(1) for m in re.finditer(r'(?ms)^```json\n(.*?)^```\s*$',text)]
files['fixtures/inflows.json'],files['fixtures/settings.json']=fixtures[:2]
companion=source/'solutions/5.13-solutions-and-reference-implementations.md'
extension=re.search(r'(?ms)^```python\n(.*?)^```\s*$',companion.read_text()).group(1)
results=[]
for name,expected in [('base',8),('extended',12)]:
 folder=output/name;folder.mkdir()
 listings=files.copy()
 if name=='extended':
  guard="if __name__ == '__main__':"
  if listings['tests/test_inflows.py'].count(guard)!=1:raise ValueError('expected one main guard')
  listings['tests/test_inflows.py']=listings['tests/test_inflows.py'].replace(guard,extension+'\n\n'+guard)
  listings['verify_package.py']=listings['verify_package.py'].replace('PASS: 8 installed tests;','PASS: 12 installed tests;')
 for relative,contents in listings.items():
  target=folder/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(contents)
  if target.suffix=='.py':ast.parse(contents)
 proc=subprocess.run([str(builder),'verify_package.py'],cwd=folder,env=env,text=True,capture_output=True,timeout=300)
 log=proc.stdout+proc.stderr;(output/(name+'.log')).write_text(log)
 matches=re.findall(r'Ran (\d+) tests? in',log);count=int(matches[0]) if len(matches)==1 else None
 compiled=subprocess.run([str(builder),'-m','compileall','-q','src','tests','verify_package.py'],cwd=folder,env=env,text=True,capture_output=True,timeout=30)
 (output/(name+'-compile.log')).write_text(compiled.stdout+compiled.stderr)
 result={'project':name,'expected_test_count':expected,'actual_test_count':count,'returncode':proc.returncode,'compile_returncode':compiled.returncode,'unittest_ok':bool(re.search(r'^OK\s*$',log,re.M)),'wheel_sha256':re.search(r'Wheel SHA-256: ([0-9a-f]{64})',log).group(1) if re.search(r'Wheel SHA-256: ([0-9a-f]{64})',log) else None,'status':'PASS' if proc.returncode==0 and count==expected and re.search(r'^OK\s*$',log,re.M) and compiled.returncode==0 else 'FAIL','log':name+'.log'}
 results.append(result);print(json.dumps(result),flush=True)
evidence={'builder_versions':versions,'source_sha256':{str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (f,companion)},'results':results,'unique_installed_test_methods':12,'installed_test_invocations':sum(x['actual_test_count'] or 0 for x in results)}
(output/'results.json').write_text(json.dumps(evidence,indent=2)+'\n')
if any(x['status']!='PASS' for x in results):sys.exit(1)
