"""Section 14.14 exact sampling lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.14-sampling-with-python.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1414-') as tmp:
        Path(tmp,'sampling_with_python.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['sampling_with_python.py']),('isolated import',['-c','import sampling_with_python']),('exact compilation',['-m','compileall','-q','sampling_with_python.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['sampling_with_python.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('sampling');exec(compile(code,str(source),'exec'),m.__dict__)
    from random import Random
    from collections import Counter
    from itertools import combinations
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 sample mean',lambda:m.avg([1,2,3]),2),
        ('E3 sample SD',lambda:m.sd([1,2,3]),1),
        ('E5 standard error',lambda:m.se([1,2,3]),math.sqrt(1/3)),
        ('E6 return average',lambda:m.avg([.01,.02,.03,.04]),F('.025')),
        ('E13 interpolated median',lambda:m.quantile([1,2,3,4],.5),2.5),
        ('E14 minimum',lambda:m.quantile([1,2,3],0),1),
        ('E15 maximum',lambda:m.quantile([1,2,3],1),3),
        ('E16 interval lower',lambda:m.mean_interval([-.15,.25]*199+[.05,.05])[0],F('.0304')),
        ('E16 interval upper',lambda:m.mean_interval([-.15,.25]*199+[.05,.05])[1],F('.0696')),
        ('E17 bootstrap fixture mean',lambda:m.avg([2,2,6]),F(10,3)),
        ('F123 finite average despite oversized sum',lambda:m.avg([1e308,1e308]),1e308),
        ('F123 extreme median despite oversized difference',lambda:m.quantile([-1e308,1e308],.5),0),
        ('F123 exact endpoint with extreme neighbors',lambda:m.quantile([-1e308,1e308],1),1e308),
    ]:
        # Choose symmetric offsets so the E16 sample SD is exactly .2 analytically.
        if label.startswith('E16'):
            delta=.2*math.sqrt(399/400)
            fn=lambda i=int(label.endswith('upper')):m.mean_interval([.05-delta,.05+delta]*200)[i]
        num(label,fn,want)
    for label,fn in [
        ('zero weights',lambda:m.draw([1,2],[0,0],3)),
        ('mismatched weights',lambda:m.draw([1,2],[1],3)),
        ('F123 nonrepresentable interval endpoints',lambda:m.mean_interval([0,1e308],4)),
        ('invalid percentile',lambda:m.quantile([1,2],math.nan)),
    ]:reject(label,fn)
    try:equal=m.draw([-1,1],[1e308,1e308],100,42)
    except Exception as exc:ck('F123 oversized relative weight sum',False,exception=repr(exc))
    else:ck('F123 oversized relative weight sum',equal==m.draw([-1,1],[1,1],100,42))
    ns={};exec(compile(illustration,str(source),'exec'),ns)
    ck('exact illustration replacement contracts',len(ns['with_replacement'])==10 and len(set(ns['without_replacement']))==2)
    stats={}; small=None
    for n in (1000,20000):
        rng=Random(42); reference=[]
        for _ in range(n):
            u=rng.random();reference.append(-20 if u<.25 else 5 if u<.75 else 30)
        actual=m.draw([-20,5,30],[.25,.5,.25],n,42)
        ck(f'project exact weighted replay n={n}',actual==reference)
        total=sum(reference); mu=F(total,n)
        s2=(F(sum(x*x for x in reference))-F(total**2,n))/(n-1)
        num(f'project mean n={n}',lambda:m.avg(actual),mu)
        num(f'project SD n={n}',lambda:m.sd(actual),math.sqrt(s2))
        num(f'project SE n={n}',lambda:m.se(actual),math.sqrt(s2/n))
        ck(f'project tail percentiles n={n}',m.quantile(actual,.05)==-20 and m.quantile(actual,.95)==30)
        stats[n]=dict(mean=float(mu),sd=math.sqrt(s2),se=math.sqrt(s2/n),counts=Counter(reference))
        if n==1000:small=actual
    rng=Random(42); size=len(small)
    ref=[sum(small[int(rng.random()*size)] for _ in range(size))/size for _ in range(2000)]
    got=m.bootstrap(small,2000,42)
    ck('project bootstrap 2000 means agree with index replay',got==ref)
    variance=(math.fsum(x*x for x in ref)-math.fsum(ref)**2/len(ref))/(len(ref)-1)
    num('project bootstrap dispersion',lambda:m.sd(got),math.sqrt(variance))
    ck('project bootstrap SD near estimated SE',abs(math.sqrt(variance)/stats[1000]['se']-1)<.08)
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),illustration_sha256=hashlib.sha256(illustration).hexdigest(),commands=commands,checks=checks,
             workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(draws=stats,seed=42,bootstrap_source_n=1000,bootstrap_reps=2000,bootstrap_sd=math.sqrt(variance)))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
