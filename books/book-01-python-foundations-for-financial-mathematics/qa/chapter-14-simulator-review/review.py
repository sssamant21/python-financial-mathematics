"""Section 14.16 exact probability simulator lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.16-chapter-project-financial-probability-simulator.md'
    code,driver=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1416-') as tmp:
        Path(tmp,'financial_probability_simulator.py').write_bytes(code)
        Path(tmp,'run_simulator.py').write_bytes(driver)
        for label,args in [('exact unit tests',['financial_probability_simulator.py']),
                           ('exact compilation',['-m','compileall','-q','financial_probability_simulator.py']),
                           ('driver compilation',['-m','compileall','-q','run_simulator.py']),
                           ('isolated import',['-c','import financial_probability_simulator']),
                           ('exact driver',['run_simulator.py']),('exact driver replay',['run_simulator.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=90)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact unit tests' else not p.stderr and (bool(p.stdout) if 'driver' in label and 'compilation' not in label else not p.stdout)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('simulator');exec(compile(code,str(source),'exec'),m.__dict__)
    from random import Random
    from collections import Counter
    from ast import literal_eval
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    outs=[-20,5,30]; w=[.25,.5,.25]
    for label,fn,want in [
        ('E2 expectation',lambda:m.exact_moments(outs,w)[0],5),
        ('E4 variance',lambda:m.exact_moments(outs,w)[1],F(675,2)-25),
        ('E5 SD',lambda:m.exact_moments(outs,w)[2],math.sqrt(312.5)),
        ('E9 stress mean',lambda:m.exact_moments([-18,7,32],w)[0],7),
        ('E10 translation variance',lambda:m.exact_moments([-18,7,32],w)[1],312.5),
        ('E11 scale mean',lambda:m.exact_moments([-40,10,60],w)[0],10),
        ('E12 scale variance',lambda:m.exact_moments([-40,10,60],w)[1],1250),
        ('E21 median',lambda:m.empirical_quantile([1,2,3,4],.5),2.5),
        ('E22 sample SE',lambda:m.summarize([1,2,3])['se'],math.sqrt(1/3)),
        ('F125 extreme median',lambda:m.empirical_quantile([-1e308,1e308],.5),0),
        ('F125 large mean',lambda:m.summarize([1e308,1e308])['mean'],1e308),
        ('F125 integer variance spread',lambda:m.exact_moments([10**18,10**18+1],[.5,.5])[1],F(1,4)),
        ('F125 zero-weight outcome',lambda:m.exact_moments([0,1e308],[1,0])[1],0),
    ]:num(label,fn,want)
    ck('F125 near-unit mass normalized',m.exact_moments([5,5],[.5,.5000000000005])[0]==5)
    ck('F125 manifest retains generator inputs',m.manifest(42,20,iter(outs),iter(w))==m.manifest(42,20,outs,w))
    for label,fn in [
        ('F125 nonfinite stressed payoff rejected',lambda:m.paired_stress([1e308,1e308],1e308)),
        ('invalid probabilities',lambda:m.simulate(outs,[.5,.5,.5],20,42)),
        ('invalid bootstrap count',lambda:m.bootstrap_mean_se([1,2],1,42)),
        ('invalid default count',lambda:m.default_count_simulation(0,.1,20,42)),
    ]:reject(label,fn)
    def moments(xs):
        n=len(xs); total=sum(xs)
        var=(F(sum(x*x for x in xs))-F(total*total,n))/(n-1)
        return dict(mean=total/n,sample_sd=math.sqrt(var),se=math.sqrt(var/n),
                    p05=-20,p95=30,loss_probability=xs.count(-20)/n)
    stats={}
    for n in (1000,20000,40000):
        rng=Random(42)
        ref=[-20 if u<.25 else 5 if u<.75 else 30 for u in (rng.random() for _ in range(n))]
        got=m.simulate(outs,w,n,42)
        ck(f'phase D weighted replay {n}',got==ref)
        summary=m.summarize(got); expected=moments(ref)
        for k in expected:close(f'phase D summary {n} {k}',summary[k],expected[k],atol=0)
        stats[n]=summary
        if n==20000:main=ref
    ck('phase D stress keeps pairing',m.paired_stress(main,2)==[x+2 for x in main])
    rng=Random(43); size=len(main)
    bootstrap=[F(sum(main[int(rng.random()*size)] for _ in range(size)),size) for _ in range(500)]
    total=sum(bootstrap)
    boot_sd=math.sqrt((sum(x*x for x in bootstrap)-total*total/500)/499)
    rng=Random(44)
    defaults=[sum(u<.1 for u in [rng.random() for _ in range(10)]) for _ in range(20000)]
    ck('phase D default count replay',m.default_count_simulation(10,.1,20000,44)==defaults)
    ck('phase C driver stdout exactly repeats',commands[-2]['stdout']==commands[-1]['stdout'])
    report=dict(line.split(': ',1) for line in commands[-2]['stdout'].splitlines())
    ck('phase B exact output',literal_eval(report['Exact moments'])==(5.,312.5,math.sqrt(312.5)))
    ck('phase C driver simulation summary',literal_eval(report['Simulation'])==stats[20000])
    close('phase D driver bootstrap SD',float(report['Bootstrap SE']),boot_sd,atol=0)
    close('phase D driver average defaults',float(report['Average defaults']),F(sum(defaults),20000),atol=0)
    meta=literal_eval(report['Manifest'])
    raw='{"outcomes":[-20.0,5.0,30.0],"prng":"random.Random","probabilities":[0.25,0.5,0.25],"seed":42,"trials":20000}'
    ck('phase C driver configuration digest and change',meta['sha256']==hashlib.sha256(raw.encode()).hexdigest() and
       m.manifest(43,20000,m.PAYOFFS,m.WEIGHTS)['sha256']!=meta['sha256'])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),driver_sha256=hashlib.sha256(driver).hexdigest(),commands=commands,checks=checks,
             workflow_records=1,local_prompt_records=24,acceptance_lab_phase_records=5,historical_unique_methods_added=0,
             project_report=dict(stats=stats,bootstrap_sd=boot_sd,default_counts=Counter(defaults),seed=42))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
