"""Exact return listing; Decimal moments/integrated CDF and replay separated."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.05-return-simulations.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
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
    with tempfile.TemporaryDirectory(prefix='book1-1805-') as tmp:
        Path(tmp,'return_simulations.py').write_bytes(code)
        for label,args in [('exact demo/tests',['return_simulations.py']),('quiet import',['-c','import return_simulations']),('compile',['-m','compileall','-q','return_simulations.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==10 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('returns_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    for label,fn,want in [('E1 simple up',lambda:F(110-100,100),F(1,10)),('E2 simple down',lambda:F(90-100,100),F(-1,10)),('E3 terminal',lambda:100*(1+F(5,100)),105),('E4 profit',lambda:F(105)-100,5),('E5 zero price return',lambda:F(0-100,100),-1),('E8 zero log conversion',lambda:exp(0)-1,0),('E9 compounded return',lambda:F(11,10)*F(9,10)-1,F(-1,100)),('E10 discrete mean',lambda:(F(-1,10)+F(1,10))/2,0),('E11 discrete variance',lambda:F(1,100),F(1,100)),('E12 discrete SD',lambda:sqrt(F(1,100)),F(1,10)),('E13 discrete loss',lambda:F(1,2),F(1,2)),('E18 mean simple return',lambda:exp(F(3,50))-1,exp(F(3,50))-1),('E19 source expectation',lambda:m.expected_terminal(100,.04,.2),100*exp(F(3,50))),('E20 median',lambda:100*exp(F(1,25)),100*exp(F(1,25))),('E22 source deterministic terminal',lambda:m.terminal_values(100,m.simulate_log_returns(.04,0,2,42))[0],100*exp(F(1,25))),('E23 zero drift volatility',lambda:m.expected_terminal(100,0,0),100),('E26 sample SE example',lambda:F(20,100),F(1,5)),('E27 fourfold N factor',lambda:sqrt(F(1,4)),F(1,2)),('E33 discounted expectation',lambda:F(100)/F(105,100),F(2000,21))]:num(label,fn,want)
    with localcontext() as c:c.prec=100;ln11=(D(11)/10).ln()
    num('E7 log return Decimal',lambda:math.log1p(.1),ln11)
    for label,val,places,want in [('printed log',ln11,7,.0953102),('printed mean',100*exp(F(3,50)),5,106.18365),('printed median',100*exp(F(1,25)),5,104.08108),('printed simple return',exp(F(3,50))-1,7,.0618365),('printed discount',F(2000,21),4,95.2381)]:ck(label,lambda val=val,places=places,want=want:round(float(val),places)==want)
    # Independent central probability benchmark via convergent integral series at x=.2.
    with localcontext() as c:
        c.prec=100;x=D(1)/5;pi=D('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679');term=x;integral=term
        for n in range(1,60):term*= -x*x/D(2*n);integral+=term/D(2*n+1)
        loss=D('.5')-integral/(2*pi).sqrt()
    ck('E21 independently integrated central CDF rounded',lambda:round(float(loss),5)==.42074)
    num('E24 exact threshold not loss',lambda:m.summarize([100,100],100)['loss_frequency'],0)
    num('constant sample SE',lambda:m.summarize([100,100],100)['standard_error_terminal'],0)
    num('known sample return',lambda:m.summarize([90,100,110],100)['mean_simple_return'],0)
    num('known sample SE',lambda:m.summarize([90,100,110],100)['standard_error_terminal'],sqrt(F(100,3)))
    ck('integer zero-log identity',lambda:m.terminal_values(10**18+1,[0])[0]==10**18+1)
    ck('integer zero-expectation identity',lambda:m.expected_terminal(10**18+1,0,0)==10**18+1)
    num('small return from integer outcomes',lambda:m.summarize([10**18+1,10**18+1],10**18)['mean_simple_return'],F(1,10**18))
    num('tiny positive SE',lambda:m.summarize([1e-308,3e-308],1e-308)['standard_error_terminal'],F(1,10**308))
    num('large spread finite SE',lambda:m.summarize([5e-324,1.79e308],100)['standard_error_terminal'],F(179*10**306,2))
    num('E34 small log1p supplemental',lambda:math.log1p(1e-20),D('1e-20'))
    num('E35 small expm1 supplemental',lambda:math.expm1(1e-20),D('1e-20'))
    num('scaled exponential extension high exponent',lambda:m.terminal_values(1e-308,[1000])[0],D('1e-308')*exp(1000))
    num('scaled exponential extension low exponent',lambda:m.expected_terminal(1e308,-1000,0),D('1e308')*exp(-1000))
    for label,fn in [('huge drift',lambda:m.simulate_log_returns(10**1000,0,2,1)),('negative volatility',lambda:m.simulate_log_returns(0,-.1,2,1)),('boolean drift',lambda:m.simulate_log_returns(True,0,2,1)),('normal generated overflow',lambda:m.simulate_log_returns(1.79e308,1.79e308,20,1)),('count1',lambda:m.simulate_log_returns(0,.1,1,1)),('bool seed',lambda:m.simulate_log_returns(0,.1,2,True)),('initial zero',lambda:m.terminal_values(0,[0])),('huge initial',lambda:m.terminal_values(10**1000,[0])),('noniterable returns',lambda:m.terminal_values(100,None)),('bool return',lambda:m.terminal_values(100,[True])),('huge log return',lambda:m.terminal_values(100,[10**1000])),('terminal overflow',lambda:m.terminal_values(100,[1000])),('terminal underflow',lambda:m.terminal_values(100,[-1000])),('summary noniterable',lambda:m.summarize(None,100)),('summary huge initial',lambda:m.summarize([100,100],10**1000)),('summary negative observation',lambda:m.summarize([-1,1],100)),('summary bool observation',lambda:m.summarize([True,1],100)),('summary huge observation',lambda:m.summarize([10**1000,1],100)),('summary overflow simple return',lambda:m.summarize([1e308,1e308],5e-324)),('expectation huge int',lambda:m.expected_terminal(10**1000,0,0)),('expectation overflow',lambda:m.expected_terminal(100,1000,0)),('expectation underflow',lambda:m.expected_terminal(100,-1000,0))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    ck('early positive exponent bound',lambda:rejects(lambda:m.expected_terminal(100,2001,0)))
    ck('early negative exponent bound',lambda:rejects(lambda:m.expected_terminal(100,-2001,0)))
    ck('empty log return iterable',lambda:m.terminal_values(100,[])==[])
    before=random.getstate();m.simulate_log_returns(.04,.2,10,42);ck('local RNG preserves global state',lambda:random.getstate()==before)
    ck('seed replay',lambda:m.simulate_log_returns(.04,.2,100,42)==m.simulate_log_returns(.04,.2,100,42))
    runs=[]
    for seed,sd in [(42,.2),(43,.2),(42,0)]:
        logs=m.simulate_log_returns(.04,sd,10000,seed);values=m.terminal_values(100,logs);summary=m.summarize(values,100);q=[F(str(v)) for v in values];mu=sum(q)/len(q);var=sum((v-mu)**2 for v in q)/(len(q)-1)
        num('sample mean independent arithmetic '+str((seed,sd)),lambda summary=summary:summary['mean_terminal'],mu)
        num('sample return independent arithmetic '+str((seed,sd)),lambda summary=summary:summary['mean_simple_return'],mu/100-1)
        num('sample SE independent arithmetic '+str((seed,sd)),lambda summary=summary:summary['standard_error_terminal'],sqrt(var/len(q)))
        num('sample strict loss count '+str((seed,sd)),lambda summary=summary:summary['loss_frequency'],F(sum(v<100 for v in q),len(q)))
        runs.append(dict(seed=seed,sd_log=sd,count=len(q),summary=summary,loss_count=sum(v<100 for v in q),log_stream_sha256=hashlib.sha256(json.dumps(logs,separators=(',',':')).encode()).hexdigest(),analytical_mean=str(100*exp(F(1,25)+F(str(sd))**2/2)),limit='actual source observations; sample arithmetic independent, statistical distribution or generator independence not certified'))
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),generator='random.Random / Mersenne Twister normalvariate',commands=commands,checks=checks,runs=runs,integrated_central_loss_probability=str(loss),counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=10,new_historical_methods=0),model=dict(initial=100,mean_log='.04',sd_log='.2',horizon='one year',units='fictional common currency; one-period dimensionless log returns',measure='uncalibrated illustrative probability distribution, not market price or forecast'),limits='Central CDF series is a supplemental fixed-point oracle, not a tail-capable source API; F165 remains open. No rare-event/interval-coverage/independence/platform or independent model acceptance.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
