"""Eight Section6.1 exercise records: exact source, probes and design limits."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.01-why-numpy.md'
def sha(raw):return hashlib.sha256(raw).hexdigest()

def run():
    text=SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==2
    m=types.ModuleType('exact_motivation');exec(compile(blocks[0],str(SOURCE),'exec'),m.__dict__)
    checks=[];commands=[]
    def ck(exercise,label,actual,expected):checks.append(dict(exercise=exercise,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
    def close(exercise,label,actual,expected,atol):
        a=np.asarray(actual);e=np.asarray(expected,dtype=np.float64)
        ck(exercise,label,a.shape==e.shape and bool(np.isfinite(a).all()) and bool(np.all(np.abs(a-e)<=atol)),True)
        checks[-1].update(actual_values=a.tolist(),expected_values=e.tolist(),rtol=0,atol=atol)
    def reject(exercise,label,fn,kind):
        try:fn();actual='no exception';detail=''
        except Exception as error:actual=type(error).__name__;detail=traceback.format_exc()
        ck(exercise,label,actual,kind);checks[-1]['expected_exception_trace']=detail
    start=np.array([100.,80.,50.,40.]);end=np.array([105.,76.,50.,44.]);before=(start.tobytes(),end.tobytes());actual=m.price_returns(start,end)
    rational=[F(105,100)-1,F(76,80)-1,F(50,50)-1,F(44,40)-1]
    ck('6.1-E1','fourth independent fraction',rational[-1],F(1,10))
    close('6.1-E1','four aligned ratios vs rational oracle',actual,list(map(float,rational)),1e-12)
    ck('6.1-E1','new output shape/dtype',(actual.shape,str(actual.dtype)),((4,),'float64'))
    ck('6.1-E1','inputs preserved, independent result',(before==(start.tobytes(),end.tobytes()),np.shares_memory(actual,start),np.shares_memory(actual,end)),(True,False,False))
    values=[2,4];array=np.array(values,dtype=np.int64)
    ck('6.1-E2','list repetition',values*2,[2,4,2,4]);ck('6.1-E2','array element multiplication',(array*2).tolist(),[4,8]);ck('6.1-E2','original values unchanged',(values,array.tolist()),([2,4],[2,4]))
    original_start=np.array([100.,80.,50.]);original_end=np.array([105.,76.,50.]);swapped=original_end[[1,0,2]];swapped_return=m.price_returns(original_start,swapped)
    want=[F(76,100)-1,F(105,80)-1,F(50,50)-1]
    close('6.1-E3','accepted but mislabeled pairs',swapped_return,list(map(float,want)),1e-12)
    ck('6.1-E3','shape/domain validation cannot know identity',(swapped_return.shape,bool(np.isfinite(swapped_return).all()),np.array_equal(swapped_return,m.price_returns(original_start,original_end))),((3,),True,False))
    ck('6.1-E3','aligned originals preserved',original_end.tolist(),[105.,76.,50.])
    reject('6.1-E4','zero-dimensional start and end',lambda:m.price_returns(np.array(100.),np.array(105.)),'ValueError')
    reject('6.1-E4','zero-dimensional end only',lambda:m.price_returns(np.array([100.]),np.array(105.)),'ValueError')
    reject('6.1-E5','missing end is not a price',lambda:m.price_returns(np.array([100.]),np.array([np.nan])),'ValueError')
    close('6.1-E5','substituted zero means total price loss',m.price_returns(np.array([100.]),np.array([0.])),[-1.],0)
    small=m.price_returns(np.array([1.]),np.array([1.0000000000003]))[0];expected=F('1.0000000000003')-1
    close('6.1-E6','proposed near-zero scale vs rational input',small,float(expected),1e-15)
    ck('6.1-E6','old absolute threshold hides discrepancy',bool(np.isclose(small,0.,rtol=1e-12,atol=1e-12)),True)
    ck('6.1-E6','proposed policy rejects false zero',bool(np.isclose(small,0.,rtol=1e-8,atol=1e-15)),False)
    ck('6.1-E6','independent tolerance inequality',abs(F(float(small)))>F('1e-15'),True)
    reject('6.1-E7','source API still rejects float32',lambda:m.price_returns(np.array([1.],dtype=np.float32),np.array([1.1],dtype=np.float32)),'TypeError')
    original=np.array([1.00000001],dtype=np.float64);narrowed=original.astype(np.float32)
    ck('6.1-E7','float32 narrowing loses small price increment',narrowed.tolist(),[1.])
    ck('6.1-E7','widening cannot recover lost input',m.price_returns(np.array([1.]),narrowed.astype(np.float64)).tolist(),[0.])
    ck('6.1-E7','precision spacing differs by representation',(float(np.finfo(np.float32).eps),float(np.finfo(np.float64).eps)),(2.**-23,2.**-52))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='motivation-exercises-') as tmp:
        lab=Path(tmp);files={'numpy_motivation.py':blocks[0],'test_numpy_motivation.py':blocks[1]}
        for name,code in files.items():(lab/name).write_text(code);compile(code,str(lab/name),'exec')
        (lab/'four_assets.py').write_bytes((HERE/'four_assets.py').read_bytes())
        def command(label,args,*,stdout=None,count=None):
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
            if stdout is not None:ok=ok and r.stdout==stdout and r.stderr==''
            if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        command('exact original eight-method suite',['-m','unittest','discover','-v'],count=8)
        command('exact original demonstration',['numpy_motivation.py'],stdout=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0])
        command('supplemental four-asset caller',['four_assets.py'],stdout='ASSET-A: 5.00%\nASSET-B: -5.00%\nASSET-C: 0.00%\nASSET-D: 10.00%\nShape: (4,)\nDtype: float64\n')
        ck('ALL','original listings unchanged',{name:sha((lab/name).read_bytes()) for name in files},{name:sha(code.encode()) for name,code in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),original_listing_sha256=[sha(code.encode()) for code in blocks],supplemental_caller_sha256=sha((HERE/'four_assets.py').read_bytes()),exercise_records=8,command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),source_method_invocations=sum(x['actual_methods'] or 0 for x in commands),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),independent_fractions=dict(aligned_ratios=list(map(str,rational)),swapped_ratios=list(map(str,want)),small_return=str(expected)),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('checks','commands','independent_fractions','original_listing_sha256')}))
    return bool(output['command_failed'] or output['failed'])
if __name__=='__main__':raise SystemExit(run())
