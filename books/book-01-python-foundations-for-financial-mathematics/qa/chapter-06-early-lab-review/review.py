"""Formal 6.1–6.4 workflow checks: exact source and independent expectations."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SPECS=[('6.01-why-numpy.md','numpy_motivation'),('6.02-numpy-arrays.md','array_contracts'),
       ('6.03-array-creation-and-data-types.md','creation_types'),('6.04-indexing-and-slicing.md','indexing_lab')]
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
    with tempfile.TemporaryDirectory(prefix='chapter6-early-labs-') as tmp:
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
        for i,(filename,name) in enumerate(SPECS,1):
            section=f'6.{i}';source=BOOK/'chapter-06'/filename;text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)
            assert len(blocks)==2 and len(expected)==1
            lab=root/name;lab.mkdir();files={name+'.py':blocks[0],'test_'+name+'.py':blocks[1]}
            for path,code in files.items():(lab/path).write_text(code);compile(code,str(lab/path),'exec')
            ck(section,'both exact sibling listings compile',True,True)
            command(section,'exact application stdout',[name+'.py'],lab,expected_stdout=expected[0])
            command(section,'exact eight-method discovery',['-m','unittest','discover','-v'],lab,expected_count=8)
            command(section,'fresh module import quiet',['-c','import '+name],lab,expected_stdout='')
            module=types.ModuleType('review_'+name);exec(compile(blocks[0],str(lab/(name+'.py')),'exec'),module.__dict__);modules[i]=module
            ck(section,'supplied files unchanged',{p:sha((lab/p).read_bytes()) for p in files},{p:sha(code.encode()) for p,code in files.items()})
            sources.append(dict(section=section,path=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),selected_files={p:sha(code.encode()) for p,code in files.items()},published_stdout=expected[0]))
        m=modules[1];start=np.array([100.,80.,50.]);end=np.array([105.,76.,50.]);before=(start.tobytes(),end.tobytes());out=m.price_returns(start,end)
        rational=[F(105,100)-1,F(76,80)-1,F(50,50)-1]
        close('6.1','source API vs exact rational ratio',out,list(map(float,rational)),1e-12)
        ck('6.1','new output/input preservation',(out.shape,str(out.dtype),np.shares_memory(out,start),np.shares_memory(out,end),(start.tobytes(),end.tobytes())==before),((3,),'float64',False,False,True))
        close('6.1','zero end is total price loss',m.price_returns(np.array([10.]),np.array([0.])),[-1.],0)
        settings=np.geterr().copy();reject('6.1','finite operands can overflow',lambda:m.price_returns(np.array([1e-300]),np.array([1e300])),'FloatingPointError');ck('6.1','error policy restored on failure',np.geterr(),settings)
        close('6.1','documented underflow limitation',m.price_returns(np.array([1e300]),np.array([1e-300])),[-1.],0)
        reject('6.1','incompatible shape cannot broadcast',lambda:m.price_returns(start,np.array([1.])),'ValueError')
        m=modules[2];dates=('2026-01-05','2026-01-06');ids=('A','B','C');prices=np.array([[100.,80.,50.],[105.,76.,50.]])
        snapshot=m.price_snapshot(prices,dates,ids)
        ck('6.2','independent attribute formula',(snapshot.shape,snapshot.ndim,snapshot.size,snapshot.itemsize,snapshot.nbytes),((2,3),2,2*3,8,2*3*8))
        snapshot[0,0]=0;ck('6.2','mutating returned snapshot preserves source',prices[0,0],100.)
        transposed=prices.T;transposed.flags.writeable=False;copied=m.price_snapshot(transposed,ids,dates)
        ck('6.2','transposed readonly source copied in C order',(copied.flags.c_contiguous,copied.flags.writeable,transposed.flags.writeable,np.shares_memory(copied,transposed)),(True,True,False,False))
        ck('6.2','stored copied values identical',copied.tolist(),[[100.,105.],[80.,76.],[50.,50.]])
        reject('6.2','duplicate observation identity',lambda:m.price_snapshot(prices,('same','same'),ids),'ValueError')
        m=modules[3];arrays=m.scenario_inputs();expected_rates=[F(1,100),F(1,40),F(1,25)];grid=[F(-1,100)+i*F(1,200) for i in range(5)]
        close('6.3','rate conversion vs rational wire values',arrays['rates'],list(map(float,expected_rates)),1e-15)
        close('6.3','independently derived point grid',arrays['shifts'],list(map(float,grid)),1e-15)
        ck('6.3','uncomputed is not zero outcome',(arrays['results'].shape,int(np.isnan(arrays['results']).sum()),bool(arrays['completed'].any())),((5,3),15,False))
        ck('6.3','integer sequence and neutral factors',(arrays['periods'].tolist(),str(arrays['periods'].dtype),arrays['factors'].tolist()),([1,2,3,4],'int64',[1.,1.,1.]))
        later=m.scenario_inputs();ck('6.3','all six arrays independent across calls',all(not np.shares_memory(arrays[k],later[k]) for k in arrays),True)
        reject('6.3','boolean wire value rejected before conversion',lambda:m.rate_vector((True,)),'TypeError')
        ck('6.3','integer casts truncate toward zero',np.array([1.9,-1.9]).astype(np.int64).tolist(),[1,-1])
        ck('6.3','float32 round-trip loses one integer',np.array([16777217],dtype=np.int64).astype(np.float32).astype(np.int64).tolist(),[16777216])
        m=modules[4];table=m.fixture();plain=[[100.,80.,50.],[105.,76.,51.],[103.,78.,52.]];selected,labels=m.select_instruments(table,ids,('C','A'));expected_selected=[[row[2],row[0]] for row in plain]
        ck('6.4','selection from independently indexed plain rows',(selected.tolist(),labels,selected.shape),(expected_selected,('C','A'),(3,2)))
        ck('6.4','independent selected storage',np.shares_memory(table,selected),False)
        empty,empty_ids=m.select_instruments(table,ids,());ck('6.4','empty request retains date axis',(empty.shape,empty_ids,str(empty.dtype)),((3,0),(),'float64'))
        ck('6.4','paired coordinate oracle',table[[0,2],[0,2]].tolist(),[plain[0][0],plain[2][2]])
        ck('6.4','rectangle oracle',table[np.ix_([0,2],[0,2])].tolist(),[[plain[i][j] for j in [0,2]] for i in [0,2]])
        mask=[value>=80 for value in plain[-1]];ck('6.4','mask/data/identity aligned',(table[:,np.array(mask)].tolist(),tuple(label for label,keep in zip(ids,mask) if keep)),([[100.],[105.],[103.]],('A',)))
        bad=table.copy();bad[0,1]=np.nan;reject('6.4','entire source validated even unselected column',lambda:m.select_instruments(bad,ids,('A',)),'ValueError')
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),runtime=runtime,workflow_records=4,derived_review_units=32,source_method_invocations=sum(x['actual_methods'] or 0 for x in commands),command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),sources=sources,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks','runtime')}))
    return bool(output['command_failed'] or output['failed'])
if __name__=='__main__':raise SystemExit(run())
