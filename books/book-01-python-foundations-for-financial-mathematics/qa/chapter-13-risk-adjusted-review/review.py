"""Section 13.13 exact risk-adjusted performance lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.13-risk-adjusted-performance-concepts.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1313-') as tmp:
        Path(tmp,'risk_adjusted_performance.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['risk_adjusted_performance.py']),('isolated import',['-c','import risk_adjusted_performance']),('exact compilation',['-m','compileall','-q','risk_adjusted_performance.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['risk_adjusted_performance.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('risk_adjusted');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def root(f):
        f=F(f)
        with localcontext() as ctx:
            ctx.prec=55
            return (D(f.numerator)/f.denominator).sqrt()
    def mean(xs):return sum(xs)/len(xs)
    def var(xs):
        return sum((a-b)**2 for a,b in combinations(xs,2))/(len(xs)*(len(xs)-1))
    def ratio(mu,variance,k=1):
        return root(mu**2*k/variance)*(-1 if mu<0 else 1)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 mean',lambda:m.mean([.1,-.1]),0),
        ('E2 sample volatility',lambda:m.sample_std([.1,-.1]),root(F('.02'))),
        ('E3 zero Sharpe',lambda:m.sharpe_ratio([.1,-.1]),0),
        ('E4 periodic excess',lambda:m.sharpe_ratio([.1,-.1],.01),ratio(F('-.01'),F('.02'))),
        ('E5 target deviation',lambda:m.downside_deviation([.1,-.1]),root(F('.005'))),
        ('E6 zero Sortino',lambda:m.sortino_ratio([.1,-.1]),0),
        ('E7 Calmar',lambda:m.calmar_ratio(.12,-.2),F('.6')),
        ('E8 zero IR',lambda:m.information_ratio([.02,-.02]),0),
        ('E9 tracking error',lambda:m.sample_std([.02,-.02]),root(F('.0008'))),
        ('E10 beta slope',lambda:m.beta([.2,-.2],[.1,-.1]),2),
        ('E11 nonzero annual scale',lambda:m.sharpe_ratio([0,1,2],.5,12),root(3)),
        ('F107 finite mean despite overflow',lambda:m.mean([1e308,1e308]),F('1e308')),
        ('F107 tiny volatility',lambda:m.sample_std([-1e-200,1e-200]),root(F('2e-400'))),
        ('F107 tiny downside',lambda:m.downside_deviation([-1e-200,1e-200]),root(F('5e-401'))),
        ('F107 beta at extreme scales',lambda:m.beta([1e200,-1e200],[1e199,-1e199]),10),
        ('F107 risk-free subtraction preserves variation',lambda:m.sharpe_ratio([-.1,.1],1e200),ratio(F('-1e200'),F('.02'))),
        ('F107 drawdown after cumulative growth beyond float range',lambda:m.max_drawdown([1e308,1e308,-.5]),F('-.5')),
        ('F107 small drawdown',lambda:m.max_drawdown([.2,-1e-18]),F('-1e-18')),
    ]:num(label,fn,want)
    for label,fn in [
        ('E13 zero excess volatility',lambda:m.sharpe_ratio([.02,.02])),
        ('E14 no downside',lambda:m.sortino_ratio([.01,.02])),
        ('E15 zero drawdown',lambda:m.calmar_ratio(.1,0)),
        ('E16 zero benchmark variance',lambda:m.beta([.1,.2],[.01,.01])),
        ('F107 NaN annual scale',lambda:m.sharpe_ratio([.1,-.1],periods_per_year=float('nan'))),
        ('F107 infinite annual scale',lambda:m.information_ratio([.1,.2],periods_per_year=float('inf'))),
        ('F107 boolean annual scale',lambda:m.sortino_ratio([.1,-.1],periods_per_year=True)),
        ('F107 boolean risk-free input',lambda:m.sharpe_ratio([.1,.2],True)),
        ('F107 unreportable Calmar',lambda:m.calmar_ratio(1e308,-1e-100)),
        ('F107 no false complete loss',lambda:m.max_drawdown([.01]+[-.99]*12)),
        ('unequal alignment',lambda:m.beta([.1,.2],[.1,.2,.3])),
    ]:reject(label,fn)
    source_text=source.read_text()
    with localcontext() as ctx:
        ctx.prec=55
        monthly=D('1.05')**(D(1)/12)-1
    ck('E12 monthly effective conversion',source_text.count(f'{monthly:.4%}')==2)
    from project import fixtures, scorecard
    strategies, bench=fixtures()
    csv_rows=[]
    for name,xs in strategies.items():
        x=list(map(float,xs)); b=list(map(float,bench))
        active=[r-t for r,t in zip(xs,bench)]
        moments=var(xs);mu=mean(xs)
        downside=sum(min(0,r)**2 for r in xs)/len(xs)
        levels=[math.prod(1+r for r in xs[:i]) for i in range(len(xs)+1)]
        worst=min(F(y,z)-1 for j,y in enumerate(levels) for z in levels[:j+1])
        pairs=[(xs[j]-xs[i],bench[j]-bench[i]) for i,j in combinations(range(len(xs)),2)]
        slope=sum(a*b for a,b in pairs)/sum(b*b for _,b in pairs)
        expected=[mu,root(moments),root(12*moments),ratio(mu-F('.002'),moments,12),
                  ratio(mu,downside,12),worst,ratio(mean(active),var(active),12),slope]
        row=scorecard(m,name,x,b);csv_rows.append(row)
        for (metric,value),want in zip(list(row.items())[1:],expected):
            close(f'project {name} {metric}',value,want,atol=0)
    import csv,io
    from project import as_csv
    parsed=list(csv.DictReader(io.StringIO(as_csv(csv_rows))))
    ck('supplemental scorecard CSV keys and strategy order',len(parsed)==2 and list(parsed[0])==list(csv_rows[0]) and [r['strategy'] for r in parsed]==['A','B'])
    demo=list(map(F,('.04','-.02','.03','-.01','.05')))
    demo_sharpe=round(float(ratio(mean(demo),var(demo))),4)
    ck('exact demo labels and max drawdown',commands[0]['stdout'].splitlines()==[
       f'Sharpe (zero periodic risk-free rate): {demo_sharpe}','Sortino (zero target): 1.8','Maximum drawdown: -2.00%'])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
