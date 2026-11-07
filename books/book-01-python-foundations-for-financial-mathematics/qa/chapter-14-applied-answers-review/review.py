"""Section 14.17 exact chapter assessment lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.17-exercises-and-applied-problems.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1417-') as tmp:
        Path(tmp,'chapter14_final_exercises.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['chapter14_final_exercises.py']),('isolated import',['-c','import chapter14_final_exercises']),('exact compilation',['-m','compileall','-q','chapter14_final_exercises.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['chapter14_final_exercises.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('assessment');exec(compile(code,str(source),'exec'),m.__dict__)
    from collections import Counter
    from itertools import product
    from random import Random
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E11 zero defaults',lambda:m.binomial_pmf(0,10,.1),F('.9')**10),
        ('E12 any default',lambda:1-m.binomial_pmf(0,10,.1),1-F('.9')**10),
        ('E14 Poisson zero',lambda:m.poisson_pmf(0,2),math.exp(-2)),
        ('E19 standard normal',lambda:m.normal_cdf(1),.8413447460685429),
        ('E20 central interval',lambda:m.normal_cdf(1)-m.normal_cdf(-1),.6826894921370859),
        ('E21 payoff mean',lambda:m.exact_moments([-20,5,30],[.25,.5,.25])[0],5),
        ('E22 payoff variance',lambda:m.exact_moments([-20,5,30],[.25,.5,.25])[1],312.5),
        ('F126 binomial center n=1100',lambda:m.binomial_pmf(550,1100,.5),F(math.comb(1100,550),2**1100)),
        ('F126 finite normal standardization',lambda:m.normal_cdf(1e308,-1e308,1e308),.9772498680518208),
        ('F126 integer spread',lambda:m.exact_moments([10**18,10**18+1],[.5,.5])[1],.25),
        ('F126 zero-weight variance contribution',lambda:m.exact_moments([0,1e308],[1,0])[1],0),
        ('F126 mean with unrepresentable sum',lambda:m.summarize([1e308,1e308])[0],1e308),
        ('F126 finite extreme median',lambda:m.empirical_quantile([-1e308,1e308],.5),0),
        ('F126 bootstrap finite large mean',lambda:m.bootstrap_means([1e308,1e308],10,42)[0],1e308),
    ]:num(label,fn,want)
    for label,fn in [
        ('invalid probability mass',lambda:m.exact_moments([0,1],[.4,.4])),
        ('invalid seed',lambda:m.sample_scenarios([0,1],[.5,.5],20,True)),
        ('invalid sigma',lambda:m.normal_cdf(0,0,0)),
        ('F126 enormous invalid probability',lambda:m.binomial_pmf(0,1,10**400)),
        ('F126 unreportable variance',lambda:m.exact_moments([-1e308,1e308],[.5,.5])),
    ]:reject(label,fn)
    ck('F126 normalized near-unit mass',m.exact_moments([5,5],[.5,.5000000000005])[0]==5)
    try:sample=m.sample_scenarios(iter([0,1]),iter([.5,.5]),20,42)
    except Exception as exc:ck('F126 sampling supports one-pass inputs',False,exception=repr(exc))
    else:ck('F126 sampling supports one-pass inputs',sample==m.sample_scenarios([0,1],[.5,.5],20,42))
    points=Counter()
    for bits in product((0,1),repeat=10):points[sum(bits)]+=9**bits.count(0)
    rng=Random(42); default=Counter(sum(rng.random()<.1 for _ in range(10)) for _ in range(20000))
    for k in range(11):
        num(f'A exact default mass {k}',lambda:m.binomial_pmf(k,10,.1),F(points[k],10**10))
    ck('A supplemental default simulation versus exact masses',sum(default.values())==20000 and
       all(abs(default[k]/20000-points[k]/10**10)<.015 for k in points))
    outcomes=[-20,5,30]; w=[.25,.5,.25]; result={}
    for n in (1000,20000):
        rng=Random(42)
        want=[-20 if u<.25 else 5 if u<.75 else 30 for u in (rng.random() for _ in range(n))]
        got=m.sample_scenarios(outcomes,w,n,42)
        ck(f'B weighted replay {n}',got==want and m.sample_scenarios(outcomes,w,n,42)==got)
        mu=F(sum(want),n); var=(F(sum(x*x for x in want))-n*mu**2)/(n-1)
        actual=m.summarize(got)
        for key,value,ref in zip(('mean','SD','SE'),actual,(mu,math.sqrt(var),math.sqrt(var/n))):close(f'B {n} {key}',value,ref,atol=0)
        ck(f'B {n} empirical quantiles',m.empirical_quantile(got,.05)==-20 and m.empirical_quantile(got,.95)==30)
        result[n]=actual
        if n==1000:base=got
    rng=Random(43)
    ref=[sum(base[int(rng.random()*len(base))] for _ in base)/len(base) for _ in range(500)]
    ck('B 500 bootstrap means match index replay',m.bootstrap_means(base,500,43)==ref)
    shifted=m.sample_scenarios([-18,7,32],w,1000,42)
    ck('B paired additive stress',all(y-x==2 for x,y in zip(base,shifted)))
    def left(z):
        n=2048; h=abs(z)/n
        y=[math.exp(-.5*(i*h)**2)/math.sqrt(2*math.pi) for i in range(n+1)]
        area=h/3*(y[0]+y[-1]+math.fsum((4 if i%2 else 2)*y[i] for i in range(1,n)))
        return .5+math.copysign(area,z)
    num('C probability below zero',lambda:m.normal_cdf(0,.01,.02),left(-.5))
    lo,hi=-2.,-1.
    for _ in range(42):
        z=(lo+hi)/2
        if left(z)<.05:lo=z
        else:hi=z
    q=.01+.02*(lo+hi)/2
    num('C source CDF at independent return quantile',lambda:m.normal_cdf(q,.01,.02),.05)
    ck('C supplemental loss VaR round cents',round(-100000*q,2)==2289.71)
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             chapter_wide_prompt_records=24,applied_problem_records=3,capstone_checklist_records=12,historical_unique_methods_added=0,
             project_report=dict(seed=42,bootstrap_seed=43,bootstrap_reps=500,bootstrap_source_n=1000,
                                 scenario_inputs=[outcomes,w],scenario_summaries=result,default_counts=dict(sorted(default.items())),
                                 return_q05=q,loss_var=-100000*q))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
