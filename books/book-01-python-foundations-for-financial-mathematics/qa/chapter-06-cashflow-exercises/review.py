"""Scoped Section 6.8 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.08-cash-flow-vectors.md'
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
    periods=np.array([0,1,3,4],dtype=np.int64);amounts=np.array([-1000.,200.,-50.,1000.]);before=(periods.tobytes(),amounts.tobytes())
    inserted_periods=np.array([0,1,2,3,4],dtype=np.int64);inserted_amounts=np.array([-1000.,200.,-25.,-50.,1000.])
    expected=[];total=F(0)
    for value in [-1000,200,-25,-50,1000]: total+=F(value);expected.append(float(total))
    added=m.cashflow_schedule(inserted_periods,inserted_amounts)
    ck('6.8-E1','ordered inserted period and amounts',(added['periods'].tolist(),added['amounts'].tolist()),([0,1,2,3,4],[-1000,200,-25,-50,1000]))
    ck('6.8-E1','independent cumulative oracle',(added['cumulative'].tolist(),added['nominal_net']),(expected,125.))
    original=m.cashflow_schedule(periods,amounts);opposite=m.cashflow_schedule(periods,-amounts)
    ck('6.8-E2','reversed perspective amounts',opposite['amounts'].tolist(),[1000,-200,50,-1000])
    ck('6.8-E2','reversed perspective cumulative/net',(opposite['cumulative'].tolist(),opposite['nominal_net']),([1000,800,850,-150],-150.))
    ck('6.8-E2','timing does not change under perspective reversal',opposite['periods'].tolist(),periods.tolist())
    dense=m.cashflow_schedule(inserted_periods,np.array([-1000.,200.,0.,-50.,1000.]))
    ck('6.8-E3','known zero gap dense amounts/cumulative',(dense['amounts'].tolist(),dense['cumulative'].tolist()),([-1000,200,0,-50,1000],[-1000,-800,-800,-850,150]))
    ck('6.8-E3','sparse vs dense nominal equality',dense['nominal_net'],original['nominal_net'])
    maximum=m.cashflow_schedule(np.array([1000000],dtype=np.int64),np.array([-1e12]))
    ck('6.8-E4','inclusive upper-period and negative-amount bounds',(maximum['periods'].tolist(),maximum['cumulative'].tolist(),maximum['nominal_net']),([1000000],[-1000000000000],-1000000000000))
    reject('6.8-E4','period immediately beyond bound',lambda:m.cashflow_schedule(np.array([1000001],dtype=np.int64),np.array([0.])),'ValueError')
    reject('6.8-E4','amount below negative magnitude bound',lambda:m.cashflow_schedule(np.array([0],dtype=np.int64),np.array([-1e12-1.])),'ValueError')
    # Supplemental controlled grouping, preserving gross raw event records.
    raw=(('receipt',2,F(200)),('payment',2,F(-50)));gross_receipts=sum(v for _,_,v in raw if v>0);gross_payments=-sum(v for _,_,v in raw if v<0);net=sum(v for _,_,v in raw)
    ck('6.8-E5','retained gross/net record',(tuple(x[0] for x in raw),gross_receipts,gross_payments,net),(('receipt','payment'),F(200),F(50),F(150)))
    reject('6.8-E5','original source still rejects duplicate periods',lambda:m.cashflow_schedule(np.array([2,2],dtype=np.int64),np.array([200.,-50.])),'ValueError')
    grouped=m.cashflow_schedule(np.array([2],dtype=np.int64),np.array([float(net)]))
    ck('6.8-E5','explicit upstream net passed as one event',(grouped['periods'].tolist(),grouped['nominal_net']),([2],150.))
    ck('6.8-E5','offsetting gross events need evidence even at net zero',(F(50)+F(-50),abs(F(50))+abs(F(-50))),(F(0),F(100)))
    unsorted_p=np.array([3,0,4,1],dtype=np.int64);unsorted_a=np.array([-50.,-1000.,1000.,200.]);order=np.argsort(unsorted_p,kind='stable')
    reject('6.8-E6','original rejects unsorted schedule',lambda:m.cashflow_schedule(unsorted_p,unsorted_a),'ValueError')
    wrong=m.cashflow_schedule(unsorted_p[order],unsorted_a);right=m.cashflow_schedule(unsorted_p[order],unsorted_a[order])
    ck('6.8-E6','paired sort restores source meaning',list(zip(right['periods'].tolist(),right['amounts'].tolist())),[(0,-1000),(1,200),(3,-50),(4,1000)])
    ck('6.8-E6','period-only sort is accepted but semantically wrong',list(zip(wrong['periods'].tolist(),wrong['amounts'].tolist())),[(0,-50),(1,-1000),(3,1000),(4,200)])
    ck('6.8-E6','wrong cumulative despite equal nominal net',(wrong['cumulative'].tolist(),wrong['nominal_net']),([-50,-1050,-50,150],150.))
    changed=m.cashflow_schedule(np.array([0,10,30,40],dtype=np.int64),amounts)
    ck('6.8-E7','timing retained while nominal operation ignores elapsed offsets',(changed['periods'].tolist(),changed['cumulative'].tolist(),changed['nominal_net']),([0,10,30,40],[-1000,-800,-850,150],150.))
    explicit_example=-F(100)+F(110)/(1+F(1,10))
    ck('6.8-E8','separate illustrative annual-effective PV at explicit rate',explicit_example,F(0))
    ck('6.8-E8','source still returns nominal addition only',m.cashflow_schedule(np.array([0,1],dtype=np.int64),np.array([-100.,110.]))['nominal_net'],10.)
    ck('ALL','caller arrays unchanged',(periods.tobytes(),amounts.tobytes()),before)
    ck('ALL','all outputs independent of source',all(not np.shares_memory(original[key],a) for key in ('periods','amounts','cumulative') for a in (periods,amounts)),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='cashflow-exercises-') as tmp:
        lab=Path(tmp);files={'cashflow_vectors.py':blocks[0],'test_cashflow_vectors.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['cashflow_vectors.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
