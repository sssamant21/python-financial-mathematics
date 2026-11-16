"""Stage exact pinned manuscript fences, run source suite/probe and retain output.
Usage: python source-review.py REV baseline|corrected OUTPUT_STEM
Baseline runs the new contract probe only; corrected also runs the three core
example/suite/compile commands. No installed artifact acceptance.
"""
from pathlib import Path
import subprocess,sys,tempfile,re,json,hashlib,platform,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];REV=sys.argv[1];mode=sys.argv[2];stem=sys.argv[3];assert mode in ('baseline','corrected');base='books/book-01-python-foundations-for-financial-mathematics/chapter-21/'
names=['21.14-visualization-layer.md','21.13-data-validation-layer.md','21.12-simulation-module.md','21.11-statistical-module.md','21.10-portfolio-module.md','21.09-return-and-performance-module.md','21.08-bond-module.md','21.07-loan-module.md','21.06-cash-flow-module.md','21.05-time-value-of-money-module.md','21.03-project-structure.md'];texts=[subprocess.check_output(['git','show',REV+':'+base+n],cwd=ROOT,text=True) for n in names];blocks=[re.findall(r'```python\n(.*?)\n```',s,re.S) for s in texts];assert all(len(b)==4 for b in blocks)
mods=['visualization','validation','simulation','statistics','portfolio','returns','bonds','loans','cashflows','time_value'];testnames=['visualization','validation','simulation','statistics_module','portfolio','returns','bonds','loans','cashflows','tvm_multi'];files={}
for mod,test,b in zip(mods,testnames,blocks):files['src/financial_toolkit/'+mod+'.py']=b[0];files['tests/test_'+test+'.py']=b[3]
files['src/financial_toolkit/__init__.py']=blocks[0][1];files['examples/visualization.py']=blocks[0][2];files['tests/test_time_value.py']=blocks[-1][3];rows=[]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for name,s in files.items():p=t/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 env=dict(os.environ);env['PYTHONPATH']=str(t/'src');env.pop('PYTHONOPTIMIZE',None);env['MPLBACKEND']='Agg'
 args=[['examples/visualization.py'],['-m','unittest','discover','-s','tests','-v'],['-m','compileall','-q','src','tests','examples']] if mode=='corrected' else []
 args.append([str(OUT/'contracts.py'),str(OUT/(stem+'-predicates.json'))])
 if mode=='corrected':args.append([str(OUT/'lazy-import.py'),str(OUT/(stem+'-lazy.json'))])
 for a in args:
  argv=[sys.executable]+a;z=subprocess.run(argv,cwd=t,env=env,capture_output=True,text=True,timeout=60);rows.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr,source_path_injection=True))
  if mode=='corrected' and a==['examples/visualization.py']:
   import shutil
   import base64
   raw=(t/'synthetic_price.png').read_bytes();(OUT/'visual-artifact.json').write_text(json.dumps(dict(filename='synthetic_price.png',sha256=hashlib.sha256(raw).hexdigest(),encoding='base64',content=base64.b64encode(raw).decode(),source_revision=REV),indent=2)+'\n')
 d=dict(source_revision=REV,mode=mode,source_paths=[base+n for n in names],staged_fence_sha256={n:hashlib.sha256(s.encode()).hexdigest() for n,s in files.items()},python=sys.version,platform=platform.platform(),commands=rows,existing_unique_methods=134,new_historical_unique_methods=0,method_invocations=134 if mode=='corrected' else 0,limits='Exact source staging with explicit PYTHONPATH. No editable/wheel/install/formal-workflow or platform/independent acceptance. Baseline UTC failures retained; corrected core suite separate from contract predicates.')
(OUT/(stem+'.json')).write_text(json.dumps(d,indent=2)+'\n');print(mode,[(x['returncode']) for x in rows]);assert all(x['returncode']==0 for x in rows) if mode=='corrected' else rows[-1]['returncode']==1
