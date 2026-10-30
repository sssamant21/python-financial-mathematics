"""Scoped Section 6.10 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.10-portfolio-weight-vectors.md'
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
    ids=('A','B','CASH');values=np.array([600.,300.,100.]);returns=np.array([.1,-.05,0.]);before=(values.tobytes(),returns.tobytes())
    def near(e,label,a,x):ck(e,label,bool(np.allclose(a,x,rtol=0,atol=1e-14,equal_nan=False)),True)
    changed=np.array([500.,400.,100.]);weights=m.weights_from_values(changed,ids);result=m.contributions(weights,ids,returns,ids)
    near('6.10-E1','new weights',weights,[.5,.4,.1]);near('6.10-E1','new contributions',result['contributions'],[.05,-.02,0.]);near('6.10-E1','new portfolio result',result['portfolio_return'],float(F(3,100)))
    original_weights=m.weights_from_values(values,ids);cash_returns=np.array([.1,-.05,.002]);cash=m.contributions(original_weights,ids,cash_returns,ids)
    near('6.10-E2','cash supplied return contribution',cash['contributions'][-1],float(F(1,5000)));near('6.10-E2','cash supplied return portfolio result',cash['portfolio_return'],float(F(113,2500)))
    perm=np.array([2,0,1]);new_ids=tuple(ids[i] for i in perm);reordered_weights=m.weights_from_values(values[perm],new_ids);base=m.contributions(original_weights,ids,returns,ids);reordered=m.contributions(reordered_weights,new_ids,returns[perm],new_ids)
    ck('6.10-E3','permuted IDs',reordered['ids'],('CASH','A','B'));near('6.10-E3','permuted contributions',reordered['contributions'],[0.,.06,-.015]);near('6.10-E3','scalar invariant under aligned permutation',reordered['portfolio_return'],base['portfolio_return'])
    reject('6.10-E3','IDs-only permutation correctly rejected',lambda:m.contributions(original_weights,ids,returns,new_ids),'ValueError')
    extended_ids=ids+('ZERO-D',);extended_values=np.array([600.,300.,100.,0.]);extended_weights=m.weights_from_values(extended_values,extended_ids)
    ck('6.10-E4','unique extra zero-value position weight',float(extended_weights[-1]),0.)
    for bad in (float('nan'),float('inf'),-1.01):
        supplied=np.array([.1,-.05,0.,bad]);raw=supplied.tobytes()
        reject('6.10-E4','invalid return on zero-value position '+str(bad),lambda:m.contributions(extended_weights,extended_ids,supplied,extended_ids),'ValueError')
        ck('6.10-E4','rejected returns preserved '+str(bad),supplied.tobytes(),raw)
    ending=[F(660),F(285),F(100)];closing=[v/sum(ending) for v in ending];closing_result=m.contributions(np.array(list(map(float,closing))),ids,returns,ids)
    ck('6.10-E5','exact closing weights',closing,[F(132,209),F(57,209),F(20,209)])
    wrong=sum(w*r for w,r in zip(closing,[F(1,10),F(-1,20),F(0)]))
    ck('6.10-E5','closing-weight hypothetical differs from opening answer',(wrong,F(9,200)),(F(207,4180),F(9,200)))
    near('6.10-E5','source computes supplied closing-weight hypothetical',closing_result['portfolio_return'],float(wrong))
    subset_weights=m.weights_from_values(values[:2],ids[:2]);subset=m.contributions(subset_weights,ids[:2],returns[:2],ids[:2])
    near('6.10-E6','invested-subset weights',subset_weights,[float(F(2,3)),float(F(1,3))]);near('6.10-E6','invested-subset result',subset['portfolio_return'],float(F(1,20)))
    near('6.10-E6','full denominator result still distinct',base['portfolio_return'],float(F(9,200)))
    reject('6.10-E7','long-only source rejects signed values',lambda:m.weights_from_values(np.array([120.,-20.]),('LONG','SHORT')),'ValueError')
    ck('6.10-E7','separate signed-exposure denominator example',(F(120)-F(20),F(120)+F(20),F(120,100),F(-20,100)),(F(100),F(140),F(6,5),F(-1,5)))
    pair=('UP','DOWN');r=np.array([.1,-.1]);initial=m.weights_from_values(np.array([50.,50.]),pair);first=m.contributions(initial,pair,r,pair)
    drift=m.weights_from_values(np.array([55.,45.]),pair);second_hold=m.contributions(drift,pair,r,pair);second_rebalance=m.contributions(initial,pair,r,pair)
    near('6.10-E8','first interval equal weights return',first['portfolio_return'],0.);near('6.10-E8','drifted opening weights',drift,[.55,.45]);near('6.10-E8','second fixed-holding interval return',second_hold['portfolio_return'],float(F(1,100)));near('6.10-E8','second rebalanced interval return',second_rebalance['portfolio_return'],0.)
    ck('6.10-E8','independent holdings vs rebalanced ending values',(F(50)*F(11,10)**2+F(50)*F(9,10)**2,F(100)),(F(101),F(100)))
    ck('ALL','caller input bytes unchanged',(values.tobytes(),returns.tobytes()),before)
    ck('ALL','computed weights and contributions independent',(np.shares_memory(original_weights,values),np.shares_memory(base['contributions'],original_weights)),(False,False))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='weight-exercises-') as tmp:
        lab=Path(tmp);files={'weight_vectors.py':blocks[0],'test_weight_vectors.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['weight_vectors.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
