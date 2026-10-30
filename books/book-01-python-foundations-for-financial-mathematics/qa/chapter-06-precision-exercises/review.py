"""Scoped Section 6.14 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from decimal import Decimal,localcontext
from fractions import Fraction as F
import math
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.14-numerical-precision-and-numpy.md'
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
    observations={};tiny_oracles=[]
    for count in (1,10):
        values=np.full(count,1e-17,dtype=np.float64);raw=values.tobytes()
        with localcontext() as ctx:
            ctx.prec=100;exact_decimal=(Decimal(1)+Decimal('1e-17'))**count-Decimal(1)
        exact_fraction=(1+F(1,10**17))**count-1;actual=m.linked_return(values);naive=float(np.prod(1+values)-1)
        ck('6.14-E1','Decimal vs rational reference '+str(count),math.isclose(float(exact_decimal),float(exact_fraction),rel_tol=1e-15,abs_tol=0),True)
        ck('6.14-E1','source tiny nonzero linked return '+str(count),math.isclose(actual,float(exact_decimal),rel_tol=1e-15,abs_tol=0),True)
        ck('6.14-E1','naive loses tiny increments '+str(count),naive,0.)
        ck('6.14-E1','source inputs preserved '+str(count),values.tobytes(),raw)
        tiny_oracles.append(dict(count=count,decimal_text_reference=str(exact_decimal),exact_fraction=str(exact_fraction),actual=actual,naive=naive,relative_error_vs_float_reference=abs(actual-float(exact_decimal))/abs(float(exact_decimal))))
    ck('6.14-E2','NumPy broadcasting would permit mismatch',np.broadcast_shapes((2,),(1,)),(2,))
    reject('6.14-E2','source forbids comparison broadcasting',lambda:m.agrees(np.array([1.,1.]),np.array([1.]),rtol=0.,atol=0.),'ValueError')
    spacing_one=float(np.spacing(np.float64(1.)));spacing_large=float(np.spacing(np.float64(1e16)))
    ck('6.14-E3','spacing near one equals exact binary epsilon',F(spacing_one),F(1,2**52))
    ck('6.14-E3','spacing near 10^16 is two',spacing_large,2.)
    ck('6.14-E3','integer increment lost locally',float(np.float64(1e16)+np.float64(1.)),1e16)
    ck('6.14-E4','illustrative rate comparison rejects chosen absolute error',m.agrees(np.array([1e-7]),np.array([0.]),rtol=1e-10,atol=1e-12),False)
    ck('6.14-E4','illustrative USD comparison accepts 0.5 micro-dollar error',m.agrees(np.array([100.+5e-7]),np.array([100.]),rtol=0.,atol=1e-6),True)
    actual,reference=np.array([100.004]),np.array([100.003]);display=(f'{actual[0]:.2f}',f'{reference[0]:.2f}')
    ck('6.14-E5','same two-decimal display',display,('100.00','100.00'))
    ck('6.14-E5','underlying values fail explicit criterion',m.agrees(actual,reference,rtol=0.,atol=1e-4),False)
    cancellation=np.array([1e16]+[1.]*100+[-1e16],dtype=np.float64);cumulative=np.cumsum(cancellation,dtype=np.float64);reduced=float(np.sum(cancellation,dtype=np.float64));scalar=math.fsum(cancellation.tolist());exact=sum(map(F,cancellation.tolist()))
    ck('6.14-E6','independent rational cancellation sum',exact,F(100))
    ck('6.14-E6','fsum matches exact supplied-float sum',F(scalar),exact)
    ck('6.14-E6','ordered cumulative loses unit increments',float(cumulative[-1]),0.)
    observations['cancellation']=dict(fixture='[1e16] + [1.0]*100 + [-1e16]',count=102,ordered_cumulative_final=float(cumulative[-1]),separate_numpy_reduction=reduced,math_fsum=scalar,exact_fraction=str(exact),absolute_errors=dict(cumulative=abs(float(cumulative[-1])-float(exact)),reduction=abs(reduced-float(exact)),fsum=abs(scalar-float(exact))))
    weights=[F(3,5),F(3,10),F(1,10)];correct=[F(1,10),F(-1,20),F(0)];mislabelled=[F(-1,20),F(1,10),F(0)]
    ck('6.14-E7','exact arithmetic cannot repair mislabeled input',(sum(w*r for w,r in zip(weights,correct)),sum(w*r for w,r in zip(weights,mislabelled))),(F(9,200),F(0)))
    reject('6.14-E8','transformed source does not accept arbitrary positive simple return',lambda:m.linked_return(np.array([1.])),'ValueError')
    rounded=m.linked_return(np.full(100,-.5))
    ck('6.14-E8','simple scalar can round to total loss despite positive exact gross',(rounded,F(1,2)**100>0),(-1.,True))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='precision-exercises-') as tmp:
        lab=Path(tmp);files={'precision_lab.py':blocks[0],'test_precision_lab.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['precision_lab.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),tiny_oracles=tiny_oracles,observations=observations,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
