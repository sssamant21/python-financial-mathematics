"""Section 14.6 exact random variables lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.06-random-variables.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1406-') as tmp:
        Path(tmp,'random_variables.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['random_variables.py']),('isolated import',['-c','import random_variables']),('exact compilation',['-m','compileall','-q','random_variables.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['random_variables.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('random_variables');exec(compile(code,str(source),'exec'),m.__dict__)
    from collections import Counter
    from random import Random
    w={'bear':.25,'base':.5,'bull':.25}; x={'bear':-20,'base':5,'bull':30}
    y={key:2*value+1 for key,value in x.items()}
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E2 point mass',lambda:m.event_probability(w,x,lambda v:v==-20),F(1,4)),
        ('E3 mean',lambda:m.expected(w,x),5),
        ('E4 variance from second moment',lambda:m.variance(w,x),F(675,2)-25),
        ('E5 SD',lambda:math.sqrt(m.variance(w,x)),math.sqrt(312.5)),
        ('E6 negative',lambda:m.event_probability(w,x,lambda v:v<0),F(1,4)),
        ('E7 positive',lambda:m.event_probability(w,x,lambda v:v>0),F(3,4)),
        ('E8 transformed mean',lambda:m.expected(w,y),11),
        ('E9 transformed variance',lambda:m.variance(w,y),1250),
        ('E10 constant variance',lambda:m.variance(w,dict.fromkeys(w,7)),0),
        ('E12 Bernoulli mean',lambda:m.expected({'D':.02,'S':.98},{'D':1,'S':0}),F(1,50)),
        ('E13 default loss',lambda:m.expected({'D':.02,'S':.98},{'D':4000,'S':0}),80),
        ('E16 inclusive CDF',lambda:m.event_probability(w,x,lambda v:v<=5),F(3,4)),
        ('E17 strict CDF',lambda:m.event_probability(w,x,lambda v:v<5),F(1,4)),
        ('E18 threshold',lambda:m.event_probability(w,x,lambda v:v>=5),F(3,4)),
        ('E21 expected loss',lambda:m.expected({'D':.1,'S':.9},{'D':100,'S':0}),10),
        ('F115 distinct adjacent integer payoff variance',lambda:m.variance({'a':.5,'b':.5},{'a':10**18,'b':10**18+1}),F(1,4)),
        ('F115 zero-weight state cannot overflow variance',lambda:m.variance({'a':1,'b':0},{'a':0,'b':1e308}),0),
        ('F115 weighted variance despite oversized square',lambda:m.variance({'a':1,'b':1e-300},{'a':0,'b':1e300}),1e300),
    ]:num(label,fn,want)
    ck('E11 aggregation',m.distribution({'a':.2,'b':.3,'c':.5},{'a':0,'b':0,'c':1})=={0:.5,1:.5})
    ck('project PMF',m.distribution(w,x)=={-20:.25,5:.5,30:.25})
    ck('F115 normalized whole-space mass',m.event_probability({'a':.5,'b':.5000000000005},{'a':0,'b':1},lambda v:True)==1)
    for label,fn in [
        ('missing mapping',lambda:m.expected(w,{'bear':0})),
        ('extra mapping',lambda:m.expected(w,dict(x,other=0))),
        ('invalid weights',lambda:m.expected(dict(w,bear=.9),x)),
        ('nonfinite payoff',lambda:m.expected(w,dict(x,bear=math.inf))),
        ('F115 invalid oversized probability',lambda:m.expected({'a':10**400},{'a':1})),
        ('F115 unreportable variance',lambda:m.variance({'a':.5,'b':.5},{'a':-1e308,'b':1e308})),
    ]:reject(label,fn)
    rng=Random(42)
    ref=[]
    for _ in range(10000):
        u=rng.random()
        ref.append(-20 if u<.25 else 5 if u<.75 else 30)
    got=m.simulate(w,x,10000,42)
    ck('project all 10000 outcomes match inverse-CDF replay',got==ref and m.simulate(w,x,10000,42)==got)
    sample=F(sum(ref),10000)
    ck('project sample mean within four theoretical standard errors',abs(float(sample)-5)<4*math.sqrt(312.5/10000))
    ck('test-only source emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=12,historical_unique_methods_added=0,
             project_report=dict(seed=42,trials=10000,counts=Counter(ref),mean=str(sample),standard_error=math.sqrt(312.5/10000)))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
