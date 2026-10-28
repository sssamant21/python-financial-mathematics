"""Extract Chapter 4 complete reference suites and run them in separate directories.

Usage: python run_reference_checks.py CHAPTER04_DIR NEW_OUTPUT_DIR
"""
import ast,hashlib,json,os,pathlib,platform,re,subprocess,sys
source=pathlib.Path(sys.argv[1]).resolve();output=pathlib.Path(sys.argv[2]).resolve()
if output.exists():raise SystemExit('Choose a new output directory to preserve previous evidence.')
output.mkdir(parents=True)
def blocks(f):return [m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())]
project=next(source.glob('4.13-*.md'));project_blocks=blocks(project)
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env['PYTHONDONTWRITEBYTECODE']='1'
results=[]
for f in sorted(source.rglob('4.*.md')):
 b=blocks(f);suites=[x for x in b if 'unittest' in x and '__main__' in x]
 if not suites:continue
 if len(suites)!=1:raise ValueError(f.name)
 code=suites[0];tree=ast.parse(code);expected=sum(isinstance(n,ast.FunctionDef) and n.name.startswith('test_') for c in tree.body if isinstance(c,ast.ClassDef) for n in c.body)
 folder=output/f.stem;folder.mkdir()
 module='portfolio_holdings_manager' if f.name.startswith('4.13-') else 'chapter04_solutions' if f.parent.name=='solutions' else 'reference'
 (folder/(module+'.py')).write_text(code)
 support=None
 if f.parent.name=='solutions':
  (folder/'portfolio_holdings_manager.py').write_text(project_blocks[0]);support=hashlib.sha256(project.read_bytes()).hexdigest()
 proc=subprocess.run([sys.executable,'-W','error::FutureWarning','-m','unittest','-v',module],cwd=folder,env=env,text=True,capture_output=True,timeout=45)
 log=proc.stdout+proc.stderr;(folder/'tests.log').write_text(log);m=re.search(r'Ran (\d+) tests? in',log);count=int(m.group(1)) if m else None
 ops=[{'operation':'tests','command':[sys.executable,'-W','error::FutureWarning','-m','unittest','-v',module],'returncode':proc.returncode,'expected_test_count':expected,'actual_test_count':count,'ok':bool(re.search(r'^OK\s*$',log,re.M)),'skipped':bool(re.search('skipped=',log)),'log':f.stem+'/tests.log'}]
 if f.name.startswith('4.13-'):
  ast.parse(project_blocks[1]);(folder/'demo_holdings_manager.py').write_text(project_blocks[1])
  demo=subprocess.run([sys.executable,'-W','error::FutureWarning','demo_holdings_manager.py'],cwd=folder,env=env,text=True,capture_output=True,timeout=30)
  (folder/'demo.log').write_text(demo.stdout+demo.stderr);ops.append({'operation':'demonstration','returncode':demo.returncode,'log':f.stem+'/demo.log'})
 compiled=subprocess.run([sys.executable,'-m','compileall','-q','.'],cwd=folder,env=env,text=True,capture_output=True,timeout=30)
 (folder/'compile.log').write_text(compiled.stdout+compiled.stderr);ops.append({'operation':'compilation','returncode':compiled.returncode,'log':f.stem+'/compile.log'})
 results.append({'file':str(f.relative_to(source)),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'supporting_project_sha256':support,'operations':ops})
 print(f.name,count,'PASS' if proc.returncode==0 and count==expected and ops[0]['ok'] and not ops[0]['skipped'] and all(x['returncode']==0 for x in ops) else 'FAIL',flush=True)
evidence={'environment':{'python':platform.python_version(),'platform':platform.platform(),'dependencies':'Python standard library'},'results':results}
(output/'results.json').write_text(json.dumps(evidence,indent=2)+'\n')
(output/'all-checks.log').write_text(''.join('\n===== '+r['file']+' / '+op['operation']+' =====\n'+(output/op['log']).read_text() for r in results for op in r['operations']))
if len(results)!=14 or any(op['returncode'] or (op['operation']=='tests' and (not op['ok'] or op['skipped'] or op['actual_test_count']!=op['expected_test_count'])) for r in results for op in r['operations']):sys.exit(1)
