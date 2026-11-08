"""Exact path listing, independent GBM algebra and shared-shock replay, separately scoped."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.06-price-path-simulation.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
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
    def exp(q):
        with localcontext() as c:c.prec=200;return dec(q).exp()
    with tempfile.TemporaryDirectory(prefix='book1-1806-') as tmp:
        Path(tmp,'price_path_simulation.py').write_bytes(code)
        for label,args in [('exact demo/tests',['price_path_simulation.py']),('quiet import',['-c','import price_path_simulation']),('compile',['-m','compileall','-q','price_path_simulation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=180);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==10 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('path_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    for label,fn,want in [('E1 compounding',lambda:100*F(11,10)*F(9,10),99),('E2 cumulative return',lambda:F(11,10)*F(9,10)-1,F(-1,100)),('E4 monthly dt',lambda:F(1,12),F(1,12)),('E5 quarterly dt',lambda:F(2,8),F(1,4)),('E6 log drift',lambda:F(5,100)-F(2,10)**2/2,F(3,100)),('E7 shock scale',lambda:D('.2')*sqrt(F(1,4)),D('.1')),('E8 E9 mean',lambda:m.expected_terminal(100,.05,1),100*exp(F(1,20))),('E10 median',lambda:100*exp(F(3,100)),100*exp(F(3,100))),('E11 log SD',lambda:D('.2')*sqrt(1),F(1,5)),('E12 four year log SD',lambda:D('.2')*sqrt(4),F(2,5)),('E18 fourfold paths factor',lambda:sqrt(F(1,4)),F(1,2)),('known terminal SE',lambda:m.summarize_terminal([[100,90],[100,110]])['standard_error'],10),('E32 zero horizon benchmark',lambda:m.expected_terminal(100,.05,0),100)]:num(label,fn,want)
    # Mixed Fraction/Decimal must be converted explicitly in the supplemental shock-scale oracle.
    for label,q,want in [('printed mean',F(1,20),105.12711),('printed median',F(3,100),103.04545)]:ck(label,lambda q=q,want=want:round(float(100*exp(q)),5)==want)
    ck('time zero barrier equality',lambda:m.observed_barrier_hit([100,110],100))
    ck('later barrier equality',lambda:m.observed_barrier_hit([100,95,110],95))
    ck('no observed hit',lambda:not m.observed_barrier_hit([100,96,110],95))
    ck('generator barrier consumed once',lambda:m.observed_barrier_hit(iter([100,90]),95))
    ck('empty-terminal paths rejected',lambda:rejects(lambda:m.summarize_terminal([[],[]])))
    ck('terminal-only summary contract',lambda:m.summarize_terminal([[None,90],[None,110]])['mean']==100)
    ck('zero dynamics integer path identity',lambda:m.simulate_paths(10**18+1,0,0,1,4,2,1)==[[10**18+1]*5]*2)
    ck('zero horizon integer benchmark identity',lambda:m.expected_terminal(10**18+1,.05,0)==10**18+1)
    ck('nonzero horizon zero drift integer identity',lambda:m.expected_terminal(10**18+1,0,1)==10**18+1)
    ck('integer summary identity',lambda:m.summarize_terminal([[10**18],[10**18+2]])['mean']==10**18+1)
    num('tiny positive SE',lambda:m.summarize_terminal([[1e-308],[3e-308]])['standard_error'],F(1,10**308))
    num('positive spread finite SE',lambda:m.summarize_terminal([[5e-324],[1.79e308]])['standard_error'],F(179*10**306,2))
    num('scaled benchmark extension',lambda:m.expected_terminal(1e-308,1000,1),D('1e-308')*exp(1000))
    # A deterministic tiny horizon has a representable square-root shock scale even if float dt is zero.
    ck('tiny horizon drift not silently discarded',lambda:rejects(lambda:m.simulate_paths(100,1e308,0,5e-324,2,2,1)) or m.simulate_paths(100,1e308,0,5e-324,2,2,1)[0][-1]>100)
    for label,fn in [('huge initial',lambda:m.simulate_paths(10**1000,.05,.2,1,4,2,1)),('huge volatility',lambda:m.simulate_paths(100,0,1e308,1,1,2,1)),('negative volatility',lambda:m.simulate_paths(100,.05,-.2,1,4,2,1)),('zero horizon',lambda:m.simulate_paths(100,.05,.2,0,4,2,1)),('zero steps',lambda:m.simulate_paths(100,.05,.2,1,0,2,1)),('count1',lambda:m.simulate_paths(100,.05,.2,1,4,1,1)),('bool seed',lambda:m.simulate_paths(100,.05,.2,1,4,2,True)),('bool drift',lambda:m.simulate_paths(100,True,.2,1,4,2,1)),('price overflow',lambda:m.simulate_paths(100,1000,0,1,1,2,1)),('price underflow',lambda:m.simulate_paths(100,-1000,0,1,1,2,1)),('paths noniterable',lambda:m.summarize_terminal(None)),('path noniterable',lambda:m.summarize_terminal([1,2])),('terminal boolean',lambda:m.summarize_terminal([[True],[100]])),('terminal huge int',lambda:m.summarize_terminal([[10**1000],[100]])),('terminal zero',lambda:m.summarize_terminal([[0],[100]])),('barrier huge int',lambda:m.observed_barrier_hit([100],10**1000)),('barrier malformed path',lambda:m.observed_barrier_hit(None,95)),('barrier boolean path',lambda:m.observed_barrier_hit([True,100],95)),('barrier huge path',lambda:m.observed_barrier_hit([10**1000],95)),('benchmark huge int',lambda:m.expected_terminal(10**1000,.05,1)),('benchmark negative horizon',lambda:m.expected_terminal(100,.05,-1))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    before=random.getstate();m.simulate_paths(100,.05,.2,1,4,2,42);ck('global state preserved',lambda:random.getstate()==before)
    ck('seed replay',lambda:m.simulate_paths(100,.05,.2,1,12,3,42)==m.simulate_paths(100,.05,.2,1,12,3,42))
    # Supplemental analytic path comparison with the same normal generator (not independent RNG evidence).
    actual=m.simulate_paths(100,.05,.2,1,4,2,42);r=random.Random(42);expected=[]
    with localcontext() as c:
        c.prec=100
        for _ in range(2):
            path_values=[D(100)];total=D(0)
            for _ in range(4):total+=D('.03')/4+D('.1')*D.from_float(r.normalvariate(0,1));path_values.append(D(100)*total.exp())
            expected.append(path_values)
    for i in range(2):
        for j in range(5):num('shared shock independent update '+str((i,j)),lambda i=i,j=j:actual[i][j],expected[i][j])
    deterministic=m.simulate_paths(100,.05,0,1,12,2,42)
    for j in [0,1,6,12]:num('deterministic grid '+str(j),lambda j=j:deterministic[0][j],100*exp(F(j,240)))
    ck('E26 supplemental average payoff depends on observations',lambda:F(100+80+120,3)!=F(100+100+120,3))
    ck('E27 supplemental terminal call same for same terminal',lambda:max(120-110,0)==10)
    runs=[]
    for seed in [42,43]:
        paths=m.simulate_paths(100,.05,.2,1,12,10000,seed);summary=m.summarize_terminal(paths);q=[F(str(p[-1])) for p in paths];mu=sum(q)/len(q);v=sum((x-mu)**2 for x in q)/(len(q)-1);hits=sum(m.observed_barrier_hit(p,95) for p in paths);observations=sum(x<=95 for p in paths for x in p)
        num('sample independent mean '+str(seed),lambda summary=summary:summary['mean'],mu)
        num('sample independent SE '+str(seed),lambda summary=summary:summary['standard_error'],sqrt(v/len(q)))
        ck('N paths and n+1 points '+str(seed),lambda paths=paths:len(paths)==10000 and all(len(p)==13 and p[0]==100 for p in paths))
        ck('path-hit count vs minima '+str(seed),lambda paths=paths,hits=hits:sum(min(p)<=95 for p in paths)==hits)
        runs.append(dict(seed=seed,path_count=len(paths),steps=12,summary=summary,barrier=95,paths_with_observed_hit=hits,observations_at_or_below_barrier=observations,total_observations=sum(map(len,paths)),first_paths=paths[:2],paths_sha256=hashlib.sha256(json.dumps(paths,separators=(',',':')).encode()).hexdigest(),limits='discrete monitoring only, includes time zero; hit-path count differs from hit-observation count; different seeds not independence proof'))
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),generator='random.Random / Mersenne Twister normalvariate',commands=commands,checks=checks,runs=runs,counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=10,new_historical_methods=0),model=dict(initial=100,drift='.05',volatility='.2',horizon='one year',steps=12,measure='uncalibrated illustrative GBM measure, not a risk-neutral price claim',units='fictional currency; annual drift/volatility and year-based horizon'),limits='Shared generator shock replay checks update algebra only. Discrete-grid monitoring, model/parameter uncertainty, tail/coverage/independence/platform and independent model acceptance remain open; F28/F32/F165 retained.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
