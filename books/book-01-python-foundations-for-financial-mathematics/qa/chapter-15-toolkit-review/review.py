"""Section 15.14 exact toolkit lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.14-chapter-project-financial-statistical-analysis-toolkit.md'
    code,helper=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    csv_bytes,=re.findall(rb'^\x60\x60\x60csv\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1514-') as tmp:
        Path(tmp,'financial_statistics_toolkit.py').write_bytes(code)
        Path(tmp,'csv_example.py').write_bytes(helper)
        Path(tmp,'prices.csv').write_bytes(csv_bytes)
        for label,args in [('exact demonstration and embedded tests',['financial_statistics_toolkit.py']),('exact CSV usage example',['csv_example.py']),('isolated import',['-c','import financial_statistics_toolkit']),('exact compilation',['-m','compileall','-q','financial_statistics_toolkit.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=(methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))) if args==['financial_statistics_toolkit.py'] else (bool(p.stdout) and not p.stderr if args==['csv_example.py'] else not(p.stdout or p.stderr))
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    (HERE/'prices.csv').write_bytes(csv_bytes)
    m=types.ModuleType('toolkit_lab');sys.modules[m.__name__]=m;exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def variance(v):
        n=len(v)
        return sum((a-b)**2 for a,b in combinations(v,2))/(n*(n-1))
    def covariance(a,b):
        n=len(a)
        return sum((a[i]-a[j])*(b[i]-b[j]) for i,j in combinations(range(n),2))/(n*(n-1))
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    dates,asset,benchmark=m.load_prices_csv(HERE/'prices.csv')
    ar=[F(str(asset[i]))/F(str(asset[i-1]))-1 for i in range(1,5)];br=[F(str(benchmark[i]))/F(str(benchmark[i-1]))-1 for i in range(1,5)]
    mu=sum(ar)/4;va=variance(ar);vb=variance(br);cv=covariance(br,ar);beta=cv/vb;alpha=mu-beta*sum(br)/4
    residuals=[y-alpha-beta*x for x,y in zip(br,ar)];sse=sum(v*v for v in residuals);sst=3*va
    actual=m.report(asset,benchmark,2)
    for key,want in [('observations',4),('mean_return',mu),('volatility',root(va)),('cumulative_return',F(1,20)),('correlation',float(root(cv*cv/(va*vb))))]:close('lab B/C report '+key,actual[key],want,atol=0)
    for key,want in [('alpha',alpha),('beta',beta),('r2',1-sse/sst),('sse',sse)]:close('lab C regression '+key,actual['regression'][key],want,atol=0)
    for i,want in enumerate([(ar[i]+ar[i+1])/2 for i in range(3)]):close('lab E w2 mean '+str(i),actual['rolling_mean'][i],want,atol=0)
    for i,want in enumerate([sum(ar[i:i+3])/3 for i in range(2)]):num('lab E w3 mean '+str(i),lambda i=i:m.rolling_mean(m.simple_returns(asset),3)[i],want)
    for key,want in [('var',-min(ar)),('es',-min(ar)),('tail_count',1)]:close('lab D tail '+key,actual['historical_tail'][key],want,atol=0)
    with localcontext() as ctx:
        ctx.prec=80
        center=D(mu.numerator)/D(mu.denominator);half=D('1.959963984540054')*root(va/4)
        ci=[center-half,center+half]
    for i in [0,1]:close('lab D normal CI '+str(i),actual['normal_ci_approx'][i],ci[i],atol=0)
    ck('lab A canonical fixture dates',dates==['2026-01-05','2026-01-06','2026-01-07','2026-01-08','2026-01-09'])
    for label,fn,want in [
        ('E1 mean',lambda:m.mean([.01,.02,.03]),F(1,50)),
        ('E2 sample SD',lambda:m.sample_sd([.01,.02,.03]),F(1,100)),
        ('E3 covariance',lambda:m.sample_covariance([1,2,3],[2,4,6]),2),
        ('E4 correlation',lambda:m.pearson([1,2,3],[2,4,6]),1),
        ('E5 simple return',lambda:m.simple_returns([100,110])[0],F(1,10)),
        ('E6 compound',lambda:m.compounded([.1,-.1]),F(-1,100)),
        ('E9 slope',lambda:m.ols([1,2,3,4],[3,5,7,9])['beta'],2),
        ('E10 intercept',lambda:m.ols([1,2,3,4],[3,5,7,9])['alpha'],1),
        ('E11 R2',lambda:m.ols([1,2,3,4],[3,5,7,9])['r2'],1),
        ('E12 VaR',lambda:m.historical_tail([-.1,-.05,.01,.02],.25)['var'],F(1,10)),
        ('E13 ES',lambda:m.historical_tail([-.1,-.05,.01,.02],.5)['es'],F(3,40)),
        ('lab B disclosed large-loss stress',lambda:m.compounded([.01,.02,-.5,.03]),F('-0.469447')),
        ('F140 large mean',lambda:m.mean([1e308]*3),1e308),
        ('F140 integer SD',lambda:m.sample_sd([10**18,10**18+2]),root(2)),
        ('F140 tiny SD',lambda:m.sample_sd([0,2e-200]),root(F(2,10**400))),
        ('F140 small-product Pearson',lambda:m.pearson([0,1e-100,2e-100],[0,2e-100,4e-100]),1),
        ('F140 large-product Pearson',lambda:m.pearson([0,1e100,2e100],[0,2e100,4e100]),1),
        ('F140 reportable-large-scale Pearson',lambda:m.pearson([0,1e200,2e200],[0,2e200,4e200]),1),
        ('F140 tiny CI lower endpoint',lambda:m.normal_mean_ci([0,2e-200])[0],D('1e-200')*(1-D('1.959963984540054'))),
        ('F140 integer OLS slope',lambda:m.ols([10**18+i for i in range(4)],[3,5,7,9])['beta'],2),
        ('F140 tiny price increment',lambda:m.simple_returns([10**18,10**18+1])[0],F(1,10**18)),
        ('F140 tail boundary',lambda:m.historical_tail(list(range(100)),.14)['tail_count'],14),
        ('F140 true bankruptcy',lambda:m.compounded([1e308,1e308,-1]),-1),
    ]:num(label,fn,want)
    try:
        high_ci=m.normal_mean_ci([1,2,3],.9999999999999999)
    except Exception as exc:ck('F140 valid near-one confidence',False,exception=repr(exc))
    else:ck('F140 valid near-one confidence',len(high_ci)==2 and all(math.isfinite(v) for v in high_ci) and high_ci[0]<2<high_ci[1],actual=high_ci)
    csv_cases={
        'zero price':csv_bytes.replace(b',101,',b',0,'),
        'duplicate date':csv_bytes.replace(b'2026-01-06',b'2026-01-05'),
        'invalid ISO calendar date':csv_bytes.replace(b'2026-01-05',b'2026-00-05'),
        'lexical dates':csv_bytes.replace(b'2026-01-',b'period-'),
        'missing schema column':csv_bytes.replace(b'benchmark_price',b'wrong'),
        'duplicate schema column':csv_bytes.replace(b'benchmark_price',b'asset_price'),
        'ragged row':csv_bytes.replace(b'100,100',b'100'),
        'extra row value':csv_bytes.replace(b'100,100',b'100,100,999'),
        'nonfinite price':csv_bytes.replace(b',101,',b',nan,'),
    }
    with tempfile.TemporaryDirectory(prefix='book1-csv-1514-') as tmp:
        for label,raw in csv_cases.items():
            path=Path(tmp,'invalid.csv');path.write_bytes(raw)
            reject('lab A CSV '+label,lambda path=path:m.load_prices_csv(path))
    for label,fn in [
        ('E15 constant correlation rejected',lambda:m.pearson([1,1,1],[1,2,3])),
        ('F140 decimal constant correlation rejected',lambda:m.pearson([.05]*3,[1,2,3])),
        ('F140 decimal constant OLS rejected',lambda:m.ols([.05]*3,[1,2,3])),
        ('nonfinite price rejected',lambda:m.simple_returns([100,math.inf])),
        ('missing observation rejected',lambda:m.mean([1,None])),
        ('boolean rejected',lambda:m.mean([1,True])),
        ('F140 false total loss rejected',lambda:m.compounded([-.99]*10)),
        ('F140 unreportable compound rejected',lambda:m.compounded([1e308,1e308])),
        ('F140 collapsed CI rejected',lambda:m.normal_mean_ci([10**18,10**18+2])),
    ]:reject(label,fn)
    (HERE/'report.json').write_text(json.dumps(actual,indent=2,allow_nan=False)+'\n')
    project=dict(dates=dates,asset_prices=asset,benchmark_prices=benchmark,price_units='fictional USD',return_units='decimal simple returns',adjustment_policy='raw fictional prices; no dividends/splits supplied',
        frequency='hypothetical daily',csv_sha256=hashlib.sha256(csv_bytes).hexdigest(),source_report=actual,
        lab_phases=['A dataset','B summaries','C dependence','D uncertainty/tails','E rolling','F audit design'],lab_step_records=32,
        audit_scope='synthetic fixture only; actual corporate actions, as-of feeds, universe, timing, security, performance and independent acceptance unresolved')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),helper_sha256=hashlib.sha256(helper).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,lab_phase_records=6,lab_step_records=32,project_deliverable_records=7,readiness_domain_records=12,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
