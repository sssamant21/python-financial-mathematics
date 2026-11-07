"""Efficient-grid lab and independent rational Pareto/optimization benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.12-efficient-portfolio-concepts.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.12-efficient-portfolio-concepts.md'])
    blocks=re.findall(rb'^```python\n(.*?)^```',source_bytes,re.M|re.S)
    code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def close(label,value,want):
        ck(label,math.isclose(value,float(want),rel_tol=1e-12,abs_tol=0),actual=float(value) if math.isfinite(value) else repr(value),independent_reference=str(want),relative_tolerance=1e-12,absolute_tolerance=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:
            if value is None:ck(label,False,actual='None',independent_reference=str(want))
            else:close(label,value,want)
    def reject(label,fn):
        try:v=fn()
        except ValueError as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(v))
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80;return (D(v.numerator)/D(v.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1612-') as tmp:
        Path(tmp,'efficient_portfolio_concepts.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['efficient_portfolio_concepts.py']),('isolated import',['-c','import efficient_portfolio_concepts']),('exact compilation',['-m','compileall','-q','efficient_portfolio_concepts.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['efficient_portfolio_concepts.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    means=[.08,.04];cov=[[.04,0],[0,.09]]
    base=m.evaluate([.5,.5],means,cov)
    for field,want in [('expected_return',F(3,50)),('variance',F(13,400)),('volatility',root(F(13,400)))]:close('E1-E3 '+field,base[field],want)
    for n,steps,count in [(2,10,11),(3,4,15),(2,20,21)]:
      weights=list(m.simplex_grid(n,steps));ck('E4/E5/E23 grid count '+str((n,steps)),len(weights)==count)
      ck('grid nonnegative unit budgets '+str((n,steps)),all(len(w)==n and min(w)>=0 and math.isclose(sum(w),1,abs_tol=1e-12) for w in weights))
    def record(mu,var):return dict(expected_return=mu,variance=var)
    for label,a,b,want in [
      ('E7 strict dominance',record(.08,.02),record(.06,.03),True),
      ('E8 genuine tradeoff',record(.08,.04),record(.06,.02),False),
      ('E9 equal risk higher mean',record(.08,.02),record(.06,.02),True),
      ('E10 equal mean lower risk',record(.06,.02),record(.06,.03),True),
      ('identical points nondominating',record(.06,.02),record(.06,.02),False),
      ('F153 tiny tradeoff not tolerance-dominated',record(2e-12,5e-13),record(0,0),False),
      ('F153 small improvement not erased',record(1e-15,0),record(0,0),True),
    ]:
      try:value=m.dominates(a,b)
      except Exception as e:ck(label,False,exception=repr(e))
      else:ck(label,value is want,actual=value,expected=want)
    grid=m.candidates(means,cov,20);gmv=m.min_variance_portfolio(grid);efficient=m.efficient_subset(grid);target=m.min_variance_for_target(grid,.07)
    for i,point in enumerate(grid):
      w=F(i,20);mu=F(1,25)+F(1,25)*w;var=F(1,25)*w*w+F(9,100)*(1-w)**2
      ck('lab full candidate '+str(i),math.isclose(point['expected_return'],float(mu),rel_tol=1e-12,abs_tol=0) and math.isclose(point['variance'],float(var),rel_tol=1e-12,abs_tol=0),mean_reference=str(mu),variance_reference=str(var),actual_mean=point['expected_return'],actual_variance=point['variance'])
    close('lab grid GMV weight',gmv['weights'][0],F(7,10));close('lab grid GMV variance',gmv['variance'],F(277,10000))
    close('E11 supplemental analytical GMV weight',F(9,100)/(F(1,25)+F(9,100)),F(9,13))
    close('E12/E13 supplemental analytical minimum variance',F(1,25)*F(9,100)/(F(1,25)+F(9,100)),F(9,325))
    close('lab grid variance approximation gap',gmv['variance']-float(F(9,325)),F(1,130000))
    ck('lab efficient weights exact grid oracle',[round(p['weights'][0],12) for p in efficient]==[.7,.75,.8,.85,.9,.95,1.0],actual=[p['weights'] for p in efficient])
    close('E14 target weight',target['weights'][0],F(3,4));close('lab target return',target['expected_return'],F(7,100));close('lab target variance',target['variance'],F(9,320))
    thirteen=m.min_variance_portfolio(m.candidates(means,cov,13));close('lab grid containing continuous optimizer',thirteen['weights'][0],F(9,13))
    num('E16 Sharpe',lambda:m.sharpe_ratio(.08,.2,.02),F(3,10))
    close('E17 supplemental excess return',F(2,25)-F(1,50),F(3,50))
    close('E22 supplemental gross exposure',abs(F(6,5))+abs(F(-1,5)),F(7,5))
    sharpes=[m.sharpe_ratio(p['expected_return'],p['volatility'],.02) for p in grid];best=grid[max(range(len(grid)),key=sharpes.__getitem__)]
    oracle=[]
    for i in range(21):
      w=F(i,20);er=F(1,25)+F(1,25)*w;var=F(1,25)*w*w+F(9,100)*(1-w)**2
      oracle.append((er-F(1,50))**2/var)
    ck('lab all Sharpe values independent oracle',all(math.isclose(sharpes[i],float(root(oracle[i])),rel_tol=1e-12,abs_tol=0) for i in range(21)))
    ck('explicit approximate dominance is opt-in',m.dominates(record(2e-12,5e-13),record(0,0),1e-12))
    ck('lab max-Sharpe grid independent squared-ratio oracle',max(range(21),key=oracle.__getitem__)==17 and best['weights'][0]==.85,actual=best['weights'])
    stresses=[]
    for rho,cross,expected_w,expected_var in [(.5,F(3,100),F(17,20),F(1543,40000)),(1,F(3,50),1,F(1,25))]:
      sc=[[.04,float(cross)],[float(cross),.09]];points=m.candidates(means,sc,20);p=m.min_variance_portfolio(points)
      close('lab stressed grid weight '+str(rho),p['weights'][0],expected_w);close('lab stressed grid variance '+str(rho),p['variance'],expected_var)
      stresses.append(dict(rho=rho,covariance=sc,grid_gmv=p,efficient_weights=[x['weights'] for x in m.efficient_subset(points)]))
    tiny=[record(.07-5e-13,.01),record(.07,.02)]
    num('explicit target slack is opt-in',lambda:m.min_variance_for_target(tiny,.07,1e-12)['variance'],F(1,100))
    num('F153 exact target requirement not relaxed by default',lambda:m.min_variance_for_target(tiny,.07)['variance'],F(1,50))
    for label,fn,want in [
      ('F153 normalized budget expected return',lambda:m.evaluate([1.00000000005],[1],[[1]])['expected_return'],1),
      ('F153 normalized budget variance',lambda:m.evaluate([1.00000000005],[1],[[1]])['variance'],1),
      ('F153 expected integer offset retained',lambda:m.evaluate([.5,.5],[10**18+2,-10**18],[[0,0],[0,0]])['expected_return'],1),
      ('F153 Sharpe integer offset retained',lambda:m.sharpe_ratio(10**18+1,1,10**18),1),
      ('F153 finite Sharpe before excess overflow',lambda:m.sharpe_ratio(1e308,1e308,-1e308),2),
    ]:num(label,fn,want)
    for label,fn in [
      ('PSD extension invalid global covariance rejected',lambda:m.evaluate([1,0],[0,0],[[1,2],[2,1]])),
      ('F153 negative tiny variance not clipped',lambda:m.evaluate([1],[0],[[-1e-300]])),
      ('F153 invalid dominance tolerance rejected',lambda:m.dominates(record(.1,.1),record(.1,.1),-1)),
      ('F153 invalid target tolerance rejected',lambda:m.min_variance_for_target(grid,.07,math.nan)),
      ('F153 invalid candidate negative risk rejected',lambda:m.min_variance_portfolio([record(.1,-1)])),
      ('F153 malformed evaluation ValueError',lambda:m.evaluate(None,None,None)),
      ('F153 unreportable variance rejected',lambda:m.evaluate([.1,.9],[0,0],[[1e-323,0],[0,0]])),
      ('F153 unreportable Sharpe overflow rejected',lambda:m.sharpe_ratio(1e308,1e-308,0)),
      ('F153 unreportable Sharpe underflow rejected',lambda:m.sharpe_ratio(1e-308,1e308,0)),
      ('F153 huge integer parameter ValueError',lambda:m.sharpe_ratio(10**1000,1,0)),
      ('E15 infeasible target rejected',lambda:m.min_variance_for_target(grid,.1)),
      ('E18 zero-volatility Sharpe undefined',lambda:m.sharpe_ratio(.08,0,.02)),
      ('E21 short weights rejected',lambda:m.evaluate([1.2,-.2],means,cov)),
    ]:reject(label,fn)
    report=dict(assets=['fictional A','fictional B'],means=means,covariance=cov,steps=20,grid=grid,grid_gmv=gmv,analytical_gmv_weight='9/13',analytical_min_variance='9/325',grid_variance_gap='1/130000',efficient_weights=[p['weights'] for p in efficient],target=.07,target_result=target,risk_free=.02,grid_sharpes=sharpes,max_sharpe_grid=best,stress_models=stresses,
      units='decimal one-period simple-return forecasts and squared covariance',horizon='one shared synthetic period',currency='fictional common USD',dates=None,scope='reported discrete candidate metrics only, no continuous/empirical acceptance',fixture_sha256=hashlib.sha256(json.dumps([means,cov,20,.07,.02]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
