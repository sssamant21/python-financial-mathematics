"""Section 14.15 exact random number generation lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.15-random-number-generation-and-reproducibility.md'
    illustration,code=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1415-') as tmp:
        Path(tmp,'random_number_generation.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['random_number_generation.py']),('isolated import',['-c','import random_number_generation']),('exact compilation',['-m','compileall','-q','random_number_generation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['random_number_generation.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('rng_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from random import Random
    from collections import Counter
    from contextlib import redirect_stdout
    from io import StringIO
    from statistics import stdev
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    demo=StringIO()
    with redirect_stdout(demo):exec(compile(illustration,str(source),'exec'),{})
    rng=Random(42)
    ck('exact uniform illustration',demo.getvalue().strip()==str([rng.random() for _ in range(3)]))
    ck('E1 same seed',m.uniform_draws(100,42)==m.uniform_draws(100,42))
    ck('E2/E3 change seed and support',m.uniform_draws(100,42)!=m.uniform_draws(100,2026) and
       all(0<=u<1 for u in m.uniform_draws(100,42)))
    # Independently consume two uniforms per Box–Muller pair.
    rng=Random(42); ref=[]
    for _ in range(50):
        angle=math.tau*rng.random(); rad=math.sqrt(-2*math.log1p(-rng.random()))
        ref.extend([.01+.02*rad*math.cos(angle),.01+.02*rad*math.sin(angle)])
    ck('E6 normal draw replay',all(math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-15)
        for a,b in zip(m.normal_draws(100,42,.01,.02),ref)))
    num('E16 deterministic CRN shift',lambda:m.paired_mean_difference(100,42,.02),F('.02'))
    num('F124 tiny paired shift retained',lambda:m.paired_mean_difference(100,42,1e-20),F('1e-20'))
    num('F124 finite mean despite oversized sum',lambda:m.mean([1e308,1e308]),1e308)
    try:scaled=m.scenario_draws([-1,1],[1e308,1e308],100,42)
    except Exception as e:ck('F124 normalize large relative weights',False,exception=repr(e))
    else:ck('F124 normalize large relative weights',scaled==m.scenario_draws([-1,1],[1,1],100,42))
    try:big_manifest=m.manifest(42,100,[1e308,1e308])
    except Exception as e:ck('F124 manifest accepts same valid weights as sampler',False,exception=repr(e))
    else:ck('F124 manifest accepts same valid weights as sampler',big_manifest['configuration']['weights']==[1e308,1e308])
    for label,fn in [
        ('F124 reject infinite normal draw',lambda:m.normal_draws(100,42,1e308,1e308)),
        ('invalid seed',lambda:m.uniform_draws(3,True)),
        ('invalid weight mass',lambda:m.scenario_draws([1],[0],3,42)),
        ('mismatched inputs',lambda:m.scenario_draws([1,2],[1],3,42)),
        ('invalid sigma',lambda:m.normal_draws(3,42,sigma=-1)),
    ]:reject(label,fn)
    stats={}
    for n in (1000,20000):
        for seed in (42,2026):
            rng=Random(seed)
            ref=[]
            for _ in range(n):
                u=rng.random();ref.append(-20 if u<.25 else 5 if u<.75 else 30)
            got=m.scenario_draws([-20,5,30],[.25,.5,.25],n,seed)
            stress=m.scenario_draws([-18,7,32],[.25,.5,.25],n,seed)
            ck(f'project exact replay and paired stress n={n} seed={seed}',got==ref and
               m.scenario_draws([-20,5,30],[.25,.5,.25],n,seed)==got and all(b-a==2 for a,b in zip(got,stress)))
            mu=F(sum(ref),n)
            se=math.sqrt((F(sum(x*x for x in ref))-n*mu*mu)/(n*(n-1)))
            num(f'project mean n={n} seed={seed}',lambda:m.mean(got),mu)
            num(f'project sample SE n={n} seed={seed}',lambda:stdev(got)/math.sqrt(n),se)
            manifest=m.manifest(seed,n,[.25,.5,.25])
            canonical=f'{{"generator":"random.Random","n":{n},"seed":{seed},"weights":[0.25,0.5,0.25]}}'
            ck(f'project configuration digest n={n} seed={seed}',manifest['sha256']==hashlib.sha256(canonical.encode('utf-8')).hexdigest())
            stats[f'{n}:{seed}']=dict(counts=Counter(got),mean=float(mu),se=se,paired_shift=2,manifest=manifest)
    ck('project exact theoretical moments',F(-20+2*5+30,4)==5 and F(400+2*25+900,4)-25==F('312.5'))
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),illustration_sha256=hashlib.sha256(illustration).hexdigest(),commands=commands,checks=checks,
             workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(payoffs=[-20,5,30],stress='add 2 USD per hypothetical one-period payoff',runs=stats))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
