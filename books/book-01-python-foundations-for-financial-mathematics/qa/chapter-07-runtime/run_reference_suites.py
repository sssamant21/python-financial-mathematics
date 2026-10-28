"""Extract and run the Chapter 7 complete reference suites, without rewriting listings."""
import ast,hashlib,json,os,pathlib,platform,re,subprocess,sys
src=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True);results=[]
for f in sorted(src.glob('7.*.md')):
 blocks=[m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())]
 suites=[i for i,x in enumerate(blocks) if 'unittest' in x and '__main__' in x]
 if not suites:continue
 if len(suites)!=1:raise ValueError(f.name)
 idx=suites[0];test=blocks[idx]; folder=out/f.stem;folder.mkdir(exist_ok=True)
 if idx:
  own=[n.module for n in ast.walk(ast.parse(test)) if isinstance(n,ast.ImportFrom) and n.module not in ('pathlib','io','numpy.testing','pandas.testing') and not n.module.startswith(('numpy','pandas'))]
  if len(own)!=1:raise ValueError((f.name,own))
  (folder/(own[0]+'.py')).write_text(blocks[idx-1])
 if f.name.startswith('7.17-'):(folder/'panel.py').write_text(blocks[0])
 if f.name.startswith(('7.05-','7.17-')):
  fixture=re.search(r'(?ms)^```csv\n(.*?)^```\s*$',f.read_text())
  if not fixture:raise ValueError('missing fixture')
  (folder/('holdings.csv' if f.name.startswith('7.05-') else 'prices.csv')).write_text(fixture.group(1))
 (folder/'test_reference.py').write_text(test)
 env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
 proc=subprocess.run([sys.executable,'-W','error::FutureWarning','-m','unittest','-v','test_reference'],cwd=folder,text=True,capture_output=True,timeout=60,env=env)
 demo=None
 if idx:
  demo=subprocess.run([sys.executable,'-W','error::FutureWarning',own[0]+'.py'],cwd=folder,text=True,capture_output=True,timeout=60,env=env)
  (folder/'demo.log').write_text(demo.stdout+demo.stderr)
 compiled=subprocess.run([sys.executable,'-m','compileall','-q','.'],cwd=folder,text=True,capture_output=True,timeout=60,env=env)
 (folder/'compile.log').write_text(compiled.stdout+compiled.stderr)
 log=proc.stdout+proc.stderr;(folder/'tests.log').write_text(log);m=re.search(r'Ran (\d+) tests? in',log)
 result={'file':f.name,'demo_returncode':demo.returncode if demo else None,'compile_returncode':compiled.returncode,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'count':int(m.group(1)) if m else 0,'returncode':proc.returncode,'skipped':bool(re.search('skipped=',log)),'ok':bool(re.search(r'^OK\s*$',log,re.M)),'log':f.stem+'/tests.log'};results.append(result)
 print(f.name,result['count'],'PASS' if result['ok'] and proc.returncode==0 else 'FAIL',flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
(out/'all-tests.log').write_text(''.join('\n===== '+r['file']+' =====\n'+(out/r['log']).read_text()+'\n--- demonstration ---\n'+((out/pathlib.Path(r['log']).parent/'demo.log').read_text() if r['demo_returncode'] is not None else 'Not applicable: standalone solution suite.\n')+'\n--- compile ---\n'+(out/pathlib.Path(r['log']).parent/'compile.log').read_text() for r in results))
if not all(r['ok'] and r['returncode']==0 and not r['skipped'] and r['demo_returncode'] in (None,0) and r['compile_returncode']==0 for r in results):sys.exit(1)
