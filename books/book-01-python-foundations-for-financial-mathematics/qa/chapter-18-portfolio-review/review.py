"""Exact one-period portfolio listing; independent moments and shared-normal replay separated."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.11-portfolio-simulation.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
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
    with tempfile.TemporaryDirectory(prefix='book1-1811-') as tmp:
        Path(tmp,'portfolio_simulation.py').write_bytes(code)
        for label,args in [('exact demo/tests',['portfolio_simulation.py']),('quiet import',['-c','import portfolio_simulation']),('compile',['-m','compileall','-q','portfolio_simulation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==12 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('portfolio_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    params=(.08,.04,.2,.1,.25,.6,.4);mu=F(3,5)*F(8,100)+F(2,5)*F(4,100);cov=F(1,4)*F(1,5)*F(1,10);var=F(3,5)**2*F(1,5)**2+F(2,5)**2*F(1,10)**2+2*F(3,5)*F(2,5)*cov
    for label,fn,want in [('E1 weights',lambda:F(3,5)+F(2,5),1),('E2 deterministic return',lambda:F(3,5)*F(1,10)+F(2,5)*F(-5,100),F(1,25)),('E3 terminal',lambda:100*(1+F(1,25)),104),('E4 profit',lambda:100*F(1,25),4),('E5 source analytical mean',lambda:m.analytical(*params)[0],mu),('E6 covariance',lambda:cov,F(1,200)),('E7 source analytical variance',lambda:m.analytical(*params)[1],var),('E9 expected terminal',lambda:100*(1+mu),F(532,5)),('E11 theoretical mean SE',lambda:100*sqrt(var)/100,sqrt(var)),('E12 zero correlation variance',lambda:m.analytical(.08,.04,.2,.1,0,.6,.4)[1],F(2,125)),('E15 deterministic stress',lambda:m.analytical(-.2,-.1,0,0,0,.6,.4)[0],F(-4,25)),('E16 stress profit',lambda:100*F(-4,25),-16)]:num(label,fn,want)
    for label,value,places,want in [('E8 volatility',sqrt(var),5,.13565),('E10 terminal SD',100*sqrt(var),3,13.565)]:ck(label,lambda value=value,places=places,want=want:round(float(value),places)==want)
    with localcontext() as c:
        c.prec=100;x=dec(mu)/dec(var).sqrt();term=x;integral=x;pi=D('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')
        for n in range(1,80):term*= -x*x/(2*n);integral+=term/(2*n+1)
        loss=D('.5')-integral/(2*pi).sqrt()
    ck('E13 central analytical loss probability rounded',lambda:round(float(loss),4)==.3185)
    num('E14 strict return equality',lambda:m.summarize([(0,0,0)]*2,100)['loss_frequency'],0)
    ck('normal-model negative terminal retained',lambda:m.summarize([(-2,-2,-2)]*2,100)['mean_terminal']==-100)
    ck('below-minus-one path count retained',lambda:m.summarize([(-2,0,-1.2),(0,0,0)],100)['paths_with_asset_return_below_minus_one']==1)
    tail_fixture=m.summarize([(-2,0,-1.2),(0,0,0)],100)
    num('tail diagnostic frequency from count',lambda:F(tail_fixture['paths_with_asset_return_below_minus_one'],tail_fixture['count']),F(1,2))
    num('tail fixture portfolio loss frequency',lambda:tail_fixture['loss_frequency'],F(1,2))
    ck('true total loss zero allowed',lambda:m.summarize([(-1,-1,-1)]*2,100)['mean_terminal']==0)
    ck('rho plus1 singular coupling',lambda:all(a==b for a,b,_ in m.simulate(10,42,0,0,1,1,1,.6,.4)))
    ck('rho minus1 singular coupling',lambda:all(a==-b for a,b,_ in m.simulate(10,42,0,0,1,1,-1,.6,.4)))
    ck('perfectly offset portfolio returns',lambda:all(rp==0 for _,_,rp in m.simulate(10,42,0,0,1,1,-1,.5,.5)))
    num('zero variance analytical hedge',lambda:m.analytical(0,0,1e308,1e308,-1,.5,.5)[1],0)
    ck('integer zero-volatility mean identity',lambda:all(a==10**18+1 and rp==10**18+1 for a,_,rp in m.simulate(2,42,10**18+1,0,0,0,0,1,0)))
    ck('integer terminal identity',lambda:m.summarize([(0,0,0)]*2,10**18+1)['mean_terminal']==10**18+1)
    ck('tiny return terminal increment identity',lambda:m.summarize([(0,0,1e-18)]*2,10**18)['mean_terminal']==10**18+1)
    ck('weight normalization analytical policy',lambda:m.analytical(.1,.1,0,0,0,.5,.5000000000005)[0]==.1)
    ck('weight normalization simulation policy',lambda:all(rp==.1 for _,_,rp in m.simulate(2,42,.1,.1,0,0,0,.5,.5000000000005)))
    ck('finite helper oversized integer false',lambda:m.finite(10**1000),False)
    ck('summary one-pass rows',lambda:m.summarize(iter([(0,0,0)]*2),100)['mean_terminal']==100)
    ck('provided portfolio-return consistency external',lambda:m.summarize([(0,0,.1)]*2,100)['mean_return']==.1)
    for label,fn in [('huge mean',lambda:m.simulate(2,42,10**1000,0,0,0,0,1,0)),('negative sd',lambda:m.simulate(2,42,0,0,-1,0,0,1,0)),('bad rho',lambda:m.simulate(2,42,0,0,1,1,1.1,.6,.4)),('negative weight',lambda:m.simulate(2,42,0,0,1,1,0,-.1,1.1)),('nonunit weights',lambda:m.analytical(0,0,1,1,0,.6,.5)),('bad count',lambda:m.simulate(1,42,*params)),('bool seed',lambda:m.simulate(2,True,*params)),('bool parameter',lambda:m.simulate(2,42,True,0,0,0,0,1,0)),('summary noniterable',lambda:m.summarize(None,100)),('row noniterable',lambda:m.summarize([None,None],100)),('malformed triple',lambda:m.summarize([(0,0)]*2,100)),('huge summary initial',lambda:m.summarize([(0,0,0)]*2,10**1000)),('huge summary return',lambda:m.summarize([(0,0,10**1000)]*2,100)),('zero initial',lambda:m.summarize([(0,0,0)]*2,0)),('terminal underflow',lambda:m.summarize([(0,0,-.75)]*2,5e-324)),('terminal overflow',lambda:m.summarize([(0,0,1e308)]*2,1e308)),('analytical variance overflow',lambda:m.analytical(0,0,1e308,1e308,1,.5,.5)),('analytical variance underflow',lambda:m.analytical(0,0,1e-200,0,0,1,0)),('analytical huge parameter',lambda:m.analytical(0,0,10**1000,0,0,1,0))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    before=random.getstate();m.simulate(2,42,*params);ck('local RNG preserves global state',lambda:random.getstate()==before)
    ck('seed replay',lambda:m.simulate(10,42,*params)==m.simulate(10,42,*params))
    r=random.Random(42);actual=m.simulate(4,42,*params)
    for i in range(4):
        z1,z2=r.normalvariate(0,1),r.normalvariate(0,1)
        with localcontext() as c:
            c.prec=100;a=D('.08')+D('.2')*D.from_float(z1);b=D('.04')+D('.1')*(D('.25')*D.from_float(z1)+(D(15)/16).sqrt()*D.from_float(z2));rp=D('.6')*a+D('.4')*b
        for j,want in enumerate([a,b,rp]):num('shared-normal independent joint mapping '+str((i,j)),lambda i=i,j=j:actual[i][j],want)
    runs=[]
    for count,seed,rho,sd1,sd2 in [(10000,42,.25,.2,.1),(10000,43,.25,.2,.1),(10000,42,0,.2,.1),(10,42,.25,0,0)]:
        rows=m.simulate(count,seed,.08,.04,sd1,sd2,rho,.6,.4);s=m.summarize(rows,100);q=[tuple(F(str(x)) for x in row) for row in rows];rps=[row[2] for row in q];mean_r=sum(rps)/count;v=sum((x-mean_r)**2 for x in rps)/(count-1)
        for key,want in [('mean_return',mean_r),('return_sd',sqrt(v)),('mean_terminal',100*(1+mean_r)),('standard_error_terminal',100*sqrt(v/count)),('loss_frequency',F(sum(x<0 for x in rps),count))]:num('sample arithmetic '+str((seed,rho,sd1,key)),lambda s=s,key=key:s[key],want)
        ck('asset tail counter '+str((seed,rho,sd1)),lambda s=s,q=q:s['paths_with_asset_return_below_minus_one']==sum(a< -1 or b< -1 for a,b,_ in q))
        asset_means=[sum(row[j] for row in q)/count for j in [0,1]];covar=sum((a-asset_means[0])*(b-asset_means[1]) for a,b,_ in q)/(count-1);v1=sum((a-asset_means[0])**2 for a,_,_ in q)/(count-1);v2=sum((b-asset_means[1])**2 for _,b,_ in q)/(count-1);corr=float(covar)/float(sqrt(v1*v2)) if v1 and v2 else None
        runs.append(dict(count=count,seed=seed,rho=rho,sd1=sd1,sd2=sd2,summary=s,observed_asset_correlation=corr,observed_asset_covariance=str(covar),first_rows=rows[:2],rows_sha256=hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),scope='source observations with independent conditional sample arithmetic; no independence or normal-tail certification'))
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),generator='random.Random / Mersenne Twister normalvariate',commands=commands,checks=checks,runs=runs,analytical_loss_probability=str(loss),counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=12,new_historical_methods=0),model=dict(initial=100,weights=['.6','.4'],asset_means=['.08','.04'],asset_SDs=['.2','.1'],correlation='.25',horizon='one specified model period; duration not supplied, all inputs must refer to same period',units='fictional common currency; normal simple returns, no clipping',measure='uncalibrated illustrative joint normal measure, no market/valuation-date data'),limits='Normal simple returns below -1 deliberately retained and counted. Summary trusts supplied portfolio return, not a weight/row reconciliation engine. No positivity-tail, correlation stability, multi-period/rebalancing, statistical coverage or independent model acceptance; F28/F32/F165 open.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
