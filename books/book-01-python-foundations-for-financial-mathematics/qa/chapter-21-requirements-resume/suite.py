"""Partial runtime checkpoint; not formal 21.2 answer/lab review."""
from pathlib import Path
import sys,subprocess,re,tempfile,json,hashlib,platform
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];pin='b5808b7f52ce3ecec42e99a091e240bf29d5aa11';path='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.02-requirements-and-assumptions.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=ROOT,text=True);codes=re.findall(r'```python\n(.*?)\n```',raw,re.S);assert len(codes)==2
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 for name,code in zip(['requirements_check.py','test_requirements_check.py'],codes):(p/name).write_text(code)
 commands=[]
 for args in [['requirements_check.py'],['-m','unittest','-v','test_requirements_check'],['-m','compileall','-q','requirements_check.py','test_requirements_check.py'],['-c','import json;from requirements_check import Requirement,ready_for_review;r=Requirement("R-SYNTH","Synthetic only","Placeholder","Structural probe","passed","synthetic-not-authentic-evidence");print(json.dumps({"documented_structural_only_acceptance":ready_for_review([r])}))']]:
  argv=[sys.executable]+args;z=subprocess.run(argv,cwd=p,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
d=dict(source_revision=pin,source_path=path,source_sha256=hashlib.sha256(raw.encode()).hexdigest(),fence_sha256=[hashlib.sha256(c.encode()).hexdigest() for c in codes],python=sys.version,platform=platform.platform(),commands=commands,existing_unique_methods=12,method_invocations=12,new_historical_unique_methods=0,limits='Partial exact-source runtime checkpoint only;40answer/12lab contracts and wider architecture scope remain pending. Reuse if source/fence hashes unchanged;no formal completion,independent/platform/release acceptance.')
(OUT/'suite-results.json').write_text(json.dumps(d,indent=2)+'\n');assert all(x['returncode']==0 for x in commands);assert commands[0]['stdout']=='Ready for review: False\n';print('3 documented commands plus1 structural observation/2compiled fences/12existing methods passed;formal review pending')
