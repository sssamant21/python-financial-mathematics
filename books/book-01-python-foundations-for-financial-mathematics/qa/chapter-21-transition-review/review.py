"""Stage immutable manuscript fence and execute documented checks plus independent observer.
Usage: python THIS source_revision first|replay
"""
from pathlib import Path
import sys,subprocess,hashlib,json,re,tempfile,platform
here=Path(__file__).resolve().parent;root=here.parents[3];pin=sys.argv[1];stem=sys.argv[2]
path='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.18-further-study-and-transition-to-book-2.md'
raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);sha=subprocess.check_output(['git','rev-parse',pin+':'+path],cwd=root,text=True).strip()
def blob(x):return hashlib.sha1(b'blob '+str(len(x)).encode()+b'\0'+x).hexdigest()
assert blob(raw)==sha
fences=re.findall(r'```python\n(.*?)```',raw.decode(),re.S);assert len(fences)==1
source=fences[0].encode();commands=[]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);s=t/'book1_transition_checks.py';s.write_bytes(source)
 for argv in [[sys.executable,'book1_transition_checks.py'],[sys.executable,'-m','compileall','-q','book1_transition_checks.py'],[sys.executable,str(here/'contracts.py'),str(s),str(here/(stem+'-predicates.json'))]]:
  z=subprocess.run(argv,cwd=t,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 assert s.read_bytes()==source
result=dict(source_revision=pin,source_path=path,source_blob=sha,fence_sha256=hashlib.sha256(source).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,source_unchanged_after=True,reference_methods=12,limits='Standalone12methods plus12observerpredicates; no package/installedwheel execution or independent acceptance.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(stem,[x['returncode'] for x in commands]);assert all(x['returncode']==0 for x in commands)
