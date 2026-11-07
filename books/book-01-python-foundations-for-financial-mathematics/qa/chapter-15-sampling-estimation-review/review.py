"""Section 15.7 exact sampling lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.07-sampling-and-estimation.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1507-') as tmp:
        Path(tmp,'sampling_and_estimation.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['sampling_and_estimation.py']),('isolated import',['-c','import sampling_and_estimation']),('exact compilation',['-m','compileall','-q','sampling_and_estimation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['sampling_and_estimation.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('sampling_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    import random
    from decimal import Decimal as D, localcontext
    from itertools import combinations,product
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def variance(v):
        v=[F(str(x)) for x in v];n=len(v)
        return sum((a-b)**2 for a,b in combinations(v,2))/(n*(n-1))
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    x=[.01,.02,.03]
    for label,fn,want in [
        ('E4 mean',lambda:m.sample_mean(x),F(1,50)),
        ('E5 variance',lambda:m.sample_variance(x),F(1,10000)),
        ('E6 SD',lambda:math.sqrt(m.sample_variance(x)),F(1,100)),
        ('E7 iid SE',lambda:m.standard_error_mean(x),root(F(1,30000))),
        ('E9 FPC sample-SD convention',lambda:m.finite_population_correction(10,100),root(F(9,10))),
        ('E10 census',lambda:m.finite_population_correction(5,5),0),
        ('singleton census',lambda:m.finite_population_correction(1,1),0),
        ('F133 large constant mean',lambda:m.sample_mean([1e308]*3),1e308),
        ('F133 integer-offset variance',lambda:m.sample_variance([10**18,10**18+2]),2),
        ('F133 small SE before variance reporting',lambda:m.standard_error_mean([0,2e-200]),1e-200),
        ('F133 exact constant variance',lambda:m.sample_variance([.05]*3),0),
    ]:num(label,fn,want)
    population=[0,2,4,6];samples=list(combinations(population,2))
    means=[F(sum(v),2) for v in samples];true_design_variance=sum((v-3)**2 for v in means)/len(means)
    num('F133 finite-population enumerated design variance',lambda:sum(m.sample_variance(list(v))/2*m.finite_population_correction(2,4)**2 for v in samples)/len(samples),true_design_variance)
    p=list(range(20));chosen=m.sample_without_replacement(p,5,11)
    ck('E11 seeded without-replacement replay',chosen==random.Random(11).sample(p,5),actual=chosen)
    ck('E12 full census identities',sorted(m.sample_without_replacement(list(range(5)),5,42))==list(range(5)))
    ck('duplicate values may represent distinct units',m.sample_without_replacement([1,1,1],3,42)==[1,1,1])
    big=[10**18+i for i in range(3)]
    ck('F133 sampled integer identities preserved',sorted(m.sample_without_replacement(big,3,42))==big)
    estimates=m.bootstrap_means(x,1000,42);rng=random.Random(42)
    draws=[rng.choices(x,k=3) for _ in range(1000)]
    exact_means=[sum(F(str(v)) for v in z)/3 for z in draws]
    ck('E13/E14 all 1000 bootstrap means replayed',len(estimates)==1000 and all(math.isclose(a,float(b),rel_tol=1e-12,abs_tol=0) for a,b in zip(estimates,exact_means)),replicates=1000)
    ck('with-replacement repeated observation occurs',any(len(set(z))<3 for z in draws))
    want_se=root(variance(exact_means))
    # variance helper accepts Fraction via str; expected SE uses independent pairwise differences.
    num('project bootstrap SE exact seeded replay',lambda:m.bootstrap_standard_error(x,1000,42),want_se)
    num('constant bootstrap SE',lambda:m.bootstrap_standard_error([.05]*3,20,42),0)
    try:large=m.bootstrap_means([1e308]*3,2,42)
    except Exception as e:ck('F133 bootstrap large mean',False,exception=repr(e))
    else:ck('F133 bootstrap large mean',large==[1e308,1e308])
    larger=random.Random(31).choices([.01,.02,.03],k=12)
    num('project larger synthetic iid SE',lambda:m.standard_error_mean(larger),root(variance(larger)/12))
    dependent=[.01,.01,.01,.01,.03,.03,.03,.03]
    num('project dependent series descriptive mean',lambda:m.sample_mean(dependent),F(1,50))
    for label,fn in [
        ('singleton variance undefined',lambda:m.sample_variance([1])),
        ('empty rejected',lambda:m.sample_mean([])),
        ('E23 missing rejected',lambda:m.sample_mean([.01,None,.03])),
        ('nonfinite rejected',lambda:m.sample_mean([math.inf,1])),
        ('boolean rejected',lambda:m.sample_mean([True,1])),
        ('oversample rejected',lambda:m.sample_without_replacement([1,2],3)),
        ('bad replicate count rejected',lambda:m.bootstrap_means(x,0)),
        ('bootstrap SE requires two replicates',lambda:m.bootstrap_standard_error(x,1)),
        ('bad FPC sizes rejected',lambda:m.finite_population_correction(0,100)),
        ('F133 unreportable variance rejected',lambda:m.sample_variance([-1e308,1e308])),
    ]:reject(label,fn)
    ck('source inputs unchanged',x==[.01,.02,.03] and population==[0,2,4,6])
    project=dict(source_returns=x,period_labels=[1,2,3],dates=None,frequency='hypothetical daily',units='decimal simple returns',estimand='mean under fictional iid generating population, not future guaranteed return',
        seed=42,replicates=1000,fixture_sha256=hashlib.sha256(json.dumps(x).encode()).hexdigest(),mean=m.sample_mean(x),sample_variance=m.sample_variance(x),iid_se=m.standard_error_mean(x),
        bootstrap_means=estimates,bootstrap_se=m.bootstrap_standard_error(x,1000,42),exact_empirical_bootstrap_theoretical_se=str(root(F(1,45000))),
        larger_source='supplemental independent synthetic draws with random.Random(31).choices([.01,.02,.03],k=12)',larger_returns=larger,larger_iid_se=m.standard_error_mean(larger),
        dependent_fixture=dependent,dependent_fixture_scope='supplemental persistence example; dependence-aware uncertainty not implemented',
        fpc_design_variance=str(true_design_variance))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
