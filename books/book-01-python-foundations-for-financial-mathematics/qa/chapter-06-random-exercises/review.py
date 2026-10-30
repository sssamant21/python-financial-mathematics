"""Scoped Section 6.13 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from copy import deepcopy
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.13-random-number-generation.md'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def _child_replay(task,m):
    rng=m.make_rng(0);rng.bit_generator.state=deepcopy(task['state_before_draw']);return m.innovations(rng,*task['shape'])
def run():
    text=SOURCE.read_text(); blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S); assert len(blocks)==2
    m=types.ModuleType('exact_indexing');exec(compile(blocks[0],str(SOURCE),'exec'),m.__dict__)
    checks=[];commands=[]
    def ck(e,label,a,x): checks.append(dict(exercise=e,label=label,actual=repr(a),expected=repr(x),status='PASS' if a==x else 'FAIL'))
    def reject(e,label,fn,kind):
        try: fn(); actual='no exception'; detail=''
        except Exception as error: actual=type(error).__name__;detail=traceback.format_exc()
        ck(e,label,actual,kind);checks[-1]['expected_exception_trace']=detail
    seed=20261030;factory_calls=[];real_default=np.random.default_rng;real_make=m.make_rng
    def forbidden(*args,**kwargs):factory_calls.append('called');raise AssertionError('hidden replacement factory called')
    np.random.default_rng=forbidden;m.make_rng=forbidden
    try:
        for invalid in (None,42,object()):reject('6.13-E1','invalid Generator '+type(invalid).__name__,lambda:m.innovations(invalid,2,2),'TypeError')
    finally:np.random.default_rng=real_default;m.make_rng=real_make
    ck('6.13-E1','no replacement via default_rng or module make_rng',factory_calls,[])
    rng=m.make_rng(seed);saved=deepcopy(rng.bit_generator.state);saved_copy=deepcopy(saved);z=m.innovations(rng,4,2);continuations=[]
    for i in range(2):
        restored=m.make_rng(0);restored.bit_generator.state=deepcopy(saved);continuations.append(m.innovations(restored,4,2))
        ck('6.13-E2','restored continuation '+str(i),bool(np.array_equal(z,continuations[-1])),True)
    ck('6.13-E2','deep checkpoint unchanged',saved,saved_copy)
    ck('6.13-E2','successful original draw advanced state',rng.bit_generator.state!=saved,True)
    names=('batch-alpha','batch-beta','batch-gamma');children=np.random.SeedSequence(seed).spawn(3);mapping=[];batches={}
    for index,(name,child) in enumerate(zip(names,children)):
        child_rng=np.random.Generator(np.random.PCG64(child));state=deepcopy(child_rng.bit_generator.state);values=m.innovations(child_rng,3,2);batches[name]=values
        mapping.append(dict(logical_name=name,child_index=index,spawn_key=list(child.spawn_key),root_entropy=seed,state_before_draw=state,shape=[3,2],method='standard_normal',dtype='float64',draw_calls=1,output_sha256=sha(values.tobytes(order='C'))))
    replay_children=np.random.SeedSequence(seed).spawn(3);replay_rngs={name:np.random.Generator(np.random.PCG64(child)) for name,child in zip(names,replay_children)}
    for name in reversed(names):ck('6.13-E3','stable logical mapping despite execution order '+name,bool(np.array_equal(m.innovations(replay_rngs[name],3,2),batches[name])),True)
    ck('6.13-E3','name/index/spawn mapping',[(x['logical_name'],x['child_index'],x['spawn_key']) for x in mapping],[(names[i],i,[i]) for i in range(3)])
    identical_workers=[m.innovations(m.make_rng(42),3,2) for _ in range(3)]
    ck('6.13-E4','same seed same request copied across logical workers repeats',all(np.array_equal(identical_workers[0],x) for x in identical_workers[1:]),True)
    ck('6.13-E4','three controlled child batches differ',all(not np.array_equal(batches[a],batches[b]) for a,b in ((names[0],names[1]),(names[0],names[2]),(names[1],names[2]))),True)
    matrix_record=dict(dtype=z.dtype.str,shape=list(z.shape),order='C',values=z.tolist(),element_bytes_sha256=sha(z.tobytes(order='C')))
    (HERE/'innovations.json').write_text(json.dumps(matrix_record,indent=2)+'\n');loaded=json.loads((HERE/'innovations.json').read_text());kept=np.array(loaded['values'],dtype=loaded['dtype']);original_bytes=kept.tobytes();low=.01*kept;high=.02*kept
    ck('6.13-E5','JSON matrix roundtrip exact',(kept.shape,sha(kept.tobytes())),(z.shape,matrix_record['element_bytes_sha256']))
    ck('6.13-E5','shared scale comparison',bool(np.allclose(high,2*low,rtol=1e-15,atol=0,equal_nan=False)),True)
    ck('6.13-E5','snapshot unchanged by transformations',kept.tobytes(),original_bytes)
    ck('6.13-E5','scaled outputs independent',all(not np.shares_memory(x,kept) for x in (low,high)),True)
    manifest=dict(schema='book1-qa-local-replay-v1',scope='local serial reproducibility; not cross-version guarantee',environment=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),byteorder=sys.byteorder,numpy_build=np.__config__.CONFIG),source=dict(path=str(SOURCE.relative_to(BOOK)),sha256=sha(SOURCE.read_bytes()),listing_sha256=sha(blocks[0].encode())),algorithm='PCG64',generator='numpy.random.Generator',seed=seed,checkpoint_before_draw=saved,request=dict(method='standard_normal',dtype='float64',shape=[4,2],call_index=0),progress=dict(task='saved-comparison',completed_draw_calls=1,completed_scenario_rows=[0,4],interval='half-open'),artifact=dict(path='innovations.json',json_sha256=sha((HERE/'innovations.json').read_bytes()),element_bytes_sha256=matrix_record['element_bytes_sha256']),child_tasks=mapping)
    (HERE/'replay-manifest.json').write_text(json.dumps(manifest,indent=2,default=str)+'\n');wire=json.loads((HERE/'replay-manifest.json').read_text());replay=m.make_rng(0);replay.bit_generator.state=deepcopy(wire['checkpoint_before_draw']);replayed=m.innovations(replay,*wire['request']['shape'])
    ck('6.13-E6','manifest state replay matches saved bytes',sha(replayed.tobytes()),wire['artifact']['element_bytes_sha256'])
    ck('6.13-E6','saved JSON artifact hash verified',sha((HERE/wire['artifact']['path']).read_bytes()),wire['artifact']['json_sha256'])
    ck('6.13-E6','request/algorithm/task metadata',(wire['algorithm'],wire['request']['method'],wire['request']['dtype'],wire['request']['shape'],wire['progress']['task']),('PCG64','standard_normal','float64',[4,2],'saved-comparison'))
    ck('6.13-E6','child checkpoint manifests replay locally',all(sha(_child_replay(x,m).tobytes())==x['output_sha256'] for x in wire['child_tasks']),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='random-exercises-') as tmp:
        lab=Path(tmp);files={'random_lab.py':blocks[0],'test_random_lab.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['random_lab.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),supplemental_artifacts={name:sha((HERE/name).read_bytes()) for name in ('innovations.json','replay-manifest.json')},conceptual_only_exercises=['6.13-E7','6.13-E8'],commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
