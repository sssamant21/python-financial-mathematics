"""Formal 6.9–6.12 workflow checks: exact source and independent expectations."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SPECS=[('6.09-return-vectors.md','return_vectors'),('6.10-portfolio-weight-vectors.md','weight_vectors'),
       ('6.11-matrices-and-financial-models.md','matrix_models'),('6.12-linear-algebra-with-numpy.md','linear_algebra_lab')]
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
    with tempfile.TemporaryDirectory(prefix='chapter6-later-labs-') as tmp:
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
        for i,(filename,name) in enumerate(SPECS,9):
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
        m=modules[9];periods=np.array([0,1,3,4],dtype=np.int64);prices=np.array([100.,110.,99.,108.9]);before=(periods.tobytes(),prices.tobytes());path=m.return_path(periods,prices)
        exact_prices=list(map(F,['100','110','99','108.9']));gross=[b/a for a,b in zip(exact_prices[:-1],exact_prices[1:])];simple=[g-1 for g in gross];growth=[];product=F(1)
        for g in gross:product*=g;growth.append(product)
        close('6.9','rational gross ratios',path['gross'],list(map(float,gross)),1e-12);close('6.9','rational simple intervals',path['simple'],list(map(float,simple)),1e-12);close('6.9','rational linked growth',path['growth'],list(map(float,growth)),1e-12)
        ck('6.9','N observations produce N-1 endpoint pairs',(path['start_periods'].tolist(),path['end_periods'].tolist(),path['simple'].shape),([0,1,3],[1,3,4],(3,)))
        ck('6.9','exact final linked versus additive answers',(product-1,sum(simple)),(F(89,1000),F(1,10)))
        later=m.return_path(np.array([0,10,30,40],dtype=np.int64),prices);ck('6.9','timing changes labels without implicit annualization',(np.array_equal(later['simple'],path['simple']),later['end_periods'].tolist()),(True,[10,30,40]))
        ck('6.9','source storage preserved',(before==(periods.tobytes(),prices.tobytes()),all(not np.shares_memory(v,s) for v in path.values() for s in (periods,prices))),(True,True))
        tiny=m.return_path(np.array([0,1],dtype=np.int64),np.array([1.,1e-20]));ck('6.9','positive gross retained despite simple rounded to -1',(tiny['gross'][0]>0,tiny['simple'][0]),(True,-1.))
        reject('6.9','terminal zero excluded by positive-path contract',lambda:m.return_path(np.array([0,1],dtype=np.int64),np.array([1.,0.])),'ValueError')
        policy=np.geterr().copy()
        for values in ([1e-300,1e300],[1e300,1e-300]):reject('6.9','extreme ratio signals '+repr(values),lambda values=values:m.return_path(np.array([0,1],dtype=np.int64),np.array(values)),'FloatingPointError')
        ck('6.9','error policy restored',np.geterr(),policy)
        m=modules[10];ids=('A','B','CASH');values=np.array([600.,300.,100.]);returns=np.array([.1,-.05,0.]);weights=m.weights_from_values(values,ids);parts=m.contributions(weights,ids,returns,ids)
        ew=[F(600,1000),F(300,1000),F(100,1000)];er=[F(1,10),F(-1,20),F(0)];ep=[a*b for a,b in zip(ew,er)];portfolio=sum(ep);ending=sum(v*(1+r) for v,r in zip([600,300,100],er))
        close('6.10','rational opening weights',weights,list(map(float,ew)),1e-15);close('6.10','rational contributions',parts['contributions'],list(map(float,ep)),1e-15)
        close('6.10','rational portfolio return',parts['portfolio_return'],float(portfolio),1e-15);ck('6.10','independent opening/ending bridge',(ending,ending/F(1000)-1),(F(1045),portfolio))
        supplied=np.array([.6,.3,.1+5e-13]);snapshot=supplied.tobytes();near=m.contributions(supplied,ids,np.ones(3),ids)
        ck('6.10','near-one acceptance preserves supplied values',(supplied.tobytes()==snapshot,near['portfolio_return']==near['weight_sum'],near['weight_sum']>1),(True,True,True))
        reject('6.10','same length wrong identity order',lambda:m.contributions(weights,ids,returns,('B','A','CASH')),'ValueError')
        reject('6.10','zero total has no meaningful denominator',lambda:m.weights_from_values(np.zeros(3),ids),'ValueError')
        reject('6.10','invalid return at zero weight is not hidden',lambda:m.contributions(np.array([1.,0.,0.]),ids,np.array([0.,np.nan,0.]),ids),'ValueError')
        ck('6.10','weight and contribution storage independent',(np.shares_memory(weights,values),np.shares_memory(parts['contributions'],weights)),(False,False))
        m=modules[11];r,rids,scenarios,w,wids,portfolios=m.inputs();result=m.allocation_scenarios(r,rids,scenarios,w,wids,portfolios)
        rr=[[F('0.1'),F('-0.05'),F(0)],[F('-0.2'),F('0.1'),F(0)],[F(0),F(0),F('0.002')]];ww=[[F('.6'),F('.3'),F('.1')],[F('.2'),F('.3'),F('.5')]]
        cells=[[sum(a*b for a,b in zip(row,weight)) for weight in ww] for row in rr]
        close('6.11','rational scalar sum-of-products',result['returns'],[[float(x) for x in row] for row in cells],1e-12)
        ck('6.11','retained scenario/portfolio axes',(result['returns'].shape,result['scenarios'],result['portfolios']),((3,2),('UP','DOWN','CASH-YIELD'),('P1','P2')))
        order=[2,0,1];permuted_ids=tuple(rids[i] for i in order);permuted=m.allocation_scenarios(r[:,order],permuted_ids,scenarios,w[:,order],permuted_ids,portfolios)
        close('6.11','consistent identity permutation',permuted['returns'],[[float(x) for x in row] for row in cells],1e-12)
        reject('6.11','one-sided identity permutation',lambda:m.allocation_scenarios(r,rids,scenarios,w[:,order],permuted_ids,portfolios),'ValueError')
        ck('6.11','budget covers each input as well as output',m.allocation_scenarios(*m.inputs(),max_cells=9)['returns'].size,6)
        reject('6.11','input9cells exceeds8budget',lambda:m.allocation_scenarios(*m.inputs(),max_cells=8),'ValueError')
        reject('6.11','output-only budget failure',lambda:m.allocation_scenarios(np.zeros((3,1)),('A',),('S1','S2','S3'),np.ones((4,1)),('A',),('P1','P2','P3','P4'),max_cells=6),'ValueError')
        ck('6.11','transpose may share but result is independent',(np.shares_memory(w,w.T),np.shares_memory(result['returns'],r),np.shares_memory(result['returns'],w)),(True,False,False))
        m=modules[12];a=np.array([[1.,1.],[1.,2.]]);target=np.array([100.,150.]);original=(a.tobytes(),target.tobytes());solved=m.solve_payoffs(a,target)
        exact_b=F(150)-100;exact_a=F(100)-exact_b
        close('6.12','manual elimination solution',solved['units'],[float(exact_a),float(exact_b)],1e-12)
        # Eigenvalues of symmetric positive A are (3+-sqrt5)/2; condition_2
        # is their ratio, equivalently (7+3*sqrt5)/2.
        with localcontext() as ctx:ctx.prec=60;condition=(Decimal(7)+3*Decimal(5).sqrt())/2
        close('6.12','analytically derived condition_2',solved['condition_2'],float(condition),1e-12)
        rec=[sum(F(x)*F(y) for x,y in zip(row,solved['units'].tolist())) for row in [[1,1],[1,2]]];close('6.12','independent reconstructed payoffs',list(map(float,rec)),[100.,150.],1e-12)
        ck('6.12','normalized infinity residual meets gate',0<=solved['normalized_residual_inf']<=1e-12,True)
        signed=m.solve_payoffs(a,np.array([100.,50.]));close('6.12','signed units are not normalized weights',signed['units'],[150.,-50.],1e-12)
        zero=m.solve_payoffs(np.eye(2),np.zeros(2));ck('6.12','zero-target residual denominator convention',(zero['units'].tolist(),zero['normalized_residual_inf']),([0.,0.],0.))
        for bad in (np.array([[1.,1.],[2.,2.]]),np.diag([1.,1e-10])):reject('6.12','singular/ill-conditioned gate',lambda bad=bad:m.solve_payoffs(bad,np.ones(2)),'ValueError')
        ck('6.12','input and solved output storage',(original==(a.tobytes(),target.tobytes()),all(not np.shares_memory(solved[k],source) for k in ('units','residual') for source in (a,target))),(True,True))
        # Supplemental diagnostic reproduces source test's raw-solver experiment;
        # guarded solve_payoffs rejects this ill-conditioned coefficient table.
        sensitive=np.array([[1.,1.],[1.,1.+1e-10]]);b=np.array([2.,2.+1e-10]);changed=b.copy();changed[1]+=1e-8
        first=np.linalg.solve(sensitive,b);second=np.linalg.solve(sensitive,changed)
        gap=F(float(sensitive[1,1]))-1;exact_delta=(F(float(changed[1]))-F(float(b[1])))/gap
        close('6.12','raw sensitivity versus exact binary-input elimination',second-first,[-float(exact_delta),float(exact_delta)],1e-9)
        ck('6.12','raw small residual with large unit shift',(float(np.max(np.abs(sensitive@second-changed)))<1e-10,float(np.max(np.abs(second-first)))>10),(True,True))
        reject('6.12','guarded API still rejects raw diagnostic case',lambda:m.solve_payoffs(sensitive,b),'ValueError')
        benchmarks={'gross':list(map(str,gross)),'simple':list(map(str,simple)),'growth':list(map(str,growth)),'weights':list(map(str,ew)),'contributions':list(map(str,ep)),'portfolio_return':str(portfolio),'matrix_cells':[[str(x) for x in row] for row in cells],'condition_2_decimal':str(condition),'sensitivity_exact_binary_delta':str(exact_delta)}
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),runtime=runtime,workflow_records=4,derived_review_units=32,source_method_invocations=sum(x['actual_methods'] or 0 for x in commands),command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),independent_benchmarks=benchmarks,sources=sources,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks','runtime','independent_benchmarks')}))
    return bool(output['command_failed'] or output['failed'])
if __name__=='__main__':raise SystemExit(run())
