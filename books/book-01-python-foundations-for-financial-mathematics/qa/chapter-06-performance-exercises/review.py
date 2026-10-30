"""Scoped Section 6.15 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
import math,statistics
from fractions import Fraction as F
from extensions import validated_python,resident_reused_out,measure,rotated_sessions,profile_workflow
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.15-performance-python-loops-vs-vectorization.md'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def run():
    text=SOURCE.read_text(); blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S); assert len(blocks)==2
    m=types.ModuleType('exact_indexing');exec(compile(blocks[0],str(SOURCE),'exec'),m.__dict__)
    checks=[];commands=[]
    def ck(e,label,a,x): checks.append(dict(exercise=e,label=label,actual=repr(a),expected=repr(x),status='PASS' if a==x else 'FAIL'))
    def reject(e,label,fn,kind):
        try: fn(); actual='no exception'; detail=''
        except Exception as error: actual=type(error).__name__;detail=traceback.format_exc()
        ck(e,label,actual,kind);checks[-1]['expected_exception_trace']=detail
    supplement={};supplement['intermediate_10000']=m.benchmark(10000)
    ck('6.15-E1','new size with original correctness gate and boundaries',(supplement['intermediate_10000']['size'],supplement['intermediate_10000']['correctness'],set(supplement['intermediate_10000']['timings'])),(10000,'passed',{'python_lists','numpy_lists','numpy_resident'}))
    supplement['rotated_sessions']=rotated_sessions(m)
    ck('6.15-E2','each method occupies each order position',len(set(tuple(s['method_order']) for s in supplement['rotated_sessions'])),3)
    supplement['tiny_20_calls']=m.benchmark(3,repeat=5,number=20)
    ck('6.15-E3','changed tiny-case protocol explicit',(supplement['tiny_20_calls']['repeat'],supplement['tiny_20_calls']['number']),(5,20))
    public_source=BOOK/'chapter-06/6.05-vectorized-financial-calculations.md';public_blocks=re.findall(r'^```python\n(.*?)^```',public_source.read_text(),re.M|re.S);assert len(public_blocks)==2
    public=types.ModuleType('exact_validated_marks');exec(compile(public_blocks[0],str(public_source),'exec'),public.__dict__)
    arrays,lists=m.prepare(1000);source_before=tuple(x.tobytes() for x in arrays)
    expected_public=public.position_changes(*arrays);python_public=validated_python(*arrays)
    ck('6.15-E4','three-output validated array boundaries agree',all(set(python_public)==set(expected_public) and np.allclose(python_public[k],expected_public[k],rtol=1e-12,atol=1e-12,equal_nan=False) for k in expected_public),True)
    known=(np.array([10.,-5.,0.]),np.array([100.,80.,50.]),np.array([105.,76.,52.]))
    for name,operation in (('source_numpy',public.position_changes),('supplemental_python',validated_python)):
        record=operation(*known)
        ck('6.15-E4','independent known public answers '+name,{k:v.tolist() for k,v in record.items()},dict(opening=[1000.,-400.,0.],closing=[1050.,-380.,0.],pnl=[50.,20.,0.]))
        reject('6.15-E4','shape contract '+name,lambda:operation(np.array([1.]),arrays[1],arrays[2]),'ValueError')
        reject('6.15-E4','flat position invalid end '+name,lambda:operation(np.array([0.]),np.array([1.]),np.array([np.nan])),'ValueError')
        reject('6.15-E4','numerical overflow '+name,lambda:operation(np.array([1e308]),np.array([2.]),np.array([2.])),'FloatingPointError')
    supplement['validated_public_array_boundary']=dict(size=1000,scope='exact float64 arrays -> dict of three independent float64 arrays; validation and allocations included in each call',timings={'source_numpy_public':measure(lambda:public.position_changes(*arrays)),'supplemental_python_public':measure(lambda:validated_python(*arrays))})
    out=np.empty_like(arrays[0]);ck('6.15-E5','reused out writable exact dtype shape and nonalias',(out.flags.writeable,str(out.dtype),out.shape,all(not np.shares_memory(out,a) for a in arrays)),(True,'float64',(1000,),True))
    first=resident_reused_out(*arrays,out);snapshot=first.copy();second=resident_reused_out(arrays[0],arrays[1],arrays[1],out)
    ck('6.15-E5','returned reference overwritten by subsequent call',(first is out,second is out,bool((first==0).all()),bool(np.array_equal(snapshot,m.numpy_resident(*arrays)))),(True,True,True,True))
    np.testing.assert_allclose(resident_reused_out(*arrays,out),m.numpy_resident(*arrays),rtol=1e-12,atol=1e-12,equal_nan=False)
    ck('6.15-E5','reused-buffer known numerical gate',bool(np.allclose(out,m.python_lists(*lists),rtol=1e-12,atol=1e-12,equal_nan=False)),True)
    supplement['resident_reused_output']=dict(size=1000,scope='prevalidated resident inputs; reused nonaliasing output changes ownership/lifetime; output allocation excluded only for explicitly named reused case',timings={'source_allocating_resident':measure(lambda:m.numpy_resident(*arrays)),'supplemental_reused_out':measure(lambda:resident_reused_out(*arrays,out))})
    ck('6.15-E5','timings did not modify source arrays',tuple(x.tobytes() for x in arrays),source_before)
    with tempfile.TemporaryDirectory(prefix='local-profile-') as tmp:
        input_path=Path(tmp)/'positions.json';output_path=Path(tmp)/'report.json';n=1000
        q=[float(i%11-5) for i in range(n)];p0=[float(50+i%101) for i in range(n)];p1=[p0[i]+float(i%5-2) for i in range(n)]
        wire=dict(position_ids=['POS'+str(i) for i in range(n)],quantity=q,start=p0,end=p1);input_path.write_text(json.dumps(wire)+'\n')
        oracle=[float(F(a)*(F(c)-F(b))) for a,b,c in zip(q,p0,p1)]
        record,profile=profile_workflow(input_path,output_path,public.position_changes,HERE)
        ck('6.15-E7','complete file workflow independently derived PnLs',record['results']['pnl'],oracle)
        ck('6.15-E7','output file/identity/report agreement',(json.loads(output_path.read_text()),len(record['position_ids'])),(record,1000))
        ck('6.15-E7','profile fraction bounded',0<=profile['public_api_fraction']<=1,True)
        profile.update(input_rows=n,input_sha256=sha(input_path.read_bytes()),output_sha256=sha(output_path.read_bytes()),upper_bound_if_all_api_time_removed=profile['public_api_fraction'])
        supplement['local_report_workflow']=profile
        (HERE/'workflow-fixture.json').write_text(json.dumps(wire,indent=2)+'\n');(HERE/'workflow-output.json').write_text(json.dumps(record,indent=2)+'\n')
    # Validate retained measurement records; never assert a speed or ranking.
    timing_groups=[supplement['intermediate_10000']['timings'],supplement['tiny_20_calls']['timings'],supplement['validated_public_array_boundary']['timings'],supplement['resident_reused_output']['timings']]+[s['timings'] for s in supplement['rotated_sessions']]
    ck('ALL','every supplementary timing has finite nonnegative raw samples',all(len(v['seconds_per_call'])==5 and all(math.isfinite(x) and x>=0 for x in v['seconds_per_call']) for group in timing_groups for v in group.values()),True)
    ck('ALL','supplementary minima/medians derived from samples',all(v['minimum']==min(v['seconds_per_call']) and v['median']==statistics.median(v['seconds_per_call']) for group in timing_groups for v in group.values()),True)
    (HERE/'supplemental-measurements.json').write_text(json.dumps(supplement,indent=2,allow_nan=False)+'\n')
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='performance-exercises-') as tmp:
        lab=Path(tmp);files={'performance_lab.py':blocks[0],'test_performance_lab.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['performance_lab.py'],None,None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))) if count is not None else r.stderr=='')
            if count is None:
                original_benchmark=json.loads(r.stdout);(HERE/'original-benchmark.json').write_text(r.stdout)
                ok=ok and [c['size'] for c in original_benchmark['cases']]==[3,1000,100000] and all(c['correctness']=='passed' for c in original_benchmark['cases'])
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    original=json.loads((HERE/'original-benchmark.json').read_text())
    ck('ALL','original samples/minima/medians consistent',all(len(v['seconds_per_call'])==5 and all(math.isfinite(x) and x>=0 for x in v['seconds_per_call']) and v['minimum']==min(v['seconds_per_call']) and v['median']==statistics.median(v['seconds_per_call']) for c in original['cases'] for v in c['timings'].values()),True)
    ck('ALL','original ratios are like-for-like list boundary',all(c['list_boundary_median_ratio']==c['timings']['python_lists']['median']/c['timings']['numpy_lists']['median'] for c in original['cases']),True)
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),comparison_source=dict(path=str(public_source.relative_to(BOOK)),source_sha256=sha(public_source.read_bytes()),listing_sha256=sha(public_blocks[0].encode()),scope='original validated public function called; its suite not rerun'),conceptual_only_exercises=['6.15-E6','6.15-E8'],evidence_sha256={name:sha((HERE/name).read_bytes()) for name in ('extensions.py','original-benchmark.json','supplemental-measurements.json','workflow-profile.txt','workflow-fixture.json','workflow-output.json')},commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
