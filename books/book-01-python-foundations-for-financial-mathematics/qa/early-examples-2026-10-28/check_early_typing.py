"""Check the typed lab and the three deliberately invalid argument calls."""
import hashlib,json,os,pathlib,subprocess,sys
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
if out.exists():raise SystemExit('Use a new output directory')
out.mkdir(parents=True);f=next((root/'chapter-03').glob('3.07-*.md'));b=[t.content for t in MarkdownIt().parse(f.read_text()) if t.type=='fence' and t.info.strip()=='python']
(out/'type_hints_lab.py').write_text(b[9]);(out/'type_hints_bad_calls.py').write_text(b[10]);env=os.environ.copy();env.pop('MYPYPATH',None);env.pop('PYTHONPATH',None);results=[]
for name,args,wanted in [('valid-lab',['-m','mypy','--strict','--no-incremental','--follow-imports=normal','type_hints_lab.py'],0),('invalid-calls',['-m','mypy','--strict','--no-incremental','--follow-imports=normal','type_hints_bad_calls.py'],1)]:
 p=subprocess.run([sys.executable,*args],cwd=out,env=env,capture_output=True,text=True,timeout=60);(out/(name+'.stdout.log')).write_text(p.stdout);(out/(name+'.stderr.log')).write_text(p.stderr)
 passed=p.returncode==wanted and not p.stderr
 if name=='valid-lab':passed=passed and 'Success: no issues found' in p.stdout
 else:passed=passed and p.stdout.count('[arg-type]')==3 and 'Found 3 errors' in p.stdout and all(f'Argument {i}' in p.stdout for i in [1,2,3])
 results.append({'case':name,'command':[sys.executable,*args],'expected_returncode':wanted,'actual_returncode':p.returncode,'status':'PASS' if passed else 'FAIL','stdout':p.stdout,'stderr':p.stderr})
version=subprocess.check_output([sys.executable,'-m','mypy','--version'],text=True).strip();(out/'results.json').write_text(json.dumps({'python':sys.version,'checker':version,'source':str(f.relative_to(root)),'code_hashes':{str(i):hashlib.sha256(b[i].encode()).hexdigest() for i in [9,10]},'results':results},indent=2)+'\n');print(json.dumps(results,indent=2))
if any(r['status']!='PASS' for r in results):sys.exit(1)
