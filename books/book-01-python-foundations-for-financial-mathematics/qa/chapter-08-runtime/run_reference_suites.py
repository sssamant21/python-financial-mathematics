import ast,json,pathlib,re,subprocess,sys,os
src=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True,exist_ok=True); results=[]
for f in sorted(src.glob('8.*.md')):
 blocks=[m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())]
 tests=[x for x in blocks if 'unittest' in x and '__main__' in x]
 if not tests:continue
 test=tests[0]
 if f.name.startswith('8.13-'):
  fixture=re.search(r'(?ms)^```csv\n(.*?)^```\s*$',f.read_text())
  if not fixture: raise ValueError('dashboard CSV fixture missing')
  (out/'prices.csv').write_text(fixture.group(1))
 code=[x for x in blocks if '__main__' in x and x is not test]
 if code:
  tree=ast.parse(test); names=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module and n.module not in ('numpy.testing','pandas.testing','pathlib','xml.etree')]
  own=[n for n in names if n not in ('datetime','zoneinfo')]
  if len(own)!=1: raise ValueError((f.name,own))
  (out/(own[0]+'.py')).write_text(code[0])
 module='test_'+f.name.replace('.md','').replace('.','_').replace('-','_'); (out/(module+'.py')).write_text(test)
 env=os.environ.copy();env['MPLBACKEND']='Agg';env['PYTHONDONTWRITEBYTECODE']='1'
 proc=subprocess.run([sys.executable,'-m','unittest','-v',module],cwd=out,text=True,capture_output=True,timeout=90,env=env)
 log=proc.stdout+proc.stderr;(out/(module+'.log')).write_text(log); m=re.search(r'Ran (\d+) tests? in',log); results.append({'file':f.name,'count':int(m.group(1)) if m else 0,'returncode':proc.returncode,'skipped':bool(re.search(r'skipped=',log)), 'ok': bool(re.search(r'^OK\s*$',log,re.M)),'log':module+'.log'})
 print(f.name,results[-1]['count'], 'PASS' if results[-1]['ok'] and proc.returncode==0 else 'FAIL',flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
