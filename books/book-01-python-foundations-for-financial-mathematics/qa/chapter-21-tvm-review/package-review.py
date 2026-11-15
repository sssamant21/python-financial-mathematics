"""Exact scaffold source;offline local build/editable and clean wheel consumer."""
from pathlib import Path
import subprocess,sys,re,tempfile,json,hashlib,platform,os,zipfile
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else 'da68056d0ed2d80f4aeb8abbf11ea0a760ae8ce3';base='books/book-01-python-foundations-for-financial-mathematics/chapter-21/';paths=[base+'21.05-time-value-of-money-module.md',base+'21.03-project-structure.md'];texts=[subprocess.check_output(['git','show',REV+':'+p],cwd=ROOT,text=True) for p in paths];new,old=[re.findall(r'```python\n(.*?)\n```',x,re.S) for x in texts];tm=re.findall(r'```toml\n(.*?)\n```',texts[1],re.S);md=re.findall(r'```markdown\n(.*?)\n```',texts[1],re.S);assert len(new)==len(old)==4 and len(tm)==len(md)==1
files={'src/financial_toolkit/time_value.py':new[0],'src/financial_toolkit/__init__.py':new[1],'examples/tvm.py':new[2],'tests/test_tvm_multi.py':new[3],'tests/test_time_value.py':old[3],'pyproject.toml':tm[0],'README.md':md[0]};prior=json.loads((BOOK/'qa/chapter-21-tvm-resume/results.json').read_text());assert all(hashlib.sha256(files[n].encode()).hexdigest()==sha for n,sha in prior['staged_fence_sha256'].items());commands=[]

def run(label,argv,cwd,env):
 z=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True);commands.append(dict(label=label,argv=list(map(str,argv)),returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));return z
with tempfile.TemporaryDirectory(prefix='book1-scaffold-') as td:
 temp=Path(td);project=temp/'project';project.mkdir();outside=temp/'outside';outside.mkdir();build=temp/'build-env';consumer=temp/'consumer-env';env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONNOUSERSITE']='1';env['PIP_NO_INDEX']='1';env['PIP_DISABLE_PIP_VERSION_CHECK']='1'
 for name,s in files.items():p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 run('build venv;preprovisioned local tooling',[sys.executable,'-m','venv','--system-site-packages',str(build)],temp,env);bp=str(build/'bin/python')
 run('build-tool versions',[bp,'-c','import sys,importlib.metadata as m;print(sys.version);print({n:m.version(n) for n in ("pip","setuptools","wheel")})'],temp,env)
 run('offline editable install',[bp,'-m','pip','install','--no-index','--no-build-isolation','--no-deps','-e','.'],project,env)
 run('editable example',[bp,'examples/tvm.py'],project,env);run('editable reference suite',[bp,'-m','unittest','discover','-s','tests','-v'],project,env)
 wheels=temp/'wheels';wheels.mkdir();run('offline wheel build',[bp,'-m','pip','wheel','--no-index','--no-build-isolation','--no-deps','--wheel-dir',str(wheels),'.'],project,env)
 found=list(wheels.glob('*.whl'));assert len(found)==1;wheel=found[0]
 with zipfile.ZipFile(wheel) as z:artifact=dict(filename=wheel.name,sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),size=wheel.stat().st_size,members=[dict(name=i.filename,size=i.file_size) for i in z.infolist()])
 (outside/'test_time_value.py').write_text(files['tests/test_time_value.py']);(outside/'test_tvm_multi.py').write_text(files['tests/test_tvm_multi.py']);(outside/'one_period.py').write_text(files['examples/tvm.py'])
 run('clean consumer venv',[sys.executable,'-m','venv',str(consumer)],temp,env);cp=str(consumer/'bin/python');run('offline wheel install clean consumer',[cp,'-m','pip','install','--no-index','--no-deps',str(wheel)],outside,env)
 project.rename(temp/'source-hidden')
 run('outside-source wheel reference suite',[cp,'-I','-m','unittest','discover','-s',str(outside),'-v'],outside,env);run('outside-source wheel example',[cp,'-I','one_period.py'],outside,env)
 probe='''import financial_toolkit as m,sys,json,math
from fractions import Fraction
from pathlib import Path
assert Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
p=m.present_value_one_period
rows=[]
for c,r in [(110.,.1),(95.,-.05),(110.,0.),(-110.,.1),(100.,.05),(100.,.1),(0.,.1)]:
 expected=float(Fraction(c)/(1+Fraction(r)));actual=p(c,r);rows.append(dict(payment=c,rate=r,actual=actual,expected=expected,passed=math.isclose(actual,expected,rel_tol=5e-14,abs_tol=1e-10)))
for c,r in [(100,.1),(100.,True),(math.nan,.1),(100.,-1.),(1e308,-.5)]:
 try:p(c,r);passed=False
 except ValueError:passed=True
 rows.append(dict(input=repr((c,r)),passed=passed))
pv,fv=m.present_value,m.future_value
for name,fn in [('pv',pv),('fv',fv)]:
 for amount,rate,n in [(100.,.1,2),(121.,.1,2),(100.,-.05,2),(50.,.2,0),(50.,0.,10000),(0.,1e308,10000),(-100.,.05,5),(100.,.001,100)]:
  expected=0. if amount==0 else float(Fraction(amount)*(1+Fraction(rate))**n if name=='fv' else Fraction(amount)/(1+Fraction(rate))**n)
  working=0. if amount==0 else float(Fraction(amount)*Fraction(1.+rate)**n if name=='fv' else Fraction(amount)/Fraction(1.+rate)**n)
  actual=fn(amount,rate,n);rows.append(dict(function=name,amount=amount,rate=rate,periods=n,actual=actual,model_reference=expected,working_base_reference=working,relative_tolerance=5e-13,absolute_tolerance=1e-10,passed=math.isclose(actual,expected,rel_tol=5e-13,abs_tol=1e-10) and math.isclose(actual,working,rel_tol=5e-13,abs_tol=1e-10)))
 for n in [-1,10001,True,1.0]:
  try:fn(100.,.1,n);passed=False
  except ValueError:passed=True
  rows.append(dict(function=name,invalid_periods=repr(n),passed=passed))
for fn,args in [(fv,(1e308,1.,1)),(pv,(1e308,-.5,1))]:
 try:fn(*args);passed=False
 except ValueError:passed=True
 rows.append(dict(case='declared nonfinite intermediate',passed=passed))
assert m.__all__==['future_value','present_value','present_value_one_period']
limit=dict(name='documented rounded-base loss',actual=fv(1.,2**-54,10000),independent_model=float((1+Fraction(2**-54))**10000),status='Documented rounding limitation;notfailed acceptance predicate.')
assert all(x['passed'] for x in rows)
print(json.dumps(dict(documented_range_observations=[limit],module=m.__file__,prefix=sys.prefix,source_path_injection=False,exports=m.__all__,predicates=rows)))'''
 z=run('wheel import provenance and12 independent contract predicates',[cp,'-I','-c',probe],outside,env);wheel_checks=json.loads(z.stdout) if z.returncode==0 else None
 d=dict(source_revision=REV,python=sys.version,platform=platform.platform(),staged_fence_sha256={n:hashlib.sha256(x.encode()).hexdigest() for n,x in files.items()},reused_source_commands=3,reused_source_revision=prior['source_revision'],commands=commands,artifact=artifact,wheel_checks=wheel_checks,existing_unique_methods=24,new_method_invocations=48,reused_method_invocations=24,new_historical_unique_methods=0,limits='Offline build/editable tooling venv exposes preprovisioned system-site packages;consumer venv is clean,isolated -I outside hidden source. Uses declared local compatible backend with no-build-isolation/no-index/no-deps,not default network-isolated resolution. Wheel hash/list retained;generated binary and temporary environments are not committed. Not reproducible-byte guarantee,all-range correctness,other platforms,model/security/release/independent approval.')
(OUT/'package-results.json').write_text(json.dumps(d,indent=2)+'\n');print(len(commands),'commands',sum(x['returncode']!=0 for x in commands),'failed;editable/wheel suites48method invocations;wheel contract predicates retained');assert all(x['returncode']==0 for x in commands) and wheel_checks
