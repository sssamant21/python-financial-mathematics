from pathlib import Path
import sys,subprocess,tempfile,re,json,hashlib,platform,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];pin='70da93bc07c55a0c0b5eb1a48b7f80bb0614289c';base='books/book-01-python-foundations-for-financial-mathematics/chapter-21/';paths=[base+'21.06-cash-flow-module.md',base+'21.05-time-value-of-money-module.md',base+'21.03-project-structure.md'];texts=[subprocess.check_output(['git','show',pin+':'+p],cwd=ROOT,text=True) for p in paths];new,tvm,old=[re.findall(r'```python\n(.*?)\n```',s,re.S) for s in texts];assert len(new)==len(tvm)==len(old)==4
files={'src/financial_toolkit/cashflows.py':new[0],'src/financial_toolkit/time_value.py':tvm[0],'src/financial_toolkit/__init__.py':new[1],'examples/cashflows.py':new[2],'tests/test_cashflows.py':new[3],'tests/test_tvm_multi.py':tvm[3],'tests/test_time_value.py':old[3]};commands=[]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for n,s in files.items():p=t/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 env=dict(os.environ);env['PYTHONPATH']=str(t/'src')
 for args in [['examples/cashflows.py'],['-m','unittest','discover','-s','tests','-v'],['-m','compileall','-q','src','tests','examples']]:
  argv=[sys.executable]+args;z=subprocess.run(argv,cwd=t,env=env,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr,source_path_injection=True))
 d=dict(source_revision=pin,source_paths=paths,source_sha256=[hashlib.sha256(s.encode()).hexdigest() for s in texts],staged_fence_sha256={n:hashlib.sha256(s.encode()).hexdigest() for n,s in files.items()},python=sys.version,platform=platform.platform(),commands=commands,existing_unique_methods=dict(cashflows=12,tvm=12,retained_scaffold=12),method_invocations=36,new_historical_unique_methods=0,limits='Partialsourceintegration only;updatedcashflowmodule/reexports/tests stagedwith21.5TVM andretained21.3tests. ExplicitPYTHONPATH;no editable/wheel/installacceptance forupdatedcashflows. Full21.6range/oracles/40answers/12lab reviewpending.')
(OUT/'results.json').write_text(json.dumps(d,indent=2)+'\n');assert all(x['returncode']==0 for x in commands);assert 'Ran 36 tests' in commands[1]['stderr'];print('3sourcecommands/36existingmethods pass;formal21.6andupdatedartifactpending')
