"""Run Chapter 3 selected snippets, standalone labs, doctests and reference suites.

Usage: python run_reference_checks.py CHAPTER03_DIR NEW_OUTPUT_DIR
"""
import ast,hashlib,json,os,pathlib,platform,re,subprocess,sys
source=pathlib.Path(sys.argv[1]).resolve();output=pathlib.Path(sys.argv[2]).resolve()
if output.exists():raise SystemExit('Choose a new output directory to preserve prior evidence.')
output.mkdir(parents=True)
def blocks(f):return [m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())]
def section(n):return next(source.glob(f'3.{n:02}-*.md'))
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env['PYTHONDONTWRITEBYTECODE']='1'
labconfig={4:(14,'return_values_lab'),5:(13,'default_keyword_arguments_lab'),6:(18,'variable_scope_lab'),7:(9,'type_hints_lab'),8:(3,'docstrings_lab'),9:(0,'valuation_lab'),10:(0,'rate_discounting_lab'),11:(3,'composition_lab'),12:(1,'reproducibility_lab')}
results=[]
def write(folder,name,code):ast.parse(code);(folder/(name+'.py')).write_text(code)
def execute(folder,label,args):
 proc=subprocess.run([sys.executable,'-W','error::FutureWarning',*args],cwd=folder,env=env,text=True,capture_output=True,timeout=45)
 log=proc.stdout+proc.stderr;(folder/(label+'.log')).write_text(log)
 result={'operation':label,'command':[sys.executable,'-W','error::FutureWarning',*args],'returncode':proc.returncode,'log':folder.name+'/'+label+'.log'}
 if label=='unittest':
  m=re.search(r'Ran (\d+) tests? in',log);result.update(test_count=int(m.group(1)) if m else None,ok=bool(re.search(r'^OK\s*$',log,re.M)),skipped=bool(re.search('skipped=',log)))
 if label=='doctest':
  m=re.search(r'(\d+) passed and (\d+) failed',log);result.update(examples_passed=int(m.group(1)) if m else None,examples_failed=int(m.group(2)) if m else None)
 return result
for f in sorted(source.rglob('3.*.md')):
 n=int(f.name.split('.')[1][:2]);b=blocks(f)
 if not b:continue
 folder=output/f.stem;folder.mkdir();ops=[];selected=[];support=[]
 if n<=3:
  selected={1:[0,3],2:[22,23],3:[0,1]}[n];write(folder,'selected_snippets','\n\n'.join(b[i] for i in selected));ops.append(execute(folder,'selected-snippets',['selected_snippets.py']))
 elif n in labconfig:
  i,module=labconfig[n];selected=[i];write(folder,module,b[i]);ops.append(execute(folder,'standalone-lab',[module+'.py']))
  if n>=8:ops.append(execute(folder,'doctest',['-m','doctest','-v',module+'.py']))
 elif n==13:
  selected=[0];write(folder,'test_present_value',b[0]);dependency=section(12);write(folder,'reproducibility_lab',blocks(dependency)[1]);support=[dependency]
  ops.append(execute(folder,'unittest',['-m','unittest','-v','test_present_value']))
 elif n==14:
  selected=[0,1,2];write(folder,'financial_functions',b[0]);write(folder,'test_function_library',b[1]);write(folder,'demo_function_library',b[2]);ops.append(execute(folder,'unittest',['-m','unittest','-v','test_function_library']));ops.append(execute(folder,'project-demonstration',['demo_function_library.py']))
 elif n==15 and f.parent.name=='solutions':
  selected=[0];write(folder,'chapter03_solutions',b[0]);dependency=section(14);write(folder,'financial_functions',blocks(dependency)[0]);support=[dependency]
  ops.append(execute(folder,'unittest',['-m','unittest','-v','chapter03_solutions']))
 else:continue
 ops.append(execute(folder,'compilation',['-m','compileall','-q','.']))
 results.append({'file':str(f.relative_to(source)),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'selected_python_block_indices':selected,'supporting_sources':{str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in support},'operations':ops})
 print(f.name,[(op['operation'],op['returncode'],op.get('test_count',op.get('examples_passed'))) for op in ops],flush=True)
evidence={'environment':{'python':platform.python_version(),'platform':platform.platform(),'dependencies':'Python standard library'},'results':results}
(output/'results.json').write_text(json.dumps(evidence,indent=2)+'\n')
(output/'all-checks.log').write_text(''.join('\n===== '+r['file']+' / '+op['operation']+' =====\n'+(output/op['log']).read_text() for r in results for op in r['operations']))
if len(results)!=15 or any(op['returncode'] or (op['operation']=='unittest' and (not op['ok'] or op['skipped'] or not op['test_count'])) or (op['operation']=='doctest' and (op['examples_failed']!=0 or not op['examples_passed'])) for r in results for op in r['operations']):sys.exit(1)
