"""Scoped Section 6.5 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.05-vectorized-financial-calculations.md'
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
    q=np.array([10.,-5.,0.,2.]);p0=np.array([100.,80.,50.,40.]);p1=np.array([105.,76.,52.,35.])
    before=tuple(a.tobytes() for a in (q,p0,p1)); result=m.position_changes(q,p0,p1)
    oracle={'opening':[1000,-400,0,80],'closing':[1050,-380,0,70],'pnl':[50,20,0,-10]}
    for key in oracle: ck('6.5-E1','four aligned positions '+key,result[key].tolist(),oracle[key])
    ck('6.5-E1','position labels and output shape',(('LONG-A','SHORT-B','FLAT-C','LONG-D'),result['pnl'].shape),(('LONG-A','SHORT-B','FLAT-C','LONG-D'),(4,)))
    short=m.position_changes(np.array([-3.]),np.array([20.]),np.array([25.]))
    for key,expected in [('opening',-60),('closing',-75),('pnl',-15)]: ck('6.5-E2','rising-price short '+key,short[key].tolist(),[expected])
    for value in (float('nan'),float('inf'),-float('inf')):
        z=np.array([0.]);start=np.array([50.]);end=np.array([value]);unchanged=tuple(a.tobytes() for a in (z,start,end))
        reject('6.5-E3','nonfinite end at zero quantity '+str(value),lambda:m.position_changes(z,start,end),'ValueError')
        ck('6.5-E3','rejected inputs unchanged '+str(value),tuple(a.tobytes() for a in (z,start,end)),unchanged)
    numerical=[]
    for quantity,start,end,expected_direct,expected_alternative in [(3.,1e16,1e16+2,6.,8.),(.1,1e16,1e16+2,.2,.25)]:
        direct=np.float64(quantity)*(np.float64(end)-np.float64(start));alternative=np.float64(quantity)*np.float64(end)-np.float64(quantity)*np.float64(start)
        exact=F(quantity)*(F(end)-F(start))
        numerical.append(dict(inputs=[quantity,start,end],input_hex=[float(x).hex() for x in (quantity,start,end)],exact_binary_input_result=str(exact),direct=float(direct),alternative=float(alternative),direct_error=str(abs(F(float(direct))-exact)),alternative_error=str(abs(F(float(alternative))-exact))))
        ck('6.5-E4','observed formulas '+str(quantity),(float(direct),float(alternative)),(expected_direct,expected_alternative))
        ck('6.5-E4','direct equals exact rational result for these binary inputs '+str(quantity),F(float(direct)),exact)
        ck('6.5-E4','original source uses direct formula '+str(quantity),m.position_changes(np.array([quantity]),np.array([start]),np.array([end]))['pnl'].tolist(),[float(direct)])
    # Supplemental rational arithmetic illustrates designs; no expanded source API.
    distribution=F('0.5'); quantities=[F(2),F(-3),F(0)]
    ck('6.5-E5','signed distribution receipts/payments',[str(x*distribution) for x in quantities],['1','-3/2','0'])
    ck('6.5-E5','fixed-quantity total change with distribution',[str(F(2)*(F(35)-F(40)+distribution)),str(F(-3)*(F(25)-F(20)+distribution))],['-9','-33/2'])
    ck('6.5-E6','chosen illustrative FX conversion, not raw mixed-currency sum',F(10)+F(20)*F('1.10'),F(32))
    scenario_ends=[[F(35),F(25)],[F(45),F(15)]];sq=[F(2),F(-3)];sp=[F(40),F(20)]
    expected=[[sq[j]*(row[j]-sp[j]) for j in range(2)] for row in scenario_ends]
    ck('6.5-E7','rational scenario-by-position oracle',expected,[[F(-10),F(-15)],[F(10),F(15)]])
    # Existing source called one scenario at a time, not a new broadcast implementation.
    for i,row in enumerate(scenario_ends):
        value=m.position_changes(np.array(list(map(float,sq))),np.array(list(map(float,sp))),np.array(list(map(float,row))))
        ck('6.5-E7','existing source scenario row '+str(i),value['pnl'].tolist(),list(map(float,expected[i])))
    ck('6.5-E8','pre-timing fixed-fixture known answers', {k:v.tolist() for k,v in result.items()},oracle)
    ck('ALL','source input bytes unchanged',tuple(a.tobytes() for a in (q,p0,p1)),before)
    ck('ALL','outputs independent of caller inputs',all(not np.shares_memory(v,a) for v in result.values() for a in (q,p0,p1)),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='vectorized-exercises-') as tmp:
        lab=Path(tmp);files={'vectorized_marks.py':blocks[0],'test_vectorized_marks.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['vectorized_marks.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),numerical_observations=numerical,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
