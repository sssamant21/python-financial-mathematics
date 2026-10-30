"""Section6.3 exercises: source boundaries and separate completion/rounding."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from completion import validate_completed

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.03-array-creation-and-data-types.md'
def sha(raw):return hashlib.sha256(raw).hexdigest()

def half_even_units(text):
    """Separately chosen exact rational whole-unit policy, not an astype rule."""
    value=F(text);q,r=divmod(abs(value).numerator,abs(value).denominator)
    rounded=q+int(2*r>value.denominator or (2*r==value.denominator and q%2==1))
    return -rounded if value<0 else rounded

def run():
    text=SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==2
    m=types.ModuleType('exact_creation_types');exec(compile(blocks[0],str(SOURCE),'exec'),m.__dict__)
    checks=[];commands=[]
    def ck(exercise,label,actual,expected):checks.append(dict(exercise=exercise,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
    def reject(exercise,label,fn,kind):
        try:fn();actual='no exception';detail=''
        except Exception as error:actual=type(error).__name__;detail=traceback.format_exc()
        ck(exercise,label,actual,kind);checks[-1]['expected_exception_trace']=detail
    shifts=np.linspace(-.015,.015,num=7,endpoint=True,dtype=np.float64);spacing=(F('0.015')-F('-0.015'))/6;oracle=[F('-0.015')+i*spacing for i in range(7)]
    ck('6.3-E1','rational grid spacing',spacing,F(1,200))
    ck('6.3-E1','count/endpoints/dtype',(shifts.size,float(shifts[0]),float(shifts[-1]),str(shifts.dtype)),(7,-.015,.015,'float64'))
    ck('6.3-E1','all grid points against rational oracle',bool(np.all(np.abs(shifts-np.array(list(map(float,oracle))))<=1e-15)),True)
    index=np.arange(7,dtype=np.int64);ck('6.3-E2','explicit zero-based typed positions',(index.tolist(),str(index.dtype),index.shape),(list(range(7)),'int64',(7,)))
    for length in (1,1000):
        inputs=('0.025',)*length;result=m.rate_vector(inputs)
        ck('6.3-E3','source accepts length '+str(length),(result.shape,str(result.dtype),bool(np.all(result==float(F(1,40))))),((length,),'float64',True))
        ck('6.3-E3','wire tuple unchanged '+str(length),inputs,('0.025',)*length)
    for length in (0,1001):reject('6.3-E3','outside length '+str(length),lambda length=length:m.rate_vector(('0',)*length),'ValueError')
    arrays=m.scenario_inputs()
    ck('6.3-E4','uncomputed results and neutral factors are different roles',(int(np.isnan(arrays['results']).sum()),int(arrays['completed'].sum()),arrays['factors'].tolist()),(15,0,[1.,1.,1.]))
    original_results,original_status=arrays['results'].tobytes(),arrays['completed'].tobytes()
    reject('6.3-E5','original uncomputed workspace rejected',lambda:validate_completed(arrays['results'],arrays['completed']),'ValueError')
    ck('6.3-E5','rejection does not fill or mark complete',(arrays['results'].tobytes(),arrays['completed'].tobytes()),(original_results,original_status))
    zeros=np.zeros((5,3),dtype=np.float64);done=np.ones((5,3),dtype=np.bool_);accepted=validate_completed(zeros,done)
    ck('6.3-E5','valid completed zero is accepted',(accepted.shape,bool(np.isfinite(accepted).all()),bool((accepted==0).all())),((5,3),True,True))
    ck('6.3-E5','completed output independent/writable/C order',(np.shares_memory(zeros,accepted),accepted.flags.writeable,accepted.flags.c_contiguous),(False,True,True))
    incomplete=done.copy();incomplete[0,0]=False
    reject('6.3-E5','one unfinished finite entry rejected',lambda:validate_completed(zeros,incomplete),'ValueError')
    reject('6.3-E5','complete flags cannot hide NaN',lambda:validate_completed(arrays['results'],done),'ValueError')
    reject('6.3-E5','numeric flags not silently coerced',lambda:validate_completed(zeros,np.ones((5,3),dtype=np.int64)),'TypeError')
    reject('6.3-E5','status shape mismatch',lambda:validate_completed(zeros,np.ones((5,1),dtype=np.bool_)),'ValueError')
    texts=['1.9','-1.9','1.5','2.5','-1.5','-2.5'];rounded=[half_even_units(x) for x in texts];truncated=np.array(list(map(float,texts))).astype(np.int64).tolist()
    ck('6.3-E6','chosen half-even whole-unit policy',rounded,[2,-2,2,2,-2,-2])
    ck('6.3-E6','astype is truncation, not that policy',truncated,[1,-1,1,2,-1,-2])
    reject('6.3-E6','safe casting rejects fractional narrowing',lambda:np.array([1.9,-1.9]).astype(np.int64,casting='safe'),'TypeError')
    identifier=2**53+1;native=np.array([identifier],dtype=np.int64);narrowed=native.astype(np.float64).astype(np.int64)
    ck('6.3-E7','int64 keeps supported integer identifier',int(native[0]),identifier)
    ck('6.3-E7','float64 route loses identifier identity',int(narrowed[0]),2**53)
    ck('6.3-E7','text/Python integer round trip exact',int(str(identifier)),identifier)
    reject('6.3-E8','source still rejects percent wire text',lambda:m.rate_vector(('2.5%',)),'ValueError')
    fraction=F('2.5')/100;ck('6.3-E8','independent percentage-unit conversion',fraction,F(1,40))
    ck('6.3-E8','source accepts separately supplied fraction text',m.rate_vector(('0.025',)).tolist(),[float(fraction)])
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='creation-exercises-') as tmp:
        lab=Path(tmp);files={'creation_types.py':blocks[0],'test_creation_types.py':blocks[1]}
        for name,code in files.items():(lab/name).write_text(code);compile(code,str(lab/name),'exec')
        (lab/'seven_points.py').write_bytes((HERE/'seven_points.py').read_bytes())
        def command(label,args,*,stdout=None,count=None):
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
            if stdout is not None:ok=ok and r.stdout==stdout and r.stderr==''
            if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        command('exact original eight-method suite',['-m','unittest','discover','-v'],count=8)
        command('exact original demonstration',['creation_types.py'],stdout=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0])
        command('supplemental seven-point construction',['seven_points.py'],stdout="Shift grid: ['-0.015', '-0.010', '-0.005', '0.000', '0.005', '0.010', '0.015']\nCount: 7\nObservation positions: [0, 1, 2, 3, 4, 5, 6]\nIndex dtype: int64\n")
        ck('ALL','original listings unchanged',{name:sha((lab/name).read_bytes()) for name in files},{name:sha(code.encode()) for name,code in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),original_listing_sha256=[sha(code.encode()) for code in blocks],supplemental_files={name:sha((HERE/name).read_bytes()) for name in ('seven_points.py','completion.py')},exercise_records=8,command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),source_method_invocations=sum(x['actual_methods'] or 0 for x in commands),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),independent_oracles=dict(spacing=str(spacing),grid=list(map(str,oracle)),half_even_inputs=texts,half_even_results=rounded,integer_identifier=str(identifier),percent_fraction=str(fraction)),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('checks','commands','independent_oracles','original_listing_sha256','supplemental_files')}))
    return bool(output['command_failed'] or output['failed'])
if __name__=='__main__':raise SystemExit(run())
