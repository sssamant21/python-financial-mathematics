"""Formal 6.5–6.8 workflow checks: exact source and independent expectations."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
SPECS=[('6.05-vectorized-financial-calculations.md','vectorized_marks'),('6.06-broadcasting.md','broadcasting_lab'),
       ('6.07-aggregation-and-statistical-operations.md','aggregation_lab'),('6.08-cash-flow-vectors.md','cashflow_vectors')]
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
    with tempfile.TemporaryDirectory(prefix='chapter6-middle-labs-') as tmp:
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
        for i,(filename,name) in enumerate(SPECS,5):
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
        m=modules[5];q=np.array([10.,-5.,0.]);p0=np.array([100.,80.,50.]);p1=np.array([105.,76.,52.]);inputs=(q,p0,p1);before=[x.tobytes() for x in inputs];out=m.position_changes(*inputs)
        integer_q=[10,-5,0];integer_start=[100,80,50];integer_end=[105,76,52]
        expect={'opening':[a*b for a,b in zip(integer_q,integer_start)],'closing':[a*b for a,b in zip(integer_q,integer_end)],'pnl':[a*(c-b) for a,b,c in zip(integer_q,integer_start,integer_end)]}
        for key,want in expect.items():close('6.5','signed integer oracle '+key,out[key],want,0)
        ck('6.5','inputs preserved and outputs independent',(before==[x.tobytes() for x in inputs],all(not np.shares_memory(a,b) for a in out.values() for b in inputs)),(True,True))
        fq=list(map(F,['0.5','-2.25','3']));f0=list(map(F,['3.1','4.7','9.2']));f1=list(map(F,['3.3','4.4','9.1']))
        decimals=m.position_changes(*[np.array(list(map(float,values))) for values in (fq,f0,f1)])
        for key,want in [('opening',[a*b for a,b in zip(fq,f0)]),('closing',[a*b for a,b in zip(fq,f1)]),('pnl',[a*(c-b) for a,b,c in zip(fq,f0,f1)])]:close('6.5','rational fractional oracle '+key,decimals[key],list(map(float,want)),1e-12)
        policy=np.geterr().copy()
        for label,values in [('overflow',(1e308,2.,2.)),('underflow',(1e-300,1e-300,1e-300))]:reject('6.5',label+' must reject',lambda values=values:m.position_changes(*[np.array([v]) for v in values]),'FloatingPointError')
        ck('6.5','error policy restored after signals',np.geterr(),policy)
        reject('6.5','flat quantity still rejects invalid price',lambda:m.position_changes(np.array([0.]),np.array([-1.]),np.array([1.])),'ValueError')
        m=modules[6];shocks=[F(-1,10),F(0),F(1,10)];grid=[[F(a)*b*s for a,b in zip(integer_q,integer_start)] for s in shocks]
        values=m.scenario_pnl(q,p0,np.array(list(map(float,shocks))))
        close('6.6','common shocks rational cross product',values,[[float(x) for x in row] for row in grid],1e-12)
        ck('6.6','output axes/payload',(values.shape,values.nbytes),((3,3),3*3*8))
        sq=[F(2),F(-3)];sp=[F(15,2),F(4)];ss=[F(-1,5),F(0),F(1,10),F(1,4)]
        nonsquare=m.scenario_pnl(*[np.array(list(map(float,x))) for x in (sq,sp,ss)])
        close('6.6','nonsquare scalar cross product',nonsquare,[[float(a*b*s) for a,b in zip(sq,sp)] for s in ss],1e-12)
        ck('6.6','no accidental pairing',(nonsquare.shape,((q*p0)*np.array([-.1,0.,.1])).shape),((4,2),(3,)))
        ck('6.6','exact cell boundary accepted',m.scenario_pnl(q,p0,np.array([-.1,0.,.1]),max_cells=9).size,9)
        for budget in (8,True):reject('6.6','cell budget rejects '+repr(budget),lambda budget=budget:m.scenario_pnl(q,p0,np.array([-.1,0.,.1]),max_cells=budget),'ValueError')
        reject('6.6','zero shock still rejects overflowing marks',lambda:m.scenario_pnl(np.array([1e308]),np.array([2.]),np.array([0.])),'FloatingPointError')
        ck('6.6','error policy restored',np.geterr(),policy)
        m=modules[7];rows=[[-100,40],[0,0],[100,-40],[200,-80]];table=np.array(rows,dtype=np.float64);snapshot=table.tobytes();summary=m.summarize(table)
        totals=[sum(map(F,row)) for row in rows];means=[sum(F(row[i]) for row in rows)/len(rows) for i in range(2)];mean=sum(totals)/len(totals);ssq=sum((x-mean)**2 for x in totals)
        close('6.7','exact row sums',summary['totals'],list(map(float,totals)),0);close('6.7','exact position means',summary['position_means'],list(map(float,means)),0)
        ck('6.7','scalar extrema/mean/counts',(summary['minimum'],summary['maximum'],summary['mean'],summary['scenario_count'],summary['position_count']),(-60.,120.,30.,4,2))
        ck('6.7','independent variance numerators/denominators',(ssq,ssq/4,ssq/3),(F(18000),F(4500),F(6000)))
        with localcontext() as ctx:
            ctx.prec=60;std0=Decimal(4500).sqrt();std1=Decimal(6000).sqrt()
        close('6.7','ddof0 Decimal square root',summary['std'],float(std0),1e-12);close('6.7','ddof1 Decimal square root',m.summarize(table,ddof=1)['std'],float(std1),1e-12)
        ck('6.7','single scenario descriptive dispersion',m.summarize(np.array([[1.,2.]]))['std'],0.)
        reject('6.7','single row ddof1 denominator rejected',lambda:m.summarize(np.array([[1.,2.]]),ddof=1),'ValueError')
        ck('6.7','joint cancellation example',m.summarize(np.array([[-10.,10.],[10.,-10.]]))['std'],0.)
        ck('6.7','independent arrays and preserved source',(all(not np.shares_memory(table,summary[k]) for k in ('totals','position_means')),snapshot==table.tobytes()),(True,True))
        reject('6.7','missing entry never silently excluded',lambda:m.summarize(np.array([[1.,np.nan]])),'ValueError')
        reject('6.7','squared deviation overflow',lambda:m.summarize(np.array([[1e200],[-1e200]])),'FloatingPointError');ck('6.7','error policy restored',np.geterr(),policy)
        m=modules[8];periods=np.array([0,1,3,4],dtype=np.int64);amounts=np.array([-1000.,200.,-50.,1000.]);originals=(periods.tobytes(),amounts.tobytes());schedule=m.cashflow_schedule(periods,amounts)
        cumulative=[];total=F(0)
        for value in [-1000,200,-50,1000]:total+=value;cumulative.append(float(total))
        close('6.8','rational cumulative addition',schedule['cumulative'],cumulative,0);ck('6.8','nominal net is final accumulation',schedule['nominal_net'],float(total))
        shifted=m.cashflow_schedule(np.array([0,10,30,40],dtype=np.int64),amounts)
        ck('6.8','changed offsets preserve nominal net but not timing',(shifted['nominal_net']==schedule['nominal_net'],np.array_equal(shifted['periods'],schedule['periods'])),(True,False))
        ck('6.8','inflow/outflow times aligned',(periods[amounts>0].tolist(),periods[amounts<0].tolist()),([1,4],[0,3]))
        ck('6.8','storage independence and original preservation',(all(not np.shares_memory(schedule[k],source) for k in ('periods','amounts','cumulative') for source in (periods,amounts)),originals==(periods.tobytes(),amounts.tobytes())),(True,True))
        for values in ([0,1,1,4],[0,3,1,4]):reject('6.8','duplicate or unsorted offsets '+str(values),lambda values=values:m.cashflow_schedule(np.array(values,dtype=np.int64),amounts),'ValueError')
        ck('6.8','bound amounts repeated 10000 times',m.cashflow_schedule(np.arange(10000,dtype=np.int64),np.full(10000,1e12))['nominal_net'],float(10000*10**12))
        ck('6.8','negative amount and maximum offset inclusive',m.cashflow_schedule(np.array([1000000],dtype=np.int64),np.array([-1e12]))['nominal_net'],-1e12)
        benchmarks={'signed_integer_outputs':expect,'scenario_grid':[[str(x) for x in row] for row in grid],'scenario_totals':list(map(str,totals)),'variance_sum_squares':str(ssq),'std0_decimal':str(std0),'std1_decimal':str(std1),'cumulative':cumulative,'nominal_net':str(total)}
    output=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),runtime=runtime,workflow_records=4,derived_review_units=32,source_method_invocations=sum(x['actual_methods'] or 0 for x in commands),command_records=len(commands),command_passed=sum(x['status']=='PASS' for x in commands),command_failed=sum(x['status']=='FAIL' for x in commands),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),independent_benchmarks=benchmarks,sources=sources,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks','runtime','independent_benchmarks')}))
    return bool(output['command_failed'] or output['failed'])
if __name__=='__main__':raise SystemExit(run())
