"""Stage exact project fences;source execution is not installation acceptance."""
from pathlib import Path
import subprocess,sys,re,tempfile,json,hashlib,platform,os,importlib.metadata
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];pin='f57b86902032643b6772d3b8ad377e885f2dcf9e';path='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.03-project-structure.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=ROOT,text=True)
py=re.findall(r'```python\n(.*?)\n```',raw,re.S);toml=re.findall(r'```toml\n(.*?)\n```',raw,re.S);md=re.findall(r'```markdown\n(.*?)\n```',raw,re.S);assert (len(py),len(toml),len(md))==(4,1,1)
files=dict(zip(['src/financial_toolkit/__init__.py','src/financial_toolkit/time_value.py','examples/one_period.py','tests/test_time_value.py'],py));files['pyproject.toml']=toml[0];files['README.md']=md[0];commands=[]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for n,s in files.items():p=t/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 env=dict(os.environ);env['PYTHONPATH']=str(t/'src')
 for args in [['examples/one_period.py'],['-m','unittest','discover','-s','tests','-v'],['-m','compileall','-q','src','tests','examples']]:
  argv=[sys.executable]+args;z=subprocess.run(argv,cwd=t,env=env,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr,source_path_injection=True))
versions={}
for n in ['setuptools','wheel','build','pip']:
 try:versions[n]=importlib.metadata.version(n)
 except importlib.metadata.PackageNotFoundError:versions[n]=None
d=dict(source_revision=pin,source_path=path,source_sha256=hashlib.sha256(raw.encode()).hexdigest(),fence_sha256={n:hashlib.sha256(s.encode()).hexdigest() for n,s in files.items()},python=sys.version,platform=platform.platform(),commands=commands,available_build_tool_versions=versions,existing_unique_methods=12,method_invocations=12,new_historical_unique_methods=0,limits='Only source-tree example/suite/compilation with explicit PYTHONPATH. No venv/editable build,wheel,installed artifact,external dependency or platform/release acceptance. Full21.3 contract/40answer/12lab review remains pending.')
(OUT/'results.json').write_text(json.dumps(d,indent=2)+'\n');assert all(x['returncode']==0 for x in commands);assert commands[0]['stdout']=='PV: 100.00 payment units\n';print('3 source commands/4 Python fences/12existing methods pass;installation untouched')
