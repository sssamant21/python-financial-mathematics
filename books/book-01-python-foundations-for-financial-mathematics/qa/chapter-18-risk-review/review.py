"""Verbatim empirical risk source and independent quantile-integral oracle."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.12-risk-simulation.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
    def ck(label,fn,expected=True):
        try:actual=fn();ok=actual==expected
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,actual=actual,expected=expected,passed=bool(ok)))
    def num(label,fn,want):
        try:actual=fn();ok=math.isclose(actual,float(want),rel_tol=1e-12,abs_tol=0)
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,actual=actual,expected=str(want),passed=bool(ok),relative_tolerance=1e-12,absolute_tolerance=0))
    def reject(fn):
        try:fn()
        except ValueError:return True
        except Exception as e:return type(e).__name__
        return False
    def oracle(values,alpha):
        q=sorted(F(x) if type(x) is int else F(str(x)) for x in values);a=F(str(alpha));n=len(q)
        # Integrate each quantile cell's overlap with [alpha,1].
        es=sum(x*max(F(0),F(i+1,n)-max(a,F(i,n))) for i,x in enumerate(q))/(1-a)
        return q[math.ceil(a*n)-1],es
    with tempfile.TemporaryDirectory(prefix='book1-1812-') as tmp:
        Path(tmp,'risk_simulation.py').write_bytes(code)
        for label,args in [('exact demo/tests',['risk_simulation.py']),('quiet import',['-c','import risk_simulation']),('compile',['-m','compileall','-q','risk_simulation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==12 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('risk_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    values=m.losses_from_values(100,[110,100,80,60]);ck('lab2 loss signs',lambda:values==[-10,0,20,40]);num('E5 mean loss',lambda:F(sum(values),len(values)),F(25,2));num('E4 loss frequency',lambda:m.loss_frequency(values),F(1,2))
    for label,fn,want in [('E1 loss',lambda:m.losses_from_values(100,[90])[0],10),('E2 gain',lambda:m.losses_from_values(100,[110])[0],-10),('E3 zero',lambda:m.losses_from_values(100,[100])[0],0),('E8 rank',lambda:math.ceil(F(3,4)*4),3),('E10 exceedance above VaR80',lambda:F(sum(x>40 for x in values),4),0),('E12 fractional tail mass',lambda:4*(1-F(5,8)),F(3,2)),('E16 99 percent tail',lambda:10000*(1-F(99,100)),100)]:num(label,fn,want)
    cases=[]
    for losses,a in [(list(range(50)),.14),(values,.75),(values,.625),(values,.8),([5,5,5],.9),([-40,-20,-10],.5),([0,0,10,10],.5),([1,2,3,4,5],.2),([0]*13+[10,20,30,40,50,60,70,80,90,100,110,120,130],.5384615384615385),([1e308,1e308],.1),([-1e308,-1e308],.1),([-1e308,1e308,1e308],.25),([10**18+1]*2,.75)]:
        v,e=oracle(losses,a)
        for key,fn,want in [('VaR',lambda losses=losses,a=a:m.nearest_rank_var(losses,a),v),('ES',lambda losses=losses,a=a:m.empirical_es(losses,a),e)]:num(key+' integral oracle '+str((len(losses),a)),fn,want)
        try:actual=[m.nearest_rank_var(losses,a),m.empirical_es(losses,a)]
        except Exception as ex:actual=repr(ex)
        cases.append(dict(losses=losses,alpha=a,reference=[str(v),str(e)],actual=actual))
    ck('constant integer ES identity',lambda:m.empirical_es([10**18+1]*2,.75)==10**18+1)
    ck('one-pass losses',lambda:m.empirical_es(iter(values),.625)==m.empirical_es(values,.625))
    ck('sorting invariance',lambda:m.nearest_rank_var(list(reversed(values)),.75)==20)
    num('E26 strict zero loss excluded',lambda:m.loss_frequency([0,0]),0)
    ck('negative ES allowed',lambda:m.empirical_es([-40,-20,-10],.5)<0)
    ck('single-observation risk allowed',lambda:m.nearest_rank_var([7],.99)==7 and m.empirical_es([7],.99)==7)
    ck('finite oversized integer false',lambda:m.finite(10**1000),False)
    ck('integer loss identity',lambda:m.losses_from_values(10**18+1,[0])==[10**18+1])
    for label,fn in [('positive nonreportable ES policy',lambda:m.empirical_es([5e-324,-5e-324],.1)),('losses noniterable',lambda:m.nearest_rank_var(None,.5)),('empty losses',lambda:m.empirical_es([],.5)),('huge loss',lambda:m.empirical_es([10**1000],.5)),('bool loss',lambda:m.loss_frequency([True])),('nan loss',lambda:m.loss_frequency([float('nan')])),('huge alpha',lambda:m.nearest_rank_var([1],10**1000)),('alpha zero',lambda:m.nearest_rank_var([1],0)),('alpha one',lambda:m.nearest_rank_var([1],1)),('frequency noniterable',lambda:m.loss_frequency(None)),('huge initial',lambda:m.losses_from_values(10**1000,[0])),('terminal noniterable',lambda:m.losses_from_values(100,None)),('huge terminal',lambda:m.losses_from_values(100,[10**1000])),('negative terminal',lambda:m.losses_from_values(100,[-1]))]:ck('reject '+label,lambda fn=fn:reject(fn))
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),commands=commands,checks=checks,cases=cases,counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=12,new_historical_methods=0),model=dict(initial=100,terminals=[110,100,80,60],losses=values,scenario_weights='equal1/4',horizon='one common model period, no actual duration/market date supplied',units='fictional common currency',convention='lower empirical nearest rank VaR and integrated empirical quantile ES'),limits='Deterministic empirical summary API only; no RNG/seed, market dynamics, unequal weights, backtest or quantile/ES confidence interval implementation. Source execution, supplemental integral and conceptual design separate; F28/F32/F165 and independent acceptance open.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
