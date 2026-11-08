"""Exact three-state source execution; analytical and shared-RNG probes separate."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.04-simulating-financial-outcomes.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
    def ck(label,fn,expected=True):
        try:actual=fn();ok=actual==expected
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,actual=actual,expected=expected,passed=bool(ok)))
    def num(label,fn,want):
        try:actual=fn();ok=math.isclose(actual,float(want),rel_tol=1e-12,abs_tol=0)
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,actual=actual,expected=str(want),passed=bool(ok),relative_tolerance=1e-12,absolute_tolerance=0))
    def rejects(fn):
        try:fn()
        except ValueError:return True
        except Exception as e:return type(e).__name__
        return False
    def sqrt(q):
        q=F(q)
        with localcontext() as c:c.prec=200;return (D(q.numerator)/D(q.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1804-') as tmp:
        Path(tmp,'financial_outcomes.py').write_bytes(code)
        for label,args in [('exact demo/tests',['financial_outcomes.py']),('quiet import',['-c','import financial_outcomes']),('compile',['-m','compileall','-q','financial_outcomes.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0
            ok=ok and (bool(methods and int(methods[1])==10 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr))
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('outcomes_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    probs=[F(1,4),F(1,2),F(1,4)];states=[80,100,120];mean=sum(p*x for p,x in zip(probs,states));var=sum(p*(x-mean)**2 for p,x in zip(probs,states))
    for label,fn,want in [('E1 sum probabilities',lambda:sum(probs),1),('E2 down profit',lambda:F(80)-100,-20),('E3 flat profit',lambda:F(100)-100,0),('E4 up profit',lambda:F(120)-100,20),('E5 down return',lambda:F(-20,100),F(-1,5)),('E6 up return',lambda:F(20,100),F(1,5)),('E7 model mean',lambda:mean,100),('E8 model profit',lambda:mean-100,0),('E9 strict loss probability',lambda:sum(p for p,x in zip(probs,states) if x<100),F(1,4)),('E10 nonpositive profit probability',lambda:sum(p for p,x in zip(probs,states) if x<=100),F(3,4)),('E14 model variance',lambda:var,200),('E15 model SD',lambda:sqrt(var),sqrt(200)),('E16 theoretical SE',lambda:sqrt(var/10000),sqrt(F(1,50))),('E17 loss indicator SE',lambda:sqrt(F(1,4)*F(3,4)/10000),sqrt(F(3,160000))),('E18 fourfold N SE factor',lambda:sqrt(var/40000)/sqrt(var/10000),F(1,2)),('E21 exact discount source',lambda:m.discount(100,.05),F(2000,21)),('E25 fee mean',lambda:sum(p*(x-2) for p,x in zip(probs,states)),98),('E26 fee loss probability',lambda:sum(p for p,x in zip(probs,states) if x-2<100),F(3,4))]:num(label,fn,want)
    for label,value,places,want in [('E15 printed SD',sqrt(200),4,14.1421),('E16 printed SE',sqrt(F(1,50)),5,.14142),('E17 printed loss SE',sqrt(F(3,160000)),5,.00433),('E21 printed PV',F(2000,21),4,95.2381)]:ck(label,lambda value=value,places=places,want=want:round(float(value),places)==want)
    sample=m.summarize([80,100,120,100,80],100)
    for key,want in [('mean_terminal',96),('mean_profit',-4),('loss_frequency',F(2,5)),('standard_error_mean',sqrt(56))]:num('E11-13 known sample '+key,lambda key=key:sample[key],want)
    ck('known sample loss count',lambda:sample['loss_count']==2)
    num('strict equality not loss',lambda:m.summarize([100,100],100)['loss_frequency'],0)
    num('constant sample SE',lambda:m.summarize([100,100],100)['standard_error_mean'],0)
    def injected(draws,fee=0):
        original=m.random.Random
        class Fixed:
            def __init__(self,seed):self.it=iter(draws)
            def random(self):return next(self.it)
        try:m.random.Random=Fixed;return m.simulate(len(draws),42,fee)
        finally:m.random.Random=original
    ck('E28 E29 source threshold boundary injection',lambda:injected([0,math.nextafter(.25,0),.25,math.nextafter(.75,0),.75,math.nextafter(1,0)])==[80,80,100,100,120,120])
    ck('E22-24 fee source mapping injection',lambda:injected([0,.5,.9],2)==[78,98,118])
    ck('fee paired same stream',lambda:m.simulate(100,42,2)==[x-2 for x in m.simulate(100,42)])
    ck('integer fee terminal identity',lambda:injected([0,.5,.9],10**18+1)==[80-(10**18+1),100-(10**18+1),120-(10**18+1)])
    ck('large integer mean identity',lambda:m.summarize([10**18,10**18+2],10**18)['mean_terminal']==10**18+1)
    num('small profit from large initial',lambda:m.summarize([10**18,10**18+2],10**18)['mean_profit'],1)
    ck('discount integer identity',lambda:m.discount(10**18+1,0)==10**18+1)
    num('tiny nonzero sample SD/SE',lambda:m.summarize([-1e-308,1e-308],0)['standard_error_mean'],F(1,10**308))
    num('reportable SE despite overflowing intermediate SD',lambda:m.summarize([-1.79e308,1.79e308],0)['standard_error_mean'],F(179*10**306))
    num('true discounted zero valid',lambda:m.discount(0,3),0)
    for label,fn in [('bad count',lambda:m.simulate(1,42)),('boolean seed',lambda:m.simulate(2,True)),('negative fee',lambda:m.simulate(2,42,-1)),('boolean fee',lambda:m.simulate(2,42,True)),('huge fee',lambda:m.simulate(2,42,10**1000)),('infinite fee',lambda:m.simulate(2,42,float('inf'))),('noniterable values',lambda:m.summarize(None,100)),('malformed values',lambda:m.summarize([None,1],100)),('bool values',lambda:m.summarize([True,1],100)),('nonfinite values',lambda:m.summarize([float('nan'),1],100)),('short sample',lambda:m.summarize([1],100)),('huge sample',lambda:m.summarize([10**1000,1],100)),('huge initial',lambda:m.summarize([1,2],10**1000)),('unreportable profit',lambda:m.summarize([1.79e308,1.79e308],-1.79e308)),('discount invalid rate',lambda:m.discount(100,-1)),('discount bool',lambda:m.discount(True,.05)),('discount huge int',lambda:m.discount(10**1000,0)),('discount underflow',lambda:m.discount(5e-324,3)),('discount overflow',lambda:m.discount(1.79e308,-.5))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    before=random.getstate();m.simulate(10,42);ck('global state preserved',lambda:random.getstate()==before)
    ck('seed replay',lambda:m.simulate(1000,42)==m.simulate(1000,42))
    runs=[]
    for seed,fee in [(42,0),(43,0),(42,2)]:
        n=10000;actual=m.simulate(n,seed,fee);summary=m.summarize(actual,100);r=random.Random(seed);us=[r.random() for _ in range(n)];counts=[sum(u<.25 for u in us),sum(.25<=u<.75 for u in us),sum(u>=.75 for u in us)];ys=[F(x-fee) for x in states];mu=sum(k*x for k,x in zip(counts,ys))/n;variance=sum(k*(x-mu)**2 for k,x in zip(counts,ys))/(n-1);losses=sum(k for k,x in zip(counts,ys) if x<100)
        num('count mean '+str((seed,fee)),lambda summary=summary:summary['mean_terminal'],mu)
        num('count profit '+str((seed,fee)),lambda summary=summary:summary['mean_profit'],mu-100)
        num('count SE '+str((seed,fee)),lambda summary=summary:summary['standard_error_mean'],sqrt(variance/n))
        num('count loss frequency '+str((seed,fee)),lambda summary=summary:summary['loss_frequency'],F(losses,n))
        ck('count loss number '+str((seed,fee)),lambda summary=summary,losses=losses:summary['loss_count']==losses)
        runs.append(dict(seed=seed,fee=fee,count=n,state_counts=counts,summary=summary,stream_sha256=hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest(),limit='count reference shares random.Random, only count/mapping/summary consistency established'))
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),generator='random.Random / Mersenne Twister',commands=commands,checks=checks,runs=runs,counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=10,new_historical_methods=0),model=dict(initial_cost=100,horizon='one year',units='fictional common currency',states=states,probabilities=['1/4','1/2','1/4'],fee_timing='terminal, paid once',discount='constant annual effective 5 percent; no calibrated probability measure or market-consistent price claim'),limits='Analytical probabilities/moments independent; seeded count replay and boundary injection are supplemental. No generator independence, confidence interval coverage, rare-event, platform or independent model acceptance.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
