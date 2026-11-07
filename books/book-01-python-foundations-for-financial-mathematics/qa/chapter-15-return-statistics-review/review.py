"""Section 15.11 exact financial return lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.11-financial-return-statistics.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1511-') as tmp:
        Path(tmp,'financial_return_statistics.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['financial_return_statistics.py']),('isolated import',['-c','import financial_return_statistics']),('exact compilation',['-m','compileall','-q','financial_return_statistics.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['financial_return_statistics.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('return_statistics_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def ln(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).ln()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    r=[-.04,-.01,0,.02,.08,.01];rf=[.001]*6;fr=[F(str(v)) for v in r]
    variance=sum((a-b)**2 for a,b in combinations(fr,2))/(6*5)
    with localcontext() as ctx:
        ctx.prec=80
        geo=D('.99').sqrt()-1
    for label,fn,want in [
        ('E1 simple gain',lambda:m.simple_returns([100,110])[0],F(1,10)),
        ('E2 log gain',lambda:m.log_returns([100,110])[0],ln(F(11,10))),
        ('E3 simple loss',lambda:m.simple_returns([110,99])[0],F(-1,10)),
        ('E4 additive logs',lambda:math.fsum(m.log_returns([100,110,99])),ln(F(99,100))),
        ('E5 arithmetic',lambda:m.arithmetic_mean([.1,-.1]),0),
        ('E6 geometric',lambda:m.geometric_mean([.1,-.1]),geo),
        ('E7 cumulative',lambda:m.cumulative_return([.1,-.1]),F(-1,100)),
        ('E10 volatility',lambda:m.sample_volatility([.01,.02,.03]),F(1,100)),
        ('E11 annual volatility',lambda:m.annualized_volatility([.01,.02,.03]),root(F(252,10000))),
        ('E17 historical VaR',lambda:m.historical_var([-.1,-.05,.01,.02],.25),F(1,10)),
        ('E18 historical ES',lambda:m.historical_expected_shortfall([-.1,-.05,.01,.02],.5),F(3,40)),
        ('E19 negative signed VaR',lambda:m.historical_var([.01,.02,.03]),F(-1,100)),
        ('E20 one-observation tail',lambda:m.historical_expected_shortfall([-.1]+[.01]*9,.05),F(1,10)),
        ('project longer mean',lambda:m.arithmetic_mean(r),sum(fr)/6),
        ('project longer volatility',lambda:m.sample_volatility(r),root(variance)),
        ('project longer annual volatility',lambda:m.annualized_volatility(r,252),root(252*variance)),
        ('project longer VaR',lambda:m.historical_var(r,.05),F(1,25)),
        ('project longer ES',lambda:m.historical_expected_shortfall(r,.05),F(1,25)),
        ('F137 integer price increment',lambda:m.simple_returns([10**18,10**18+1])[0],F(1,10**18)),
        ('F137 tiny simple gain',lambda:m.simple_returns([1e-308,1.1e-308])[0],F(1,10)),
        ('F137 extreme log ratio',lambda:m.log_returns([1e-308,1e308])[0],ln(F(10)**616)),
        ('F137 maximum-float geometric mean',lambda:m.geometric_mean([1.7976931348623157e308]*2),1.7976931348623157e308),
        ('F137 large mean',lambda:m.arithmetic_mean([1e308,1e308]),1e308),
        ('F137 integer-offset volatility',lambda:m.sample_volatility([10**18,10**18+2]),root(2)),
        ('F137 tiny volatility',lambda:m.sample_volatility([0,2e-200]),root(F(2,10**400))),
        ('F137 reportable large volatility',lambda:m.sample_volatility([-1e200,1e200]),root(F(2)*10**400)),
        ('F137 VaR decimal rank boundary',lambda:m.historical_var(list(range(100)),.14),-13),
        ('F137 ES decimal rank boundary',lambda:m.historical_expected_shortfall(list(range(100)),.14),F(-13,2)),
        ('F137 large ES sum',lambda:m.historical_expected_shortfall([-1e308,-1e308],.75),1e308),
        ('F137 true bankruptcy after large growth',lambda:m.cumulative_return([1e308,1e308,-1]),-1),
    ]:num(label,fn,want)
    excess=[float(F(str(a))-F(str(b))) for a,b in zip(r,rf)]
    num('project excess mean',lambda:m.arithmetic_mean(excess),F(9,1000))
    num('project excess Sharpe',lambda:m.arithmetic_mean(excess)/m.sample_volatility(excess),F(9,40))
    # E12/E13 are supplemental annualization calculations, not exported source functions.
    with localcontext() as ctx:
        ctx.prec=80
        annual_growth=D('1.001')**252-1
    ck('E12/E13 linear vs compounded convention',F(252,1000)!=F(annual_growth),linear_reference='0.252',compounded_reference=str(annual_growth))
    for label,fn in [
        ('E15 nonpositive price rejected',lambda:m.log_returns([100,0])),
        ('geometric bankruptcy rejected',lambda:m.geometric_mean([.01,-1])),
        ('below -100 return rejected',lambda:m.cumulative_return([-1.01])),
        ('singleton volatility rejected',lambda:m.sample_volatility([.1])),
        ('missing rejected',lambda:m.arithmetic_mean([.1,None])),
        ('nonfinite rejected',lambda:m.arithmetic_mean([.1,math.inf])),
        ('boolean rejected',lambda:m.arithmetic_mean([True,1])),
        ('bad alpha rejected',lambda:m.historical_var(r,0)),
        ('bad annualization rejected',lambda:m.annualized_volatility(r,0)),
        ('F137 false total loss price ratio rejected',lambda:m.simple_returns([1e308,1e-308])),
        ('F137 false total loss cumulative rejected',lambda:m.cumulative_return([-.99]*10)),
        ('F137 annual volatility overflow rejected',lambda:m.annualized_volatility([-1e308,1e308])),
    ]:reject(label,fn)
    ck('source fixtures unchanged',r==[-.04,-.01,0,.02,.08,.01] and rf==[.001]*6)
    project=dict(prices=[100,110,99],price_period_labels=[0,1,2],dates=None,currency='fictional USD',frequency='hypothetical daily',longer_returns=r,risk_free_returns=rf,
        fixture_sha256=hashlib.sha256(json.dumps([[100,110,99],r,rf]).encode()).hexdigest(),simple=m.simple_returns([100,110,99]),logs=m.log_returns([100,110,99]),
        arithmetic=m.arithmetic_mean([.1,-.1]),geometric=m.geometric_mean([.1,-.1]),cumulative=m.cumulative_return([.1,-.1]),sample_volatility=m.sample_volatility(r),
        annual_volatility=m.annualized_volatility(r),periods_per_year=252,excess_returns=excess,excess_mean=m.arithmetic_mean(excess),period_sharpe=m.arithmetic_mean(excess)/m.sample_volatility(excess),
        var_alpha=.05,var_loss=m.historical_var(r,.05),es_loss=m.historical_expected_shortfall(r,.05),convention='signed loss, nearest left-return rank and ceil-count ES; no flooring')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
