"""Exact uncertainty listing; independent rational/Decimal formula checks, no coverage claim."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.10-confidence-and-simulation-error.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
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
    def wilson(k,n,z=F(49,25)):
        # Independent score-quadratic roots: A p^2-B p+C=0.
        with localcontext() as c:
            c.prec=600;n=D(n);k=D(k);z=dec(z);a=n*(n+z*z);b=n*(2*k+z*z);cc=k*k;disc=(b*b-4*a*cc).sqrt()
            lo=(2*cc)/(b+disc) if k else D(0);hi=(b+disc)/(2*a)
            return lo,hi
    with tempfile.TemporaryDirectory(prefix='book1-1810-') as tmp:
        Path(tmp,'simulation_error.py').write_bytes(code)
        for label,args in [('exact demo/tests',['simulation_error.py']),('quiet import',['-c','import simulation_error']),('compile',['-m','compileall','-q','simulation_error.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==12 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('error_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    probs=[F(1,4),F(1,2),F(1,4)];vals=[80,100,120];mu=sum(p*x for p,x in zip(probs,vals));variance=sum(p*(x-mu)**2 for p,x in zip(probs,vals));theory_se=sqrt(variance/10000)
    for label,fn,want in [('E2 SE20 at10000',lambda:F(20,100),F(1,5)),('E3 fourfold N',lambda:sqrt(F(1,4)),F(1,2)),('E4 halfwidth SE.2',lambda:F(49,25)*F(1,5),F(49,125)),('E5 CI lower',lambda:F(1001,10)-F(49,125),F(24927,250)),('E5 CI upper',lambda:F(1001,10)+F(49,125),F(25123,250)),('E10 model mean',lambda:mu,100),('E11 model variance',lambda:variance,200),('E12 theoretical SE',lambda:theory_se,sqrt(F(1,50))),('E14 strict event probability',lambda:sum(p for p,x in zip(probs,vals) if x<100),F(1,4)),('E15 theoretical event SE',lambda:sqrt(F(3,160000)),sqrt(F(3,160000))),('E19 discount',lambda:F(100)/F(21,20),F(2000,21)),('E20 discounted SE',lambda:theory_se/D('1.05'),theory_se/D('1.05'))]:num(label,fn,want)
    constructed=[float(D('100.1')-theory_se),float(D('100.1')+theory_se)]
    hypothetical=m.mean_interval(constructed)
    num('lab4 constructed sample mean',lambda:hypothetical['mean'],D('100.1'))
    num('lab4 constructed sample SE',lambda:hypothetical['standard_error'],theory_se)
    for i,sign in [(0,-1),(1,1)]:num('lab4 hypothetical interval '+str(i),lambda i=i:hypothetical['interval'][i],D('100.1')+D(sign)*D('1.96')*theory_se)
    ck('E12 printed SE',lambda:round(float(theory_se),5)==.14142)
    ck('E13 rounded-input arithmetic differs from unrounded benchmark',lambda:round(float(F(49,25)*F(14142,100000)),5)==.27718)
    ck('E13 source prompt specifies unrounded benchmark',lambda:b'1.96' in data and '**Half-width:** 1.96×.14142'.encode('utf-8') not in data)
    ck('E13 unrounded halfwidth rounds .27719',lambda:round(float(D('1.96')*theory_se),5)==.27719)
    ck('E15 printed event SE',lambda:round(float(sqrt(F(3,160000))),5)==.00433)
    ck('E18 zero events closed form',lambda:round(float(F(49,25)**2/(100+F(49,25)**2)),4)==.0370)
    ck('E19 printed discounted mean',lambda:round(float(F(2000,21)),4)==95.2381)
    plan=(F(49,25)*20/F(1,2))**2;ck('E22 exact planning ceil6146.56',lambda:plan==F(153664,25) and math.ceil(plan)==6147)
    ck('source planning',lambda:m.planned_count(20,.5)==6147)
    ck('zero SD planning mathematical zero',lambda:m.planned_count(0,.5)==0)
    ck('positive tiny planning rounds upward to one',lambda:m.planned_count(1e-200,1e200)==1)
    ck('large finite-input count computed exactly',lambda:m.planned_count(1e200,1e-100,1)==10**600)
    ck('planning exact integer z huge',lambda:m.planned_count(1,1,10**18+1)==(10**18+1)**2)
    ck('finite predicate oversized integer false',lambda:m.finite_number(10**1000),False)
    mean=m.mean_interval([80,100,120]);num('known sample mean',lambda:mean['mean'],100);num('known sample SE',lambda:mean['standard_error'],sqrt(F(400,3)))
    for i,sign in [(0,-1),(1,1)]:num('known sample endpoint '+str(i),lambda i=i:mean['interval'][i],D(100)+D(sign)*D('1.96')*sqrt(F(400,3)))
    ck('constant integer interval identity',lambda:m.mean_interval([10**18+1]*2)['interval']==(10**18+1,10**18+1))
    num('finite SE despite intermediate SD overflow',lambda:m.mean_interval([-1.79e308,1.79e308],.1)['standard_error'],F(179*10**306))
    num('tiny positive mean SE',lambda:m.mean_interval([-1e-308,1e-308])['standard_error'],F(1,10**308))
    ck('one-pass observations',lambda:m.mean_interval(iter([80,100,120]))['mean']==100)
    wilson_cases=[]
    for k,n,z in [(0,100,1.96),(100,100,1.96),(50,100,1.96),(1,1,1.96),(0,1,1.96),(1,1000,1.96),(2500,10000,1.96),(1,10,1e100),(0,10**300,1.96),(1,10**300,1.96)]:
        expected=wilson(k,n,F(str(z)))
        for i in [0,1]:num('Wilson independent quadratic '+str((k,n,z,i)),lambda k=k,n=n,z=z,i=i:m.wilson_interval(k,n,z)[i],expected[i])
        try:actual=m.wilson_interval(k,n,z)
        except Exception as e:actual=repr(e)
        wilson_cases.append(dict(events=k,trials=n,critical_value=z,actual=actual,reference=list(map(str,expected))))
    for k in [0,1,3,9,10]:
        ck('Wilson finite ordered bounded '+str(k),lambda k=k:all(math.isfinite(x) for x in m.wilson_interval(k,10)) and 0<=m.wilson_interval(k,10)[0]<=m.wilson_interval(k,10)[1]<=1)
        num('Wilson complement symmetry '+str(k),lambda k=k:m.wilson_interval(k,10)[1],1-wilson(10-k,10)[0])
    ck('higher critical value widens fixed sample interval',lambda:m.mean_interval([80,100,120],3)['interval'][0]<m.mean_interval([80,100,120],1)['interval'][0] and m.mean_interval([80,100,120],3)['interval'][1]>m.mean_interval([80,100,120],1)['interval'][1])
    for label,fn in [('mean noniterable',lambda:m.mean_interval(None)),('short mean sample',lambda:m.mean_interval([1])),('boolean sample',lambda:m.mean_interval([True,1])),('huge observation',lambda:m.mean_interval([10**1000,1])),('nonfinite observation',lambda:m.mean_interval([float('inf'),1])),('huge critical value',lambda:m.mean_interval([1,2],10**1000)),('mean interval overflow',lambda:m.mean_interval([-1e308,1e308])),('negative critical value',lambda:m.mean_interval([1,2],-1)),('wilson invalid events',lambda:m.wilson_interval(11,10)),('wilson bool count',lambda:m.wilson_interval(True,10)),('wilson zero trials',lambda:m.wilson_interval(0,0)),('wilson huge critical value',lambda:m.wilson_interval(1,10,10**1000)),('wilson nonreportable positive endpoint policy',lambda:m.wilson_interval(1,10,1e200)),('planning huge input',lambda:m.planned_count(10**1000,.5)),('planning zero width',lambda:m.planned_count(20,0)),('planning bool SD',lambda:m.planned_count(True,.5))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    ck('E17 supplemental zero event plugin SE',lambda:F(0)*(1-F(0))/100==0)
    ck('E28 supplemental pair averages',lambda:[F(a+b,2) for a,b in [(80,120),(120,80),(100,100)]]==[100]*3)
    ck('E29 supplemental paired differences',lambda:[b-a for a,b in [(80,82),(100,102),(120,122)]]==[2]*3)
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),commands=commands,checks=checks,known_sample=mean,hypothetical_interval_fixture=dict(observations=constructed,result=hypothetical,scope="supplemental constructed two-point sample for arithmetic, not a stochastic coverage experiment"),wilson_cases=wilson_cases,planning_exact_count=str(plan),counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=12,new_historical_methods=0),model=dict(payoffs=vals,probabilities=['1/4','1/2','1/4'],units='fictional common currency',estimands='model mean and independent Bernoulli event probability',discount='one-year payoff at constant annual effective5%, no calibrated measure',confidence='caller-supplied normal critical value1.96, nominal fixed-sample approximation'),limits='Deterministic formula/API checks, no RNG or replication sampler in source. No empirical/exact nominal coverage, sequential/dependence/Student-t implementation or independent model acceptance. Very large planned counts are arithmetic, not executed simulations. F28/F32/F165 retained.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
