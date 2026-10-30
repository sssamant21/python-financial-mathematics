"""Scoped Section 6.7 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
from decimal import Decimal,localcontext
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.07-aggregation-and-statistical-operations.md'
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
    source=m.fixture();before=source.tobytes();extended=np.vstack((source,np.array([[50.,-10.]])))
    rows=[[-100,40],[0,0],[100,-40],[200,-80],[50,-10]]
    totals=[sum(map(F,row)) for row in rows];mean=sum(totals)/len(totals)
    result=m.summarize(extended)
    ck('6.7-E1','five totals independently added',result['totals'].tolist(),list(map(float,totals)))
    ck('6.7-E1','mean/min/max',(result['mean'],result['minimum'],result['maximum']),(float(mean),-60.,120.))
    ck('6.7-E1','counts and position means',(result['scenario_count'],result['position_count'],result['position_means'].tolist()),(5,2,[50.,-18.]))
    variance=sum((v-mean)**2 for v in totals)/len(totals)
    with localcontext() as ctx:
        ctx.prec=60;std_oracle=(Decimal(variance.numerator)/Decimal(variance.denominator)).sqrt()
    ck('6.7-E1','independent variance',variance,F(3616))
    ck('6.7-E1','std against 60-digit decimal sqrt',abs(Decimal.from_float(result['std'])-std_oracle)<Decimal('1e-12'),True)
    negative=np.array([[-5.,-2.],[-1.,-3.]]);neg=m.summarize(negative)
    ck('6.7-E2','all-negative finite table accepted',(neg['totals'].tolist(),neg['minimum'],neg['maximum'],neg['mean'],neg['std']),([-7.,-4.],-7.,-4.,-5.5,1.5))
    scenario_ids=('down','flat','up','stress');position_ids=('A','B')
    axis0=np.sum(source,axis=0);axis1=np.sum(source,axis=1)
    ck('6.7-E3','scenario axis removed leaves position labels',list(zip(position_ids,axis0.tolist())),[('A',200.),('B',-80.)])
    ck('6.7-E3','position axis removed leaves scenario labels',list(zip(scenario_ids,axis1.tolist())),[('down',-60.),('flat',0.),('up',60.),('stress',120.)])
    ck('6.7-E3','nonsquare shapes with keepdims',(source.shape,axis0.shape,axis1.shape,np.sum(source,axis=1,keepdims=True).shape),((4,2),(2,),(4,),(4,1)))
    ck('6.7-E3','source position means preserve position labels',list(zip(position_ids,m.summarize(source)['position_means'].tolist())),[('A',50.),('B',-20.)])
    single=np.array([[-2.],[0.],[5.]]);one=m.summarize(single)
    ck('6.7-E4','single position multiple scenarios',(one['totals'].tolist(),one['totals'].shape,one['position_means'].shape,one['scenario_count'],one['position_count']),([-2.,0.,5.],(3,),(1,),3,1))
    ck('6.7-E4','single position statistics',(one['mean'],one['minimum'],one['maximum'],one['position_means'].tolist()),(1.,-2.,5.,[1.]))
    with localcontext() as ctx:
        ctx.prec=60;single_std=(Decimal(26)/3).sqrt()
    ck('6.7-E4','single position dispersion',abs(Decimal.from_float(one['std'])-single_std)<Decimal('1e-12'),True)
    ck('6.7-E5','flattened numerical total only',float(np.sum(source)),120.)
    ck('6.7-E5','one scenario total differs from flattened sum',m.summarize(source)['totals'][0],-60.)
    # Supplemental controlled missing-data record, not a replacement summarize API.
    missing=[[F(1),None,None],[F(3),F(5),None],[None,F(7),None]]
    counts=[];means=[]
    for j in range(3):
        valid=[r[j] for r in missing if r[j] is not None];counts.append(len(valid));means.append(None if not valid else sum(valid)/len(valid))
    ck('6.7-E6','explicit valid counts incl all-missing position',counts,[2,2,0])
    ck('6.7-E6','descriptive means incl explicit all-missing result',means,[F(2),F(6),None])
    ck('6.7-E6','differing source counts remain visible',[sum(v is not None for v in r) for r in missing],[1,2,1])
    reject('6.7-E6','original strict source still rejects missing table',lambda:m.summarize(np.array([[1.,np.nan,np.nan],[3.,5.,np.nan],[np.nan,7.,np.nan]])),'ValueError')
    weights=[F(1,10),F(2,10),F(3,10),F(4,10)];base_totals=[F(-60),F(0),F(60),F(120)]
    ck('6.7-E7','chosen rational probabilities sum exactly to one',sum(weights),F(1))
    ck('6.7-E7','illustrative weighted descriptive mean',sum(w*t for w,t in zip(weights,base_totals)),F(60))
    ck('6.7-E7','unchanged source remains unweighted',m.summarize(source)['mean'],30.)
    cancel=np.array([[-10.,10.],[10.,-10.]]);summary=m.summarize(cancel)
    ck('6.7-E8','hand-selected aggregate cancellations',(summary['totals'].tolist(),summary['std']),([0.,0.],0.))
    outside=np.array([[-10.,10.],[10.,-10.],[-10.,-10.]])
    ck('6.7-E8','unrepresented joint-loss scenario is possible in illustrative extension',m.summarize(outside)['minimum'],-20.)
    ck('ALL','original source fixture unchanged',source.tobytes(),before)
    ck('ALL','source outputs independent',all(not np.shares_memory(extended,result[k]) for k in ('totals','position_means')),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='aggregation-exercises-') as tmp:
        lab=Path(tmp);files={'aggregation_lab.py':blocks[0],'test_aggregation_lab.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['aggregation_lab.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),independent_oracles=dict(fifth_scenario_totals=list(map(str,totals)),mean=str(mean),variance=str(variance),std_decimal_60=str(std_oracle),single_position_std_decimal_60=str(single_std)),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
