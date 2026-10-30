"""Exact corrected reference suite, observed locals, independent scalar oracles."""
import ast,hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
PROBLEMS=BOOK/'chapter-06/6.17-exercises-and-applied-problems.md'
SOURCE=BOOK/'chapter-06/6.17-solutions-and-reference-implementations.md'
def sha(raw):return hashlib.sha256(raw).hexdigest()

def run():
    code=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S)[0]
    operations=[];checks=[]
    def ck(problem,label,actual,expected):checks.append(dict(problem=problem,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
    def close(problem,label,actual,expected,atol=1e-12):
        a=np.asarray(actual);e=np.asarray(expected,dtype=np.float64)
        ok=a.shape==e.shape and bool(np.isfinite(a).all()) and bool(np.all(np.abs(a-e)<=atol))
        ck(problem,label,ok,True)
        checks[-1].update(observed_values=a.tolist(),expected_values=e.tolist(),rtol=0,atol=atol)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='chapter6-answers-') as tmp:
        root=Path(tmp);lab=root/'numpy_lab_617';lab.mkdir();path=lab/'chapter06_solutions.py';path.write_text(code)
        def command(label,args,expected_count=None):
            r=subprocess.run([sys.executable,'-B',*map(str,args)],cwd=root,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0
            if expected_count is not None:ok=ok and actual==expected_count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
            operations.append(dict(label=label,args=list(map(str,args)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
            return r
        command('exact corrected source explicit discovery',['-W','error::FutureWarning','-m','unittest','discover','-s','numpy_lab_617','-p','chapter06_solutions.py','-v'],20)
        compile(code,str(path),'exec');ck('ALL','exact listing compiles',True,True)
        observed=command('same source twenty-method observer rerun',[HERE/'observe_reference.py',path])
        observations=json.loads(observed.stdout);ck('ALL','observer successful/method count',(observations['successful'],observations['tests_run']),(True,20))
        (HERE/'observed-locals.json').write_text(json.dumps(observations,indent=2,allow_nan=False)+'\n')
        local=observations['locals']
        def vals(n,name):return local[f'test_problem_{n:02d}'][name]['values']
        a=local['test_problem_01']['a'];ck(1,'shape/dtype/dimension',(a['shape'],a['dtype'],len(a['shape'])),([3],'float64',1));ck(1,'exact array values',a['values'],[100.,102.,99.])
        ck(2,'integer truncation observed',vals(2,'a'),[1,2]);ck(2,'floating alternative observed',vals(2,'b'),[1.75,2.])
        ck(3,'source slice modifies source',vals(3,'a'),[100.,0.,102.]);ck(3,'copied slice later edit stays separate',vals(3,'c'),[9.,102.])
        fresh=np.array([100.,101.,102.]);copied=fresh[1:].copy();copied[0]=0
        ck(3,'fresh repeat copy preserves source',fresh.tolist(),[100.,101.,102.]);ck(3,'fresh copied result',copied.tolist(),[0.,102.])
        q=[F(10),F(-5),F(0)];p0=[F(100),F(80),F(50)];p1=[F(105),F(76),F(52)]
        pnl=[x*(z-y) for x,y,z in zip(q,p0,p1)];ck(4,'independent exact signed P&L',pnl,[F(50),F(20),F(0)])
        close(4,'observed fixture scalar P&L',np.array(vals(4,'q'))*(np.array(vals(4,'p1'))-vals(4,'p0')),[float(x) for x in pnl],0)
        returns=[[F(110,100)-1,F(95,100)-1],[F(80,100)-1,F(105,100)-1]]
        close(5,'source return matrix vs rational ratios',vals(5,'r'),[[float(x) for x in row] for row in returns])
        rowmeans=[sum(row)/2 for row in returns];colmeans=[sum(row[j] for row in returns)/2 for j in range(2)]
        ck(6,'exact row/column means',(rowmeans,colmeans),([F(1,40),F(-3,40)],[F(-1,20),F(0)]))
        close(6,'observed means axis1',np.mean(vals(6,'r'),axis=1),list(map(float,rowmeans)));close(6,'observed means axis0',np.mean(vals(6,'r'),axis=0),list(map(float,colmeans)))
        pv=sum(c/F(21,20)**t for c,t in zip([100,100,1100],[1,2,3]));close(7,'observed PV vs exact rational discount',local['test_problem_07']['pv'],float(pv),1e-10)
        close(7,'companion printed PV',float(pv),1136.162401469,1e-9)
        price=[F(100),F(110),F(99)];interval=[price[i+1]/price[i]-1 for i in range(2)];cumulative=price[-1]/price[0]-1
        ck(8,'rational interval and linked result',(interval,cumulative),([F(1,10),F(-1,10)],F(-1,100)));close(8,'observed interval returns',vals(8,'r'),list(map(float,interval)))
        w=[F(600,1000),F(300,1000),F(100,1000)];r=[F(1,10),F(-1,20),F(0)];portfolio=sum(x*y for x,y in zip(w,r))
        ck(9,'rational opening weighted return',portfolio,F(9,200));close(9,'source opening weights',vals(9,'w'),list(map(float,w)))
        rr=[r,[F(-1,5),F(1,20),F(0)]];ww=[w,[F(0),F(1),F(0)]]
        matrix=[[sum(x*y for x,y in zip(scenario,weights)) for weights in ww] for scenario in rr]
        close(10,'observed matrix product vs scalar rational',np.array(vals(10,'r'))@np.array(vals(10,'w')).T,[[float(x) for x in row] for row in matrix])
        det=F(2)*3-1;solution=[(F(5)*3-5)/det,(F(2)*5-5)/det]
        ck(11,'exact two-equation elimination solution',solution,[F(2),F(1)]);close(11,'observed linear solver result',vals(11,'x'),list(map(float,solution)))
        ck(12,'singular determinant and consistent RHS',(F(1)*4-F(2)*2,F(6)-2*3),(F(0),F(0)))
        close(13,'fresh same-protocol draws equal',vals(13,'x'),vals(13,'y'),0)
        ck(13,'random arrays shape',local['test_problem_13']['x']['shape'],[5])
        with localcontext() as ctx:
            ctx.prec=80;exact_tiny=(Decimal(1)+Decimal('1e-17'))**3-1
        small=np.full(3,1e-17);naive=float(np.prod(1+small)-1);stable=float(np.expm1(np.log1p(small).sum()))
        ck(14,'float64 additions lose tiny terms',naive,0.0);close(14,'stable vs high precision Decimal product',stable,float(exact_tiny),1e-31)
        a15=np.array(vals(15,'a'));b15=np.array(vals(15,'b'));ck(15,'broadcast accepts mismatched shapes',(a15.shape!=b15.shape,bool(np.allclose(a15,b15))),(True,True))
        ck(16,'nonfinite fixture classification',np.isfinite(np.array([1.,np.nan,np.inf])).tolist(),[True,False,False])
        ck(17,'scalar payload formula',1000*20*8,160000);ck(17,'source array payload',local['test_problem_17']['a']['nbytes'],160000)
        m=types.ModuleType('source_chapter06_solutions');exec(compile(code,str(path),'exec'),m.__dict__)
        ck(18,'corrected top-level function definitions',{n.name for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)},{'python_pnl','numpy_pnl'})
        for name in ['python_pnl','numpy_pnl']:
            result=getattr(m,name)(list(map(float,q)),list(map(float,p0)),list(map(float,p1)))
            ck(18,name+' exact oracle/list return',(result,type(result).__name__),([50.,20.,0.],'list'))
            try:getattr(m,name)([1.],[1.,2.],[2.]);error='no exception'
            except Exception as e:error=type(e).__name__
            ck(18,name+' unequal lengths',error,'ValueError')
        quantities=[6,3,1];opening=1000;closes=[[110,95,100],[80,105,100],[100,100,100]]
        ending=[sum(F(n)*p for n,p in zip(quantities,row)) for row in closes];gains=[end-opening for end in ending]
        ck(19,'rational direct valuation/P&L',(ending,gains),([F(1045),F(895),F(1000)],[F(45),F(-105),F(0)]));close(19,'observed ending values',vals(19,'ends'),list(map(float,ending)),0)
        close(19,'observed weighted/direct reconciliation',vals(19,'r'),[float(x/opening) for x in gains])
        order=[2,0,1];both=sum(r[i]*w[i] for i in order);wrong=sum(x*y for x,y in zip(r,w[::-1]))
        ck(20,'joint permutation retains return',both,portfolio);ck(20,'weights-only reversal changes return',wrong,F(-1,200))
        close(20,'observed mismatched weights',np.array(vals(20,'r'))@np.array(vals(20,'w'))[::-1],float(wrong))
        benchmarks=dict(pv_exact=str(pv),pv_decimal=float(pv),interval_returns=list(map(str,interval)),opening_weights=list(map(str,w)),portfolio_return=str(portfolio),matrix=[[str(x) for x in row] for row in matrix],tiny_product_decimal=str(exact_tiny),ending_values=list(map(str,ending)),pnl=list(map(str,gains)),wrong_weight_return=str(wrong))
    out=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),sources={str(p.relative_to(BOOK)):sha(p.read_bytes()) for p in [PROBLEMS,SOURCE]},code_sha256=sha(code.encode()),exercise_records=20,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),direct_source_methods=20,observer_source_methods=observations['tests_run'],predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks,independent_benchmarks=benchmarks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','independent_benchmarks')}))
    return bool(out['failed'] or out['command_failed'])
if __name__=='__main__':raise SystemExit(run())
