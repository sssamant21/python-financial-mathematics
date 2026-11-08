"""Numerical motivation lab and independent rational/root/grid benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-17/17.01-why-numerical-methods-are-needed.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-17/17.01-why-numerical-methods-are-needed.md'])
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
    with tempfile.TemporaryDirectory(prefix='book1-1701-') as tmp:
        Path(tmp,'why_numerical_methods_are_needed.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['why_numerical_methods_are_needed.py']),('isolated import',['-c','import why_numerical_methods_are_needed']),('exact compilation',['-m','compileall','-q','why_numerical_methods_are_needed.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['why_numerical_methods_are_needed.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    def reject_runtime(label,fn):
      try:value=fn()
      except RuntimeError as e:ck(label,True,exception=repr(e))
      except Exception as e:ck(label,False,exception=repr(e))
      else:ck(label,False,actual=repr(value))
    ck('E1 source NPV at ten percent',abs(m.npv(.1,[-100,110]))<=1e-12,actual=m.npv(.1,[-100,110]),independent_reference='0',absolute_dollar_tolerance=1e-12)
    irr=m.irr([-100,110]);num('E30 original-equation residual',lambda:abs(m.npv(irr['root'],[-100,110])),abs(F(str(irr['residual']))))
    ck('lab IRR independently bounded root error',abs(F(str(irr['root']))-F(1,10))<=F(1,10**12),actual=irr,reference='1/10',absolute_root_tolerance='1e-12')
    roots=[]
    for tol in [1e-6,1e-9,1e-12]:
      value=m.bisection(lambda x:x*x-2,0,2,tol);roots.append(value)
      ck('lab sqrt2 root absolute error '+str(tol),abs(D(str(value['root']))-root(2))<=D(str(tol)),actual=value,independent_reference=str(root(2)))
    try:ck('diagnostic extension reported radius meets coordinate tolerance',all(v['x_error_bound']<=tol and v['termination']=='interval_tolerance' and v['interval_halvings']==v['iterations']-1 for v,tol in zip(roots,[1e-6,1e-9,1e-12])))
    except KeyError as e:ck('diagnostic extension reported radius meets coordinate tolerance',False,exception=repr(e))
    ck('lab tighter tolerance takes no fewer iterations',all(roots[i]['iterations']<=roots[i+1]['iterations'] for i in range(2)))
    close('E5 supplemental midpoint',F(0+2,2),1);close('E6 supplemental bracket width',F(2,2**10),F(1,512));close('E7 supplemental midpoint bound after ten halvings',F(2,2**11),F(1,1024))
    endpoint=m.bisection(lambda x:x-1,1,2);ck('endpoint root no iterations',endpoint['root']==1 and endpoint['iterations']==0)
    for rate in [.1,.2]:ck('E9 independent NPV root '+str(rate),abs(m.npv(rate,[-100,230,-132]))<=1e-12,actual=m.npv(rate,[-100,230,-132]),independent_reference='0',absolute_dollar_tolerance=1e-12)
    for bracket,want in [((.05,.15),F(1,10)),((.15,.25),F(1,5))]:
      result=m.irr([-100,230,-132],*bracket);ck('lab separate multiple-IRR bracket '+str(bracket),abs(F(str(result['root']))-want)<=F(1,10**12),actual=result,independent_reference=str(want))
    for steps in [1,10,100]:num('E18 linear trapezoid '+str(steps),lambda steps=steps:m.trapezoid(lambda x:x,0,1,steps),F(1,2))
    integrals=[]
    for n in [10,100,1000]:
      result=m.trapezoid(lambda x:x*x,0,1,n);expected=F(1,3)+F(1,6*n*n)
      close('E19 exact finite-grid quadratic trapezoid '+str(n),result,expected);integrals.append(result)
    ck('E29 quadrature refinement errors shrink',abs(integrals[2]-1/3)<abs(integrals[1]-1/3)<abs(integrals[0]-1/3),actual=integrals,oracle_error='1/(6*N^2)')
    grids=[]
    for steps in [10,20,100]:
      r=m.grid_minimize(lambda x:(x-.34)**2,0,1,steps);grids.append(r)
      close('lab grid spacing '+str(steps),r['grid_spacing'],F(1,steps))
    close('E14 coarse-grid minimizer',grids[0]['x'],F(3,10));close('lab fine grid hits minimizer',grids[2]['x'],F(17,50))
    exact=m.grid_minimize(lambda x:(x-.3)**2,0,1,10);close('E13 exact grid optimum',exact['x'],F(3,10));close('E13 exact grid objective',exact['value'],0)
    for label,fn,want in [
      ('F158 tiny NPV difference retained',lambda:m.npv(1e-308,[-1,1]),F(-1,10**308)),
      ('F158 NPV avoids discount-power overflow',lambda:m.npv(1e308,[0,0,1e308]),F(1,10**308)),
      ('F158 finite integral after weighted accumulation',lambda:m.trapezoid(lambda x:1e308,0,1,2),1e308),
      ('F158 finite integral across huge interval',lambda:m.trapezoid(lambda x:1e-308,-1e308,1e308,2),2),
      ('F158 large-coordinate grid avoids width overflow',lambda:m.grid_minimize(lambda x:abs(x)/1e308,-1e308,1e308,2)['x'],0),
      ('F158 large-coordinate midpoint avoids overflow',lambda:m.bisection(lambda x:x/1e308-1.5,1e308,1.7e308,1e292)['root'],1.5e308),
    ]:num(label,fn,want)
    for label,fn in [
      ('F158 tiny same-sign endpoints reject',lambda:m.bisection(lambda x:1e-300,0,1)),
      ('F158 unresolved integer coordinate interval rejected',lambda:m.bisection(lambda x:x-10**18-.5,10**18,10**18+1)),
      ('F158 typed callback bool rejects',lambda:m.bisection(lambda x:False,0,1)),
      ('F158 nonnumeric callback has ValueError',lambda:m.bisection(lambda x:None,0,1)),
      ('F158 grid rejects boolean bounds',lambda:m.grid_minimize(lambda x:x,False,True,2)),
      ('F158 grid rejects infinite bounds',lambda:m.grid_minimize(lambda x:1,-math.inf,math.inf,2)),
      ('F158 nonzero integral underflow rejected',lambda:m.trapezoid(lambda x:1e-300,0,1e-300,2)),
      ('F158 huge integer input has ValueError',lambda:m.npv(0,[10**1000,1])),
      ('E10 nonidentifiable zero-cashflow IRR rejected',lambda:m.irr([0,0,0])),
      ('invalid discount domain rejected',lambda:m.npv(-1,[-100,110])),
      ('E8 nonbracketing function rejected',lambda:m.bisection(lambda x:x*x+1,-1,1)),
      ('nonfinite interior value rejected',lambda:m.bisection(lambda x: -1 if x==0 else (1 if x==1 else math.nan),0,1)),
    ]:reject(label,fn)
    reject_runtime('E34 iteration cap reported',lambda:m.bisection(lambda x:x*x-2,0,2,1e-15,1))
    reject_runtime('F158 coordinate stagnation reports failure',lambda:m.bisection(lambda x:x*x-2,1,2,1e-30,200))
    # Sign change across a discontinuity is a precondition failure the callback interface cannot prove.
    discontinuity=m.bisection(lambda x:-1 if x<.3 else 1,0,1)
    ck('E11 width convergence does not prove continuity',abs(discontinuity['residual'])==1,actual=discontinuity,scope='counterexample: bracket-width termination is not original-equation residual or existence proof')
    project=dict(single_year_cashflows=[-100,110],single_year_irr=irr,sqrt2_tolerance_runs=roots,multiple_cashflows=[-100,230,-132],multiple_brackets=[[.05,.15],[.15,.25]],quadratic_steps=[10,100,1000],quadratic_integrals=integrals,grid_steps=[10,20,100],grid_results=grids,
      units='fictional common USD cashflows at integer annual times; dimensionless rates and toy function coordinates',cashflow_timing='initial t0 followed by equally spaced year-end flows',dates=None,scope='numerical examples only; continuity/financial model assumptions are caller responsibilities, no SciPy backend executed',fixture_sha256=hashlib.sha256(json.dumps([[-100,110],[-100,230,-132],[1e-6,1e-9,1e-12],[10,100,1000]]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=35,lab_step_records=12,historical_unique_methods_added=0,project_report=project)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
