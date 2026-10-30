"""Source-backed review of Section6.2's eight local exercise contracts."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.02-numpy-arrays.md'
def sha(raw):return hashlib.sha256(raw).hexdigest()

def run():
    text=SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==2
    m=types.ModuleType('exact_array_contracts');exec(compile(blocks[0],str(SOURCE),'exec'),m.__dict__)
    checks=[];commands=[]
    def ck(exercise,label,actual,expected):checks.append(dict(exercise=exercise,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
    def reject(exercise,label,fn,kind):
        try:fn();actual='no exception';detail=''
        except Exception as error:actual=type(error).__name__;detail=traceback.format_exc()
        ck(exercise,label,actual,kind);checks[-1]['expected_exception_trace']=detail
    dates=('2026-01-05','2026-01-06','2026-01-07');ids=('ASSET-A','ASSET-B','ASSET-C')
    rows=[[100.,80.,50.],[105.,76.,50.],[103.,78.,52.]];source=np.array(rows,dtype=np.float64);before=source.tobytes();snapshot=m.price_snapshot(source,dates,ids)
    ck('6.2-E1','all predicted metadata',(snapshot.shape,snapshot.ndim,snapshot.size,str(snapshot.dtype),snapshot.itemsize,snapshot.nbytes),((3,3),2,3*3,'float64',8,3*3*8))
    ck('6.2-E1','stored rows preserve supplied values',snapshot.tolist(),rows)
    ck('6.2-E1','source untouched',source.tobytes(),before)
    reject('6.2-E2','one-dimensional vector rejected',lambda:m.price_snapshot(np.array([1.,2.,3.]),('d0',),ids),'ValueError')
    row=m.price_snapshot(np.array([[1.,2.,3.]]),('d0',),ids)
    column=m.price_snapshot(np.array([[1.],[2.],[3.]]),dates,('ONE',))
    ck('6.2-E2','rank-two row/column accepted with matching labels',(row.shape,column.shape),((1,3),(3,1)))
    for value in (np.array([[1.,2.,3.]]),np.array([[1.],[2.],[3.]])):
        reject('6.2-E2','original two-date/three-ID labels cannot fit '+str(value.shape),lambda value=value:m.price_snapshot(value,('d0','d1'),ids),'ValueError')
    reject('6.2-E3','duplicate observation identity with valid prices',lambda:m.price_snapshot(source,('same','same','last'),ids),'ValueError')
    independent=m.price_snapshot(source,dates,ids);independent[0,0]=1.
    ck('6.2-E4','edit snapshot leaves source bytes unchanged',source.tobytes(),before)
    ck('6.2-E4','returned copy writable and independent',(independent.flags.writeable,np.shares_memory(independent,source)),(True,False))
    source[1,0]=2.;ck('6.2-E4','later source edit cannot change existing snapshot',independent[1,0],105.)
    readonly=source.T;readonly.flags.writeable=False;copied=m.price_snapshot(readonly,ids,dates)
    ck('6.2-E4','noncontiguous readonly source policy',(copied.flags.c_contiguous,copied.flags.writeable,readonly.flags.writeable,np.shares_memory(copied,readonly)),(True,True,False,False))
    wrong_ids=(ids[1],ids[0],ids[2]);wrong=m.price_snapshot(np.array(rows),dates,wrong_ids)
    ck('6.2-E5','valid but mislabeled numbers are copied unchanged',wrong.tolist(),rows)
    ck('6.2-E5','shape/label uniqueness cannot certify semantics',(wrong.shape,len(set(wrong_ids))),((3,3),3))
    # Observations of the source's declared label-only contract, not a date parser.
    unparsed=m.price_snapshot(np.array(rows),('not-a-date','2026-99-99','still-text'),ids)
    reversed_dates=m.price_snapshot(np.array(rows),dates[::-1],ids)
    ck('6.2-E6','non-calendar text labels accepted by original',unparsed.tolist(),rows)
    ck('6.2-E6','source does not sort dates or rows',reversed_dates.tolist(),rows)
    count_dates,count_ids=1000,500;estimated=count_dates*count_ids*8
    ck('6.2-E7','independent byte estimate',estimated,4000000)
    large=np.zeros((count_dates,count_ids),dtype=np.float64)
    large_copy=m.price_snapshot(large,tuple(f'd{i}' for i in range(count_dates)),tuple(f'I{i}' for i in range(count_ids)))
    ck('6.2-E7','actual source table payload agrees',(large.nbytes,large_copy.nbytes,large_copy.shape),(estimated,estimated,(1000,500)))
    ck('6.2-E7','two independent table payloads',np.shares_memory(large,large_copy),False)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='snapshot-exercises-') as tmp:
        lab=Path(tmp);files={'array_contracts.py':blocks[0],'test_array_contracts.py':blocks[1]}
        for name,code in files.items():(lab/name).write_text(code);compile(code,str(lab/name),'exec')
        (lab/'third_date.py').write_bytes((HERE/'third_date.py').read_bytes())
        def command(label,args,*,stdout=None,count=None):
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
            if stdout is not None:ok=ok and r.stdout==stdout and r.stderr==''
            if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        command('exact original eight-method suite',['-m','unittest','discover','-v'],count=8)
        command('exact original demonstration',['array_contracts.py'],stdout=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0])
        command('supplemental third-date caller',['third_date.py'],stdout='Axes: date, instrument\nShape: (3, 3)\nDimensions: 2\nElements: 9\nDtype: float64\nBytes per element: 8\nElement bytes: 72\nStored rows: [[100.0, 80.0, 50.0], [105.0, 76.0, 50.0], [103.0, 78.0, 52.0]]\n')
        ck('ALL','original listings unchanged',{name:sha((lab/name).read_bytes()) for name in files},{name:sha(code.encode()) for name,code in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),original_listing_sha256=[sha(code.encode()) for code in blocks],supplemental_caller_sha256=sha((HERE/'third_date.py').read_bytes()),exercise_records=8,command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),source_method_invocations=sum(x['actual_methods'] or 0 for x in commands),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),design_only_exercises=['6.2-E6 date boundary (source limitations probed)','6.2-E8 concurrency guarantee'],commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('checks','commands','original_listing_sha256')}))
    return bool(output['command_failed'] or output['failed'])
if __name__=='__main__':raise SystemExit(run())
