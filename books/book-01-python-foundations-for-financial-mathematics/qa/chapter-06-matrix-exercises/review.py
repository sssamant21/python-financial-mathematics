"""Scoped Section 6.11 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.11-matrices-and-financial-models.md'
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
    r,ids,scenarios,w,_,portfolios=m.inputs();before=(r.tobytes(),w.tobytes())
    def near(e,label,a,x):ck(e,label,bool(np.allclose(a,x,rtol=1e-12,atol=1e-14,equal_nan=False)),True)
    extended_w=np.vstack((w,np.array([[0.,0.,1.]])));extended_p=portfolios+('P3-CASH',)
    rational_r=[[F(1,10),F(-1,20),F(0)],[F(-1,5),F(1,10),F(0)],[F(0),F(0),F(1,500)]]
    rational_w=[[F(3,5),F(3,10),F(1,10)],[F(1,5),F(3,10),F(1,2)],[F(0),F(0),F(1)]]
    oracle=[[float(sum(a*b for a,b in zip(row,weights))) for weights in rational_w] for row in rational_r]
    extended=m.allocation_scenarios(r,ids,scenarios,extended_w,ids,extended_p)
    near('6.11-E1','all original scenarios with third cash portfolio',extended['returns'],oracle)
    near('6.11-E1','third portfolio results',extended['returns'][:,2],[0.,0.,.002])
    ck('6.11-E1','output axes with third portfolio',(extended['returns'].shape,extended['scenarios'],extended['portfolios']),((3,3),scenarios,('P1','P2','P3-CASH')))
    fourth=np.vstack((r,np.array([[.05,.05,0.]])));fourth_s=scenarios+('BROAD-UP',);fourth_result=m.allocation_scenarios(fourth,ids,fourth_s,extended_w,ids,extended_p)
    fourth_oracle=[sum(a*b for a,b in zip([F(1,20),F(1,20),F(0)],weights)) for weights in rational_w]
    ck('6.11-E2','rational fourth scenario hand cells',fourth_oracle,[F(9,200),F(1,40),F(0)])
    near('6.11-E2','fourth scenario every portfolio',fourth_result['returns'][-1],list(map(float,fourth_oracle)))
    ck('6.11-E2','fourth scenario output axes',(fourth_result['returns'].shape,fourth_result['scenarios'][-1]),((4,3),'BROAD-UP'))
    order=[2,0,1];relabelled=tuple(scenarios[i] for i in order);reordered=m.allocation_scenarios(r[order],ids,relabelled,w,ids,portfolios);base=m.allocation_scenarios(*m.inputs())
    ck('6.11-E3','scenario labels travel with rows',reordered['scenarios'],('CASH-YIELD','UP','DOWN'))
    near('6.11-E3','output rows follow input permutation',reordered['returns'],base['returns'][order])
    ck('6.11-E3','portfolio columns unchanged',reordered['portfolios'],portfolios)
    # Shape-valid stale labels are not detectable from numbers alone.
    stale=m.allocation_scenarios(r,ids,relabelled,w,ids,portfolios)
    ck('6.11-E3','caller can attach stale scenario labels without domain failure',stale['returns'].tolist(),base['returns'].tolist())
    reject('6.11-E4','duplicate portfolio label despite valid weights',lambda:m.allocation_scenarios(r,ids,scenarios,w,ids,('P1','P1')),'ValueError')
    cells=1000*200;payload=8*cells
    ck('6.11-E5','independent element count/bytes/MiB',(cells,payload,F(payload,2**20)),(200000,1600000,F(3125,2048)))
    large_r=np.zeros((1000,3),dtype=np.float64);large_w=np.tile(np.array([[0.,0.,1.]]),(200,1));large_s=tuple('S'+str(i) for i in range(1000));large_p=tuple('P'+str(i) for i in range(200))
    large=m.allocation_scenarios(large_r,ids,large_s,large_w,ids,large_p,max_cells=200000)
    ck('6.11-E5','actual bounded output shape/dtype/payload',(large['returns'].shape,str(large['returns'].dtype),large['returns'].nbytes,bool((large['returns']==0).all())),((1000,200),'float64',1600000,True))
    reject('6.11-E5','output-only budget boundary with small inputs',lambda:m.allocation_scenarios(large_r,ids,large_s,large_w,ids,large_p,max_cells=199999),'ValueError')
    companion=BOOK/'chapter-06/6.10-portfolio-weight-vectors.md';companion_blocks=re.findall(r'^```python\n(.*?)^```',companion.read_text(),re.M|re.S);assert len(companion_blocks)==2
    one=types.ModuleType('exact_weight_comparison');exec(compile(companion_blocks[0],str(companion),'exec'),one.__dict__)
    for portfolio in range(2):
        column=[one.contributions(w[portfolio],ids,row,ids)['portfolio_return'] for row in r]
        near('6.11-E6','Section 6.10 original function portfolio '+str(portfolio),base['returns'][:,portfolio],column)
        near('6.11-E6','independent rational portfolio '+str(portfolio),base['returns'][:,portfolio],[row[portfolio] for row in oracle])
    ck('6.11-E7','alternative-scenario outputs preserve axes',base['returns'].shape,(3,2))
    ck('6.11-E8','no scenario probabilities supplied',set(base),{'scenarios','portfolios','returns','weight_sums'})
    ck('ALL','original inputs unchanged',(r.tobytes(),w.tobytes()),before)
    ck('ALL','outputs independent of inputs',all(not np.shares_memory(base['returns'],a) for a in (r,w)),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='matrix-exercises-') as tmp:
        lab=Path(tmp);files={'matrix_models.py':blocks[0],'test_matrix_models.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['matrix_models.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),comparison_source=dict(path=str(companion.relative_to(BOOK)),source_sha256=sha(companion.read_bytes()),executed_listing_sha256=sha(companion_blocks[0].encode()),scope='unchanged first listing, function calls only; no companion suite rerun'),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
