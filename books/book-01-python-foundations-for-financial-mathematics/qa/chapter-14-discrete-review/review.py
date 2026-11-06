"""Section 14.7 exact discrete random variables lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.07-discrete-random-variables.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1407-') as tmp:
        Path(tmp,'discrete_random_variables.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['discrete_random_variables.py']),('isolated import',['-c','import discrete_random_variables']),('exact compilation',['-m','compileall','-q','discrete_random_variables.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['discrete_random_variables.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('discrete');exec(compile(code,str(source),'exec'),m.__dict__)
    from random import Random
    from collections import Counter
    from itertools import product
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,float(value),want,atol=0)
    b={0:.7,1:.3};d={-20:.25,5:.5,30:.25}
    for label,fn,want in [
        ('E1 unit mass',lambda:m.cdf(b,1),1),
        ('E3 Bernoulli mean',lambda:m.expectation(b),F('.3')),
        ('E4 Bernoulli variance',lambda:m.variance(b),F('.21')),
        ('E6 inclusive zero',lambda:m.cdf(b,0),F('.7')),
        ('E7 below support',lambda:m.cdf(b,-1),0),
        ('E8 above support',lambda:m.cdf(b,2),1),
        ('E9 strict tail',lambda:m.tail_probability(b,0),F('.3')),
        ('E10 mean',lambda:m.expectation(d),5),
        ('E11 variance',lambda:m.variance(d),F('312.5')),
        ('E12 CDF',lambda:m.cdf(d,5),F('.75')),
        ('E13 loss',lambda:m.cdf(d,-1),F('.25')),
        ('E14 strict cutoff',lambda:m.cdf(d,4),F('.25')),
        ('E16 binomial mean',lambda:m.expectation(m.binomial_pmf(10,.1)),1),
        ('E17 binomial variance',lambda:m.variance(m.binomial_pmf(10,.1)),F('.9')),
        ('E18 zero count',lambda:m.binomial_pmf(5,.2)[0],F('.32768')),
        ('E19 positive count',lambda:m.tail_probability(m.binomial_pmf(5,.2),0),F('.67232')),
        ('E20 exact two',lambda:m.binomial_pmf(4,.25)[2],F('.2109375')),
        ('E21 expected default loss',lambda:m.expectation({0:.98,4000:.02}),80),
        ('F116 exact integer spread',lambda:m.variance({10**18:.5,10**18+1:.5}),F('.25')),
        ('F116 zero mass cannot overflow variance',lambda:m.variance({0:1,1e308:0}),0),
        ('F116 tiny weight applied before reporting variance',lambda:m.variance({0:1,1e300:1e-300}),1e300),
        ('F116 binomial mean for n=1100',lambda:m.expectation(m.binomial_pmf(1100,.5)),550),
    ]:num(label,fn,want)
    for label,fn in [
        ('E2 invalid mass',lambda:m.validate_pmf({0:.4,1:.4,2:.4})),
        ('F116 huge invalid probability',lambda:m.validate_pmf({0:10**400})),
        ('F116 unreportable variance',lambda:m.variance({-1e308:.5,1e308:.5})),
        ('invalid n',lambda:m.binomial_pmf(-1,.1)),
        ('invalid p',lambda:m.binomial_pmf(1,1.1)),
        ('invalid sample count',lambda:m.sample(d,0)),
    ]:reject(label,fn)
    ck('F116 normalized accepted near-unit mass',m.cdf({0:.5,1:.5000000000005},1)==1)
    ck('E15 two-loan masses',all(math.isclose(m.binomial_pmf(2,.1)[k],v) for k,v in enumerate([.81,.18,.01])))
    # Independently enumerate the 1,024 equally structured binary paths,
    # weighting each by integer tenths before collecting default counts.
    points=Counter()
    for bits in product((0,1),repeat=10):
        points[sum(bits)]+=9**bits.count(0)
    d10=m.binomial_pmf(10,.1)
    for k in range(11):num(f'project mass for {k} defaults',lambda:d10[k],F(points[k],10**10))
    ck('project mass and count moments',sum(points.values())==10**10 and sum(k*v for k,v in points.items())==10**10
       and sum((k-1)**2*v for k,v in points.items())==9*10**9)
    for k in (0,1):num(f'project tail P(X>{k})',lambda:m.tail_probability(d10,k),F(sum(v for i,v in points.items() if i>k),10**10))
    from itertools import accumulate
    from bisect import bisect_right
    bounds=[v/10**10 for v in accumulate(points[k] for k in range(11))]
    means={}
    for seed in (42,43):
        rng=Random(seed)
        want=[bisect_right(bounds,rng.random()) for _ in range(20000)]
        got=m.sample(d10,20000,seed)
        ck(f'project seed {seed} inverse-CDF sequence',got==want)
        means[seed]=F(sum(want),len(want))
    ck('project distinct sample means within four standard errors',means[42]!=means[43] and
       all(abs(float(x)-1)<4*math.sqrt(.9/20000) for x in means.values()))
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(sample_means={k:str(v) for k,v in means.items()},standard_error=math.sqrt(.9/20000),integer_path_weights=points))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
