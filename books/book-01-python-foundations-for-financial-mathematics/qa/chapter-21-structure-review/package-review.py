"""Exact scaffold source;offline local build/editable and clean wheel consumer."""
from pathlib import Path
import subprocess,sys,re,tempfile,json,hashlib,platform,os,zipfile
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else '7f6de3a0495e0e3cb65fd3a0f3f5fbf67e902fdd';rel=str((BOOK/'chapter-21/21.03-project-structure.md').relative_to(ROOT));raw=subprocess.check_output(['git','show',REV+':'+rel],cwd=ROOT,text=True)
py=re.findall(r'```python\n(.*?)\n```',raw,re.S);tm=re.findall(r'```toml\n(.*?)\n```',raw,re.S);md=re.findall(r'```markdown\n(.*?)\n```',raw,re.S);assert (len(py),len(tm),len(md))==(4,1,1)
files=dict(zip(['src/financial_toolkit/__init__.py','src/financial_toolkit/time_value.py','examples/one_period.py','tests/test_time_value.py'],py));files['pyproject.toml']=tm[0];files['README.md']=md[0];prior=json.loads((BOOK/'qa/chapter-21-structure-resume/results.json').read_text());assert prior['fence_sha256']=={n:hashlib.sha256(s.encode()).hexdigest() for n,s in files.items()};commands=[]
def run(label,argv,cwd,env):
 z=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True);commands.append(dict(label=label,argv=list(map(str,argv)),returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));return z
with tempfile.TemporaryDirectory(prefix='book1-scaffold-') as td:
 temp=Path(td);project=temp/'project';project.mkdir();outside=temp/'outside';outside.mkdir();build=temp/'build-env';consumer=temp/'consumer-env';env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONNOUSERSITE']='1';env['PIP_NO_INDEX']='1';env['PIP_DISABLE_PIP_VERSION_CHECK']='1'
 for name,s in files.items():p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 run('build venv;preprovisioned local tooling',[sys.executable,'-m','venv','--system-site-packages',str(build)],temp,env);bp=str(build/'bin/python')
 run('build-tool versions',[bp,'-c','import sys,importlib.metadata as m;print(sys.version);print({n:m.version(n) for n in ("pip","setuptools","wheel")})'],temp,env)
 run('offline editable install',[bp,'-m','pip','install','--no-index','--no-build-isolation','--no-deps','-e','.'],project,env)
 run('editable example',[bp,'examples/one_period.py'],project,env);run('editable reference suite',[bp,'-m','unittest','discover','-s','tests','-v'],project,env)
 wheels=temp/'wheels';wheels.mkdir();run('offline wheel build',[bp,'-m','pip','wheel','--no-index','--no-build-isolation','--no-deps','--wheel-dir',str(wheels),'.'],project,env)
 found=list(wheels.glob('*.whl'));assert len(found)==1;wheel=found[0]
 with zipfile.ZipFile(wheel) as z:artifact=dict(filename=wheel.name,sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),size=wheel.stat().st_size,members=[dict(name=i.filename,size=i.file_size) for i in z.infolist()])
 (outside/'test_time_value.py').write_text(files['tests/test_time_value.py']);(outside/'one_period.py').write_text(files['examples/one_period.py'])
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
assert all(x['passed'] for x in rows)
print(json.dumps(dict(module=m.__file__,prefix=sys.prefix,source_path_injection=False,exports=m.__all__,predicates=rows)))'''
 z=run('wheel import provenance and12 independent contract predicates',[cp,'-I','-c',probe],outside,env);wheel_checks=json.loads(z.stdout) if z.returncode==0 else None
 d=dict(source_revision=REV,python=sys.version,platform=platform.platform(),fence_sha256=prior['fence_sha256'],reused_source_commands=3,reused_source_revision=prior['source_revision'],commands=commands,artifact=artifact,wheel_checks=wheel_checks,existing_unique_methods=12,new_method_invocations=24,reused_method_invocations=12,new_historical_unique_methods=0,limits='Offline build/editable tooling venv exposes preprovisioned system-site packages;consumer venv is clean,isolated -I outside hidden source. Uses declared local compatible backend with no-build-isolation/no-index/no-deps,not default network-isolated resolution. Wheel hash/list retained;generated binary and temporary environments are not committed. Not reproducible-byte guarantee,all-range correctness,other platforms,model/security/release/independent approval.')
(OUT/'package-results.json').write_text(json.dumps(d,indent=2)+'\n');print(len(commands),'commands',sum(x['returncode']!=0 for x in commands),'failed;editable/wheel suites24method invocations;12wheel predicates');assert all(x['returncode']==0 for x in commands) and wheel_checks
