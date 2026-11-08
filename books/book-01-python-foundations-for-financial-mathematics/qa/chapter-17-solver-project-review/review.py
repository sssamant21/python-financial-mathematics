"""Exact two-file project execution and independent periodic-rate expectations."""
import dataclasses,hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.14-chapter-project-financial-numerical-solver.md';source=BOOK/path
    data=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path])
    blocks=re.findall(rb'^(?:```|~~~)python\n(.*?)^(?:```|~~~)',data,re.M|re.S);code=blocks[0];testcode=blocks[1];commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn,kind=ValueError):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,kind),exception=repr(e),expected_exception=kind.__name__)
        else:ck(label,False,actual=repr(v),expected_exception=kind.__name__)
    with tempfile.TemporaryDirectory(prefix='book1-1714-') as tmp:
        Path(tmp,'financial_solver.py').write_bytes(code);Path(tmp,'test_financial_solver.py').write_bytes(testcode)
        for label,args in [('exact project demonstration',['financial_solver.py']),('exact twelve separate-file methods',['-m','unittest','-v','test_financial_solver']),('compile both exact files',['-m','compileall','-q','financial_solver.py','test_financial_solver.py']),('silent implementation and test import',['-c','import financial_solver,test_financial_solver'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact twelve separate-file methods':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label in ['compile both exact files','silent implementation and test import']:ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
    m=types.ModuleType('project_lab');sys.modules[m.__name__]=m;exec(compile(code,str(source),'exec'),m.__dict__)
    flows=[-100,110];baseline=m.solve_rate(flows,0,.2);endpoint=m.solve_rate([-100,100],0,.2)
    for label,fn,want in [
      ('baseline zero-rate NPV',lambda:m.npv(flows,0),10),
      ('baseline ten-percent NPV',lambda:m.npv(flows,.1),0),
      ('E8 eleven-percent NPV',lambda:m.npv(flows,.11),F(-100,111)),
      ('E5 analytic root',lambda:baseline.rate,F(1,10)),
      ('E31 finite one-bp change',lambda:m.one_bp_change(flows,.1),F(-100,11001)),
      ('E19 doubled-flow NPV',lambda:m.npv([-200,220],.05),F(200,21)),
      ('E20 appended zero preserves timing',lambda:m.npv([-100,110,0],.1),0),
      ('E32 inserted zero delays terminal payment',lambda:m.npv([-100,0,110],.1),F(-100,11)),
      ('E25 valid negative rate',lambda:m.npv(flows,-.05),F(300,19)),
      ('F171 integer NPV cancellation',lambda:m.npv([-10**18,10**18+1],0),1),
      ('F171 tiny NPV rate retained',lambda:m.npv([-1,1],1e-308),F(-1,10**308)),
      ('F171 discounted value before power loss',lambda:m.npv([0,0,1e308],1e308),F(1,10**308)),
      ('F171 one-bp original iterable consumed once',lambda:m.one_bp_change((x for x in flows),.1),F(-100,11001)),
      ('F171 one-bp difference before large NPV reporting',lambda:m.one_bp_change([1e308,110],.1),F(-100,11001)),
      ('F171 one-bp rate addition retains tiny bump',lambda:m.one_bp_change([0,1e20],1e20),F(10**20)*(1/(1+F(10**20)+F(1,10000))-1/(1+F(10**20)))),
    ]:num(label,fn,want,atol=1e-12 if want==0 or label=='E5 analytic root' else 0)
    num('independent repricing at returned root',lambda:float(-F(100)+F(110)/(1+F(str(baseline.rate)))),0,atol=1e-8,rtol=0)
    ck('endpoint diagnostics',endpoint.rate==0 and endpoint.method=='endpoint' and endpoint.iterations==0 and endpoint.function_calls==2,report=dataclasses.asdict(endpoint))
    ck('brent diagnostics bounded and separate',baseline.converged and baseline.method=='brentq' and baseline.bracket==(0,.2) and baseline.iterations>=1 and baseline.function_calls>=baseline.iterations and baseline.residual_accepted,report=dataclasses.asdict(baseline))
    loose=m.solve_rate([-1e200,1.1e200],0,.2,rate_xtol=.01,residual_tolerance=1e-8)
    ck('E16 rate convergence does not force residual acceptance',loose.converged and not loose.residual_accepted and abs(loose.residual)>loose.residual_tolerance,report=dataclasses.asdict(loose))
    for lo,hi,want in [(.05,.15,F(1,10)),(.15,.25,F(1,5))]:
        r=m.solve_rate([-100,230,-132],lo,hi);num('E13 bracketed root '+str(lo),lambda r=r:r.rate,want,atol=1e-10,rtol=0)
        num('E13 original-equation repricing '+str(lo),lambda r=r:float(-F(100)+F(230)/(1+F(str(r.rate)))-F(132)/(1+F(str(r.rate)))**2),0,atol=1e-8,rtol=0)
    num('small-scale root with explicit currency budget',lambda:m.solve_rate([-1e-200,1.1e-200],0,.2,residual_tolerance=1e-210).rate,F(1,10),atol=1e-10,rtol=0)
    for label,fn,kind in [
      ('all-zero flows non-identifiable',lambda:m.solve_rate([0,0],0,.2),ValueError),
      ('invalid rate',lambda:m.npv(flows,-1),ValueError),
      ('invalid bracket',lambda:m.solve_rate(flows,.2,.3),ValueError),
      ('bracket encloses two crossings same signs',lambda:m.solve_rate([-100,230,-132],.05,.25),ValueError),
      ('empty flows',lambda:m.npv([],.1),ValueError),
      ('nonfinite flow',lambda:m.npv([0,float('nan')],.1),ValueError),
      ('malformed iterable',lambda:m.validate_flows(None),ValueError),
      ('huge integer input',lambda:m.npv([0,10**1000],.1),ValueError),
      ('unreportable nonzero NPV',lambda:m.npv([0,0,5e-324],1),ValueError),
      ('integer bound would lose identity',lambda:m.solve_rate(flows,10**18+1,10**18+2),ValueError),
      ('nonconverged maxiter',lambda:m.solve_rate(flows,0,.2,maxiter=1),RuntimeError),
      ('boolean rate',lambda:m.npv(flows,True),ValueError),
    ]:reject('F171 '+label,fn,kind)
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),implementation_sha256=hashlib.sha256(code).hexdigest(),tests_sha256=hashlib.sha256(testcode).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,architecture_acceptance_records=6,worked_example_records=4,extension_design_records=5,historical_unique_methods_added=0,reports=dict(baseline=dataclasses.asdict(baseline),endpoint=dataclasses.asdict(endpoint),converged_residual_rejected=dataclasses.asdict(loose)),model=dict(cashflows=flows,bracket=[0,.2],rate_xtol=1e-12,currency_residual_tolerance=1e-8,one_bp='1/10000',timing='t0 purchase and t1 payment, integer periods',units='fictional common currency, periodic effective decimal rate',scope='no dates/day-count/fees unless supplied; no investment recommendation'))
    def safe(x):
        if isinstance(x,F):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
