"""Section 14.13 exact normal distribution lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.13-normal-distribution.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1413-') as tmp:
        Path(tmp,'normal_distribution.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['normal_distribution.py']),('isolated import',['-c','import normal_distribution']),('exact compilation',['-m','compileall','-q','normal_distribution.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['normal_distribution.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('normal_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from random import Random
    from statistics import mean, stdev
    def area(a,b,n=4096):
        h=(b-a)/n
        def density(i):
            x=a+i*h
            return math.exp(-x*x/2)/math.sqrt(2*math.pi)
        return h/3*(density(0)+density(n)+math.fsum((4 if i%2 else 2)*density(i) for i in range(1,n)))
    def left(x):
        return .5 + area(0,x) if x>=0 else .5 - area(x,0)
    lo,hi=1.,2.
    for _ in range(42):
        mid=(lo+hi)/2
        if left(mid)<.95:lo=mid
        else:hi=mid
    z95=(lo+hi)/2
    def num(label,fn,want,rtol=1e-10):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0,rtol=rtol)
    for label,fn,want in [
        ('E1 origin density',lambda:m.pdf(0),1/math.sqrt(2*math.pi)),
        ('E2 center CDF',lambda:m.cdf(0),.5),
        ('E3/E4 one sigma CDF',lambda:m.cdf(1),left(1)),
        ('E5 one sigma survival',lambda:m.survival(1),left(-1)),
        ('E6 interval one SD',lambda:m.interval(-1,1),area(-1,1)),
        ('E7 interval two SD',lambda:m.interval(-2,2),area(-2,2)),
        ('E8 interval three SD',lambda:m.interval(-3,3),area(-3,3)),
        ('E10 nonstandard CDF',lambda:m.cdf(12,10,2),left(1)),
        ('E11 nonstandard tail',lambda:m.survival(12,10,2),left(-1)),
        ('E12 nonstandard interval',lambda:m.interval(8,12,10,2),area(-1,1)),
        ('E13 median',lambda:m.quantile(.5,10,2),10),
        ('E15 upper quantile',lambda:m.quantile(.95),z95),
        ('E16 lower quantile',lambda:m.quantile(.05),-z95),
        ('E20 loss VaR',lambda:m.loss_var(.01,.02,.95,100000),100000*(.02*z95-.01)),
        ('E21 negative unfloored VaR',lambda:m.loss_var(.1,.02,.95,100000),100000*(.02*z95-.1)),
        ('project probability of nonpositive return',lambda:m.cdf(0,.01,.02),left(-.5)),
        ('project probability of return at or below -3%',lambda:m.cdf(-.03,.01,.02),left(-2)),
        ('project 5th percentile',lambda:m.quantile(.05,.01,.02),.01-.02*z95),
        ('project 95th percentile',lambda:m.quantile(.95,.01,.02),.01+.02*z95),
        ('F122 far right interval',lambda:m.interval(10,11),area(10,11)),
        ('F122 extreme finite standardization',lambda:m.cdf(1e308,-1e308,1e308),left(2)),
        ('F122 median when old bracket overflows',lambda:m.quantile(.5,0,1e308),0),
        ('F122 scaled VaR retains a finite result',lambda:m.loss_var(-1e308,1e308,.95,.1),1e307*(1+z95)),
    ]:num(label,fn,want)
    q=m.quantile(1e-50)
    num('F122 lower quantile below old bracket via quadrature',lambda:area(-q,-q+4,32768),1e-50,1e-9)
    for label,fn in [
        ('invalid sigma',lambda:m.pdf(0,sigma=0)),
        ('invalid confidence',lambda:m.loss_var(0,1,1,100)),
        ('invalid exposure',lambda:m.loss_var(0,1,.95,-1)),
        ('invalid count',lambda:m.simulate(0)),
        ('F122 boolean observation',lambda:m.pdf(True)),
        ('F122 unreportable quantile',lambda:m.quantile(.99,1e308,1e308)),
        ('F122 unreportable simulated output',lambda:m.simulate(100,1e308,1e308,42)),
    ]:reject(label,fn)
    data=m.simulate(20000,.01,.02,42)
    rng=Random(42); reference=[]
    for _ in range(10000):
        angle=2*math.pi*rng.random()
        radius=math.sqrt(-2*math.log1p(-rng.random()))
        reference.extend([.01+.02*radius*math.cos(angle),.01+.02*radius*math.sin(angle)])
    ck('project seeded Box–Muller replay',data==m.simulate(20000,.01,.02,42) and len(data)==20000 and
       all(math.isclose(a,b,rel_tol=1e-10,abs_tol=2e-15) for a,b in zip(data,reference)))
    avg=mean(data); sd=stdev(data); q05=sorted(data)[999]
    ck('project simulated mean',abs(avg-.01)<4*.02/math.sqrt(20000),actual=avg)
    ck('project simulated SD',abs(sd-.02)<4*.02/math.sqrt(2*19999),actual=sd)
    q_se=.02*math.sqrt(.05*.95/20000)/(math.exp(-z95*z95/2)/math.sqrt(2*math.pi))
    ck('project nearest-rank 5th percentile',abs(q05-(.01-.02*z95))<4*q_se,actual=q05)
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(trials=20000,seed=42,mean=avg,sample_sd=sd,nearest_rank_q05=q05,quadrature_z95=z95,
                                 model='synthetic one-period decimal returns; unfloored loss in dollars'))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
