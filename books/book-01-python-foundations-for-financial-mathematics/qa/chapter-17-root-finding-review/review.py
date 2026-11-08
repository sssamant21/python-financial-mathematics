"""Exact-source root-finding runs; separate independent rational/Decimal predicates."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    relative='chapter-17/17.03-numerical-root-finding.md';source=BOOK/relative
    data=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+relative])
    blocks=re.findall(rb'^```python\n(.*?)^```',data,re.M|re.S);code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,passed,**kw):checks.append(dict(label=label,passed=bool(passed),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn,kind=ValueError):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,kind),exception=repr(e),expected_exception=kind.__name__)
        else:ck(label,False,actual=repr(v),expected_exception=kind.__name__)
    with tempfile.TemporaryDirectory(prefix='book1-1703-') as tmp:
        Path(tmp,'numerical_root_finding.py').write_bytes(code)
        for label,args in [('exact demonstration and twelve tests',['numerical_root_finding.py']),('silent isolated import',['-c','import numerical_root_finding']),('exact compilation',['-m','compileall','-q','numerical_root_finding.py']),('exact SciPy snippet',['scipy_example.py'])]:
            if args==['scipy_example.py']:Path(tmp,'scipy_example.py').write_bytes(blocks[0])
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['numerical_root_finding.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('root_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    with localcontext() as ctx:ctx.prec=80;sqrt2=D(2).sqrt()
    lab=[]
    for name,args in [('bisection',(lambda x:x*x-2,1,2)),('newton',(lambda x:x*x-2,lambda x:2*x,1)),('secant',(lambda x:x*x-2,1,2))]:
        result=getattr(m,name)(*args);lab.append(dict(method=name,result=result))
        num('lab '+name+' root',lambda result=result:result['root'],sqrt2,atol=1e-10,rtol=0)
        num('lab '+name+' original residual',lambda result=result:result['root']**2-2,0,atol=1e-10,rtol=0)
    num('E3 first midpoint',lambda:F(1+2,2),F(3,2));num('E3 residual',lambda:F(3,2)**2-2,F(1,4))
    num('E4 second midpoint',lambda:F(1+F(3,2),2),F(5,4));num('E4 residual',lambda:F(5,4)**2-2,F(-7,16))
    num('E5 ten retained halvings width',lambda:F(1,2**10),F(1,1024));num('E6 midpoint bound',lambda:F(1,2**11),F(1,2048))
    num('E12 Newton first update',lambda:F(1)-F(-1,2),F(3,2));num('E13 second update',lambda:F(3,2)-F(1,4)/3,F(17,12))
    num('E23 residual',lambda:F(7,5)**2-2,F(-1,25));num('E24 root error',lambda:abs(D('1.4')-sqrt2),sqrt2-D('1.4'))
    num('E19 lab IRR',lambda:m.irr_bracketed([-100,110])['root'],F(1,10),atol=1e-12,rtol=0)
    num('E18 source NPV',lambda:m.npv(.1,[-100,110]),0,atol=1e-12,rtol=0)
    for lo,hi,want in [(.05,.15,F(1,10)),(.15,.25,F(1,5))]:
        num('E21 separate bracket '+str(lo),lambda lo=lo,hi=hi:m.irr_bracketed([-100,230,-132],lo,hi)['root'],want,atol=1e-12,rtol=0)
        num('E21 substitute '+str(want),lambda want=want:m.npv(float(want),[-100,230,-132]),0,atol=1e-12,rtol=0)
    for name,fn,want in [
      ('stable wide midpoint',lambda:m.bisection(lambda x:x/1e308,-1e308,1e308)['root'],0),
      ('Newton tiny nonzero derivative',lambda:m.newton(lambda x:1e-200*(x-2),lambda x:1e-200,0,ftol=0)['root'],2),
      ('secant large coordinates',lambda:m.secant(lambda x:x/1e308,-1e308,1e308,ftol=0)['root'],0),
      ('secant first guess already root',lambda:m.secant(lambda x:x,0,1,max_iter=1,ftol=0)['root'],0),
      ('NPV preserves integer cancellation',lambda:m.npv(0,[-10**18,10**18+1]),1),
      ('NPV tiny rate',lambda:m.npv(1e-308,[-1,1]),F(-1,10**308)),
      ('NPV avoids power overflow',lambda:m.npv(1e308,[0,0,1e308]),F(1,10**308))]:
        num('F160 '+name,fn,want)
    # Linear callbacks expose intermediate overflow while retaining a valid exact root.
    num('F160 Newton large step finite destination',lambda:m.newton(lambda x:x/2+5e307,lambda x:.5,1e308,ftol=0,max_iter=1)['root'],-1e308)
    num('F160 secant function difference overflow',lambda:m.secant(lambda x:1e308*x,-1,1,ftol=0)['root'],0)
    for label,fn,kind in [
      ('no bracket',lambda:m.bisection(lambda x:x*x+1,-1,1),ValueError),
      ('even multiplicity no bracket',lambda:m.bisection(lambda x:(x-1)**2,0,2),ValueError),
      ('zero derivative',lambda:m.newton(lambda x:x*x+1,lambda x:2*x,0),ValueError),
      ('Newton domain',lambda:m.newton(lambda x:x+2,lambda x:1,0,domain=lambda x:x>-1),ValueError),
      ('secant zero slope',lambda:m.secant(lambda x:1,0,1),ValueError),
      ('invalid NPV domain',lambda:m.npv(-1,[-100,110]),ValueError),
      ('bisection iteration budget',lambda:m.bisection(lambda x:x*x-2,1,2,max_iter=1),RuntimeError),
      ('bisection float stagnation',lambda:m.bisection(lambda x:-1 if x<=1 else 1,1,math.nextafter(1,2),xtol=1e-30),RuntimeError),
      ('Newton float stagnation',lambda:m.newton(lambda x:1,lambda x:1e308,1,ftol=0),RuntimeError),
      ('secant float stagnation',lambda:m.secant(lambda x:1 if x==1 else 1e308,0,1,ftol=0),RuntimeError),
      ('huge integer coordinate',lambda:m.bisection(lambda x:x,10**1000,10**1000+1),ValueError),
      ('unrepresentable integer coordinate',lambda:m.bisection(lambda x:-1,10**18+1,10**18+2),ValueError),
      ('all zero IRR',lambda:m.irr_bracketed([0,0]),ValueError),
      ('IRR invalid string bound',lambda:m.irr_bracketed([-100,110],'bad',1),ValueError),
      ('NPV unreportable nonzero',lambda:m.npv(1,[0,0,5e-324]),ValueError),
      ('boolean callback',lambda:m.bisection(lambda x:False,0,1),ValueError),
      ('boolean derivative',lambda:m.newton(lambda x:x-1,lambda x:True,0,ftol=0),ValueError),
      ('noncallable function',lambda:m.bisection(None,0,1),ValueError),
      ('nonboolean domain decision',lambda:m.newton(lambda x:x-1,lambda x:1,0,domain=lambda x:1),ValueError),
    ]:reject('F160 '+label,fn,kind)
    r=m.bisection(lambda x:-1 if x<.3 else 1,0,1)
    ck('discontinuity can meet interval rule without zero residual',r['residual'] in (-1,1),result=r,limit='not evidence of a mathematical root')
    ck('bisection explicit termination and radius',all(k in lab[0]['result'] for k in ('termination','x_error_bound','interval_halvings')))
    # Source residual-only acceptance deliberately illustrated; no x-error certification.
    r=m.newton(lambda x:1e-20*(x-2),lambda x:1e-20,0)
    ck('E25 tiny residual can accept inaccurate root',r['root']==0,root_error=2,result=r)
    try:import scipy;scipy_version=scipy.__version__
    except ImportError:scipy_version=None
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy_version,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,lab_results=lab,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0)
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
