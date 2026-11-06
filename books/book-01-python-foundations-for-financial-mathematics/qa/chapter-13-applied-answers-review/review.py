"""Section 13.15 exact chapter assessment lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.15-exercises-and-applied-problems.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1315-') as tmp:
        Path(tmp,'chapter13_exercises.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['chapter13_exercises.py']),('isolated import',['-c','import chapter13_exercises']),('exact compilation',['-m','compileall','-q','chapter13_exercises.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['chapter13_exercises.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('assessment');exec(compile(code,str(source),'exec'),m.__dict__)
    from datetime import date
    from decimal import Decimal as D, localcontext
    from scorecard import scorecard,root
    def num(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    with localcontext() as ctx:
        ctx.prec=55
        root144=(D(60100).sqrt()-50)/200-1
    for label,fn,want,atol in [
        ('E5 compounded return',lambda:m.cumulative([.1,-.1]),F('-.01'),0),
        ('E6 three-period return',lambda:m.cumulative([.05,-.02,.03]),F('.05987'),0),
        ('E9 arithmetic',lambda:m.arithmetic([.2,-.1]),F('.05'),0),
        ('E10 geometric',lambda:m.geometric([.2,-.1]),root(F('1.08'))-1,0),
        ('E12 portfolio TWR',lambda:m.twr(100,[(110,50),(144,0)]),F('-.01'),0),
        ('E13 investor IRR',lambda:m.irr([-100,110]),F('.1'),1e-10),
        ('E14 and B investor IRR',lambda:m.irr([-100,-50,144]),root144,1e-10),
        ('B IRR repricing',lambda:m.npv(m.irr([-100,-50,144]),[-100,-50,144]),0,1e-7),
        ('E17 sample dispersion',lambda:m.sample_volatility([.1,-.1]),root(F('.02')),0),
        ('E20 drawdown',lambda:min(m.drawdowns([.2,-.25,1/3])),F('-.25'),0),
        ('E22 annual Sharpe',lambda:m.sharpe([-.01,.01,.03],.002,12),root(F('1.92')),0),
        ('E27 and E left root',lambda:m.irr([-100,230,-132],lower=0,upper=.15),F('.1'),1e-10),
        ('E27 and E right root',lambda:m.irr([-100,230,-132],lower=.15,upper=.25),F('.2'),1e-10),
        ('E28 total loss',lambda:m.cumulative([.1,-1,1]),-1,0),
        ('A cash-held return using account-level periods',lambda:m.cumulative([.06,float(F(-3,106))]),F('.03'),0),
        ('A reinvestment contrast',lambda:m.cumulative([.06,float(F(-3,104))]),F(153,5200),0),
        ('F109 tiny cumulative return',lambda:m.cumulative([1e-18]),F('1e-18'),0),
        ('F109 growth cancellation with total loss',lambda:m.cumulative([1e308,1e308,-1]),-1,0),
        ('F109 tiny volatility',lambda:m.sample_volatility([-1e-200,1e-200]),root(F('2e-400')),0),
        ('F109 TWR after offsetting factors',lambda:m.twr(1e-308,[(1e308,0),(2e-308,0)]),1,0),
        ('F109 IRR scale invariance',lambda:m.irr([-1e-250,1.125e-250]),F('.125'),1e-10),
    ]:num(label,fn,want,atol)
    for label,fn in [
        ('E30 flat Sharpe',lambda:m.sharpe([.01,.01])),
        ('E same sign bracket cannot disambiguate',lambda:m.irr([-100,230,-132],lower=0,upper=.3)),
        ('F109 scaled same-sign bracket',lambda:m.irr([-1e-250,2e-250],lower=0,upper=.5)),
        ('F109 numeric-string risk-free rate',lambda:m.sharpe([.01,.02],'0.002')),
        ('F109 boolean flow',lambda:m.twr(100,[(110,True),(110,0)])),
        ('F109 boolean discount rate',lambda:m.npv(True,[-100,110])),
        ('F109 false complete loss',lambda:m.cumulative([-.99]*10)),
        ('missing return',lambda:m.cumulative([.01,None])),
    ]:reject(label,fn)
    ck('E15 elapsed day count',(date(2026,1,1)-date(2025,1,1)).days==365)
    path=[100,108,104,112,98,91,100,112,118]
    dds=m.drawdowns([float(F(y,x)-1) for x,y in zip(path,path[1:])])
    want,peak,trough=min((F(w,p)-1,i,j) for j,w in enumerate(path) for i,p in enumerate(path[:j+1]))
    for i,x in enumerate(dds):close(f'C observation {i}',x,F(path[i],max(path[:i+1]))-1,atol=0)
    ck('C peak/trough/recovery/high-water and gain',(peak,trough,path.index(path[peak],trough+1),max(path),F(path[peak],path[trough])-1)==(3,5,7,118,F(21,91)))
    ck('C depth',math.isclose(min(dds),float(want),rel_tol=1e-12))
    rates=lambda x:[F(n,100) for n in x]
    bench=rates([2,-1,2,-1,1,1]); results={}
    for name,xs in [('A',rates([3,-2,4,-1,2,1])),('B',rates([2,-1,3,-2,1,2]))]:
        results[name]=scorecard(xs,bench)
        r=list(map(float,xs)); independently=results[name]
        for label,fn in [('mean',lambda:m.arithmetic(r)),('geo',lambda:m.geometric(r)),
                         ('cumulative',lambda:m.cumulative(r)),('vol',lambda:m.sample_volatility(r)),
                         ('annual_vol',lambda:m.sample_volatility(r)*math.sqrt(12)),
                         ('mdd',lambda:min(m.drawdowns(r))),('sharpe',lambda:m.sharpe(r,.002,12))]:
            num(f'D {name} {label}',fn,independently[label])
        ck(f'D {name} geometric reconciliation and AM–GM',
           math.isclose((1+m.geometric(r))**6,1+m.cumulative(r),rel_tol=1e-12) and m.arithmetic(r)>=m.geometric(r))
    prose=source.read_text()
    ck('F109 printed IRRs agree',prose.count(f'−{abs(root144):.2%}')==2)
    ck('F109 printed downside, Sortino and IR supplied',all(f'{results[k]["downside"]:.6%}' in prose and
        all(f'{results[k][field]:.6f}' in prose for field in ['sortino','information']) for k in results))
    a=results['A']
    ck('exact demo',commands[0]['stdout'].splitlines()==[
        f'Cumulative: {float(a["cumulative"]):.6%}',f'Geometric monthly: {a["geo"]:.6%}',
        f'Sample monthly volatility: {a["vol"]:.6%}',f'Maximum drawdown: {float(a["mdd"]):.6%}',
        f'Annualized Sharpe: {a["sharpe"]:.6f}'])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             chapter_wide_prompt_records=30,applied_problem_records=5,acceptance_project_deliverable_records=12,
             knowledge_check_records=7,historical_unique_methods_added=0,
             supplemental_strategy_scorecards={k:{n:str(v) for n,v in row.items()} for k,row in results.items()})
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
