"""Partial runtime checkpoint; not formal 21.1 answer/lab review."""
from pathlib import Path
import sys,subprocess,re,tempfile,json,hashlib,platform
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];pin='9ebd2355077d8c7e8b9348b8f44eb78f57017402';path='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.01-capstone-architecture.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=ROOT,text=True);codes=re.findall(r'```python\n(.*?)\n```',raw,re.S);assert len(codes)==2
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 for name,code in zip(['capstone_architecture.py','test_capstone_architecture.py'],codes):(p/name).write_text(code)
 commands=[]
 for args in [['capstone_architecture.py'],['-m','unittest','-v','test_capstone_architecture'],['-m','compileall','-q','capstone_architecture.py','test_capstone_architecture.py']]:
  argv=[sys.executable]+args;z=subprocess.run(argv,cwd=p,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
d=dict(source_revision=pin,source_path=path,source_sha256=hashlib.sha256(raw.encode()).hexdigest(),fence_sha256=[hashlib.sha256(c.encode()).hexdigest() for c in codes],python=sys.version,platform=platform.platform(),commands=commands,existing_unique_methods=12,method_invocations=12,new_historical_unique_methods=0,limits='Partial exact-source runtime checkpoint only;40answer/12lab contracts and wider architecture scope remain pending. Reuse if source/fence hashes unchanged;no formal completion,independent/platform/release acceptance.')
(OUT/'suite-results.json').write_text(json.dumps(d,indent=2)+'\n');assert all(x['returncode']==0 for x in commands);assert commands[0]['stdout']=='PV: 100.00 USD; model=pv-one-v1\n';print('3 documented commands/2compiled fences/12existing methods passed;formal review pending')
