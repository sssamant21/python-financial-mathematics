"""Section 13.14 exact performance analyzer lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.14-chapter-project-investment-performance-analyzer.md'
    fragment,code=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1314-') as tmp:
        Path(tmp,'investment_performance_analyzer.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['investment_performance_analyzer.py']),('isolated import',['-c','import investment_performance_analyzer']),('exact compilation',['-m','compileall','-q','investment_performance_analyzer.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['investment_performance_analyzer.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('analyzer');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def dec(f):
        f=F(f);return D(f.numerator)/f.denominator
    def power(f,n=1,d=2):
        with localcontext() as ctx:
            ctx.prec=55
            return dec(f)**(D(n)/d)
    def num(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    xs=[F(n,100) for n in [3,-2,4,-1,2,1]]
    rs=list(map(float,xs));mu=sum(xs)/6
    factors=[math.prod(1+r for r in xs[:i]) for i in range(7)]
    depth=[min(F(v,p)-1 for p in factors[:i+1]) for i,v in enumerate(factors)]
    var=sum((a-b)**2 for a,b in combinations(xs,2))/30
    geo=power(factors[-1],1,6)-1
    expected_sharpe=power((mu-F('.002'))**2*12/var)
    with localcontext() as ctx:
        ctx.prec=55
        irr=(D(60100).sqrt()-50)/200-1
    for label,fn,want,atol in [
        ('E1 dataset A arithmetic',lambda:m.arithmetic(rs),mu,0),
        ('E2 factor',lambda:1+m.link(rs[:2]),F('1.0094'),0),
        ('E3 link',lambda:m.link([.2,-.1]),F('.08'),0),
        ('E4 geometric',lambda:m.geometric([.2,-.1]),power(F('1.08'))-1,0),
        ('E5 arithmetic',lambda:m.arithmetic([.2,-.1]),F('.05'),0),
        ('E6 sample volatility',lambda:m.sample_vol([.1,-.1]),power(F('.02')),0),
        ('E8 drawdown',lambda:min(m.drawdowns([.2,-.25])),F('-.25'),0),
        ('E10 periodic Sharpe',lambda:m.sharpe([-.01,.01,.03],.002,1),F('.4'),0),
        ('E11 annualized Sharpe',lambda:m.sharpe([-.01,.01,.03],.002,12),power(F('1.92')),0),
        ('E12 simple return',lambda:m.returns_from_values([100,110])[0],F('.1'),0),
        ('E13 second return',lambda:m.returns_from_values([160,144])[0],F('-.1'),0),
        ('E14 B exact TWR',lambda:m.twr(100,[(110,50),(144,0)]),F('-.01'),0),
        ('E16 periodic IRR',lambda:m.irr([-100,110]),F('.1'),1e-10),
        ('E17 NPV residual',lambda:m.npv(.1,[-100,110]),0,1e-12),
        ('C IRR via positive quadratic gross root',lambda:m.irr([-100,-50,144]),irr,1e-10),
        ('C residual',lambda:m.npv(m.irr([-100,-50,144]),[-100,-50,144]),0,1e-7),
        ('A sample volatility',lambda:m.sample_vol(rs),power(var),0),
        ('A annualized Sharpe',lambda:m.sharpe(rs,.002),expected_sharpe,0),
        ('A cumulative return',lambda:m.link(rs),factors[-1]-1,0),
        ('A geometric mean',lambda:m.geometric(rs),geo,0),
        ('A contextual geometric fragment',lambda:eval(compile(fragment,str(source),'eval'),{'returns':rs,'math':math}),geo,0),
        ('A geometric reconciliation',lambda:(1+m.geometric(rs))**6,factors[-1],0),
        ('A wealth reconciliation',lambda:100*(1+m.link(rs)),100*factors[-1],0),
        ('true depletion geometric',lambda:m.geometric([.2,-1,.1]),-1,0),
        ('true depletion drawdown',lambda:min(m.drawdowns([.2,-1,.1])),-1,0),
        ('F108 tiny simple return',lambda:m.returns_from_values([10**18,10**18+1])[0],F('1e-18'),0),
        ('F108 tiny link',lambda:m.link([1e-18]),F('1e-18'),0),
        ('F108 link after offsetting large factors',lambda:m.link([1e308,1e308,-.99,-1]),-1,0),
        ('F108 TWR after offsetting large factors',lambda:m.twr(1e-308,[(1e308,0),(2e-308,0)]),1,0),
        ('F108 tiny sample volatility',lambda:m.sample_vol([-1e-200,1e-200]),power(F('2e-400')),0),
        ('F108 tiny cash-flow IRR',lambda:m.irr([-1e-250,1.125e-250]),F('.125'),1e-10),
        ('F108 tiny drawdown',lambda:min(m.drawdowns([.01,-1e-18])),F('-1e-18'),0),
    ]:num(label,fn,want,atol)
    for label,fn in [
        ('E18 undefined scalar Sharpe',lambda:m.sharpe([.01,.01])),
        ('F108 empty drawdown',lambda:m.drawdowns([])),
        ('F108 impossible arithmetic return',lambda:m.arithmetic([-1.01])),
        ('F108 positive linked factor not a true total loss',lambda:m.link([-.99]*10)),
        ('F108 scaled same-sign bracket',lambda:m.irr([-1e-250,2e-250],low=0,high=.5)),
        ('nonfinite return',lambda:m.report([.1,float('nan')])),
        ('nonpositive post-flow base',lambda:m.twr(100,[(100,-100),(0,0)])),
    ]:reject(label,fn)
    for i,(value,want) in enumerate(zip(m.drawdowns(rs),depth)):
        close(f'A drawdown observation {i}',value,want,atol=0)
    ck('A drawdown count and range',len(m.drawdowns(rs))==7 and all(-1<=d<=0 for d in m.drawdowns(rs)))
    ck('A AM–GM',m.arithmetic(rs)>=m.geometric(rs))
    try:
        flat=m.report([.01,.01]);ck('F108 report retains defined metrics on flat returns',flat['annualized_sharpe'] is None and flat['maximum_drawdown']==0)
    except Exception as e:ck('F108 report retains defined metrics on flat returns',False,exception=repr(e))
    report=m.report(rs,.002)
    num('F108 annual volatility in report',lambda:report['annualized_volatility'],power(var*12))
    ck('F108 Dataset C prose agrees with reference',source.read_text().count(f'−{abs(irr):.2%}')==2)
    expected_values=dict(arithmetic=mu,geometric=geo,cumulative=factors[-1]-1,sample_volatility=power(var),
                         maximum_drawdown=min(depth),annualized_sharpe=expected_sharpe,annualized_volatility=power(var*12))
    ck('exact demo lines',commands[0]['stdout'].splitlines()==[f'{k}: {float(expected_values[k]):.6f}' for k in report])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),fragment_sha256=hashlib.sha256(fragment).hexdigest(),
             commands=commands,checks=checks,workflow_records=1,lab_step_records=12,local_prompt_records=18,extension_records=5,
             historical_unique_methods_added=0,independent_dataset_a={k:str(v) for k,v in expected_values.items()},
             independent_wealth_index=[str(x*100) for x in factors])
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
