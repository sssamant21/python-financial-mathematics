"""Scoped Section 6.9 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.09-return-vectors.md'
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
    periods=np.array([0,1,3,4],dtype=np.int64);prices=np.array([100.,110.,99.,108.9]);before=(periods.tobytes(),prices.tobytes())
    added=m.return_path(np.array([0,1,3,4,5],dtype=np.int64),np.array([100.,110.,99.,108.9,100.]))
    ck('6.9-E1','added final interval',(added['start_periods'].tolist(),added['end_periods'].tolist()),([0,1,3,4],[1,3,4,5]))
    ck('6.9-E1','final linked return zero within explicit tolerance',abs(float(added['growth'][-1])-1.)<=1e-14,True)
    last_simple=F(100)/F('108.9')-1
    ck('6.9-E1','last interval against decimal-rational ratio',abs(float(added['simple'][-1])-float(last_simple))<=1e-14,True)
    up_down=m.return_path(np.array([0,1,2],dtype=np.int64),np.array([100.,120.,96.]))
    ck('6.9-E2','20 percent up/down gross',bool(np.allclose(up_down['gross'],[float(F(6,5)),float(F(4,5))],rtol=0,atol=1e-15)),True)
    ck('6.9-E2','linked loss vs summed zero',(abs(float(up_down['growth'][-1]-1)-float(F(-1,25)))<=1e-15,abs(float(up_down['simple'].sum()))<=1e-15),(True,True))
    original=m.return_path(periods,prices)
    ck('6.9-E3','every output has N minus one elements',{k:v.shape for k,v in original.items()},{k:(3,) for k in ('start_periods','end_periods','gross','simple','growth')})
    ck('6.9-E3','actual intervals only',list(zip(original['start_periods'].tolist(),original['end_periods'].tolist())),[(0,1),(1,3),(3,4)])
    ck('6.9-E3','first output is first actual return not artificial zero',abs(float(original['simple'][0])-float(F(1,10)))<=1e-15,True)
    one=m.return_path(np.array([4,9],dtype=np.int64),np.array([10.,12.]))
    ck('6.9-E3','two observations give exactly one labelled interval',(one['simple'].shape,one['start_periods'].tolist(),one['end_periods'].tolist()),((1,),[4],[9]))
    reject('6.9-E4','original positive-path API rejects terminal zero',lambda:m.return_path(np.array([0,1],dtype=np.int64),np.array([100.,0.])),'ValueError')
    reject('6.9-E4','source rejects attempted resurrection after zero',lambda:m.return_path(np.array([0,1,2],dtype=np.int64),np.array([100.,0.,10.])),'ValueError')
    ck('6.9-E4','separate rational terminal-event design',(F(0)/F(100),F(0)/F(100)-1),(F(0),F(-1)))
    missing=np.array([100.,np.nan,99.,108.9])
    reject('6.9-E5','strict source rejects middle NaN',lambda:m.return_path(periods,missing),'ValueError')
    keep=np.array([True,False,True,True]);bridged=m.return_path(periods[keep],missing[keep])
    ck('6.9-E5','explicit paired filtering records longer interval',list(zip(bridged['start_periods'].tolist(),bridged['end_periods'].tolist())),[(0,3),(3,4)])
    ck('6.9-E5','bridge ratio derives endpoints only',abs(float(bridged['gross'][0])-float(F(99,100)))<=1e-15,True)
    ck('6.9-E6','separate cash-distribution convention',((F(95)+F(10))/F(100)-1,(F(95)/F(100)-1)),(F(1,20),F(-1,20)))
    ck('6.9-E6','source price-only path excludes cash',abs(float(m.return_path(np.array([0,1],dtype=np.int64),np.array([100.,95.]))['simple'][0])-float(F(-1,20)))<=1e-15,True)
    integer_prices=[100+(17*i)%31 for i in range(257)];long_prices=np.array(integer_prices,dtype=np.float64);long_periods=np.arange(257,dtype=np.int64)
    long_result=m.return_path(long_periods,long_prices);exact_growth=[F(p,integer_prices[0]) for p in integer_prices[1:]]
    oracle=np.array(list(map(float,exact_growth)));endpoint=long_prices[1:]/long_prices[0]
    absolute_error=float(np.max(np.abs(long_result['growth']-oracle)));rtol=1e-12;atol=1e-14
    ck('6.9-E7','deterministic longer output counts',(long_result['growth'].shape,len(exact_growth)),((256,),256))
    ck('6.9-E7','linked path vs independently telescoped rational endpoints',bool(np.allclose(long_result['growth'],oracle,rtol=rtol,atol=atol,equal_nan=False)),True)
    ck('6.9-E7','linked path vs float endpoint division',bool(np.allclose(long_result['growth'],endpoint,rtol=rtol,atol=atol,equal_nan=False)),True)
    ck('6.9-E7','all interval endpoints preserved',(long_result['start_periods'].tolist(),long_result['end_periods'].tolist()),(list(range(256)),list(range(1,257))))
    irregular=m.return_path(np.array([0,10,30,40],dtype=np.int64),prices)
    ck('6.9-E8','timing changed but return arithmetic not annualized',(irregular['simple'].tolist(),irregular['end_periods'].tolist()),(original['simple'].tolist(),[10,30,40]))
    ck('ALL','original inputs unchanged',(periods.tobytes(),prices.tobytes()),before)
    ck('ALL','outputs do not share caller storage',all(not np.shares_memory(out,a) for out in original.values() for a in (periods,prices)),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='return-exercises-') as tmp:
        lab=Path(tmp);files={'return_vectors.py':blocks[0],'test_return_vectors.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['return_vectors.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),independent_oracles=dict(last_interval_simple=str(last_simple),long_price_formula='100+(17*i)%31 for i in range(257)',long_endpoint_fraction=str(exact_growth[-1]),long_max_absolute_error=absolute_error,long_comparison_rtol=rtol,long_comparison_atol=atol),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
