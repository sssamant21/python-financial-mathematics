"""Chapter17 assessment: exact snippet/project runs, linked sources, independent oracles."""
import contextlib,hashlib,io,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
PATTERN=rb'^(?:```|~~~)python\n(.*?)^(?:```|~~~)'
def main():
    revision=sys.argv[1] if len(sys.argv)>1 else None
    def read(relative):
        return (BOOK/relative).read_bytes() if revision is None else subprocess.check_output(['git','-C',str(BOOK),'show',revision+':books/book-01-python-foundations-for-financial-mathematics/'+relative])
    path='chapter-17/17.15-exercises-and-applied-problems.md';data=read(path);snippet=re.findall(PATTERN,data,re.M|re.S)[0]
    linked={};modules={}
    def load(key,relative):
        raw=read(relative);blocks=re.findall(PATTERN,raw,re.M|re.S)
        if key=='project':code=blocks[0]
        else:code=next(b for b in blocks if b'import unittest' in b)
        linked[key]=dict(path=relative,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest())
        module=types.ModuleType('assessment_'+key);sys.modules[module.__name__]=module
        exec(compile(code,relative,'exec'),module.__dict__);modules[key]=module
        return blocks
    project_blocks=load('project','chapter-17/17.14-chapter-project-financial-numerical-solver.md')
    for key,relative in [('portfolio','17.07-portfolio-optimization.md'),('integration','17.12-convergence-and-error.md'),('interpolation','17.09-interpolation.md'),('stability','17.11-numerical-stability.md'),('validation','17.13-validation-of-numerical-results.md')]:load(key,'chapter-17/'+relative)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,ValueError),exception=repr(e),expected_exception='ValueError')
        else:ck(label,False,actual=repr(v),expected_exception='ValueError')
    with tempfile.TemporaryDirectory(prefix='book1-1715-') as tmp:
        Path(tmp,'assessment_example.py').write_bytes(snippet);Path(tmp,'financial_solver.py').write_bytes(project_blocks[0]);Path(tmp,'test_financial_solver.py').write_bytes(project_blocks[1])
        tasks=[('exact assessment SciPy snippet',['assessment_example.py']),('exact linked project demonstration',['financial_solver.py']),('linked twelve existing project methods',['-m','unittest','-v','test_financial_solver']),('compile exact snippet and project files',['-m','compileall','-q','assessment_example.py','financial_solver.py','test_financial_solver.py']),('silent linked project/test import',['-c','import financial_solver,test_financial_solver'])]
        for label,args in tasks:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='linked twelve existing project methods':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label.startswith(('compile','silent')):ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
    ns={};capture=io.StringIO()
    with contextlib.redirect_stdout(capture):exec(compile(snippet,'exact_assessment_snippet','exec'),ns)
    project=modules['project'];risk=modules['portfolio'];integration=modules['integration'];interpolation=modules['interpolation'];stability=modules['stability'];validation=modules['validation']
    with localcontext() as ctx:
        ctx.prec=200;irr=(D(3)+D(69).sqrt())/10-1;annuity=D(2000)*(1-D('-.1').exp());sd0=(D(13)/400).sqrt();sd1=(D(19)/400).sqrt();log_return=D('1.01').ln()
    num('exact assessment snippet independent two-period root',lambda:ns['result'].root,irr,atol=1e-12,rtol=0)
    num('exact snippet independently repriced',lambda:float(-F(100)+F(60)/(1+F(str(ns['result'].root)))+F(60)/(1+F(str(ns['result'].root)))**2),0,atol=1e-10,rtol=0)
    for label,fn,want in [
      ('E1 linked one-period PV',lambda:project.npv([0,110],.1),100),
      ('E2 linked one-period root',lambda:project.solve_rate([-100,110],0,.2).rate,F(1,10)),
      ('E3 left bracket residual',lambda:project.npv([-100,110],0),10),
      ('E3 right bracket residual',lambda:project.npv([-100,110],.2),F(-25,3)),
      ('E4 exact midpoint NPV',lambda:project.npv([-100,110],.1),0),
      ('E5 ideal ten-halving width',lambda:F(1,5)/2**10,F(1,5120)),
      ('E5 midpoint basis-point bound',lambda:F(1,10240)*10000,F(125,128)),
      ('E7 returned-rate residual',lambda:project.npv([-100,110],.101),F(-100,1101)),
      ('E10 endpoint root',lambda:project.solve_rate([-100,100],0,.2).rate,0),
      ('E13 exact budget residual supplemental',lambda:F(2,5)+F(3,5)-1,0),
      ('E14 budget violation supplemental',lambda:F(2,5)+F(61,100)-1,F(1,100)),
      ('E15 linked equal-weight variance',lambda:risk.portfolio_stats(.5,[.08,.04],[[.04,0],[0,.09]])['variance'],F(13,400)),
      ('E15 linked equal-weight volatility',lambda:risk.portfolio_stats(.5,[.08,.04],[[.04,0],[0,.09]])['volatility'],sd0),
      ('E16 linked correlated variance',lambda:risk.portfolio_stats(.5,[.08,.04],[[.04,.03],[.03,.09]])['variance'],F(19,400)),
      ('E16 linked correlated volatility',lambda:risk.portfolio_stats(.5,[.08,.04],[[.04,.03],[.03,.09]])['volatility'],sd1),
      ('E21 exact antiderivative benchmark supplemental',lambda:F(1,3),F(1,3)),
      ('E22 linked two-panel trapezoid',lambda:integration.trapezoid(lambda x:x*x,0,1,2),F(3,8)),
      ('E23 linked four-panel trapezoid',lambda:integration.trapezoid(lambda x:x*x,0,1,4),F(11,32)),
      ('E24 linked continuous annuity',lambda:stability.continuous_annuity(.05,2,100),annuity),
      ('E26 linked linear-zero midpoint',lambda:interpolation.linear_interpolate([1,3],[.04,.06],2),F(1,20)),
      ('E28 linked average forward',lambda:interpolation.forward_rate(math.exp(-.04),math.exp(-.1),1,2),F(3,50)),
      ('E32 accurate-sum primitive',lambda:math.fsum([1e16,1,-1e16]),1),
      ('E33 linked log return',lambda:stability.stable_log_return(100,101),log_return),
      ('E34 linked log-sum-exp',lambda:stability.log_sum_exp([1000,1000]),1000+math.log(2)),
      ('E35 absolute price error supplemental',lambda:F('100.02')-100,F(1,50)),
      ('E35 relative price error supplemental',lambda:(F('100.02')-100)/100,F(1,5000)),
      ('E38 flat residual supplemental',lambda:(F('1.01')-1)**3,F(1,10**6)),
      ('E38 root error supplemental',lambda:F('1.01')-1,F(1,100)),
      ('E41 linked annual coupon price',lambda:project.npv([0,5,105],.05),100),
      ('E42 linked coupon price residual',lambda:validation.price_residual(100,[0,5,105],.05),0),
      ('E43 linked single-payment11percent price',lambda:project.npv([0,110],.11),F(11000,111)),
      ('E44 linked one-bp finite price change',lambda:project.one_bp_change([0,110],.1),F(-100,11001)),
      ('E44 linked bumped price',lambda:project.npv([0,110],.1001),F(1100000,11001)),
      ('E45 linked currency-scaled NPV',lambda:project.npv([-100000,110000],.05),F(100000,21)),
      ('E45 linked currency-scaled root',lambda:project.solve_rate([-100000,110000],0,.2).rate,F(1,10)),
      ('E46 linked two-period NPV',lambda:project.npv([-100,60,60],.1),F(500,121)),
      ('E47 linked two-period IRR',lambda:project.solve_rate([-100,60,60],0,.3).rate,irr),
      ('E48 materiality supplemental',lambda:F(1,50)*500000,10000),
      ('E49 standard-error arithmetic supplemental',lambda:F(20,100),F(1,5)),
    ]:num(label,fn,want,atol=1e-12 if label in ['E2 linked one-period root','E45 linked currency-scaled root','E47 linked two-period IRR'] or want==0 else 0)
    ck('E11 analytic quadratic optimum',F(3)==3 and (F(3)-3)**2+2==2,derivation='square>=0,unique zero atx=3; supplemental analytic proof, not NPV export')
    ck('E12 analytic constrained optimum',2<3 and (F(2)-3)**2+2==3,derivation='on[0,2],derivative2(x-3)<0,so right boundary minimizes')
    num('E23 actual error ratio supplemental',lambda:(F(3,8)-F(1,3))/(F(11,32)-F(1,3)),4)
    ck('E25 small subtraction primitive',math.exp(-1e-20)==1 and -math.expm1(-1e-20)>0,argument=1e-20,naive=1-math.exp(-1e-20),stable=-math.expm1(-1e-20))
    ck('E31 binary64 operation observed',((1e16+1.0)-1e16)==0)
    ck('E37 linked mixed tolerance fails',validation.close_to_reference(100.02,100,.01,.00005) is False,independent_error='.02',independent_threshold='.015')
    for lo,hi,want in [(.05,.15,F(1,10)),(.15,.25,F(1,5))]:num('E9 separate root bracket '+str(lo),lambda lo=lo,hi=hi:project.solve_rate([-100,230,-132],lo,hi).rate,want,atol=1e-10,rtol=0)
    reject('E6 linked no-bracket guard',lambda:project.solve_rate([-100,110],.2,.3))
    reject('E17 linked invalid covariance guard',lambda:risk.portfolio_stats(.5,[.08,.04],[[.04,.07],[.07,.09]]))
    reject('E27 linked default extrapolation rejection',lambda:interpolation.linear_interpolate([1,3],[.04,.06],4))
    reject('lab linked invalid rate guard',lambda:project.npv([-100,110],-1))
    reject('lab linked nonfinite flow guard',lambda:project.npv([-100,float('nan')],.1))
    # Check displayed answer rounding against independent math; do not replace the
    # source execution predicates or use the manuscript as its own oracle.
    for label,value,places,displayed in [('E7',float(F(-100,1101)),6,-.090827),('E15',float(sd0),5,.18028),('E16',float(sd1),5,.21794),('E24',float(annuity),5,190.32516),('E33',float(log_return),8,.00995033),('E43',float(F(11000,111)),6,99.099099),('E44 price',float(F(1100000,11001)),6,99.990910),('E44 change',float(F(-100,11001)),6,-.009090),('E46',float(F(500,121)),5,4.13223),('E47',float(irr),6,.130662)]:
        ck('worked-answer rounded presentation '+label,round(value,places)==displayed,unrounded=value,decimal_places=places,presented=displayed)
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),snippet_sha256=hashlib.sha256(snippet).hexdigest(),linked_sources=linked,commands=commands,checks=checks,workflow_records=1,chapter_wide_answer_records=50,local_prompt_records=0,applied_case_records=10,applied_cases_are_subset_of_answers=True,lab_step_records=12,historical_unique_methods_added=0,existing_linked_project_methods_rerun=12,model=dict(cashflows=[-100,110],coupon_cashflows=[0,5,105],two_period_flows=[-100,60,60],root_bracket=[0,.3],risk=dict(variances=[.04,.09],covariances=[0,.03]),units='fictional common currency; annual-effective periodic rates except explicit continuous annuity/forward/log-return examples',timing='t0 initial then integer year ends; no actual market/calendar data'),criteria=dict(ordinary_rtol=1e-12,known_zero_currency_atol=1e-12,root_atol=1e-12,multiple_root_atol=1e-10,optional_snippet_repricing_atol=1e-10),assessment_snippet_secondary_stdout=capture.getvalue())
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    prior_setup=json.loads(read('qa/chapter-17-solver-project-review/setup-results.json'))
    out['prior_clean_project_evidence']=dict(path='qa/chapter-17-solver-project-review/setup-results.json',source_sha256=prior_setup['source_sha256'],matches_current_linked_project=prior_setup['source_sha256']==linked['project']['source_sha256'],scope='prior clean install/project execution, not a new environment run in this assessment')
    destination='results.json' if revision is None else 'baseline.json';(HERE/destination).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks));return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
