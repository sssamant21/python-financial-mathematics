"""Exact-source portfolio lab and independent rational/Decimal expectations."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.07-portfolio-optimization.md';source=BOOK/path
    data=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path])
    blocks=re.findall(rb'^```python\n(.*?)^```',data,re.M|re.S);code=next(b for b in blocks if b'import unittest' in b);commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn,kind=ValueError):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,kind),exception=repr(e),expected_exception=kind.__name__)
        else:ck(label,False,actual=repr(v),expected_exception=kind.__name__)
    def sqrt(q):
        q=F(q)
        with localcontext() as ctx:ctx.prec=100;return (D(q.numerator)/D(q.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1707-') as tmp:
        Path(tmp,'portfolio_optimization.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[0])
        for label,args in [('exact demonstration and twelve tests',['portfolio_optimization.py']),('silent import',['-c','import portfolio_optimization']),('compile exact listing',['-m','compileall','-q','portfolio_optimization.py']),('exact SciPy SLSQP snippet',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact demonstration and twelve tests':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label!='exact SciPy SLSQP snippet':ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        ns={}
        # The unmodified snippet prints; capture that separate execution explicitly.
        import contextlib,io
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):exec(compile(blocks[0],'exact_scipy_snippet','exec'),ns)
        weights=list(map(float,ns['result'].x))
        num('SciPy analytic capped weight A',lambda:weights[0],F(2,5),atol=1e-8,rtol=0)
        num('SciPy analytic capped weight B',lambda:weights[1],F(3,5),atol=1e-8,rtol=0)
        num('SciPy independently repriced variance',lambda:F(str(weights[0]))**2/25+F(str(weights[1]))**2*F(9,100),F(97,2500),atol=1e-9,rtol=0)
        ck('SciPy independent feasibility',all(-1e-8<=x<=1+1e-8 for x in weights) and weights[0]<=.4+1e-8 and abs(sum(weights)-1)<1e-8,actual=weights,second_exact_snippet_stdout=capture.getvalue())
    m=types.ModuleType('portfolio_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    mu=(.08,.04);cov=((.04,0),(0,.09));equal=m.portfolio_stats(.5,mu,cov);free=m.gmv(mu,cov);capped=m.gmv(mu,cov,cap_a=.4);target=m.efficient_target(mu,cov,.07)
    for label,fn,want in [
      ('E2 equal expected return',lambda:equal['expected_return'],F(3,50)),
      ('E3 equal variance',lambda:equal['variance'],F(13,400)),
      ('E4 equal volatility',lambda:equal['volatility'],sqrt(F(13,400))),
      ('E5 supplemental covariance',lambda:F(1,2)*F(1,5)*F(3,10),F(3,100)),
      ('E10 free A weight',lambda:free['weights'][0],F(9,13)),
      ('E11 free B weight',lambda:free['weights'][1],F(4,13)),
      ('E12 GMV expected return',lambda:free['expected_return'],F(22,325)),
      ('E13 GMV variance',lambda:free['variance'],F(9,325)),
      ('E14 GMV volatility',lambda:free['volatility'],sqrt(F(9,325))),
      ('E15 capped A',lambda:capped['weights'][0],F(2,5)),
      ('E16 capped risk',lambda:capped['variance'],F(97,2500)),
      ('E17 capped mean',lambda:capped['expected_return'],F(7,125)),
      ('lab cap objective increase',lambda:F(str(capped['variance']))-F(9,325),F(361,32500)),
      ('E18 target A weight',lambda:target['weights'][0],F(3,4)),
      ('E19 target risk',lambda:target['variance'],F(9,320)),
      ('E23 Sharpe',lambda:m.sharpe(.08,.2,.02),F(3,10)),
      ('E27 supplemental information ratio',lambda:F(2,100)/F(4,100),F(1,2)),
      ('E28 supplemental cost fraction',lambda:F(1,5)*F(10,10000),F(2,10000)),
      ('E29 supplemental gross turnover',lambda:abs(F(6,10)-F(5,10))+abs(F(4,10)-F(5,10)),F(1,5)),
      ('F164 tiny scale GMV',lambda:m.gmv(mu,((4e-200,0),(0,9e-200)))['weights'][0],F(9,13)),
      ('F164 large Sharpe numerator finite ratio',lambda:m.sharpe(1e308,1e308,-1e308),2),
      ('F164 integer expected-return difference',lambda:m.efficient_target((10**18+1,10**18),cov,10**18+1)['weights'][0],1),
      ('F164 negative mean slope target',lambda:m.efficient_target((.04,.08),cov,.07)['weights'][0],F(1,4)),
      ('F164 equal means feasible target',lambda:m.efficient_target((.04,.04),cov,.04)['weights'][0],F(9,13)),
    ]:num(label,fn,want)
    frontier=[]
    for t,w in [(.04,F(9,13)),(.06,F(9,13)),(.07,F(3,4)),(.08,F(1))]:
        r=m.efficient_target(mu,cov,t);frontier.append(dict(target=t,result=r));num('lab frontier weight '+str(t),lambda r=r:r['weights'][0],w)
    grid=m.grid_max_sharpe(mu,cov,.02,1000)
    def squared_score(w):
        mean=F(2,25)*w+F(1,25)*(1-w);risk=F(1,25)*w*w+F(9,100)*(1-w)**2
        return (mean-F(1,50))**2/risk
    winner=max((F(i,1000) for i in range(1001)),key=squared_score)
    num('finite Sharpe grid independent rational winner',lambda:grid['weights'][0],winner)
    num('finite Sharpe grid independent score',lambda:grid['sharpe'],sqrt(squared_score(winner)))
    # Continuous tangency: Sigma^-1 excess normalized => (27/31,4/31).
    ck('grid score below continuous tangency bound',F(str(grid['sharpe']))**2<=F(17,180)+F(1,10**15),continuous_weight='27/31',continuous_squared_sharpe='17/180',finite_grid_weight=str(winner))
    unique=m.gmv(mu,((.04,.04),(.04,.04)),cap_a=.4,cap_b=.6)
    ck('F164 singleton GMV unique',unique['nonunique'] is False,result=unique)
    ck('identical-assets interval nonunique',m.gmv(mu,((.04,.04),(.04,.04)))['nonunique'] is True)
    for label,fn in [
      ('target below actual cap frontier',lambda:m.efficient_target(mu,cov,.056000000000001,cap_a=.4)),
      ('negative-slope target above cap frontier',lambda:m.efficient_target((.04,.08),cov,.064000000000001,cap_b=.6)),
      ('tiny invalid PSD',lambda:m.gmv(mu,((1e-200,2e-200),(2e-200,1e-200)))),
      ('large invalid PSD',lambda:m.gmv(mu,((1e200,2e200),(2e200,1e200)))),
      ('tiny asymmetric covariance',lambda:m.gmv(mu,((1e-200,0),(1e-210,1e-200)))),
      ('invalid shape',lambda:m.validate(None,None)),
      ('huge integer input',lambda:m.sharpe(10**1000,1,0)),
      ('nonfinite weight',lambda:m.portfolio_stats(float('nan'),mu,cov)),
      ('ordinary invalid PSD',lambda:m.gmv(mu,((.04,.1),(.1,.09)))),
      ('infeasible caps',lambda:m.gmv(mu,cov,.4,.4)),
      ('unreachable target',lambda:m.efficient_target(mu,cov,.1)),
      ('equal means unreachable target',lambda:m.efficient_target((.04,.04),cov,.05)),
      ('zero volatility Sharpe',lambda:m.sharpe(.08,0,.02)),
      ('zero volatility grid',lambda:m.grid_max_sharpe(mu,((0,0),(0,0)),.02,10)),
      ('nonzero variance cannot disappear',lambda:m.portfolio_stats(.5,mu,((5e-324,0),(0,0)))),
      ('boolean input',lambda:m.sharpe(True,1,0)),
    ]:reject('F164 '+label,fn)
    partial=m.grid_max_sharpe(mu,((0,0),(0,.09)),.02,10)
    num('finite grid with zero-risk endpoint winner',lambda:partial['weights'][0],F(9,10))
    num('finite grid with zero-risk endpoint score',lambda:partial['sharpe'],F(28,15))
    import scipy,numpy
    out=dict(python=platform.python_version(),platform=platform.platform(),numpy=numpy.__version__,scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,acceptance_control_records=12,historical_unique_methods_added=0,lab_results=dict(equal=equal,gmv=free,capped=capped,target=target,frontier=frontier,sharpe_grid=grid),model=dict(means=mu,covariance=cov,risk_free=.02,asset_order=['A','B'],units='single-period returns, squared-return covariance and dimensionless long-only weights',timing='fictional compatible horizon; no market/as-of input'))
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
