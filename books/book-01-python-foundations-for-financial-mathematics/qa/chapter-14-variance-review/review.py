"""Section 14.10 exact variance lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.10-variance-and-standard-deviation.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1410-') as tmp:
        Path(tmp,'variance_and_standard_deviation.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['variance_and_standard_deviation.py']),('isolated import',['-c','import variance_and_standard_deviation']),('exact compilation',['-m','compileall','-q','variance_and_standard_deviation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['variance_and_standard_deviation.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('variance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from itertools import combinations, product
    d={-20:.25,5:.5,30:.25}
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    moment=F(400+2*25+900,4); mu=F(-20+2*5+30,4)
    for label,fn,want in [
        ('E1 mean',lambda:m.mean(d),mu),('E2/E5 variance',lambda:m.variance(d),moment-mu**2),
        ('E3 standard deviation',lambda:m.standard_deviation(d),math.sqrt(312.5)),
        ('E6 constant',lambda:m.variance({8:1}),0),
        ('E7 shift',lambda:m.variance(m.transformed(d,1,10)),312.5),
        ('E8 scale',lambda:m.variance(m.transformed(d,2,0)),1250),
        ('E9 reversal',lambda:m.variance(m.transformed(d,-1,0)),312.5),
        ('E10/project transformed SD',lambda:m.standard_deviation(m.transformed(d,2,10)),math.sqrt(1250)),
        ('project transformed mean',lambda:m.mean(m.transformed(d,2,10)),20),
        ('E11 Bernoulli',lambda:m.variance({0:.8,1:.2}),F('.16')),
        ('E13 population',lambda:m.population_variance([1,2,3]),F(2,3)),
        ('E14 sample',lambda:m.sample_variance([1,2,3]),1),
        ('E15 sample n=5',lambda:m.sample_variance([1,2,3,4,5]),F(5,2)),
        ('E18 two-point variance',lambda:m.variance({0:.5,10:.5}),25),
        ('project default variance',lambda:m.variance({0:.98,1:.02}),F('.0196')),
        ('F119 PMF integer spread',lambda:m.variance({10**18:.5,10**18+1:.5}),F(1,4)),
        ('F119 sample integer spread',lambda:m.sample_variance([10**18,10**18+1]),F(1,2)),
        ('F119 population integer spread',lambda:m.population_variance([10**18,10**18+1]),F(1,4)),
        ('F119 transform preserves spread',lambda:m.variance(m.transformed({0:.5,1:.5},1.,1e18)),F(1,4)),
        ('F119 SD despite overflowing variance',lambda:m.standard_deviation({-1e200:.5,1e200:.5}),1e200),
        ('F119 SD despite underflowing variance',lambda:m.standard_deviation({-1e-200:.5,1e-200:.5}),1e-200),
        ('F119 zero-weight atom',lambda:m.variance({7:1,1e308:0}),0),
    ]:num(label,fn,want)
    ck('F119 normalized accepted weights',m.mean({100:.5,101:.5000000000005})==float((50+101*F('.5000000000005'))/F('1.0000000000005')))
    for label,fn in [
        ('E24 invalid weights',lambda:m.variance({0:.6,1:.6})),
        ('nonfinite outcome',lambda:m.variance({float('inf'):1})),
        ('short sample',lambda:m.sample_variance([1])),
        ('F119 unreportable variance',lambda:m.variance({-1e200:.5,1e200:.5})),
    ]:reject(label,fn)
    pairs=[(2*u,u+2*v+2*w) for u,v,w in product((-1,1),repeat=3)]
    def pmf(values):
        return {x:values.count(x)/len(values) for x in set(values)}
    xx,yy=map(list,zip(*pairs))
    for label,values,want in [('X',xx,4),('Y',yy,9),('X+Y',[x+y for x,y in pairs],17),('X-Y',[x-y for x,y in pairs],9)]:
        num('project covariance fixture '+label,lambda:m.variance(pmf(values)),want)
    ck('project direct covariance and E22 perfect hedge',sum(x*y for x,y in pairs)==16 and m.variance({0:1})==0)
    ck('project empirical pairwise identity',sum((x-y)**2 for x,y in combinations([1,2,3],2))==6)
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(second_moment=str(moment),covariance_fixture=pairs,units='dollars and dollars squared; indicator variance dimensionless'))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
