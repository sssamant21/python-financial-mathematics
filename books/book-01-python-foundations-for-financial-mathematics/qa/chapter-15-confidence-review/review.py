"""Section 15.8 exact confidence lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.08-confidence-intervals.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1508-') as tmp:
        Path(tmp,'confidence_intervals.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['confidence_intervals.py']),('isolated import',['-c','import confidence_intervals']),('exact compilation',['-m','compileall','-q','confidence_intervals.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['confidence_intervals.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('confidence_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    import random
    from decimal import Decimal as D, localcontext
    from itertools import combinations,product
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    def var(v):
        n=len(v);v=[F(str(x)) for x in v]
        return sum((a-b)**2 for a,b in combinations(v,2))/(n*(n-1))
    x=[.01,.02,.03];z=F('1.959963984540054');tc=F('4.302652729911275')
    se=root(F(1,30000))
    with localcontext() as ctx:
        ctx.prec=80
        normal=[D('.02')-D(str(float(z)))*se,D('.02')+D(str(float(z)))*se]
        tci=[D('.02')-D(str(float(tc)))*se,D('.02')+D(str(float(tc)))*se]
    num('E1 mean',lambda:m.sample_mean_se(x)[0],F(1,50))
    num('E2/E3 standard error',lambda:m.sample_mean_se(x)[1],se)
    for i in [0,1]:
        num('E4/E5 normal endpoint '+str(i),lambda i=i:m.normal_approx_mean_ci(x)[i],normal[i])
        num('E8/E9 t endpoint '+str(i),lambda i=i:m.t_mean_ci(x,float(tc))[i],tci[i])
    ck('E10 t wider than normal',float(tci[1]-tci[0])>float(normal[1]-normal[0]))
    # For df=2, CDF(t)=1/2+t/(2 sqrt(t^2+2)); solve CDF=.975.
    close('E6/E7 independent df2 t critical',float(tc),root(F(2)*F(19,20)**2/(1-F(19,20)**2)),atol=5e-9,rtol=0)
    ck('E13 alpha tails',F(1,20)/2==F(1,40))
    num('E17 type7 median',lambda:m.percentile([1,2,3],.5),2)
    num('type7 nonintegral rank',lambda:m.percentile([0,10,20,30],.25),F(15,2))
    rng=random.Random(42);draws=[rng.choices(x,k=3) for _ in range(2000)]
    estimates=sorted(sum(F(str(v)) for v in d)/3 for d in draws)
    def q(p):
        h=(len(estimates)-1)*p;j=h.numerator//h.denominator
        return estimates[j] if h==j else (1-(h-j))*estimates[j]+(h-j)*estimates[j+1]
    for i,want in enumerate([q(F(1,40)),q(F(39,40))]):num('project exact 2000-draw percentile endpoint '+str(i),lambda i=i:m.bootstrap_percentile_ci(x,2000,.05,42)[i],want)
    # Wilson: endpoints invert n(p_hat-p)^2 <= z^2 p(1-p).
    def wilson_root(successes,trials):
        ph=F(successes,trials);z2=z*z;a=trials+z2;b=2*successes+z2;c=F(successes*successes,trials)
        with localcontext() as ctx:
            ctx.prec=80
            disc=root(b*b-4*a*c);bd=D(b.numerator)/D(b.denominator);ad=D(a.numerator)/D(a.denominator)
            return [(bd-disc)/(2*ad),(bd+disc)/(2*ad)]
    for successes in [0,3,10]:
        want=wilson_root(successes,10)
        for i in [0,1]:num('E18/E19 Wilson '+str((successes,i)),lambda successes=successes,i=i:m.wilson_proportion_ci(successes,10)[i],want[i])
    for label,fn,want in [
        ('F134 large constant mean',lambda:m.sample_mean_se([1e308]*3)[0],1e308),
        ('F134 exact constant SE',lambda:m.sample_mean_se([.05]*3)[1],0),
        ('F134 integer spread SE',lambda:m.sample_mean_se([10**18,10**18+2])[1],1),
        ('F134 tiny SE',lambda:m.sample_mean_se([0,2e-200])[1],1e-200),
        ('F134 large reportable interval lower',lambda:m.normal_approx_mean_ci([-1e308,1e308],1)[0],-1e308),
        ('F134 stable extreme interpolation',lambda:m.percentile([-1e308,1e308],.5),0),
        ('F134 extreme endpoint',lambda:m.percentile([-1e308,1e308],0),-1e308),
        ('F134 large constant bootstrap',lambda:m.bootstrap_percentile_ci([1e308]*3,2)[0],1e308),
        ('F134 extreme Wilson zero lower',lambda:m.wilson_proportion_ci(0,10,1e200)[0],0),
        ('F134 extreme Wilson zero upper',lambda:m.wilson_proportion_ci(0,10,1e200)[1],1),
    ]:num(label,fn,want)
    for label,fn in [
        ('singleton rejected',lambda:m.sample_mean_se([1])),
        ('missing rejected',lambda:m.sample_mean_se([1,None])),
        ('boolean rejected',lambda:m.sample_mean_se([True,2])),
        ('nonfinite rejected',lambda:m.sample_mean_se([1,math.inf])),
        ('bad critical rejected',lambda:m.normal_approx_mean_ci(x,0)),
        ('bad t rejected',lambda:m.t_mean_ci(x,math.nan)),
        ('unsorted percentile rejected',lambda:m.percentile([2,1],.5)),
        ('bad probability rejected',lambda:m.percentile([1,2],math.nan)),
        ('bad alpha rejected',lambda:m.bootstrap_percentile_ci(x,2,1)),
        ('too few replicates rejected',lambda:m.bootstrap_percentile_ci(x,1)),
        ('bad success count rejected',lambda:m.wilson_proportion_ci(11,10)),
        ('F134 overflowing endpoint rejected',lambda:m.normal_approx_mean_ci([-1e308,1e308],2)),
        ('F134 collapsed positive-width interval rejected',lambda:m.normal_approx_mean_ci([10**18,10**18+2])),
    ]:reject(label,fn)
    ck('source input preserved',x==[.01,.02,.03])
    project=dict(source_returns=x,frequency='hypothetical daily',period_labels=[1,2,3],dates=None,units='decimal simple returns',estimand='fictional iid population mean',
        fixture_sha256=hashlib.sha256(json.dumps(x).encode()).hexdigest(),mean_se=m.sample_mean_se(x),normal=m.normal_approx_mean_ci(x),t=m.t_mean_ci(x,float(tc)),
        bootstrap=m.bootstrap_percentile_ci(x,2000,.05,42),bootstrap_seed=42,replicates=2000,bootstrap_quantile='type 7',wilson_zero=m.wilson_proportion_ci(0,10))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
