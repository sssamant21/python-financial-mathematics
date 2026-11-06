"""Section 14.12 exact distribution survey lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.12-common-probability-distributions.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1412-') as tmp:
        Path(tmp,'common_probability_distributions.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['common_probability_distributions.py']),('isolated import',['-c','import common_probability_distributions']),('exact compilation',['-m','compileall','-q','common_probability_distributions.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['common_probability_distributions.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('distribution_survey');exec(compile(code,str(source),'exec'),m.__dict__)
    from collections import Counter
    from random import Random
    from itertools import product
    def normal_tail(x):
        n=20000; h=4/n
        def f(i):
            z=x+h*i
            return math.exp(-z*z/2)/math.sqrt(2*math.pi)
        return h/3*(f(0)+f(n)+math.fsum((4 if i%2 else 2)*f(i) for i in range(1,n)))
    def num(label,fn,want,rtol=1e-12):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0,rtol=rtol)
    for label,fn,want in [
        ('E1 Bernoulli event',lambda:m.bernoulli_pmf(1,.02),F('.02')),
        ('E2 Bernoulli complement',lambda:m.bernoulli_pmf(0,.02),F('.98')),
        ('E5 binomial zero',lambda:m.binomial_pmf(0,10,.1),F('.9')**10),
        ('E6 binomial one',lambda:m.binomial_pmf(1,10,.1),F('.9')**9),
        ('E7 binomial two',lambda:m.binomial_pmf(2,4,.25),F('.2109375')),
        ('E10 any default',lambda:1-m.binomial_pmf(0,10,.1),1-F('.9')**10),
        ('E11 Poisson zero',lambda:m.poisson_pmf(0,2),math.exp(-2)),
        ('E12 Poisson one',lambda:m.poisson_pmf(1,2),2*math.exp(-2)),
        ('E16 uniform interval',lambda:m.uniform_cdf(5,0,10)-m.uniform_cdf(2,0,10),F('.3')),
        ('E20 exponential tail',lambda:1-m.exponential_cdf(2,.5),math.exp(-1)),
        ('E21 normal center',lambda:m.normal_cdf(0),F('.5')),
        ('E22 normal symmetry',lambda:m.normal_cdf(-1),.15865525393145705),
        ('F121 binomial center n=1100',lambda:m.binomial_pmf(550,1100,.5),F(math.comb(1100,550),2**1100)),
        ('F121 uniform huge symmetric endpoints',lambda:m.uniform_cdf(0,-1e308,1e308),F('.5')),
        ('F121 standardize without premature overflow',lambda:m.normal_cdf(1e308,-1e308,1e308),.9772498680518208),
    ]:num(label,fn,want)
    num('F121 normal left tail at -10',lambda:m.normal_cdf(-10),normal_tail(10),1e-9)
    for label,fn in [
        ('invalid binomial count',lambda:m.binomial_pmf(0,-1,.1)),
        ('invalid probability',lambda:m.bernoulli_pmf(1,True)),
        ('F121 oversized probability rejected',lambda:m.bernoulli_pmf(1,10**400)),
        ('invalid rate',lambda:m.poisson_pmf(0,0)),
        ('invalid uniform endpoints',lambda:m.uniform_cdf(1,2,2)),
        ('invalid normal sigma',lambda:m.normal_cdf(0,0,0)),
        ('invalid simulation count',lambda:m.simulate_defaults(4,.1,0)),
    ]:reject(label,fn)
    points=Counter()
    for bits in product((0,1),repeat=10):
        points[sum(bits)] += 9**bits.count(0)
    for k in range(11):num(f'project binomial mass {k}',lambda:m.binomial_pmf(k,10,.1),F(points[k],10**10))
    ck('project integer path normalization and moments',sum(points.values())==10**10
       and sum(k*v for k,v in points.items())==10**10
       and sum((k-1)**2*v for k,v in points.items())==9*10**9)
    poisson=[math.exp(-1)]
    for k in range(1,11):poisson.append(poisson[-1]/k)
    ck('project Poisson recurrence through count 10',all(math.isclose(m.poisson_pmf(k,1),v,rel_tol=1e-12) for k,v in enumerate(poisson)))
    rng=Random(42); expected=[]
    for _ in range(20000):
        bits=[rng.random() for _ in range(10)]
        expected.append(len([x for x in bits if x<.1]))
    actual=m.simulate_defaults(10,.1,20000,42); counts=Counter(actual)
    ck('project seeded replay and reproducibility',actual==expected and actual==m.simulate_defaults(10,.1,20000,42))
    ck('project empirical count probabilities versus exact',all(abs(counts[k]/20000-points[k]/10**10)<.015 for k in points))
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(trials=20000,seed=42,empirical_counts=dict(sorted(counts.items())),
                                 mean=sum(actual)/20000,poisson_zero=poisson[0],binomial_zero=points[0]/10**10))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
