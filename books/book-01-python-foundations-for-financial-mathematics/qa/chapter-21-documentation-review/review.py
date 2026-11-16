"""Execute exact standalone metadata fences and a separately staged PV example.
Usage: python THIS source_revision
"""
from pathlib import Path
import subprocess,sys,tempfile,re,json,hashlib,os,platform
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];REV=sys.argv[1];STEM=sys.argv[2] if len(sys.argv)>2 else 'results';path='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.16-documentation-and-reproducibility.md';financial='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.05-time-value-of-money-module.md';text=subprocess.check_output(['git','show',REV+':'+path],cwd=ROOT,text=True);blocks=re.findall(r'```python\n(.*?)\n```',text,re.S);assert len(blocks)==2;tv=re.findall(r'```python\n(.*?)\n```',subprocess.check_output(['git','show',REV+':'+financial],cwd=ROOT,text=True),re.S);assert len(tv)==4;files={'run_metadata.py':blocks[0],'test_run_metadata.py':blocks[1],'time_value.py':tv[0]};commands=[]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for n,s in files.items():(t/n).write_text(s)
 env=dict(os.environ);env['PYTHONPATH']=str(t);env.pop('PYTHONOPTIMIZE',None)
 for a in [['run_metadata.py'],['-m','unittest','-v','test_run_metadata'],['-m','compileall','-q','run_metadata.py','test_run_metadata.py'],[str(OUT/'contracts.py'),str(OUT/(STEM+'-predicates.json')),REV]]:
  argv=[sys.executable]+a;z=subprocess.run(argv,cwd=t,env=env,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 d=dict(source_revision=REV,source_paths=[path,financial],staged_sha256={n:hashlib.sha256(s.encode()).hexdigest() for n,s in files.items()},commands=commands,python=sys.version,platform=platform.platform(),existing_reference_methods=12,method_invocations=12,newly_authored_unittest_methods=0,limits='Standalone metadata example and source-injected controls;separate PV module stage is not integration into metadata helper. Prior wheel/toolkit evidence not rerun or recounted. No cryptographic/security/provenance/model/platform/release approval.')
(OUT/(STEM+'.json')).write_text(json.dumps(d,indent=2)+'\n');print('commands',len(commands),[x['returncode'] for x in commands]);assert all(x['returncode']==0 for x in commands)
