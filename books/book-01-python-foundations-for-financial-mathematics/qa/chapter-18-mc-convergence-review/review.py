"""Exact nested-prefix listing; rational expectations and supplemental streams separated."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.09-convergence.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
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
    with tempfile.TemporaryDirectory(prefix='book1-1809-') as tmp:
        Path(tmp,'monte_carlo_convergence.py').write_bytes(code)
        for label,args in [('exact demo/tests',['monte_carlo_convergence.py']),('quiet import',['-c','import monte_carlo_convergence']),('compile',['-m','compileall','-q','monte_carlo_convergence.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==12 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('convergence_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    probs=[F(1,4),F(1,2),F(1,4)];states=[80,100,120];mean=sum(p*x for p,x in zip(probs,states));variance=sum(p*(x-mean)**2 for p,x in zip(probs,states))
    num('E4 exact model mean',lambda:mean,100);num('E5 exact model variance',lambda:variance,200)
    ck('E6 printed SD',lambda:round(float(sqrt(200)),4)==14.1421)
    for n,want in [(100,1.41421),(400,.70711),(10000,.14142),(40000,.07071)]:
        num('source theoretical SE '+str(n),lambda n=n:m.theoretical_se(float(sqrt(200)),n),sqrt(F(200,n)))
        ck('printed table SE '+str(n),lambda n=n,want=want:round(float(sqrt(F(200,n))),5)==want)
    ck('E7 printed exercise SE100',lambda:round(float(sqrt(2)),4)==1.4142)
    ck('E8 printed exercise SE400',lambda:round(float(sqrt(F(1,2))),4)==.7071)
    num('E10 theoretical fourfold factor',lambda:m.theoretical_se(10,400)/m.theoretical_se(10,100),F(1,2))
    num('E11 inverse squared factor',lambda:F(1)/F(1,2)**2,4)
    num('E19 supplemental discounted expectation',lambda:F(100)/F(105,100),F(2000,21))
    ck('printed discounted expectation',lambda:round(float(F(2000,21)),4)==95.2381)
    num('E21 rare event expected count',lambda:F(1,1000)*1000,1)
    with localcontext() as c:c.prec=100;no_events=(D(999)/1000)**1000
    ck('E22 zero-event probability nonzero',lambda:D('.36')<no_events<D('.38'))
    num('E23 theoretical event SE not plugin zero',lambda:sqrt(F(1,1000)*F(999,1000)/1000),sqrt(F(999,10**9)))
    known=m.summary([80,100,120],100)
    num('known sample mean',lambda:known['mean'],100);num('known sample SE',lambda:known['estimated_se'],sqrt(F(400,3)));num('known absolute error',lambda:known['absolute_error'],0)
    num('E32 constant SE',lambda:m.summary([100,100],100)['estimated_se'],0)
    ck('E35 theoretical SE count1 allowed',lambda:m.theoretical_se(10,1)==10)
    ck('nested errors need not improve',lambda:[r['absolute_error'] for r in m.prefix_study([80,120,80,80],[2,4],100)]==[0,10])
    ck('only used prefix observations validated',lambda:m.prefix_study([80,100,None],[2],100)[0]['mean']==90)
    ck('one-pass samples and sizes',lambda:[x['count'] for x in m.prefix_study(iter([80,100,120,100]),iter([2,4]),100)]==[2,4])
    ck('integer mean identity',lambda:m.summary([10**18,10**18+2],0)['mean']==10**18+1)
    num('error calculated before mean rounding',lambda:m.summary([10**18,10**18+1],10**18)['absolute_error'],F(1,2))
    num('finite SE despite overflowing SD',lambda:m.summary([-1.79e308,1.79e308],0)['estimated_se'],F(179*10**306))
    num('tiny positive SE',lambda:m.summary([-1e-308,1e-308],0)['estimated_se'],F(1,10**308))
    num('large theoretical count support',lambda:m.theoretical_se(10,10**400),F(1,10**199))
    num('zero SD arbitrary positive count',lambda:m.theoretical_se(0,10**1000),0)
    for label,fn in [('count1 sample',lambda:m.sample_payoffs(1,42)),('bool seed',lambda:m.sample_payoffs(2,True)),('summary noniterable',lambda:m.summary(None,100)),('summary short',lambda:m.summary([1],0)),('summary bool',lambda:m.summary([True,1],0)),('summary huge observation',lambda:m.summary([10**1000,1],0)),('summary huge reference',lambda:m.summary([1,2],10**1000)),('unreportable absolute error',lambda:m.summary([1.79e308,1.79e308],-1.79e308)),('nonfinite observations',lambda:m.summary([1,float('inf')],0)),('prefix noniterable samples',lambda:m.prefix_study(None,[2],0)),('prefix noniterable sizes',lambda:m.prefix_study([1,2],None,0)),('empty sizes',lambda:m.prefix_study([1,2],[],0)),('descending sizes',lambda:m.prefix_study([1,2,3],[3,2],0)),('duplicate sizes',lambda:m.prefix_study([1,2,3],[2,2],0)),('oversized prefix',lambda:m.prefix_study([1,2],[3],0)),('used prefix malformed',lambda:m.prefix_study([1,None],[2],0)),('SD negative',lambda:m.theoretical_se(-1,100)),('SD bool',lambda:m.theoretical_se(True,100)),('SD huge int',lambda:m.theoretical_se(10**1000,100)),('theoretical zero count',lambda:m.theoretical_se(10,0)),('theoretical bool count',lambda:m.theoretical_se(10,True)),('theoretical SE underflow',lambda:m.theoretical_se(10,10**1000))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    before=random.getstate();m.sample_payoffs(10,42);ck('local RNG preserves global state',lambda:random.getstate()==before)
    ck('same seed replay',lambda:m.sample_payoffs(100,42)==m.sample_payoffs(100,42))
    def inspect(label,values,sizes):
        rows=m.prefix_study(values,sizes,100)
        for n,row in zip(sizes,rows):
            q=[F(str(x)) for x in values[:n]];mu=sum(q)/n;v=sum((x-mu)**2 for x in q)/(n-1)
            for key,want in [('mean',mu),('estimated_se',sqrt(v/n)),('absolute_error',abs(mu-100))]:num(label+' independent prefix '+str((n,key)),lambda row=row,key=key:row[key],want)
        return rows
    samples=m.sample_payoffs(40000,42);sizes=[100,400,10000,40000];rows=inspect('source nested stream',samples,sizes)
    ck('prefix matches shorter seed replay',lambda:samples[:10000]==m.sample_payoffs(10000,42))
    # Supplemental one-year discount transform, followed by exact-source prefix summaries.
    discounted=[float(F(str(x))/F(21,20)) for x in samples]
    discounted_rows=m.prefix_study(discounted,sizes,float(F(2000,21)))
    for row,base_row in zip(discounted_rows,rows):
        num('discounted prefix mean '+str(row['count']),lambda row=row:row['mean'],F(str(base_row['mean']))/F(21,20))
        num('discounted prefix SE '+str(row['count']),lambda row=row:row['estimated_se'],F(str(base_row['estimated_se']))/F(21,20))
    import numpy as np
    children=np.random.SeedSequence(2026).spawn(3);replications=[]
    for i,child in enumerate(children):
        rng=np.random.default_rng(child);u=rng.random(10000);values=np.where(u<.25,80,np.where(u<.75,100,120)).tolist();r=inspect('supplemental spawned '+str(i),values,[10000]);replications.append(dict(worker=i,spawn_key=list(child.spawn_key),rows=r,observations_sha256=hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest(),scope='supplemental NumPy PCG64 sampler with source prefix/summary; designed spawning not a proof of independent streams'))
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),generator='source random.Random / Mersenne Twister',numpy=np.__version__,supplemental_bit_generator='PCG64',supplemental_spawn_parent=2026,source_nested_rows=rows,supplemental_discounted_prefix_rows=discounted_rows,source_samples_sha256=hashlib.sha256(json.dumps(samples,separators=(',',':')).encode()).hexdigest(),supplemental_replications=replications,rare_event_probability_of_zero_count=str(no_events),commands=commands,checks=checks,counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=12,new_historical_methods=0),model=dict(payoffs=states,probabilities=['1/4','1/2','1/4'],units='fictional common currency',discounted_example='one-year payoff at constant annual effective5%; no market-price claim',sample_sizes=sizes,reference=100,stopping='fixed predefined sizes, no sequential stopping rule'),limits='One source nested stream and supplemental designed replications only; no LLN/CLT theorem proved by finite runs, no formal independence/coverage/tail/monitoring/sequential or independent model acceptance; F28/F32/F165 retained. Unused trailing samples are not validated.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
