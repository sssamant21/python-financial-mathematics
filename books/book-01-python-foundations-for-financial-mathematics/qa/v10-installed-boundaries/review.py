"""Build pinned exact scaffold offline; test installed wheel with isolated probes."""
from pathlib import Path
import subprocess,sys,re,tempfile,json,hashlib,platform,os,zipfile
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV='7e98df4194191241042e19c5dba66873a8b4a852';base='books/book-01-python-foundations-for-financial-mathematics/chapter-21/';sources={};files={};mapping=[('21.12-simulation-module.md','simulation'),('21.11-statistical-module.md','statistics'),('21.10-portfolio-module.md','portfolio'),('21.09-return-and-performance-module.md','returns'),('21.08-bond-module.md','bonds'),('21.07-loan-module.md','loans'),('21.06-cash-flow-module.md','cashflows'),('21.05-time-value-of-money-module.md','time_value')]
for name,module in mapping:
 raw=subprocess.check_output(['git','show',REV+':'+base+name],cwd=ROOT);fences=re.findall(r'```python\n(.*?)\n```',raw.decode(),re.S);assert len(fences)==4;files['src/financial_toolkit/'+module+'.py']=fences[0];sources[base+name]=hashlib.sha256(raw).hexdigest()
 if module=='simulation':files['src/financial_toolkit/__init__.py']=fences[1]
raw=subprocess.check_output(['git','show',REV+':'+base+'21.03-project-structure.md'],cwd=ROOT);text=raw.decode();files['pyproject.toml']=re.findall(r'```toml\n(.*?)\n```',text,re.S)[0];files['README.md']=re.findall(r'```markdown\n(.*?)\n```',text,re.S)[0];sources[base+'21.03-project-structure.md']=hashlib.sha256(raw).hexdigest();prior=json.loads((BOOK/'qa/chapter-21-simulation-resume/results.json').read_text());unchanged={name:hashlib.sha256(text.encode()).hexdigest()==prior['staged_fence_sha256'][name] for name,text in files.items() if name in prior['staged_fence_sha256']};assert all(unchanged.values());commands=[]
def run(label,argv,cwd,env):
 z=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True,timeout=120);commands.append(dict(label=label,argv=list(map(str,argv)),returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0;return z
try:
 with tempfile.TemporaryDirectory(prefix='book1-v10-wheel-') as td:
  temp=Path(td);project=temp/'project';project.mkdir();outside=temp/'outside';outside.mkdir();build=temp/'build';consumer=temp/'consumer';wheels=temp/'wheels';wheels.mkdir();env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONNOUSERSITE']='1';env['PIP_NO_INDEX']='1';env['PIP_DISABLE_PIP_VERSION_CHECK']='1'
  for name,text in files.items():p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
  run('build environment local tools',[sys.executable,'-m','venv','--system-site-packages',build],temp,env);bp=build/'bin/python'
  run('tool versions',[bp,'-c','import importlib.metadata as m;print({x:m.version(x) for x in ["pip","setuptools","wheel"]})'],outside,env)
  run('offline exact-scaffold wheel build',[bp,'-m','pip','wheel','--no-index','--no-build-isolation','--no-deps','--wheel-dir',wheels,'.'],project,env);found=list(wheels.glob('*.whl'));assert len(found)==1;wheel=found[0]
  with zipfile.ZipFile(wheel) as z:artifact=dict(filename=wheel.name,sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),size=wheel.stat().st_size,members={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()})
  run('clean consumer',[sys.executable,'-m','venv',consumer],outside,env);cp=consumer/'bin/python';run('offline local wheel install',[cp,'-m','pip','install','--no-index','--no-deps',wheel],outside,env)
  project.rename(temp/'source-hidden');(outside/'probe.py').write_bytes((OUT/'probe.py').read_bytes())
  for stage in ['first','replay']:
   run('isolated installed '+stage,[cp,'-I',outside/'probe.py',outside/(stage+'.json')],outside,env);raw=(outside/(stage+'.json')).read_bytes();(OUT/(stage+'.json')).write_bytes(raw);data=json.loads(raw)
   for module,identity in data['installed_modules'].items():assert identity['sha256']==hashlib.sha256(files['src/'+module.replace('.','/')+'.py'].encode()).hexdigest()
  a=json.loads((OUT/'first.json').read_text());b=json.loads((OUT/'replay.json').read_text());assert a['rows']==b['rows'];(OUT/'artifact-manifest.json').write_text(json.dumps(dict(source_pin=REV,source_sha256=sources,staged_sha256={n:hashlib.sha256(s.encode()).hexdigest() for n,s in files.items()},prior_selected_fences_unchanged=unchanged,artifact=artifact),indent=2)+'\n')
finally:(OUT/'commands.json').write_text(json.dumps(dict(source_pin=REV,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),commands=commands,scope='New selected clean-wheel probes, not rerun of355 historical predicates or108 methods; no global/index installation or release acceptance'),indent=2)+'\n')
print('installed checks',a['passed'],b['passed'],'commands',len(commands))
