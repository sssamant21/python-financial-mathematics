"""Exact-source optimization runs and separate rational/Decimal expectations."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.05-optimization-fundamentals.md';source=BOOK/path
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
    with tempfile.TemporaryDirectory(prefix='book1-1705-') as tmp:
        Path(tmp,'optimization_fundamentals.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[0])
        for label,args in [('exact demonstration and twelve tests',['optimization_fundamentals.py']),('silent import',['-c','import optimization_fundamentals']),('compile exact listing',['-m','compileall','-q','optimization_fundamentals.py']),('exact SciPy snippet',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            ok=p.returncode==0
            if label=='exact demonstration and twelve tests':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label!='exact SciPy snippet':ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        # Run unchanged snippet in a separate namespace to inspect its outputs; the
        # original snippet only asserted vector budget, not the analytic optimum.
        scipy_ns={};exec(compile(blocks[0],'exact_scipy_snippet','exec'),scipy_ns)
        v=scipy_ns['vector'];scalar=scipy_ns['scalar']
        num('SciPy scalar analytic optimum',lambda:scalar.x,F(3,10),atol=1e-8,rtol=0)
        num('SciPy vector analytic weight A',lambda:v.x[0],F(2,3),atol=1e-6,rtol=0)
        num('SciPy vector analytic weight B',lambda:v.x[1],F(1,3),atol=1e-6,rtol=0)
        num('SciPy vector independently repriced objective',lambda:F(str(v.x[0]))**2+2*F(str(v.x[1]))**2,F(2,3),atol=1e-10,rtol=0)
        ck('SciPy vector independent feasibility',all(0<=x<=1 for x in v.x) and abs(sum(v.x)-1)<1e-7,actual=v.x.tolist())
    m=types.ModuleType('optimization_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    lab=[]
    for steps in [10,100,1000]:
        r=m.grid_minimize(lambda x:(x-.3)**2,0,1,steps);lab.append(dict(method='grid',steps=steps,result=r));num('lab grid optimum '+str(steps),lambda r=r:r['x'],F(3,10),atol=1e-15,rtol=0)
    r=m.golden_minimize(lambda x:(x-.3)**2,0,1);lab.append(dict(method='golden',result=r));num('lab golden optimum',lambda:r['x'],F(3,10),atol=1e-10,rtol=0)
    num('E1 known minimum',lambda:m.golden_minimize(lambda x:(x-3)**2,0,5)['x'],3,atol=1e-10,rtol=0)
    num('E2 maximization via negative objective',lambda:m.golden_minimize(lambda x:x*x-4*x,0,4)['x'],2,atol=2e-8,rtol=0)
    num('E7 constrained grid endpoint',lambda:m.grid_minimize(lambda x:(x-.3)**2,.5,1,10)['x'],F(1,2))
    num('E7 constrained golden endpoint',lambda:m.golden_minimize(lambda x:(x-.3)**2,.5,1)['x'],F(1,2),atol=1e-10,rtol=0)
    num('E8 grid spacing',lambda:m.grid_minimize(lambda x:x,0,1,10)['spacing'],F(1,10))
    num('E9 discrete optimum .34 on coarse grid',lambda:m.grid_minimize(lambda x:(x-.34)**2,0,1,10)['x'],F(3,10),atol=1e-15,rtol=0)
    num('E10 refined grid .34',lambda:m.grid_minimize(lambda x:(x-.34)**2,0,1,100)['x'],F(17,50),atol=1e-15,rtol=0)
    num('E22 GMV A',lambda:m.two_asset_min_variance(.04,.09,0)['weight_a'],F(9,13))
    num('E23 supplemental expected return',lambda:F(9,13)*F(8,100)+F(4,13)*F(4,100),F(22,325))
    num('lab equal-weight risk',lambda:m.portfolio_variance([.5,.5],[[.04,0],[0,.09]]),F(13,400))
    num('E24 analytic GMV risk',lambda:m.portfolio_variance([9/13,4/13],[[.04,0],[0,.09]]),F(9,325))
    num('cap .4 boundary risk',lambda:m.portfolio_variance([.4,.6],[[.04,0],[0,.09]]),F(97,2500))
    r=m.grid_minimize(lambda x:m.portfolio_variance([x,1-x],[[.04,0],[0,.09]]),0,1,1000);lab.append(dict(method='portfolio_grid',result=r))
    num('lab finite-grid GMV weight',lambda:r['x'],F(173,250))
    num('lab finite-grid GMV value',lambda:r['value'],F(4,100)*F(173,250)**2+F(9,100)*F(77,250)**2)
    for scale in [1e-200,1e200]:num('F162 scaled covariance GMV '+str(scale),lambda scale=scale:m.two_asset_min_variance(4*scale,9*scale,0)['weight_a'],F(9,13))
    num('F162 tiny reportable variance',lambda:m.portfolio_variance([.5,.5],[[4e-200,0],[0,9e-200]]),F(13,4*10**200))
    num('F162 normalized tolerated budget',lambda:m.portfolio_variance([.5,.50000000001],[[1e200,0],[0,1e200]]),10**200*(F(5,10)**2+F(50000000001,10**11)**2)/(F(5,10)+F(50000000001,10**11))**2)
    num('F162 wide grid coordinate',lambda:m.grid_minimize(lambda x:abs(x),-1e308,1e308,2)['x'],0)
    num('F162 wide golden minimizer',lambda:m.golden_minimize(lambda x:abs(x/1e308),-1e308,1e308,tol=1e295,max_iter=200)['x'],0,atol=1e295,rtol=0)
    num('F162 preserve integer objective ordering',lambda:m.grid_minimize(lambda x:10**18+int((x-1)**2),0,2,2)['x'],1)
    ck('E27 exact nonuniqueness',m.two_asset_min_variance(.04,.04,.04)['nonunique'] is True)
    for label,fn,kind in [
      ('tiny invalid PSD not hidden',lambda:m.two_asset_min_variance(1e-200,1e-200,2e-200),ValueError),
      ('large invalid PSD not hidden',lambda:m.two_asset_min_variance(1e200,1e200,2e200),ValueError),
      ('arbitrary matrix untested negative direction',lambda:m.portfolio_variance([1,0,0],[[1,0,0],[0,1,2],[0,2,1]]),ValueError),
      ('negative tiny diagonal',lambda:m.portfolio_variance([1,0],[[1,0],[0,-1e-200]]),ValueError),
      ('tiny asymmetry',lambda:m.portfolio_variance([.5,.5],[[1e-200,0],[1e-210,1e-200]]),ValueError),
      ('unreportable nonzero variance',lambda:m.portfolio_variance([.5,.5],[[5e-324,0],[0,0]]),ValueError),
      ('golden coordinate stagnation',lambda:m.golden_minimize(lambda x:x,1,math.nextafter(1,2),tol=1e-30),RuntimeError),
      ('grid repeated coordinates',lambda:m.grid_minimize(lambda x:x,1,math.nextafter(1,2),2),ValueError),
      ('huge integer bound',lambda:m.grid_minimize(lambda x:x,10**1000,10**1000+1,2),ValueError),
      ('noncallable objective',lambda:m.grid_minimize(None,0,1,2),ValueError),
      ('bad covariance shape',lambda:m.portfolio_variance([1],None),ValueError),
      ('nonfinite objective',lambda:m.grid_minimize(lambda x:float('nan'),0,1,2),ValueError),
      ('boolean objective',lambda:m.golden_minimize(lambda x:False,0,1),ValueError),
      ('bad budget',lambda:m.portfolio_variance([.4,.4],[[.04,0],[0,.09]]),ValueError),
      ('obvious non PSD',lambda:m.two_asset_min_variance(.04,.09,.1),ValueError),
      ('iteration limit',lambda:m.golden_minimize(lambda x:(x-.3)**2,0,1,1e-15,1),RuntimeError),
    ]:reject('F162 '+label,fn,kind)
    num('E26 singular PSD risk',lambda:m.portfolio_variance([.5,.5],[[.04,.06],[.06,.09]]),F(1,16))
    num('PSD zero pivot with zero coupling',lambda:m.portfolio_variance([1,0],[[0,0],[0,.09]]),0)
    num('three-asset diagonal benchmark',lambda:m.portfolio_variance([.2,.3,.5],[[.01,0,0],[0,.01,0],[0,0,.01]]),F(19,5000))
    reject('PSD zero pivot with nonzero coupling',lambda:m.portfolio_variance([0,1],[[0,.01],[.01,1]]))
    reject('strict displayed budget policy',lambda:m.portfolio_variance([.5,.50000000001],[[1,0],[0,1]],budget_tolerance=0))
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,lab_results=lab,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,model=dict(covariance=[[.04,0],[0,.09]],means=[.08,.04],units='dimensionless weights, single-period returns and squared-return variances',timing='same hypothetical period, no market observations/as-of dates'))
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
