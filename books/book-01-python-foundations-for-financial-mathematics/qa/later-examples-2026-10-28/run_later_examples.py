"""Run explicit reviewed plans, preserving exact source payloads and all outcomes."""
import ast,hashlib,json,os,pathlib,subprocess,sys
from markdown_it import MarkdownIt
from later_plan import PLANS
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
if out.exists():raise SystemExit('Use a new output directory')
out.mkdir(parents=True);parser=MarkdownIt();results=[]
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env['PYTHONDONTWRITEBYTECODE']='1';env['MPLBACKEND']='Agg'
def get(ch,sec,idx,companion=False):
 folder=root/f'chapter-{ch:02}'
 candidates=sorted(folder.rglob(f'{ch}.{sec:02}-*.md'))
 if companion:candidates=[p for p in candidates if 'solutions' in str(p)]
 else:candidates=[p for p in candidates if 'solutions' not in str(p)]
 f=candidates[0];ts=[t for t in parser.parse(f.read_text()) if t.type=='fence' and t.info.strip() in ('python','py','python3')];t=ts[idx]
 return t.content,{'path':str(f.relative_to(root)),'python_block_index':idx,'line':t.map[0]+1,'code_sha256':hashlib.sha256(t.content.encode()).hexdigest()}
for plan in PLANS:
 compile(plan['checks'],'<oracle>','exec');compile(plan['setup'],'<fixture>','exec')
 for idx in plan['indices']:get(plan['chapter'],plan['section'],idx,plan.get('companion',False))
 for ch,sec,idx,target in plan.get('target_files',[]):get(ch,sec,idx)
for number,plan in enumerate(PLANS,1):
 name=f'{number:03}-'+plan['name'];folder=out/name;folder.mkdir();sources=[];payload=[]
 for support in plan['support']:
  ch,sec,idx,*target=support;code,ref=get(ch,sec,idx);ref['role']='support';sources.append(ref)
  if target:
   p=folder/target[0];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
  else:payload.append(code)
 for ch,sec,idx,target in plan.get('target_files',[]):
  code,ref=get(ch,sec,idx);ref['role']='target';sources.append(ref);p=folder/target;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
 for filename,content in plan['files'].items():
  p=folder/filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
 for ch,sec,lang,index,target in plan['fixtures']:
  f=next((root/f'chapter-{ch:02}').glob(f'{ch}.{sec:02}-*.md'));ts=[t for t in parser.parse(f.read_text()) if t.type=='fence' and t.info.strip()==lang];p=folder/target;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(ts[index].content)
 for idx in plan['indices']:
  code,ref=get(plan['chapter'],plan['section'],idx,plan.get('companion',False));ref['role']='target';sources.append(ref);payload.append(code)
 (folder/'payload.py').write_text('\n\n'.join(payload))
 driver='''import contextlib,io,json,math,sys,types\nfrom decimal import Decimal,ROUND_HALF_UP,ROUND_HALF_EVEN\nmodule=types.ModuleType(MODULE_NAME);sys.modules[module.__name__]=module\nns=module.__dict__;ns.update(Decimal=Decimal,ROUND_HALF_UP=ROUND_HALF_UP,ROUND_HALF_EVEN=ROUND_HALF_EVEN,math=math,sys=sys)\nexec(SETUP,ns)\nbuffer=io.StringIO();error=None\ntry:\n with contextlib.redirect_stdout(buffer):\n  exec(compile(open('payload.py').read(),'payload.py','exec'),ns)\nexcept BaseException as exc:\n error=exc\ncaptured=buffer.getvalue();ns['captured']=captured;ns['_caught_error']=error\nif EXPECTED_EXCEPTION:\n assert error is not None and type(error).__name__==EXPECTED_EXCEPTION,(type(error).__name__,str(error))\nelse:\n if error is not None:raise error\nif EXPECTED_STDOUT is not None:assert captured==EXPECTED_STDOUT,(repr(captured),repr(EXPECTED_STDOUT))\nwith contextlib.redirect_stdout(buffer):exec(CHECKS,ns)\nprint(buffer.getvalue(),end='')\nprint('CHECKS PASSED')\n'''
 config='MODULE_NAME='+repr(plan['module_name'])+'\nSETUP='+repr(plan['setup'])+'\nEXPECTED_EXCEPTION='+repr(plan['expected_exception'])+'\nEXPECTED_STDOUT='+repr(plan['stdout'])+'\nCHECKS='+repr(plan['checks'])+'\n'
 (folder/'check.py').write_text(config+driver)
 try:
  p=subprocess.run([sys.executable,'-W','error::FutureWarning','check.py'],cwd=folder,env=env,input=plan.get('stdin',''),capture_output=True,text=True,timeout=120);stdout,stderr,rc=p.stdout,p.stderr,p.returncode
 except subprocess.TimeoutExpired as exc:stdout=str(exc.stdout or '');stderr=str(exc.stderr or '');rc=None
 (folder/'stdout.log').write_text(stdout);(folder/'stderr.log').write_text(stderr)
 result={'workflow':name,'sources':sources,'plan':plan,'command':[sys.executable,'-W','error::FutureWarning','check.py'],'returncode':rc,'status':'PASS' if rc==0 and stderr=='' and stdout.endswith('CHECKS PASSED\n') else 'FAIL','stdout':name+'/stdout.log','stderr':name+'/stderr.log'};results.append(result);print(name,result['status'],flush=True)
(out/'results.json').write_text(json.dumps({'python':sys.version,'results':results},indent=2)+'\n')
if any(r['status']!='PASS' for r in results):sys.exit(1)
