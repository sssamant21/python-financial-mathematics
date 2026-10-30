"""Scoped Section 6.6 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.06-broadcasting.md'
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
    q=np.array([10.,-5.,0.]);p=np.array([100.,80.,50.]);s=np.array([-.1,0.,.1,.25]);before=tuple(a.tobytes() for a in (q,p,s))
    result=m.scenario_pnl(q,p,s)
    marks=[F(1000),F(-400),F(0)]; shock_texts=['-0.1','0','0.1','0.25']
    oracle=[[float(mark*F(shock)) for mark in marks] for shock in shock_texts]
    ck('6.6-E1','independent rational four-row grid',result.tolist(),oracle)
    ck('6.6-E1','new fourth shock row',result[-1].tolist(),[250,-100,0])
    ck('6.6-E1','nonsquare axes and payload',(result.shape,str(result.dtype),result.nbytes),((4,3),'float64',96))
    ck('6.6-E2','shape-only broadcast prediction',np.broadcast_shapes((7,1),(1,4)),(7,4))
    one=m.scenario_pnl(q,p,np.array([.25]));ck('6.6-E3','one scenario retains both axes',(one.shape,one.tolist()),((1,3),[[250,-100,0]]))
    for shock in (0.,-1.):
        value=m.scenario_pnl(q,p,np.array([shock]));ck('6.6-E3','one scenario '+str(shock),(value.shape,value.tolist()),((1,3),[[float(mark*F(shock)) for mark in marks]]))
    instrument_shocks=np.array([[-.1,0.,.25],[.2,-.5,0.]])
    reject('6.6-E4','matrix not silently accepted by common-shock source',lambda:m.scenario_pnl(q,p,instrument_shocks),'ValueError')
    custom=[[marks[j]*F(h) for j,h in enumerate(row)] for row in [['-0.1','0','0.25'],['0.2','-0.5','0']]]
    ck('6.6-E4','design-only matrix rational example',custom,[[F(-100),F(0),F(0)],[F(200),F(200),F(0)]])
    cells=10000*2000;payload=cells*8
    ck('6.6-E5','Python integer output-cell count',cells,20000000)
    ck('6.6-E5','element bytes and MiB',(payload,F(payload,2**20)),(160000000,F(78125,512)))
    # Only small input vectors are allocated; original budget check precedes output arithmetic.
    reject('6.6-E5','default budget rejects 20 million output cells',lambda:m.scenario_pnl(np.ones(2000),np.ones(2000),np.zeros(10000)),'ValueError')
    for price in (-1.,float('nan'),float('inf')):
        price_vector=np.array([price]);zero=np.array([0.]);unchanged=price_vector.tobytes()
        reject('6.6-E6','invalid price for flat position '+str(price),lambda:m.scenario_pnl(zero,price_vector,np.array([0.])),'ValueError')
        ck('6.6-E6','invalid input unchanged '+str(price),price_vector.tobytes(),unchanged)
    owned=np.array([10.,20.,30.]);view=np.broadcast_to(owned,(2,3))
    ck('6.6-E7','broadcast view readonly/alias/zero scenario stride',(view.flags.writeable,np.shares_memory(view,owned),view.strides[0]),(False,True,0))
    reject('6.6-E7','ordinary broadcast write rejected',lambda:view.__setitem__((0,0),999.),'ValueError')
    independent=view.copy();independent[0,0]=77.
    ck('6.6-E7','deliberate independent copy edit',(owned.tolist(),independent[1].tolist()),([10,20,30],[10,20,30]))
    # Deliberately unsafe counterexample on owned disposable storage, never source input.
    view.setflags(write=True);view[0,0]=999.
    ck('6.6-E7','forced write aliases both scenarios and backing array',(view[:,0].tolist(),owned[0]),([999,999],999))
    labels=('down','flat','up','stress','loss');shocks=np.array([-.1,0.,.1,.25,-1.]);rows=[];seen=[];chunk_shapes=[]
    for lo in range(0,len(labels),2):
        hi=min(lo+2,len(labels));part=m.scenario_pnl(q,p,shocks[lo:hi],max_cells=6)
        chunk_shapes.append(part.shape);rows.extend(part.tolist());seen.extend(labels[lo:hi])
    chunk_oracle=[[float(mark*F(shock)) for mark in marks] for shock in ['-0.1','0','0.1','0.25','-1']]
    ck('6.6-E8','all chunk values against rational grid',rows,chunk_oracle)
    ck('6.6-E8','labels preserved without duplication',tuple(seen),labels)
    ck('6.6-E8','uneven final chunk retains two axes',chunk_shapes,[(2,3),(2,3),(1,3)])
    ck('6.6-E8','no implicit reduction',(len(rows),len(rows[0])),(5,3))
    ck('ALL','original inputs unchanged',tuple(a.tobytes() for a in (q,p,s)),before)
    ck('ALL','source result independent',all(not np.shares_memory(result,a) for a in (q,p,s)),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='broadcasting-exercises-') as tmp:
        lab=Path(tmp);files={'broadcasting_lab.py':blocks[0],'test_broadcasting_lab.py':blocks[1]}
        for name,code in files.items(): (lab/name).write_text(code);compile(code,name,'exec')
        for label,args,expected,count in [('original source suite',['-m','unittest','discover','-v'],None,8),('original source demo',['broadcasting_lab.py'],re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0],None)]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((r.stdout==expected and r.stderr=='') if expected is not None else (actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','extracted source/test bytes unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__': raise SystemExit(run())
