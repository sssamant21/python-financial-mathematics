"""Exact-source validation examples; independent expectations and contract probes."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.13-validation-of-numerical-results.md';source=BOOK/path
    data=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path])
    blocks=re.findall(rb'^(?:```|~~~)python\n(.*?)^(?:```|~~~)',data,re.M|re.S);code=next(b for b in blocks if b'import unittest' in b);commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,ValueError),exception=repr(e),expected_exception='ValueError')
        else:ck(label,False,actual=repr(v),expected_exception='ValueError')
    with tempfile.TemporaryDirectory(prefix='book1-1713-') as tmp:
        Path(tmp,'validate_numerics.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[1])
        for label,args in [('exact eight reference tests',['validate_numerics.py']),('silent import',['-c','import validate_numerics']),('compile exact listing',['-m','compileall','-q','validate_numerics.py']),('exact SciPy root snippet',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact eight reference tests':ok=ok and methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label in ['silent import','compile exact listing']:ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        import contextlib,io
        ns={};capture=io.StringIO()
        with contextlib.redirect_stdout(capture):exec(compile(blocks[1],'exact_scipy_snippet','exec'),ns)
        num('SciPy independently derived yield',lambda:ns['result'].root,F(1,10),atol=1e-12,rtol=0)
        num('SciPy independent repricing',lambda:float(F(110)/(1+F(str(ns['result'].root)))-100),0,atol=1e-10,rtol=0)
    m=types.ModuleType('validation_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    for label,fn,want in [
      ('E3 one-year PV',lambda:m.npv([0,110],.1),100),
      ('E4 NPV zero',lambda:m.npv([-100,110],.1),0),
      ('E5 zero-rate PV',lambda:m.npv([0,100],0),100),
      ('E14 price residual',lambda:m.price_residual(100,[0,100.03],0),F(3,100)),
      ('E17 separate-price residual',lambda:m.price_residual(100,[0,110],.1),0),
      ('E25 equal-weight variance',lambda:m.two_asset_variance(.5,.5,.04,.09,0),F(13,400)),
      ('E35 NPV at11 percent',lambda:m.npv([-100,110],.11),F(-100,111)),
      ('F170 integer NPV cancellation',lambda:m.npv([-10**18,10**18+1],0),1),
      ('F170 tiny NPV rate',lambda:m.npv([-1,1],1e-308),F(-1,10**308)),
      ('F170 discounted cashflow remains reportable',lambda:m.npv([0,0,1e308],1e308),F(1,10**308)),
      ('F170 whole price residual before report',lambda:m.price_residual(1e308,[1e308,1],0),1),
      ('F170 rank-one signed variance cancellation',lambda:m.two_asset_variance(1e308,-1e308,1e308,1e308,1e308),0),
      ('variance does not assert budget feasibility',lambda:m.two_asset_variance(.4,.4,.04,.09,0),F(13,625)),
    ]:num(label,fn,want,atol=1e-12 if want==0 and label.startswith('E') else 0)
    ck('E9 specified mixed tolerance fails',m.close_to_reference(100.02,100,.01,.00005) is False,independent_threshold='3/200=.015',independent_error='1/50=.02')
    ck('F170 exact displayed mixed-tolerance boundary',m.close_to_reference(100.015,100,.01,.00005) is True,independent_error='3/200',independent_threshold='3/200')
    ck('F170 overflowed difference cannot pass overflowed threshold',m.close_to_reference(1.79e308,-1.79e308,1.79e308,.1) is False,independent_error='3.58e308',independent_threshold='1.969e308')
    ck('F170 integer versus float reference retains unit gap',m.close_to_reference(10**18+1,1e18,0,0) is False,independent_error='1')
    ck('mixed tolerance exact equality',m.close_to_reference(100,100,0,0) is True)
    for rate in [0,.05,-.5,1e-308]:
        expected=-F(100)+F(110)/(1+F(str(rate)))
        num('independent analytic NPV '+str(rate),lambda rate=rate:m.npv([-100,110],rate),expected,atol=1e-12 if expected==0 else 0)
        num('E7 doubling cashflows '+str(rate),lambda rate=rate:m.npv([-200,220],rate),2*expected,atol=1e-12 if expected==0 else 0)
    num('E8 appended zero preserves existing timing',lambda:m.npv([0,110,0],.1),100)
    num('inserted period changes payment time',lambda:m.npv([0,0,110],.1),F(1000,11))
    ck('E6 positive-flow PV decreases with valid rate',m.npv([0,110],.11)<m.npv([0,110],.1))
    ck('E30 negative-flow reverses monotonicity',m.npv([0,-110],.11)>m.npv([0,-110],.1))
    num('currency units scaled consistently',lambda:m.npv([0,11000],.1),10000)
    num('E13 rate increase in basis points supplemental',lambda:(F(11,100)-F(1,10))*10000,100)
    num('E24 budget residual supplemental',lambda:F('1.001')-1,F(1,1000))
    for label,fn in [
      ('nonfinite comparator NaN',lambda:m.close_to_reference(float('nan'),0,1,0)),
      ('nonfinite comparator infinity',lambda:m.close_to_reference(float('inf'),0,1,0)),
      ('negative tolerance',lambda:m.close_to_reference(1,1,-1,0)),
      ('huge integer comparator',lambda:m.close_to_reference(10**1000,0,0,0)),
      ('bad rate',lambda:m.npv([1],-1)),
      ('empty NPV',lambda:m.npv([],.1)),
      ('malformed NPV iterable',lambda:m.npv(None,.1)),
      ('nonfinite flow',lambda:m.npv([float('nan')],.1)),
      ('ordinary invalid covariance',lambda:m.two_asset_variance(.5,.5,.04,.09,.1)),
      ('PSD boundary not relaxed by rounded square roots',lambda:m.two_asset_variance(1,0,.04,.04,.04000000000000001)),
      ('nonzero variance underflow',lambda:m.two_asset_variance(.5,.5,5e-324,0,0)),
      ('boolean weight',lambda:m.two_asset_variance(True,0,.04,.09,0)),
    ]:reject('F170 '+label,fn)
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,process_control_records=10,historical_unique_methods_added=0,model=dict(price=100,future_cashflows=[0,110],npv_cashflows=[-100,110],rates=[.1,.11],units='fictional common currency, annual-effective decimal rate, integer periods;1bp=.0001',timing='initial flow at t0, future at t1; price is separate from future_cashflows, no market dates',variance=dict(weights=[.5,.5],variances=[.04,.09],covariance=0)),criteria=dict(known_zero_currency_atol=1e-12,scipy_root_atol=1e-12,scipy_repricing_currency_atol=1e-10,other_numeric_rtol=1e-12),scipy_secondary_stdout=capture.getvalue())
    def safe(x):
        if isinstance(x,F):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
