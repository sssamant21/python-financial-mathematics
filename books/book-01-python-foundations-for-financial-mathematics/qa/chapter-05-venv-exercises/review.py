"""Original venv marker/runtime probes with scoped supplemental exercise cases."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,textwrap,types,venv
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.07-*.md'))
CODE=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S)[0]
H=types.ModuleType('exact_environment_helpers');exec(compile(CODE,str(SOURCE),'exec'),H.__dict__)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 checks=[];operations=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 for key in ['PYTHONPATH','PYTHONHOME','PYTHONSAFEPATH','VIRTUAL_ENV']:env.pop(key,None)
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 with tempfile.TemporaryDirectory(prefix='venv-exercises-') as tmp:
  root=Path(tmp);work=root/'work';work.mkdir();a=root/'environment-a';b=root/'environment-b';builder=venv.EnvBuilder(with_pip=False,system_site_packages=False);builder.create(a);builder.create(b)
  def command(label,python,args,*,stdout=None,expected=0,diagnostic=None,extra_env=None):
   r=subprocess.run([str(python),*map(str,args)],cwd=work,env=dict(env,**(extra_env or {})),capture_output=True,text=True,timeout=120);ok=r.returncode==expected
   if stdout is not None:ok=ok and r.stdout==stdout and r.stderr==''
   if diagnostic:ok=ok and diagnostic in r.stdout+r.stderr
   operations.append(dict(label=label,argv=[str(python),*map(str,args)],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_returncode=expected,expected_diagnostic=diagnostic,status='PASS' if ok else 'FAIL'));return r
  info={}
  for name,target in [('a',a),('b',b)]:
   python=H.interpreter(target);info[name]=json.loads(command('E1 five runtime fields '+name,python,['-I','-c',H.INFO_CODE]).stdout);data=info[name]
   ck('5.7-E1','five named fields '+name,set(data),{'executable','prefix','base_prefix','purelib','isolated'});ck('5.7-E1','explicit executable '+name,data['executable'],str(python));ck('5.7-E1','owned prefix '+name,Path(data['prefix']).resolve(),target.resolve());ck('5.7-E1','base differs '+name,data['prefix']!=data['base_prefix'],True);ck('5.7-E1','purelib beneath runtime '+name,Path(data['purelib']).resolve().is_relative_to(target.resolve()),True);ck('5.7-E1','isolated flag '+name,data['isolated'],1);ck('5.7-E1','system-site false '+name,'include-system-site-packages = false' in (target/'pyvenv.cfg').read_text().lower(),True)
  ck('5.7-E2','purelib directories differ',Path(info['a']['purelib']).resolve()!=Path(info['b']['purelib']).resolve(),True)
  recipe=root/'marker-recipe.txt';recipe.write_text(textwrap.dedent(H.MARKER_SOURCE));H.copy_marker(recipe,info['a'],'A');H.copy_marker(recipe,info['b'],'B')
  command('original A behavior',H.interpreter(a),['-I','-c',H.BEHAVIOR_CODE],stdout='A\n');command('original B behavior',H.interpreter(b),['-I','-c',H.BEHAVIOR_CODE],stdout='B\n')
  shadow=work/(H.MODULE_NAME+'.py');shadow.write_text(textwrap.dedent(H.MARKER_SOURCE).format(label='SHADOW'))
  command('E3 original origin assertion without -I rejects shadow',H.interpreter(a),['-c',H.BEHAVIOR_CODE],expected=1,diagnostic='AssertionError')
  inspect="import book1_environment_marker_57 as marker,json;print(json.dumps(dict(label=marker.ENVIRONMENT_LABEL,origin=marker.__file__)))"
  observed=json.loads(command('E3 ordinary cwd import origin',H.interpreter(a),['-c',inspect]).stdout);ck('5.7-E3','shadow label',observed['label'],'SHADOW');ck('5.7-E3','shadow origin',Path(observed['origin']).resolve(),shadow.resolve())
  isolated=json.loads(command('E3 isolated environment origin',H.interpreter(a),['-I','-c',inspect]).stdout);ck('5.7-E3','isolated label',isolated['label'],'A');ck('5.7-E3','isolated origin',Path(isolated['origin']).resolve(),Path(info['a']['purelib'])/(H.MODULE_NAME+'.py'));command('E3 isolated original behavior restored',H.interpreter(a),['-I','-c',H.BEHAVIOR_CODE],stdout='A\n')
  pip_env=root/'with-pip';command('E4 supported fresh venv with pip',sys.executable,['-m','venv',pip_env]);pip_python=H.interpreter(pip_env);pip=command('E4 explicit interpreter pip version',pip_python,['-m','pip','--version']);ck('5.7-E4','pip path is owned environment',str(pip_env) in pip.stdout,True)
  baseline=json.loads(command('E5 explicit base-runtime identity',sys.executable,['-c',H.INFO_CODE]).stdout);claimed=json.loads(command('E5 VIRTUAL_ENV alone changes no interpreter',sys.executable,['-c',H.INFO_CODE],extra_env={'VIRTUAL_ENV':str(a)}).stdout);ck('5.7-E5','all runtime fields unchanged',claimed,baseline)
  outside=root/'owned-note.txt';outside.write_text('owned synthetic file outside environment');command('E8 benign outside-venv filesystem access',H.interpreter(a),['-I','-c',"from pathlib import Path;import sys;assert Path(sys.argv[1]).read_text()=='owned synthetic file outside environment';print('read owned file outside venv')",outside],stdout='read owned file outside venv\n')
  ck('all','source recipe unchanged',sha(recipe.read_bytes()),sha(textwrap.dedent(H.MARKER_SOURCE).encode()))
 ck('all','owned temporary resources cleaned',root.exists(),False)
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),code_sha256=sha(CODE.encode()),runtime_info=info,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','runtime_info')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
