"""Exact-source convergence lab; independent error and refinement expectations."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.12-convergence-and-error.md';source=BOOK/path
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
    with tempfile.TemporaryDirectory(prefix='book1-1712-') as tmp:
        Path(tmp,'convergence_error.py').write_bytes(code)
        tasks=[('exact eight reference methods',['convergence_error.py']),('silent import',['-c','import convergence_error']),('compile exact listing',['-m','compileall','-q','convergence_error.py'])]
        for i,label in enumerate(['exact SciPy root snippet','exact SciPy quadrature snippet']):
            filename='example_'+str(i)+'.py';Path(tmp,filename).write_bytes(blocks[i]);tasks.append((label,[filename]))
        for label,args in tasks:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact eight reference methods':ok=ok and methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label in ['silent import','compile exact listing']:ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        import contextlib,io
        ns={};capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            for i in range(2):exec(compile(blocks[i],'exact_scipy_'+str(i),'exec'),ns)
        num('SciPy independently checked yield',lambda:ns['result'].root,F(1,10),atol=1e-12,rtol=0)
        num('SciPy independently repriced residual',lambda:float(F(110)/(1+F(str(ns['result'].root)))-100),0,atol=1e-10,rtol=0)
        with localcontext() as ctx:
            ctx.prec=1000;pv=D(2000)*(1-D('-.1').exp());sqrt2=D(2).sqrt()
            high_order=D('1e308')/(D(2)**2000-1);tiny_order=D('1e-308')/((D('1e-308')*D(2).ln()).exp()-1)
        num('SciPy quadrature independent Decimal PV',lambda:ns['value'],pv)
    m=types.ModuleType('convergence_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    num('E1 supplemental absolute price error',lambda:abs(F('100.02')-100),F(1,50))
    num('E2 supplemental relative price error',lambda:abs(F('100.02')-100)/100,F(1,5000))
    num('E4 ten-halving bracket width',lambda:F(1,2**10),F(1,1024))
    num('E5 midpoint bound basis points',lambda:F(1,2**11)*10000,F(625,128))
    num('E7 flat-function residual',lambda:(F('1.01')-1)**3,F(1,10**6))
    num('E8 flat-function root error',lambda:F('1.01')-1,F(1,100))
    yield_records=[]
    f=lambda y:110/(1+y)-100
    for t in [1e-6,1e-9,1e-12]:
        r=m.bisect(f,0,.2,width_tol=t);x,a,b,n,res=r;yield_records.append(dict(width_tol=t,result=r,actual_float_radius=max(x-a,b-x),radius_basis_points=max(x-a,b-x)*10000))
        num('lab yield absolute error '+str(t),lambda x=x:x,F(1,10),atol=t,rtol=0)
        ck('lab reported bracket width '+str(t),F.from_float(b)-F.from_float(a)<=F(str(t)),result=r)
    ck('lab refinement halvings nondecreasing',all(a['result'][3]<=b['result'][3] for a,b in zip(yield_records,yield_records[1:])))
    num('E9 E10 price residual at yield zero',lambda:f(0),10)
    num('one-period residual at .2',lambda:f(.2),F(-25,3))
    integrals=[]
    for n in [2,4,8]:
        v=m.trapezoid(lambda x:x*x,0,1,n);integrals.append(v);num('lab finite trapezoid '+str(n),lambda v=v:v,F(1,3)+F(1,6*n*n))
    num('E13 actual refinement ratio',lambda:(F(str(integrals[0]))-F(1,3))/(F(str(integrals[1]))-F(1,3)),4)
    num('E14 fine error estimate',lambda:m.fine_error_estimate(integrals[0],integrals[1],2),F(1,96))
    derivatives=[]
    for h in [.01,.001,.0001]:
        value=m.central_difference(f,.1,h);derivatives.append(dict(h=h,value=value))
        num('lab finite central-difference expectation '+str(h),lambda value=value:value,-F(110)/(F(121,100)-F(str(h))**2),rtol=1e-8)
    num('E25 materiality supplemental',lambda:F(1,100)*10**6,10000)
    num('E35 yield sensitivity supplemental',lambda:F(1,100)/100,F(1,10000))
    num('E36 additive error budget supplemental',lambda:F(1,100)+F(2,100),F(3,100))
    num('F169 wide bisection midpoint',lambda:m.bisect(lambda x:x/1e308,-1e308,1e308)[0],0)
    num('F169 wide trapezoid',lambda:m.trapezoid(lambda x:1e-308,-1e308,1e308,2),2)
    num('F169 large weighted trapezoid',lambda:m.trapezoid(lambda x:1e308,0,1,10),1e308)
    num('F169 estimate avoids difference overflow',lambda:m.fine_error_estimate(-1e308,1e308,2),F(2*10**308,3))
    num('F169 tiny order denominator retained',lambda:m.fine_error_estimate(0,1e-308,1e-308),tiny_order)
    num('F169 high-order finite estimate retained',lambda:m.fine_error_estimate(0,1e308,2000),high_order)
    num('F169 derivative numerator finite after division',lambda:m.central_difference(lambda x:1e308*x,0,1),1e308)
    for label,fn,kind in [
      ('boolean bisection callback',lambda:m.bisect(lambda x:False,0,1),ValueError),
      ('noncallable bisection',lambda:m.bisect(None,0,1),ValueError),
      ('huge endpoint',lambda:m.bisect(lambda x:x,10**1000,10**1000+1),ValueError),
      ('bad bracket',lambda:m.bisect(lambda x:x*x+1,-1,1),ValueError),
      ('iteration failure',lambda:m.bisect(lambda x:x*x-2,0,2,max_iter=0),RuntimeError),
      ('bisection stagnation',lambda:m.bisect(lambda x:-1 if x<=1 else 1,1,math.nextafter(1,2),width_tol=1e-30),RuntimeError),
      ('trapezoid repeated nodes',lambda:m.trapezoid(lambda x:x,1,math.nextafter(1,2),2),ValueError),
      ('trapezoid boolean callback',lambda:m.trapezoid(lambda x:False,0,1,2),ValueError),
      ('derivative repeated coordinates',lambda:m.central_difference(lambda x:x*x,1,1e-30),ValueError),
      ('derivative nonfinite callback',lambda:m.central_difference(lambda x:float('inf'),1,.1),ValueError),
      ('derivative boolean coordinate',lambda:m.central_difference(lambda x:x,True,.1),ValueError),
      ('boolean convergence order',lambda:m.fine_error_estimate(1,2,True),ValueError),
    ]:reject('F169 '+label,fn,kind)
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,lab_results=dict(yields=yield_records,trapezoids=integrals,derivatives=derivatives),model=dict(one_period_price=100,next_period_cashflow=110,periodic_yield=.1,units='fictional currency, decimal periodic yield;1bp=.0001; integration/differentiation fixtures dimensionless unless price/yield',timing='t0 price,t1 payment; separate continuous cashflow SciPy example, no market dates'),scipy_secondary_stdout=capture.getvalue())
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
