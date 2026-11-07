"""Section 15.15 exact applied answers lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.15-exercises-and-applied-problems.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1515-') as tmp:
        Path(tmp,'chapter15_applied_problems.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['chapter15_applied_problems.py']),('isolated import',['-c','import chapter15_applied_problems']),('exact compilation',['-m','compileall','-q','chapter15_applied_problems.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['chapter15_applied_problems.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('applied_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    def variance(v):
        a=[F(str(x)) for x in v];n=len(a)
        return sum((x-y)**2 for x,y in combinations(a,2))/(n*(n-1))
    for label,fn,want in [
        ('E1 mean',lambda:m.mean([1,2,3]),2),
        ('E6 SD',lambda:m.sd([.01,.02,.03]),F(1,100)),
        ('E10/E11 correlation',lambda:m.corr([1,2,3],[2,4,6]),1),
        ('E12 negative correlation',lambda:m.corr([1,2,3],[6,4,2]),-1),
        ('E20 Bonferroni',lambda:m.bonferroni(.05,20),F(1,400)),
        ('E27 compounded return',lambda:m.cumulative([.1,-.1]),F(-1,100)),
        ('E28 arithmetic mean',lambda:m.mean([.1,-.1]),0),
        ('E38 full universe mean',lambda:m.mean([.2,-.5]),F(-3,20)),
        ('F141 large mean',lambda:m.mean([1e308]*3),1e308),
        ('F141 integer-offset SD',lambda:m.sd([10**18,10**18+2]),root(2)),
        ('F141 tiny SD',lambda:m.sd([0,2e-200]),root(F(2,10**400))),
        ('F141 large SD',lambda:m.sd([-1e200,1e200]),root(F(2)*10**400)),
        ('F141 integer correlation',lambda:m.corr([10**18+i for i in range(3)],[1,2,3]),1),
        ('F141 large product correlation',lambda:m.corr([0,1e100,2e100],[0,2e100,4e100]),1),
        ('F141 small product correlation',lambda:m.corr([0,1e-100,2e-100],[0,2e-100,4e-100]),1),
        ('F141 bankruptcy before averaging overflow',lambda:m.cumulative([1e308,1e308,-1]),-1),
    ]:num(label,fn,want)
    a=[.01,-.02,.03,0,.02];fa=list(map(lambda v:F(str(v)),a));gross=math.prod((1+v for v in fa),start=F(1))
    num('case B mean',lambda:m.mean(a),F(1,125))
    num('case B SD',lambda:m.sd(a),root(F(37,100000)))
    num('case B cumulative',lambda:m.cumulative(a),gross-1)
    rolling=m.rolling(a,3)
    for i,want in enumerate([F(1,150),F(1,300),F(1,60)]):close('case B rolling '+str(i),rolling[i],want,atol=0)
    stressed=a+[-.2]
    num('case B disclosed append stress mean',lambda:m.mean(stressed),F(-2,75))
    num('case B disclosed append stress SD',lambda:m.sd(stressed),root(variance(stressed)))
    num('case B disclosed append stress cumulative',lambda:m.cumulative(stressed),gross*F(4,5)-1)
    # Case C and Part F use the exact linked toolkit, not a supplemental regression implementation.
    tk_source=BOOK/'chapter-15/15.14-chapter-project-financial-statistical-analysis-toolkit.md'
    tk_code,tk_helper=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',tk_source.read_bytes(),re.M|re.S)
    csv_bytes,=re.findall(rb'^\x60\x60\x60csv\n(.*?)^\x60\x60\x60',tk_source.read_bytes(),re.M|re.S)
    tk=types.ModuleType('assessment_toolkit');sys.modules[tk.__name__]=tk;exec(compile(tk_code,str(tk_source),'exec'),tk.__dict__)
    model=tk.ols([1,2,3,4],[3,5,7,9])
    for k,v in [('alpha',1),('beta',2),('r2',1),('sse',0)]:close('case C source OLS '+k,model[k],v,atol=0)
    num('case C prediction from source coefficients',lambda:model['alpha']+model['beta']*5,11)
    with localcontext() as ctx:
        ctx.prec=80
        d_ci=[D('.02')-D('1.959963984540054')*D('.01'),D('.02')+D('1.959963984540054')*D('.01')]
    ck('case D summary-statistic CI',float(d_ci[0])>0 and float(d_ci[0])<.02<float(d_ci[1]),independent_endpoints=list(map(str,d_ci)),se_reference='.01',scope='supplemental summary-statistic arithmetic; no raw n=100 dataset supplied')
    with tempfile.TemporaryDirectory(prefix='book1-capstone-1515-') as tmp:
        path=Path(tmp,'prices.csv');path.write_bytes(csv_bytes);dates,prices,bench=tk.load_prices_csv(path)
        capstone=tk.report(prices,bench,2)
    returns=[F(str(prices[i]))/F(str(prices[i-1]))-1 for i in range(1,5)]
    close('Part F source capstone mean',capstone['mean_return'],sum(returns)/4,atol=0)
    close('Part F source capstone SD',capstone['volatility'],root(variance(returns)),atol=0)
    close('Part F source capstone cumulative',capstone['cumulative_return'],F(1,20),atol=0)
    ck('Part F capstone output/rolling cardinality',capstone['observations']==4 and len(capstone['rolling_mean'])==3)
    for label,fn in [
        ('E13 constant correlation rejected',lambda:m.corr([1,1,1],[1,2,3])),
        ('F141 decimal constant correlation rejected',lambda:m.corr([.05]*3,[1,2,3])),
        ('singleton SD rejected',lambda:m.sd([1])),
        ('mismatched correlations rejected',lambda:m.corr([1,2,3],[1,2])),
        ('missing rejected',lambda:m.mean([1,None])),
        ('nonfinite rejected',lambda:m.mean([1,math.inf])),
        ('boolean rejected',lambda:m.mean([True,2])),
        ('bad rolling window rejected',lambda:m.rolling([1,2],0)),
        ('below total loss rejected',lambda:m.cumulative([-1.01])),
        ('bad alpha rejected',lambda:m.bonferroni(1,20)),
        ('F141 unreportable threshold rejected',lambda:m.bonferroni(1e-323,10)),
        ('F141 false total loss rejected',lambda:m.cumulative([-.99]*10)),
        ('F141 unreportable compound rejected',lambda:m.cumulative([1e308,1e308])),
    ]:reject(label,fn)
    ck('case B original fixture unchanged',a==[.01,-.02,.03,0,.02])
    project=dict(case_B=dict(returns=a,mean=m.mean(a),sample_sd=m.sd(a),cumulative=m.cumulative(a),rolling_w3=rolling,
        stress_policy='append -.20 as a sixth synthetic period',stress_returns=stressed,stress_mean=m.mean(stressed),stress_sd=m.sd(stressed),stress_cumulative=m.cumulative(stressed)),
        case_C=dict(x=[1,2,3,4],y=[3,5,7,9],source_ols=model,prediction_x5=model['alpha']+5*model['beta'],fitted=[3,5,7,9],residuals=[0,0,0,0]),
        case_D=dict(summary_n=100,summary_mean=.02,summary_sample_sd=.1,independent_ci=list(map(str,d_ci)),bonferroni=m.bonferroni(.05,20),raw_observations='not supplied'),
        case_E='design review: reject fictional backtest as decision-quality evidence until universe/as-of/cost gaps repaired; no actual data reconstruction performed',
        part_F_capstone=capstone,capstone_dates=dates,capstone_csv_sha256=hashlib.sha256(csv_bytes).hexdigest(),linked_toolkit_listing_sha256=hashlib.sha256(tk_code).hexdigest(),linked_toolkit_source_sha256=hashlib.sha256(tk_source.read_bytes()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=0,chapter_wide_prompt_records=48,applied_case_records=4,capstone_checklist_records=9,rubric_maximum=100,historical_unique_methods_added=0,linked_toolkit_calls=3,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
