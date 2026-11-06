"""Section 14.8 exact continuous random variables lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.08-continuous-random-variables.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1408-') as tmp:
        Path(tmp,'continuous_random_variables.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['continuous_random_variables.py']),('isolated import',['-c','import continuous_random_variables']),('exact compilation',['-m','compileall','-q','continuous_random_variables.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['continuous_random_variables.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('continuous');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from random import Random
    with localcontext() as ctx:
        ctx.prec=60
        half=D('.5')
        s1=(-half).exp();s2=(-D(1)).exp()
        mean=1/half;var=mean**2
        median=D(2).ln()/half;q90=D(10).ln()/half
        tail_interval=(-D(40)).exp()-(-D(41)).exp()
        rescued_pdf=D('1e308')*(-D(750)).exp()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 origin density',lambda:m.exponential_pdf(0,.5),.5),
        ('E2 one-hour density',lambda:m.exponential_pdf(1,.5),s1/2),
        ('E3 negative support',lambda:m.exponential_pdf(-1,.5),0),
        ('E4 origin CDF',lambda:m.exponential_cdf(0,.5),0),
        ('E5 one-hour CDF',lambda:m.exponential_cdf(1,.5),1-s1),
        ('E6 one-hour survival',lambda:m.exponential_survival(1,.5),s1),
        ('E7 two-hour survival',lambda:m.exponential_survival(2,.5),s2),
        ('E8 interval',lambda:m.interval_probability(1,2,.5),s1-s2),
        ('E12 median',lambda:m.exponential_quantile(.5,.5),median),
        ('E13/E20 90th percentile',lambda:m.exponential_quantile(.9,.5),q90),
        ('E17 CDF and survival',lambda:m.exponential_cdf(1,.5)+m.exponential_survival(1,.5),1),
        ('point interval probability',lambda:m.interval_probability(1,1,.5),0),
        ('interval crosses origin',lambda:m.interval_probability(-1,1,.5),1-s1),
        ('interval below origin',lambda:m.interval_probability(-3,-1,.5),0),
        ('tiny CDF not erased',lambda:m.exponential_cdf(1e-20,.5),5e-21),
        ('F117 interval survives far-tail cancellation',lambda:m.interval_probability(40,41,1),tail_interval),
        ('F117 density survives intermediate underflow',lambda:m.exponential_pdf(7.5e-306,1e308),rescued_pdf),
    ]:num(label,fn,want)
    ck('E16 monotone CDF',sorted(m.exponential_cdf(t,.5) for t in [-2,0,1,2,40])==[m.exponential_cdf(t,.5) for t in [-2,0,1,2,40]])
    for label,fn in [
        ('invalid rate',lambda:m.exponential_pdf(0,0)),
        ('reversed interval',lambda:m.interval_probability(2,1,.5)),
        ('unbounded quantile',lambda:m.exponential_quantile(1,.5)),
        ('invalid sample size',lambda:m.sample_exponential(.5,0)),
        ('F117 boolean time rejected',lambda:m.exponential_cdf(True,.5)),
        ('F117 string time rejected',lambda:m.exponential_survival('1',.5)),
        ('F117 enormous integer rate rejected',lambda:m.exponential_cdf(1,10**400)),
        ('F117 unreportable quantile rejected',lambda:m.exponential_quantile(.5,5e-324)),
        ('F117 unreportable sample rejected',lambda:m.sample_exponential(5e-324,1,42)),
    ]:reject(label,fn)
    draws=m.sample_exponential(.5,20000,42)
    rng=Random(42)
    ref=[-2*math.log1p(-rng.random()) for _ in range(20000)]
    ck('project reproducible sequence and inverse-CDF agreement',draws==m.sample_exponential(.5,20000,42) and
       len(draws)==20000 and all(math.isclose(x,y,rel_tol=1e-10,abs_tol=2e-15) for x,y in zip(draws,ref)))
    average=math.fsum(draws)/len(draws)
    empirical=sorted(draws)[math.ceil(.9*len(draws))-1]
    mean_se=2/math.sqrt(len(draws))
    q_se=math.sqrt(.9*.1/len(draws))/.05
    ck('project sample mean within four standard errors',abs(average-float(mean))<4*mean_se,actual=average,standard_error=mean_se)
    ck('project nearest-rank quantile within four asymptotic standard errors',abs(empirical-float(q90))<4*q_se,actual=empirical,standard_error=q_se)
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(version='14.8 synthetic fixture',rate_per_hour=.5,seed=42,trials=20000,
                                 analytic_mean_hours=str(mean),analytic_variance_hours_squared=str(var),
                                 empirical_mean_hours=average,empirical_nearest_rank_q90_hours=empirical))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
