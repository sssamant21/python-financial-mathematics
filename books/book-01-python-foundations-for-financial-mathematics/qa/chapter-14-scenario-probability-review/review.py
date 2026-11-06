"""Section 14.1 exact scenario probability lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.01-why-probability-matters-in-finance.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1401-') as tmp:
        Path(tmp,'why_probability_matters.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['why_probability_matters.py']),('isolated import',['-c','import why_probability_matters']),('exact compilation',['-m','compileall','-q','why_probability_matters.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['why_probability_matters.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('scenarios');exec(compile(code,str(source),'exec'),m.__dict__)
    from random import Random
    from itertools import combinations
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    stock=[(.6,.2),(.4,-.1)]
    project=[(.05,-.35),(.20,-.10),(.50,.05),(.25,.18)]
    exact=[(F(str(p)),F(str(x))) for p,x in project]
    var=sum(p*q*(x-y)**2 for (p,x),(q,y) in combinations(exact,2))
    mean=F('0.0325')
    for label,fn,want in [
        ('E1 modeled certainty',lambda:m.expected_payoff([(1,100)]),100),
        ('E2 expected return',lambda:m.expected_payoff(stock),F('.08')),
        ('E3 probability of loss',lambda:m.probability_of_loss(stock),F('.4')),
        ('E4 two-point variance',lambda:m.outcome_variance(stock),F('.0216')),
        ('E5 payout',lambda:m.expected_payoff([(.3,100),(.7,0)]),30),
        ('E10 expected loss magnitude',lambda:m.expected_shortfall_below_zero([(.01,-1000),(.99,0)]),10),
        ('E11 expected loss magnitude',lambda:m.expected_shortfall_below_zero([(.01,-.50),(.99,0)]),F('.005')),
        ('E12 zero mean',lambda:m.expected_payoff([(.5,.1),(.5,-.1)]),0),
        ('E12 variance',lambda:m.outcome_variance([(.5,.1),(.5,-.1)]),F('.01')),
        ('E19 constant payoff variance',lambda:m.outcome_variance([(1,5)]),0),
        ('project return',lambda:m.expected_payoff(project),mean),
        ('project variance via pairwise differences',lambda:m.outcome_variance(project),var),
        ('project probability of loss',lambda:m.probability_of_loss(project),F('.25')),
        ('project expected loss contribution',lambda:m.expected_shortfall_below_zero(project),F('.0375')),
        ('F110 impossible outcomes cannot overflow variance',lambda:m.outcome_variance([(1,7),(0,1e308)]),0),
        ('F110 weighted variance despite oversized square',lambda:m.outcome_variance([(1,0),(1e-300,1e300)]),F('1e300')),
        ('F110 simulated mean despite overflow in sum',lambda:m.simulated_mean([(1,1e308)],10,42),F('1e308')),
    ]:num(label,fn,want)
    for label,fn in [
        ('E9 reject excess mass',lambda:m.expected_payoff([(.6,1),(.6,2)])),
        ('project reject negative weight',lambda:m.expected_payoff([(-.05,-.35),*project[1:]])),
        ('F110 unreportable variance',lambda:m.outcome_variance([(.5,-1e308),(.5,1e308)])),
        ('F110 unreportable nonzero mean',lambda:m.expected_payoff([(.01,5e-324),(.99,0)])),
        ('nonfinite payoff',lambda:m.expected_payoff([(1,float('inf'))])),
    ]:reject(label,fn)
    ck('F110 near-unit mass normalized for theory',m.expected_payoff([(.5,100),(.4999999999991,100)])==100)
    ck('project exact mass and variance',sum(p for p,_ in exact)==1 and var==F('.01641875'))
    observed=[]
    for seed in (42,43):
        rng=Random(seed)
        expected=[]
        for _ in range(10000):
            u=rng.random()
            expected.append(-.35 if u<.05 else -.10 if u<.25 else .05 if u<.75 else .18)
        sample=m.sample_scenarios(project,10000,seed)
        ck(f'project fixed-environment stream for seed {seed}',sample==expected and sample==m.sample_scenarios(project,10000,seed))
        want=sum((F(str(x)) for x in expected),F(0))/len(expected)
        num(f'project realized mean for seed {seed}',lambda:m.simulated_mean(project,10000,seed),want)
        observed.append(want)
    se=math.sqrt(float(var)/10000)
    ck('project samples differ and errors within four standard errors',
       observed[0]!=observed[1] and all(abs(float(x-mean))<4*se for x in observed))
    ck('exact demo',commands[0]['stdout'].splitlines()[:4]==['Expected payoff: 5.0','Variance: 312.5','Probability of loss: 0.25','Expected loss below zero: 5.0'])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=22,mini_project_records=1,mini_project_task_records=10,
             historical_unique_methods_added=0,project_standard_error=se,project_seed_means=list(map(float,observed)))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
