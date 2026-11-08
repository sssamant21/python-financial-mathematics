"""Execute verbatim fences; supplemental rational oracles are not RNG certification."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.02-random-number-generators.md'
    data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path])
    fences=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S);commands=[];checks=[]
    def ck(label,fn,expected=True):
        try:actual=fn();ok=actual==expected
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,passed=bool(ok),actual=actual,expected=expected))
    def num(label,fn,want):
        try:actual=fn();ok=math.isclose(actual,float(want),rel_tol=1e-12,abs_tol=0)
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,passed=ok,actual=actual,expected=str(want),relative_tolerance=1e-12,absolute_tolerance=0))
    def rejects(fn):
        try:fn()
        except ValueError:return True
        except Exception as e:return type(e).__name__
        return False
    def sqrt(q):
        q=F(q)
        with localcontext() as c:c.prec=200;return (D(q.numerator)/D(q.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1802-') as tmp:
        for i,code in enumerate(fences):
            name='random_generators.py' if i==len(fences)-1 else f'example{i+1}.py';Path(tmp,name).write_bytes(code)
            p=subprocess.run([sys.executable,'-B',name],cwd=tmp,capture_output=True,text=True,timeout=60)
            methods=re.search(r'Ran (\d+) tests',p.stderr)
            commands.append(dict(label=f'exact fence {i+1}',args=[name],stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,existing_methods=int(methods[1]) if methods else 0,passed=p.returncode==0 and (i!=len(fences)-1 or bool(methods and int(methods[1])==10 and re.search(r'^OK\s*$',p.stderr,re.M)))))
        for args in [['-c','import random_generators'],['-m','compileall','-q','random_generators.py']]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(label='exact module check',args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,existing_methods=0,passed=p.returncode==0 and not(p.stdout or p.stderr)))
    m=types.ModuleType('generators_lab');exec(compile(fences[-1],str(BOOK/path),'exec'),m.__dict__)
    num('independent ideal uniform mean integral',lambda:F(1,2),F(1,2))
    num('independent ideal uniform variance integral',lambda:F(1,3)-F(1,2)**2,F(1,12))
    num('E13 independent two-outcome expectation',lambda:F(3,5)*110+F(2,5)*90,102)
    num('independent two-outcome variance',lambda:F(3,5)*(110-102)**2+F(2,5)*(90-102)**2,96)
    num('E14 normal variance',lambda:F(15,100)**2,F(225,10000))
    num('E30 SE',lambda:F(10,100),F(1,10))
    num('E31 fourfold N factor',lambda:sqrt(F(10000,40000)),F(1,2))
    for rho in [F(0),F(1),F(-1),F(3,5)]:
        num('correlation construction variance '+str(rho),lambda rho=rho:rho*rho+(1-rho*rho),1)
        num('correlation construction covariance '+str(rho),lambda rho=rho:rho,rho)
    ck('E29 invalid correlation domain',lambda:abs(F(11,10))>1)
    num('E33 negative simple-return terminal',lambda:F(100)*(1-F(11,10)),-10)
    for label,fn,want in [('sample mean',lambda:m.summary([0,1,0,1])['mean'],F(1,2)),('sample variance ddof1',lambda:m.summary([0,1,0,1])['sample_variance'],F(1,3)),('sample SE',lambda:m.summary([0,1,0,1])['standard_error'],sqrt(F(1,12))),('constant SE E37',lambda:m.summary([2,2])['standard_error'],0),('normal zero SD',lambda:m.normal_draws(2,0,4,1)[0],2)]:num(label,fn,want)
    ck('exact terminal increment',lambda:m.terminal_values(10**18,1e-18,0,[1,0])==[10**18+1,10**18])
    ck('exact mean integer identity',lambda:m.summary([10**18,10**18+2])['mean']==10**18+1)
    num('used branches only policy',lambda:m.terminal_values(1e308,1e308,0,[0])[0],1e308)
    ck('true total-loss zero',lambda:m.terminal_values(100,-1,0,[1])==[0])
    ck('normal zero SD preserves integer',lambda:m.normal_draws(10**18+1,0,2,1)==[10**18+1]*2)
    for label,fn in [
      ('bad probability',lambda:m.bernoulli_draws(1.1,2,1)),('bool probability',lambda:m.bernoulli_draws(True,2,1)),('huge probability',lambda:m.bernoulli_draws(10**1000,2,1)),
      ('count1',lambda:m.uniform_draws(1,1)),('bool count',lambda:m.uniform_draws(True,1)),('bool seed',lambda:m.uniform_draws(2,True)),
      ('negative sd',lambda:m.normal_draws(0,-1,2,1)),('huge normal mean',lambda:m.normal_draws(10**1000,1,2,1)),('normal output overflow',lambda:m.normal_draws(1.79e308,1.79e308,20,1)),
      ('short sample',lambda:m.summary([1])),('sample noniterable',lambda:m.summary(None)),('sample malformed',lambda:m.summary([None,1])),('bool sample',lambda:m.summary([True,1])),('infinite sample',lambda:m.summary([1,float('inf')])),('huge sample',lambda:m.summary([10**1000,1])),('variance overflow',lambda:m.summary([-1e308,1e308])),('variance underflow',lambda:m.summary([-1e-200,1e-200])),
      ('outcomes noniterable',lambda:m.terminal_values(100,.1,-.1,None)),('bool outcome',lambda:m.terminal_values(100,.1,-.1,[True])),('bad return',lambda:m.terminal_values(100,.1,-1.1,[0])),('huge initial',lambda:m.terminal_values(10**1000,.1,0,[1])),('terminal underflow',lambda:m.terminal_values(5e-324,-.75,0,[1])),('terminal overflow',lambda:m.terminal_values(1e308,1e308,0,[1])),
    ]:ck('reject '+label,lambda fn=fn:rejects(fn))
    before=random.getstate();u=m.uniform_draws(1000,2026);b=m.bernoulli_draws(.6,1000,42);n=m.normal_draws(.05,.15,1000,42)
    ck('global state unchanged',lambda:random.getstate()==before)
    ck('uniform range',lambda:all(0<=x<1 for x in u))
    ck('uniform replay',lambda:m.uniform_draws(1000,2026)==u)
    ck('Bernoulli replay',lambda:m.bernoulli_draws(.6,1000,42)==b)
    ck('normal replay',lambda:m.normal_draws(.05,.15,1000,42)==n)
    ck('Bernoulli p0',lambda:m.bernoulli_draws(0,5,1)==[0]*5)
    ck('Bernoulli p1',lambda:m.bernoulli_draws(1,5,1)==[1]*5)
    ck('Bernoulli threshold mapping shares uniform generator',lambda:b==[int(F.from_float(x)<F(3,5)) for x in m.uniform_draws(1000,42)])
    lab_summaries={}
    for label,xs in [('uniform',u),('normal',n)]:
        q=[F(str(x)) for x in xs];mean=sum(q)/len(q);variance=sum((x-mean)**2 for x in q)/(len(q)-1);actual=m.summary(xs);lab_summaries[label]=actual
        num(label+' independent decimal sample mean',lambda actual=actual:actual['mean'],mean)
        num(label+' independent decimal sample variance',lambda actual=actual:actual['sample_variance'],variance)
        num(label+' independent decimal sample SE',lambda actual=actual:actual['standard_error'],sqrt(variance/len(q)))
    streams=[]
    for seed in [42,43,44]:
        events=m.bernoulli_draws(.6,1000,seed);k=sum(events);values=m.terminal_values(100,.1,-.1,events);s=m.summary(values)
        num('count oracle mean '+str(seed),lambda s=s:s['mean'],F(90)+F(20*k,1000))
        num('count oracle variance '+str(seed),lambda s=s:s['sample_variance'],F(400*k*(1000-k),1000*999))
        num('count oracle SE '+str(seed),lambda s=s:s['standard_error'],sqrt(F(400*k*(1000-k),1000**2*999)))
        streams.append(dict(seed=seed,up_count=k,frequency=k/1000,summary=s))
    # Replay/state probes share the source library and are explicitly not independent RNG oracles.
    r=random.Random(10);state=r.getstate();first=r.random();r.setstate(state);ck('state restoration',lambda:r.random()==first)
    r=random.Random(10);r.random();ck('extra draw shifts selected stream',lambda:r.random()!=first)
    import numpy as np
    parent=np.random.SeedSequence(2026);children=parent.spawn(4);workers=[np.random.default_rng(c) for c in children];draws=[w.random(10).tolist() for w in workers]
    parent2=np.random.SeedSequence(2026);replay=[np.random.default_rng(c).random(10).tolist() for c in parent2.spawn(4)]
    ck('spawn replay fixed assignment',lambda:draws==replay)
    ck('chosen child streams differ',lambda:len({tuple(x) for x in draws})==4)
    ck('identically seeded workers duplicate',lambda:np.random.default_rng(42).random(10).tolist()==np.random.default_rng(42).random(10).tolist())
    def stats(xs):
        q=[F.from_float(x) if isinstance(x,float) else F(x) for x in xs];mean=sum(q)/len(q);v=sum((x-mean)**2 for x in q)/(len(q)-1)
        return dict(count=len(xs),mean=float(mean),sample_variance=float(v),sample_sd=float(sqrt(v)))
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=[hashlib.sha256(c).hexdigest() for c in fences],python=platform.python_version(),platform=platform.platform(),numpy=np.__version__,bit_generator=type(workers[0].bit_generator).__name__,commands=commands,checks=checks,source_lab_summaries=lab_summaries,uniform_lab=stats(u),normal_lab=dict(**stats(n),below_minus_one=sum(x< -1 for x in n)),bernoulli_runs=streams,children=[dict(worker=i,spawn_key=list(c.spawn_key),draws=draws[i]) for i,c in enumerate(children)],counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=10,new_historical_methods=0),limits='Rational moments are ideal-model derivations; exact-count checks validate mapping/statistics, state/spawn checks share generators. No independence, distribution-tail, model or platform certification. Binary uniform draws have 53-bit grid resolution; arbitrary probabilities only approximate ideal Bernoulli laws.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks));return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
