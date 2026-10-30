"""Scoped Section 6.12 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
import math
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.12-linear-algebra-with-numpy.md'
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
    a=np.array([[1.,1.],[1.,2.]]);target=np.array([80.,120.]);before=(a.tobytes(),target.tobytes())
    def near(e,label,x,y):ck(e,label,bool(np.allclose(x,y,rtol=1e-12,atol=1e-12,equal_nan=False)),True)
    first=m.solve_payoffs(a,target);near('6.12-E1','manual subtraction gives 40 units each',first['units'],[40.,40.]);near('6.12-E1','state payoff reconstruction',a@first['units'],[80.,120.])
    a3=np.array([[1.,1.,0.],[1.,2.,0.],[0.,0.,4.]]);b3=np.array([100.,150.,12.]);third=m.solve_payoffs(a3,b3)
    near('6.12-E2','third independent equation 4*xC=12',third['units'],[50.,50.,3.]);near('6.12-E2','three-state reconstruction',a3@third['units'],[100.,150.,12.]);ck('6.12-E2','unknown/residual shapes',(third['units'].shape,third['residual'].shape),((3,),(3,)))
    # Use unequal solved units so a column permutation cannot pass vacuously.
    distinct=np.array([80.,130.]);base=m.solve_payoffs(a,distinct);row_order=[1,0];rows=m.solve_payoffs(a[row_order],distinct[row_order])
    near('6.12-E3','row and target joint permutation preserves units',rows['units'],[30.,50.]);near('6.12-E3','row permutation preserves original solution',rows['units'],base['units'])
    ck('6.12-E3','caller state label order',tuple(('STATE-1','STATE-2')[i] for i in row_order),('STATE-2','STATE-1'))
    col_order=[1,0];cols=m.solve_payoffs(a[:,col_order],distinct);instrument_ids=('A','B');reordered_ids=tuple(instrument_ids[i] for i in col_order)
    near('6.12-E4','column order changes output unit order',cols['units'],[50.,30.]);near('6.12-E4','mapping restored to original instrument order',cols['units'][col_order],base['units']);ck('6.12-E4','caller instrument labels travel with columns',reordered_ids,('B','A'))
    for bad in (float('nan'),float('inf'),-float('inf')):
        invalid=a.copy();invalid[0,1]=bad;raw=invalid.tobytes();policy=np.geterr().copy()
        reject('6.12-E5','nonfinite coefficient '+str(bad),lambda:m.solve_payoffs(invalid,target),'ValueError');ck('6.12-E5','coefficient rejection preserves bytes/error policy '+str(bad),(invalid.tobytes(),np.geterr()),(raw,policy))
    diagnostics=[]
    for factor in (1.,100000.):
        scaled_a=np.array([[.1,.2],[.3,.7]])*factor;scaled_b=np.array([.4,1.1])*factor;record=m.solve_payoffs(scaled_a,scaled_b)
        near('6.12-E6','uniform scale '+str(factor)+' retains intended decimal solution',record['units'],[6.,-1.])
        absolute=max(map(abs,record['residual'].tolist()));scale=max(math.fsum(abs(v) for v in row) for row in scaled_a.tolist())*max(map(abs,record['units'].tolist()))+max(map(abs,scaled_b.tolist()))
        computed=absolute/scale if scale else absolute
        ck('6.12-E6','normalized diagnostic formula '+str(factor),math.isclose(record['normalized_residual_inf'],computed,rel_tol=1e-14,abs_tol=0.),True)
        ck('6.12-E6','finite diagnostics and stated gates '+str(factor),(math.isfinite(absolute),record['condition_2']<=1e8,record['normalized_residual_inf']<=1e-12),(True,True,True))
        exact_residual=[sum(F(float(coef))*F(float(unit)) for coef,unit in zip(row,record['units']))-F(float(bv)) for row,bv in zip(scaled_a,scaled_b)]
        diagnostics.append(dict(uniform_factor=factor,a=scaled_a.tolist(),target=scaled_b.tolist(),units=record['units'].tolist(),residual=record['residual'].tolist(),absolute_residual_inf=absolute,normalization_scale=scale,normalized_residual_inf=record['normalized_residual_inf'],condition_2=record['condition_2'],exact_represented_input_residuals=list(map(str,exact_residual))))
    reject('6.12-E7','square source does not silently fit rectangular system',lambda:m.solve_payoffs(np.array([[1.],[1.]]),np.array([1.,2.])),'ValueError')
    ck('6.12-E7','separate unweighted least-squares toy optimum and objective',(F(3,2),(F(3,2)-1)**2+(F(3,2)-2)**2),(F(3,2),F(1,2)))
    ck('6.12-E8','solver record contains no prices/trades',set(base),{'units','residual','condition_2','normalized_residual_inf'})
    ck('ALL','source arrays unchanged',(a.tobytes(),target.tobytes()),before);ck('ALL','outputs independent',all(not np.shares_memory(first[key],v) for key in ('units','residual') for v in (a,target)),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='linear-exercises-') as tmp:
        lab=Path(tmp);files={'linear_algebra_lab.py':blocks[0],'test_linear_algebra_lab.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['linear_algebra_lab.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),rescaling_observations=diagnostics,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
