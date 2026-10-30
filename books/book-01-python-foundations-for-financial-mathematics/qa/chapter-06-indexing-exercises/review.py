"""Scoped Section 6.4 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.04-indexing-and-slicing.md'
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
    source=m.fixture(); ids=('A','B','C'); observations=('obs0','obs1','obs2')
    # Independent oracle: literal transcription of the source table by label.
    rows=[dict(A=100,B=80,C=50),dict(A=105,B=76,C=51),dict(A=103,B=78,C=52)]
    selected,labels=m.select_instruments(source,ids,('B','C')); last=selected[-2:]
    oracle=[[row[key] for key in ('B','C')] for row in rows[1:]]
    ck('6.4-E1','last two B/C values',last.tolist(),oracle)
    ck('6.4-E1','shape and both axis labels',(last.shape,labels,observations[-2:]),((2,2),('B','C'),('obs1','obs2')))
    ck('6.4-E1','selection independent of source',np.shares_memory(source,last),False)
    reject('6.4-E2','zero step is invalid',lambda:source[::0],'ValueError')
    ck('6.4-E2','out-of-range slice is empty',source[99:100].shape,(0,3))
    reject('6.4-E2','out-of-range integer is distinct',lambda:source[99],'IndexError')
    mask=(source[-1]>=50)&(source[-1]<100)
    expected_ids=tuple(k for k in ids if 50<=rows[-1][k]<100)
    ck('6.4-E3','explicit instrument mask',mask.tolist(),[False,True,True])
    ck('6.4-E3','mask values and labels',(source[:,mask].tolist(),tuple(k for k,keep in zip(ids,mask) if keep)),([[r[k] for k in expected_ids] for r in rows],('B','C')))
    ck('6.4-E3','all observation labels retained',(source[:,mask].shape,observations),((3,2),('obs0','obs1','obs2')))
    reversed_rows=source[::-1]; reversed_labels=observations[::-1]
    ck('6.4-E4','reverse row/label pairs',list(zip(reversed_labels,reversed_rows.tolist())),[(observations[i],[rows[i][k] for k in ids]) for i in (2,1,0)])
    ck('6.4-E4','basic reverse shares storage',np.shares_memory(source,reversed_rows),True)
    ck('6.4-E4','scenario copy independent',np.shares_memory(source,reversed_rows.copy()),False)
    full=source>=100; values=source[full];coords=list(zip(*np.nonzero(full)))
    ck('6.4-E5','full mask selects cells in row order',values.tolist(),[100,105,103])
    ck('6.4-E5','rank loses table axes',(full.shape,values.shape,values.ndim),((3,3),(3,),1))
    ck('6.4-E5','separately retained identity coordinates',[(observations[i],ids[j]) for i,j in coords],[('obs0','A'),('obs1','A'),('obs2','A')])
    for value in (float('nan'),float('inf'),-1.):
        bad=source.copy();bad[1,1]=value;before=bad.tobytes()
        reject('6.4-E6','invalid unselected B '+str(value),lambda: m.select_instruments(bad,ids,('A',)),'ValueError')
        ck('6.4-E6','rejection leaves source unchanged '+str(value),bad.tobytes(),before)
    disposable=source.copy();advanced=disposable[:,[0,2]];advanced[0,0]=999
    ck('6.4-E7','advanced copy edit has no source effect',disposable.tolist(),source.tolist())
    ck('6.4-E7','advanced copy does not share storage',np.shares_memory(advanced,disposable),False)
    disposable[0,[0,2]]=[999,888]
    ck('6.4-E7','direct indexed assignment updates owned source',disposable[0].tolist(),[999,80,888])
    ck('6.4-E7','original fixture remains unchanged',source.tolist(),[[100,80,50],[105,76,51],[103,78,52]])
    none=(source[-1]>1000);requested=tuple(k for k,keep in zip(ids,none) if keep)
    empty,empty_ids=m.select_instruments(source,ids,requested)
    ck('6.4-E8','original selector permits explicit empty result',(empty.shape,empty_ids),((3,0),()))
    # Supplemental report policy: do not fabricate a price/return or mark a full report complete.
    report={'status':'NO_MATCH' if not empty_ids else 'MATCHED','instrument_ids':empty_ids,'observation_ids':observations,'shape':empty.shape,'valuation':None}
    ck('6.4-E8','explicit supplemental no-match report',report,dict(status='NO_MATCH',instrument_ids=(),observation_ids=('obs0','obs1','obs2'),shape=(3,0),valuation=None))
    ck('ALL','source fixture still unchanged',source.tolist(),[[100,80,50],[105,76,51],[103,78,52]])
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='indexing-exercises-') as tmp:
        lab=Path(tmp);files={'indexing_lab.py':blocks[0],'test_indexing_lab.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['indexing_lab.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
