"""Scoped Section 6.16 review; unchanged source plus supplemental predicates."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from pathlib import Path
import numpy as np
import math
from fractions import Fraction as F
from copy import deepcopy
from extensions import lookup,render_contributions,align_prices,batch_portfolios,distribution_report,resident_snapshot,measure
HERE=Path(__file__).resolve().parent; BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-06/6.16-chapter-project-vectorized-portfolio-calculator.md'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def run():
    text=SOURCE.read_text(); blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S); assert len(blocks)==2
    m=types.ModuleType('exact_portfolio');sys.modules[m.__name__]=m;exec(compile(blocks[0],str(SOURCE),'exec'),m.__dict__)
    checks=[];commands=[]
    def ck(e,label,a,x): checks.append(dict(exercise=e,label=label,actual=repr(a),expected=repr(x),status='PASS' if a==x else 'FAIL'))
    def reject(e,label,fn,kind):
        try: fn(); actual='no exception'; detail=''
        except Exception as error: actual=type(error).__name__;detail=traceback.format_exc()
        ck(e,label,actual,kind);checks[-1]['expected_exception_trace']=detail
    assets=('ALPHA','BETA','CASH');scenarios=('up','down','flat')
    args=dict(assets=assets,quantities=[6,3,1],opening_prices=[100,100,100],scenario_assets=assets,scenarios=scenarios,closing_prices=[[110,95,100],[80,105,100],[100,100,100]])
    base=m.calculate(**args);fields=('weights','asset_returns','contributions','portfolio_returns','ending_values','pnl');before={k:getattr(base,k).tobytes() for k in fields}
    def near(e,label,a,x):ck(e,label,bool(np.allclose(a,x,rtol=1e-12,atol=1e-12,equal_nan=False)),True)
    rendered=render_contributions(base,'up')
    ck('6.16-E1','percentage-point rendering',rendered,'up (percentage points)\nALPHA: +6.0000 pp\nBETA: -1.5000 pp\nCASH: +0.0000 pp\n')
    ck('6.16-E1','stored precision unchanged',base.contributions.tobytes(),before['contributions'])
    found=lookup(base,'down');ck('6.16-E2','named scenario preserves row identity',(found['name'],found['row'],found['assets']),('down',1,assets));near('6.16-E2','named outcome',found['pnl'],-105.)
    ck('6.16-E2','lookup contribution snapshot independent/readonly',(np.shares_memory(found['contributions'],base.contributions),found['contributions'].flags.writeable),(False,False))
    reject('6.16-E2','unknown scenario rejected',lambda:lookup(base,'missing'),'KeyError')
    aligned=align_prices(assets,{'CASH':100,'BETA':95,'ALPHA':110});ck('6.16-E3','mapping explicitly aligned',(aligned.tolist(),str(aligned.dtype)),([110.,95.,100.],'float64'))
    # Lossless pairs retain duplicate wire keys which an already built dict cannot.
    array_calls=[];real_array=np.array
    def forbidden_array(*a,**k):array_calls.append('called');raise AssertionError('array construction before key rejection')
    np.array=forbidden_array
    try:
        for label,pairs in [('missing',[('ALPHA',110),('BETA',95)]),('extra',[('ALPHA',110),('BETA',95),('CASH',100),('OTHER',1)]),('duplicate',[('ALPHA',110),('BETA',95),('CASH',100),('ALPHA',111)])]:reject('6.16-E3','key failure before arrays '+label,lambda pairs=pairs:align_prices(assets,pairs),'ValueError')
    finally:np.array=real_array
    ck('6.16-E3','no array construction for invalid identifiers',array_calls,[])
    reject('6.16-E3','Boolean mixture rejected before inference',lambda:align_prices(assets,[('ALPHA',True),('BETA',95),('CASH',100)]),'ValueError')
    aligned_report=m.calculate(**dict(args,scenarios=('up',),closing_prices=aligned[None,:]));near('6.16-E3','aligned source ingestion result',aligned_report.ending_values,[1045.])
    interest=np.array(args['closing_prices'],dtype=np.float64);interest[:,2]=100.2
    bearing=m.calculate(**dict(args,closing_prices=interest));near('6.16-E4','supplied cash quote includes all interest once',bearing.ending_values,[1045.2,895.2,1000.2]);near('6.16-E4','interest-bearing portfolio returns',bearing.portfolio_returns,[float(F(113,2500)),float(F(-131,1250)),float(F(1,5000))])
    quantities=np.array([[6.,3.,1.],[2.,3.,5.]]);p0=np.array([100.,100.,100.]);p1=np.array(args['closing_prices'],dtype=np.float64);portfolio_ids=('P1','P2')
    batch=batch_portfolios(assets,quantities,p0,assets,scenarios,p1,portfolio_ids)
    ck('6.16-E5','batch axis contract',(batch['portfolio_returns'].shape,batch['weights'].shape,batch['scenarios'],batch['portfolios']),((3,2),(2,3),scenarios,portfolio_ids))
    near('6.16-E5','independent batch ending values',batch['ending_values'],[[1045.,1005.],[895.,975.],[1000.,1000.]])
    near('6.16-E5','independent batch returns',batch['portfolio_returns'],[[.045,.005],[-.105,-.025],[0.,0.]])
    for j in range(2):
        standalone=m.calculate(**dict(args,quantities=quantities[j]));near('6.16-E5','individual source reconciliation '+str(j),batch['portfolio_returns'][:,j],standalone.portfolio_returns)
    reject('6.16-E5','cell budget rejects oversized labelled inputs',lambda:batch_portfolios(assets,quantities,p0,assets,scenarios,p1,portfolio_ids,max_cells=8),'ValueError')
    reject('6.16-E5','duplicate portfolio names rejected',lambda:batch_portfolios(assets,quantities,p0,assets,scenarios,p1,('P1','P1')),'ValueError')
    reject('6.16-E5','zero-value portfolio rejected',lambda:batch_portfolios(assets,np.array([[0.,0.,0.],[2.,3.,5.]]),p0,assets,scenarios,p1,portfolio_ids),'ValueError')
    cash=np.array([[1.,2.,0.],[0.,1.,0.],[.5,0.,0.]],dtype=np.float64);cash_bytes=cash.tobytes();dist=distribution_report(m,args,cash)
    near('6.16-E6','per-unit distributions give direct cash amounts',dist['cash_received'],[12.,3.,3.]);near('6.16-E6','direct value route updated with cash',dist['ending_values'],[1057.,898.,1003.]);near('6.16-E6','return route updated consistently',dist['portfolio_returns'],[.057,-.102,.003]);near('6.16-E6','direct and return routes reconcile',(dist['ending_values']-dist['opening_value'])/dist['opening_value'],dist['portfolio_returns'])
    ck('6.16-E6','distribution input preserved',cash.tobytes(),cash_bytes)
    reject('6.16-E6','distribution shape mismatch',lambda:distribution_report(m,args,np.zeros((1,3))),'ValueError')
    resident=resident_snapshot(m,args);resident_report=resident()
    ck('6.16-E7','same Report representation',type(resident_report) is m.Report,True)
    for field in fields:near('6.16-E7','resident/source numerical gate '+field,getattr(resident_report,field),getattr(base,field))
    ck('6.16-E7','resident outputs readonly and separate across calls',all(not getattr(resident_report,k).flags.writeable and not np.shares_memory(getattr(resident_report,k),getattr(resident(),k)) for k in fields),True)
    mutable=deepcopy(args);owned=resident_snapshot(m,mutable);mutable['quantities'][0]=99;near('6.16-E7','validated resident snapshot isolated from later caller edit',owned().ending_values,base.ending_values)
    timings=dict(scope='tiny three-asset/three-scenario workload; source validates/copies each call; resident validates/copies once outside timing and recomputes same Report outputs',source_validated=measure(lambda:m.calculate(**args)),supplemental_resident=measure(resident))
    (HERE/'timings.json').write_text(json.dumps(timings,indent=2,allow_nan=False)+'\n')
    ck('6.16-E7','raw repeated samples finite',all(len(timings[k]['seconds_per_call'])==5 and all(math.isfinite(v) and v>=0 for v in timings[k]['seconds_per_call']) for k in ('source_validated','supplemental_resident')),True)
    tiny=m.calculate(('ONE',),[3],[1e16],('ONE',),('tiny-up',),[[1e16+2]])
    exact=F(3)*(F(10000000000000002)-F(10000000000000000));direct=float(tiny.pnl[0]);reconstructed=float(tiny.opening_value*tiny.portfolio_returns[0]);delta_route=float(np.float64(3)*(np.float64(1e16+2)-np.float64(1e16)))
    ck('6.16-E8','independent exact represented-input change',exact,F(6));ck('6.16-E8','observed alternative delta expression',delta_route,6.)
    diagnostic=dict(quantity=3,opening_price=10000000000000000,closing_price=10000000000000002,exact_price_only_pnl=str(exact),project_direct_pnl=direct,project_return_reconstruction=reconstructed,delta_expression=delta_route,direct_absolute_error=str(abs(F(direct)-exact)),return_reconstruction_absolute_error=str(abs(F(reconstructed)-exact)),scope='supported finite calculation; extreme-scale accuracy is not promised; no universal winning formula')
    (HERE/'tiny-change.json').write_text(json.dumps(diagnostic,indent=2)+'\n')
    ck('ALL','base report remains unchanged',{k:getattr(base,k).tobytes() for k in fields},before)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='project-extensions-') as tmp:
        parent=Path(tmp);lab=parent/'numpy_lab_616';lab.mkdir();files={'portfolio.py':blocks[0],'test_portfolio.py':blocks[1]}
        for name,code in files.items():(lab/name).write_text(code);compile(code,name,'exec')
        specs=[('original project suite',['-m','unittest','discover','-s','numpy_lab_616','-v'],8,None),('original project demo',['numpy_lab_616/portfolio.py'],None,re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]),('original compileall command',['-m','compileall','-q','numpy_lab_616'],None,'')]
        for label,args,count,expected in specs:
            r=subprocess.run([sys.executable,'-B',*args],cwd=parent,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))) if count is not None else (r.stdout==expected and r.stderr==''))
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','source listings unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),listing_sha256=[sha(c.encode()) for c in blocks],exercise_records=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),source_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),supplemental_artifact_sha256={name:sha((HERE/name).read_bytes()) for name in ('extensions.py','timings.json','tiny-change.json')},commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('checks','commands','listing_sha256')}))
    return bool(output['failed'] or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
