"""Formal 6.13–6.16 workflow checks: exact source and independent expectations."""
import copy,statistics
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SPECS=[('6.13-random-number-generation.md','random_lab'),('6.14-numerical-precision-and-numpy.md','precision_lab'),
       ('6.15-performance-python-loops-vs-vectorization.md','performance_lab'),('6.16-chapter-project-vectorized-portfolio-calculator.md','portfolio')]
def sha(raw):return hashlib.sha256(raw).hexdigest()

def run():
    commands=[];checks=[];sources=[];modules={}
    def ck(section,label,actual,expected):checks.append(dict(section=section,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
    def close(section,label,actual,expected,atol):
        a=np.asarray(actual);b=np.asarray(expected,dtype=np.float64)
        ck(section,label,a.shape==b.shape and bool(np.isfinite(a).all()) and bool(np.all(np.abs(a-b)<=atol)),True)
        checks[-1].update(actual_values=a.tolist(),expected_values=b.tolist(),rtol=0,atol=atol)
    def reject(section,label,fn,kind):
        try:fn();actual='no exception';detail=''
        except Exception as error:actual=type(error).__name__;detail=traceback.format_exc()
        ck(section,label,actual,kind);checks[-1]['expected_exception_trace']=detail
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='chapter6-final-workflows-') as tmp:
        root=Path(tmp)
        def command(section,label,args,cwd,*,expected_stdout=None,expected_count=None):
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*map(str,args)],cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual_count=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
            if expected_stdout is not None:ok=ok and r.stdout==expected_stdout and r.stderr==''
            if expected_count is not None:ok=ok and actual_count==expected_count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
            commands.append(dict(section=section,label=label,args=list(map(str,args)),cwd=str(cwd),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_stdout=expected_stdout,expected_methods=expected_count,actual_methods=actual_count,status='PASS' if ok else 'FAIL'))
            return r
        identity=command('ALL','actual runtime identity',['-c',"import json,sys,numpy;print(json.dumps(dict(executable=sys.executable,numpy=numpy.__version__,numpy_origin=numpy.__file__)))"],root)
        runtime=json.loads(identity.stdout);ck('ALL','documented NumPy version',runtime['numpy'],'2.3.5')
        for i,(filename,name) in enumerate(SPECS,13):
            section=f'6.{i}';source=BOOK/'chapter-06'/filename;text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)
            assert len(blocks)==2 and len(expected)==(0 if i==15 else 1)
            lab=root/('numpy_lab_616' if i==16 else name);lab.mkdir();files={name+'.py':blocks[0],'test_'+name+'.py':blocks[1]}
            for path,code in files.items():(lab/path).write_text(code);compile(code,str(lab/path),'exec')
            ck(section,'both exact sibling listings compile',True,True)
            if i==15:
                command(section,'exact eight-method discovery before benchmark',['-m','unittest','discover','-v'],lab,expected_count=8)
                measured=command(section,'exact bounded benchmark main',[name+'.py'],lab)
                benchmark_report=json.loads(measured.stdout)
                (HERE/'benchmark.json').write_text(json.dumps(benchmark_report,indent=2)+'\n')
            elif i==16:
                command(section,'exact project demonstration from parent',['numpy_lab_616/portfolio.py'],root,expected_stdout=expected[0])
                command(section,'exact project discovery from parent',['-m','unittest','discover','-s','numpy_lab_616','-v'],root,expected_count=8)
            else:
                command(section,'exact application stdout',[name+'.py'],lab,expected_stdout=expected[0])
                command(section,'exact eight-method discovery',['-m','unittest','discover','-v'],lab,expected_count=8)
            command(section,'fresh module import quiet',['-c','import '+name],lab,expected_stdout='')
            module=types.ModuleType('review_'+name);sys.modules[module.__name__]=module;exec(compile(blocks[0],str(lab/(name+'.py')),'exec'),module.__dict__);modules[i]=module
            ck(section,'supplied files unchanged',{p:sha((lab/p).read_bytes()) for p in files},{p:sha(code.encode()) for p,code in files.items()})
            sources.append(dict(section=section,path=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),selected_files={p:sha(code.encode()) for p,code in files.items()},published_stdout=expected[0] if expected else 'DYNAMIC_TIMING_JSON_NOT_LITERAL_FIXTURE'))
        command('ALL','documented compileall on reconstructed labs',['-m','compileall','-q',root],root,expected_stdout='')
        m=modules[13];rng=m.make_rng(42);state0=copy.deepcopy(rng.bit_generator.state);draw=m.innovations(rng,4,3);state1=copy.deepcopy(rng.bit_generator.state)
        ck('6.13','shape/dtype/finite and stream advancement',(draw.shape,str(draw.dtype),bool(np.isfinite(draw).all()),state0!=state1),((4,3),'float64',True,True))
        reference=np.random.Generator(np.random.PCG64(42)).standard_normal(size=(4,3),dtype=np.float64)
        close('6.13','same declared NumPy draw protocol, not independent RNG-quality validation',draw,reference,0)
        saved=copy.deepcopy(rng.bit_generator.state);next_draw=m.innovations(rng,3,2);replayed=m.make_rng(0);replayed.bit_generator.state=copy.deepcopy(saved)
        close('6.13','checkpoint continuation replay',m.innovations(replayed,3,2),next_draw,0)
        state=copy.deepcopy(rng.bit_generator.state)
        for shape in [(0,2),(True,2),(1001,1000)]:reject('6.13','invalid request before stream use '+repr(shape),lambda shape=shape:m.innovations(rng,*shape),'ValueError')
        ck('6.13','validation leaves state unchanged',rng.bit_generator.state,state)
        children=np.random.SeedSequence(100).spawn(2);repeated_children=np.random.SeedSequence(100).spawn(2)
        first=[m.innovations(np.random.Generator(np.random.PCG64(c)),3,2) for c in children];second=[m.innovations(np.random.Generator(np.random.PCG64(c)),3,2) for c in repeated_children]
        ck('6.13','logical child mapping recorded',[c.spawn_key for c in children],[(0,),(1,)])
        ck('6.13','serial child replay and fixture difference',(all(np.array_equal(a,b) for a,b in zip(first,second)),not np.array_equal(first[0],first[1])),(True,True))
        m=modules[14];tiny=np.full(3,1e-17)
        with localcontext() as ctx:ctx.prec=80;decimal_tiny=(Decimal(1)+Decimal('1e-17'))**3-1
        actual=m.linked_return(tiny);ck('6.14','tiny result nonzero, naive loses increments',(actual!=0,float(np.prod(1+tiny)-1)),(True,0.))
        close('6.14','Decimal precision80 tiny linking',actual,float(decimal_tiny),1e-31)
        close('6.14','rational ordinary linking',m.linked_return(np.array([.1,-.1,.1])),float(F(11,10)*F(9,10)*F(11,10)-1),1e-15)
        ck('6.14','reference-oriented criterion independently derived',(F(1)<=F(3,5)*2,F(1)<=F(3,5)*1),(True,False))
        ck('6.14','reference asymmetry observed',(m.agrees(np.array([1.]),np.array([2.]),rtol=.6,atol=0.),m.agrees(np.array([2.]),np.array([1.]),rtol=.6,atol=0.)),(True,False))
        reject('6.14','comparison cannot broadcast shape mismatch',lambda:m.agrees(np.ones(2),np.ones(1),rtol=0.,atol=0.),'ValueError')
        reject('6.14','boolean tolerance not coerced',lambda:m.agrees(np.ones(1),np.ones(1),rtol=True,atol=0.),'ValueError')
        policy=np.geterr().copy();reject('6.14','stable formulation still has overflow limit',lambda:m.linked_return(np.full(10000,.5)),'FloatingPointError');ck('6.14','error policy restored',np.geterr(),policy)
        ck('6.14','association loses unit but exact rational sum keeps it',((1e16+1.)-1e16,(1e16-1e16)+1.,sum([F(10**16),F(1),F(-10**16)])),(0.,1.,F(1)))
        m=modules[15];ck('6.15','benchmark cases/protocol',[(c['size'],c['repeat'],c['number'],c['correctness']) for c in benchmark_report['cases']],[(3,5,3,'passed'),(1000,5,3,'passed'),(100000,5,3,'passed')])
        for case in benchmark_report['cases']:
            n=case['size'];ck('6.15',str(n)+' payload arithmetic',(case['input_array_element_bytes'],case['output_array_element_bytes']),(3*n*8,n*8))
            for name,timing in case['timings'].items():
                samples=timing['seconds_per_call'];ck('6.15',str(n)+' '+name+' sample/min/median contract',(len(samples),all(np.isfinite(x) and x>0 for x in samples),timing['minimum'],timing['median']),(5,True,min(samples),statistics.median(samples)))
            ck('6.15',str(n)+' ratio recomputed',case['list_boundary_median_ratio'],case['timings']['python_lists']['median']/case['timings']['numpy_lists']['median'])
        quantities=[10.,-5.,0.];start=[100.,80.,50.];end=[105.,76.,52.];expected=[50.,20.,0.]
        ck('6.15','list boundary kernels vs integer known answer',(m.python_lists(quantities,start,end),m.numpy_lists(quantities,start,end)),(expected,expected))
        close('6.15','resident boundary kernel vs integer known answer',m.numpy_resident(*[np.array(x) for x in (quantities,start,end)]),expected,0)
        # Supplemental fault injection: prove benchmark aborts after its correctness
        # gate fails, before a timer. The exact child benchmark ran unmodified above.
        original_verify,original_repeat=m.verify,m.timeit.repeat;timer_calls=[]
        def failing_gate(*args):original_verify(*args);raise AssertionError('intentional QA correctness-gate failure')
        def forbidden_timer(*args,**kwargs):timer_calls.append(True);raise AssertionError('timer must not run')
        m.verify=failing_gate;m.timeit.repeat=forbidden_timer
        try:reject('6.15','injected correctness failure propagates',lambda:m.benchmark(3),'AssertionError')
        finally:m.verify=original_verify;m.timeit.repeat=original_repeat
        ck('6.15','no timer reached after injected failure',timer_calls,[])
        historical_source=BOOK/'chapter-06/6.15-performance-python-loops-vs-vectorization.md';historical=re.findall(r'^```json\n(.*?)^```',historical_source.read_text(),re.M|re.S)[0];historical=json.loads(historical)
        rows=re.findall(r'^\| (3|1000|100000) \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \|',historical_source.read_text(),re.M)
        for row,case in zip(rows,historical['cases']):
            med={name:statistics.median(values) for name,values in case['samples'].items()};shown=[format(med[name]*1e6,'.3f') for name in ('python_lists','numpy_lists','numpy_resident')]+[format(med['python_lists']/med['numpy_lists'],'.3f')]
            ck('6.15','historical table is consistent with its own raw samples '+row[0],shown,list(row[1:]))
        ck('6.15','historical sizes checked',len(rows),3)
        m=modules[16];assets=('ALPHA','BETA','CASH');scenarios=('up','down','flat');quantities=np.array([6.,3.,1.]);opening=np.array([100.,100.,100.]);closes=np.array([[110.,95.,100.],[80.,105.,100.],[100.,100.,100.]])
        original_inputs=[x.tobytes() for x in (quantities,opening,closes)];report=m.calculate(assets,quantities,opening,assets,scenarios,closes)
        values=[F(q)*p for q,p in zip([6,3,1],[100,100,100])];total=sum(values);weights=[v/total for v in values];end_values=[sum(F(q)*p for q,p in zip([6,3,1],row)) for row in [[110,95,100],[80,105,100],[100,100,100]]];pnl=[v-total for v in end_values]
        er=[[F(p,100)-1 for p in row] for row in [[110,95,100],[80,105,100],[100,100,100]]];contributions=[[r*w for r,w in zip(row,weights)] for row in er];returns=[sum(row) for row in contributions]
        ck('6.16','independent opening value',report.opening_value,float(total))
        for label,actual,wanted,tolerance in [('weights',report.weights,weights,1e-12),('ending_values',report.ending_values,end_values,1e-10),('pnl',report.pnl,pnl,1e-10),('portfolio_returns',report.portfolio_returns,returns,1e-12)]:close('6.16','rational '+label,actual,list(map(float,wanted)),tolerance)
        close('6.16','rational asset return matrix',report.asset_returns,[[float(x) for x in row] for row in er],1e-12);close('6.16','rational contribution matrix',report.contributions,[[float(x) for x in row] for row in contributions],1e-12)
        ck('6.16','currency versus return reconciliation',[v-total for v in end_values],[total*r for r in returns])
        outputs=[report.weights,report.asset_returns,report.contributions,report.portfolio_returns,report.ending_values,report.pnl]
        ck('6.16','inputs unchanged/result readonly/independent',(original_inputs==[x.tobytes() for x in (quantities,opening,closes)],all(not x.flags.writeable for x in outputs),all(not np.shares_memory(x,source) for x in outputs for source in (quantities,opening,closes))),(True,True,True))
        reject('6.16','ordinary result array assignment fails',lambda:report.weights.__setitem__(0,0.),'ValueError');reject('6.16','ordinary frozen field assignment fails',lambda:setattr(report,'opening_value',0.),'FrozenInstanceError')
        reject('6.16','mislabeled closing matrix rejected',lambda:m.calculate(assets,quantities,opening,('BETA','ALPHA','CASH'),scenarios,closes),'ValueError')
        loss=m.calculate(('A',),[2],[50],('A',),('loss',),[[0]]);ck('6.16','single asset total loss',(loss.portfolio_returns.tolist(),loss.ending_values.tolist(),loss.pnl.tolist()),([-1.],[0.],[-100.]))
        # Documented caller-precondition probe; do not claim arbitrary Boolean
        # wire validation from a helper whose inference erases mixed types.
        mixed=m.calculate(assets,[True,3,1],opening,assets,scenarios,closes);ck('6.16','documented mixed-Boolean inference limit retained',mixed.opening_value,500.)
        benchmarks={'tiny_return_decimal':str(decimal_tiny),'opening_value':str(total),'weights':list(map(str,weights)),'ending_values':list(map(str,end_values)),'pnl':list(map(str,pnl)),'portfolio_returns':list(map(str,returns)),'contributions':[[str(x) for x in row] for row in contributions]}
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),runtime=runtime,workflow_records=4,derived_review_units=32,project_review_units=20,source_method_invocations=sum(x['actual_methods'] or 0 for x in commands),command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),independent_benchmarks=benchmarks,sources=sources,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks','runtime','independent_benchmarks')}))
    return bool(output['command_failed'] or output['failed'])
if __name__=='__main__':raise SystemExit(run())
