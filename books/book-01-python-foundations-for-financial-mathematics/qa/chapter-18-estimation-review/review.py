"""Exact estimation source; independent arithmetic and supplemental spawned streams separate."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.08-monte-carlo-estimation.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
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
    def dec(q):
        q=F(q);return D(q.numerator)/D(q.denominator)
    def sqrt(q):
        with localcontext() as c:c.prec=200;return dec(q).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1808-') as tmp:
        Path(tmp,'monte_carlo_estimation.py').write_bytes(code)
        for label,args in [('exact demo/tests',['monte_carlo_estimation.py']),('quiet import',['-c','import monte_carlo_estimation']),('compile',['-m','compileall','-q','monte_carlo_estimation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==12 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('estimation_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    probs=[F(1,4),F(1,2),F(1,4)];states=[80,100,120];mu=sum(p*x for p,x in zip(probs,states));var=sum(p*(x-mu)**2 for p,x in zip(probs,states))
    for label,fn,want in [('E3 model mean',lambda:mu,100),('E4 model variance',lambda:var,200),('E5 model SD',lambda:sqrt(var),sqrt(200)),('E6 theoretical mean SE',lambda:sqrt(var/10000),sqrt(F(1,50))),('E11 model strict event probability',lambda:sum(p for p,x in zip(probs,states) if x<100),F(1,4)),('E13 indicator SE',lambda:sqrt(F(3,16)/10000),sqrt(F(3,160000))),('E15 discounted source mean',lambda:m.discount([100],.05)[0],F(2000,21)),('E16 discounted model SD',lambda:sqrt(200)/D('1.05'),sqrt(200)/D('1.05')),('E17 discounted theoretical SE',lambda:sqrt(F(1,50))/D('1.05'),sqrt(F(1,50))/D('1.05')),('E18 fourfold N factor',lambda:sqrt(F(1,4)),F(1,2)),('E19 inverse square factor',lambda:F(1)/F(1,2)**2,4),('E25 supplemental MSE example',lambda:F(9)+F(2)**2,13)]:num(label,fn,want)
    for label,value,places,want in [('printed SD',sqrt(200),4,14.1421),('printed mean SE',sqrt(F(1,50)),5,.14142),('printed event SE',sqrt(F(3,160000)),5,.00433),('printed discounted mean',F(2000,21),4,95.2381),('printed discounted SD',sqrt(200)/D('1.05'),4,13.4687),('printed discounted SE',sqrt(F(1,50))/D('1.05'),5,.13469),('printed sample SE',sqrt(F(400,3)),3,11.547)]:ck(label,lambda value=value,places=places,want=want:round(float(value),places)==want)
    plan=F(196,100)**2*200/F(1,2)**2;ck('E32 planning ceil3073.28 to3074',lambda:math.ceil(plan)==3074)
    for label,want in [('lower',F(1001,10)-F(196,100)*F(14142,100000)),('upper',F(1001,10)+F(196,100)*F(14142,100000))]:ck('E20 printed illustrative interval '+label,lambda label=label,want=want:round(float(want),3)==(99.823 if label=='lower' else 100.377))
    result=m.estimate_mean([80,100,120])
    for key,want in [('mean',100),('sample_sd',20),('standard_error',sqrt(F(400,3)))]:num('E7-10 known sample '+key,lambda key=key:result[key],want)
    for i,sign in [(0,-1),(1,1)]:num('known sample normal interval '+str(i),lambda i=i:result['normal_95_interval'][i],D(100)+D(sign)*D('1.96')*sqrt(F(400,3)))
    num('E12 equality excluded',lambda:m.event_frequency([100],100),0)
    num('single event observation allowed',lambda:m.event_frequency([80],100),1)
    num('E27 constant SE',lambda:m.estimate_mean([100,100])['standard_error'],0)
    ck('empty discount allowed',lambda:m.discount([],.05)==[])
    ck('constant integer interval identity',lambda:m.estimate_mean([10**18+1]*2)['normal_95_interval']==(10**18+1,10**18+1))
    ck('discount integer identity',lambda:m.discount([10**18+1],0)==[10**18+1])
    num('tiny nonzero sample SD',lambda:m.estimate_mean([-1e-308,1e-308])['sample_sd'],sqrt(F(2,10**616)))
    num('tiny nonzero sample SE',lambda:m.estimate_mean([-1e-308,1e-308])['standard_error'],F(1,10**308))
    ck('one-pass estimator observations',lambda:m.estimate_mean(iter([80,100,120]))['mean']==100)
    for label,fn in [('count1',lambda:m.draw_payoffs(1,42)),('bool count',lambda:m.draw_payoffs(True,42)),('bool seed',lambda:m.draw_payoffs(2,True)),('estimate noniterable',lambda:m.estimate_mean(None)),('estimate short',lambda:m.estimate_mean([1])),('estimate bool',lambda:m.estimate_mean([True,1])),('estimate huge',lambda:m.estimate_mean([10**1000,1])),('estimate malformed',lambda:m.estimate_mean([None,1])),('estimate nonfinite',lambda:m.estimate_mean([float('nan'),1])),('unreportable SD',lambda:m.estimate_mean([-1.79e308,1.79e308])),('unreportable interval',lambda:m.estimate_mean([-1e308,1e308])),('event noniterable',lambda:m.event_frequency(None,100)),('event empty',lambda:m.event_frequency([],100)),('event huge observation',lambda:m.event_frequency([10**1000],100)),('event huge threshold',lambda:m.event_frequency([100],10**1000)),('event bool threshold',lambda:m.event_frequency([100],True)),('discount noniterable',lambda:m.discount(None,.05)),('discount huge value',lambda:m.discount([10**1000],0)),('discount huge rate',lambda:m.discount([100],10**1000)),('discount invalid rate',lambda:m.discount([100],-1)),('discount underflow',lambda:m.discount([5e-324],3)),('discount overflow',lambda:m.discount([1.79e308],-.5))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    before=random.getstate();m.draw_payoffs(10,42);ck('local RNG preserves global state',lambda:random.getstate()==before)
    ck('source seed replay',lambda:m.draw_payoffs(100,42)==m.draw_payoffs(100,42))
    def inspect(label,values):
        q=[F(str(x)) for x in values];n=len(q);mean=sum(q)/n;variance=sum((x-mean)**2 for x in q)/(n-1);sd=sqrt(variance);se=sqrt(variance/n);actual=m.estimate_mean(values)
        for key,want in [('mean',mean),('sample_sd',sd),('standard_error',se)]:num(label+' independent sample '+key,lambda key=key:actual[key],want)
        for i,sgn in [(0,-1),(1,1)]:num(label+' independent interval '+str(i),lambda i=i:actual['normal_95_interval'][i],dec(mean)+D(sgn)*D('1.96')*se)
        num(label+' strict event count',lambda:m.event_frequency(values,100),F(sum(x<100 for x in q),n))
        return dict(count=n,estimate=actual,event_frequency=m.event_frequency(values,100),standardized_error=(actual['mean']-100)/actual['standard_error'] if actual['standard_error'] else None,observations_sha256=hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest())
    runs=[]
    for count,seed in [(10000,42),(10000,43),(1000,42)]:
        vals=m.draw_payoffs(count,seed);r=inspect('source '+str((count,seed)),vals);r.update(seed=seed,kind='exact-source sampler supplemental invocation; changing seed not proof of independence',support_counts=[vals.count(x) for x in states]);discounted=m.discount(vals,.05);d=m.estimate_mean(discounted);num('discounted sample mean '+str((count,seed)),lambda d=d:d['mean'],F(str(r['estimate']['mean']))/F(105,100));num('discounted sample SE '+str((count,seed)),lambda d=d:d['standard_error'],F(str(r['estimate']['standard_error']))/F(105,100));r['discounted_estimate']=d;runs.append(r)
    import numpy as np
    children=np.random.SeedSequence(2026).spawn(3);spawned=[]
    for i,child in enumerate(children):
        rng=np.random.default_rng(child);u=rng.random(10000);vals=np.where(u<.25,80,np.where(u<.75,100,120)).tolist();r=inspect('supplemental NumPy child '+str(i),vals);r.update(worker=i,spawn_key=list(child.spawn_key),kind='supplemental NumPy PCG64 sampler, source estimator; designed spawning, not independent statistical certification');spawned.append(r)
    # Supplemental dependence design examples, no source antithetic/comparison API.
    ck('E30 pair averages constant in illustration',lambda:[F(a+b,2) for a,b in [(80,120),(120,80),(100,100)]]==[100]*3)
    ck('E31 paired differences constant in illustration',lambda:[b-a for a,b in [(80,82),(100,102),(120,122)]]==[2]*3)
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),generator='source random.Random / Mersenne Twister',numpy=np.__version__,supplemental_bit_generator='PCG64',source_runs=runs,supplemental_spawn_parent=2026,supplemental_spawned_runs=spawned,planning_exact_N=str(plan),commands=commands,checks=checks,counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=12,new_historical_methods=0),model=dict(payoffs=states,probabilities=['1/4','1/2','1/4'],estimand='expected fictional one-year payoff and P(X<100)',units='common fictional currency',discount='constant annual effective5%; no calibrated probability measure/market-price claim'),limits='Arithmetic consistency and selected runs only. Source seed42 count1000 is a prefix of count10000, not independent. Spawned NumPy samplers are supplemental, not source random.Random execution or a proof of independence/nominal coverage. No binomial interval, sequential stopping or independent model acceptance; F28/F32/F165 open.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
