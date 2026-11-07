"""Portfolio volatility, risk budgets and independent rational/Decimal benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.07-portfolio-volatility.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.07-portfolio-volatility.md'])
    blocks=re.findall(rb'^```python\n(.*?)^```',source_bytes,re.M|re.S)
    code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def close(label,value,want):
        ck(label,math.isclose(value,float(want),rel_tol=1e-12,abs_tol=0),actual=float(value) if math.isfinite(value) else repr(value),independent_reference=str(want),relative_tolerance=1e-12,absolute_tolerance=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want)
    def reject(label,fn):
        try:v=fn()
        except ValueError as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(v))
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80;return (D(v.numerator)/D(v.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1607-') as tmp:
        Path(tmp,'portfolio_volatility.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['portfolio_volatility.py']),('isolated import',['-c','import portfolio_volatility']),('exact compilation',['-m','compileall','-q','portfolio_volatility.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['portfolio_volatility.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    c=[[.04,.01],[.01,.09]];w=[.6,.4];sigma=root(F(21,625));r=m.component_volatility(w,c)
    def ratio_root(value,variance):return root(value*value/variance)*(1 if value>=0 else -1)
    for label,fn,want in [
      ('E1 source variance to SD',lambda:m.portfolio_volatility([1],[[.04]]),F(1,5)),
      ('E3 worked variance',lambda:m.portfolio_variance(w,c),F(21,625)),
      ('E3 worked SD',lambda:m.portfolio_volatility(w,c),sigma),
      ('E4 concentrated',lambda:m.portfolio_volatility([1,0],c),F(1,5)),
      ('E5 independent equal risk',lambda:m.portfolio_volatility([.5,.5],[[.04,0],[0,.04]]),root(F(1,50))),
      ('E6 perfectly positive equal risk',lambda:m.portfolio_volatility([.5,.5],[[.04,.04],[.04,.04]]),F(1,5)),
      ('E7 perfect hedge',lambda:m.portfolio_volatility([.5,.5],[[.04,-.04],[-.04,.04]]),0),
      ('E8 daily annualization',lambda:m.scale_volatility(.01,252),root(F(63,2500))),
      ('E9 monthly annualization',lambda:m.scale_volatility(.04,12),root(F(12,625))),
      ('E10 sample realized',lambda:m.realized_sample_volatility([.1,-.1]),root(F(1,50))),
      ('E12 component A',lambda:r['component'][0],ratio_root(F(21,1250),F(21,625))),
      ('E12 component B',lambda:r['component'][1],ratio_root(F(21,1250),F(21,625))),
      ('E13 percentage A',lambda:r['percent'][0],F(1,2)),
      ('E13 percentage B',lambda:r['percent'][1],F(1,2)),
      ('E14 marginal A',lambda:r['marginal'][0],ratio_root(F(7,250),F(21,625))),
      ('E15 marginal B',lambda:r['marginal'][1],ratio_root(F(21,500),F(21,625))),
      ('E16 Euler component sum',lambda:math.fsum(r['component']),sigma),
      ('E19 explicit short exposure',lambda:m.portfolio_volatility([1.2,-.2],c,True),root(F(141,2500))),
      ('E20 percentage scale',lambda:m.portfolio_volatility(w,[[400,100],[100,900]]),100*sigma),
      ('E24 valid negative hedge component',lambda:m.component_volatility([.75,.25],[[1,-2],[-2,4]])['component'][1],F(-1,2)),
      ('F148 realized integer spread',lambda:m.realized_sample_volatility([10**18,10**18+1]),root(F(1,2))),
      ('F148 realized constant huge mean',lambda:m.realized_sample_volatility([1e308,1e308]),0),
      ('F148 realized tiny spread',lambda:m.realized_sample_volatility([0,1e-200]),root(F(1,2*10**400))),
      ('F148 realized large finite SD',lambda:m.realized_sample_volatility([-1e308,1e308]),root(2*F(10**616))),
      ('F148 quadratic integer-weight cancellation',lambda:m.portfolio_variance([10**18+1,-10**18],[[1,1],[1,1]],True),1),
      ('F148 quadratic large signed cancellation',lambda:m.portfolio_volatility([1e308,-1e308,1],[[2,2,2],[2,2,2],[2,2,2]],True),root(2)),
      ('F148 normalized tolerated budget',lambda:m.portfolio_volatility([1.00000000005],[[1]]),1),
      ('F148 SD before variance underflow',lambda:m.portfolio_volatility([.1,.9],[[1e-323,0],[0,0]]),root(F(1,10**325))),
      ('F148 SD before variance overflow',lambda:m.portfolio_volatility([1.5,-.5],[[1e308,0],[0,1e308]],True),root(F(5,2)*10**308)),
      ('F148 scale uses rational product before root',lambda:m.scale_volatility(1e-200,1e-200),F(1,10**300)),
    ]:num(label,fn,want)
    close('E2 supplemental volatility squared',F(15,100)**2,F(9,400))
    close('E11 supplemental population SD',root((F(1,10)**2+F(-1,10)**2)/2),F(1,10))
    close('E29 supplemental diversification ratio',F(22,100)/F(18,100),F(11,9))
    close('E30 supplemental target scale',F(9,100)/F(12,100),F(3,4))
    # Separate one-risky-sleeve model with hypothetical zero-variance residual cash.
    target=m.portfolio_volatility([.75,.25],[[.0144,0],[0,0]])
    close('lab separate target model reaches nine percent',target,F(9,100))
    close('lab original model with cash scales to 13.7477 percent',m.portfolio_volatility([.45,.3,.25],[[.04,.01,0],[.01,.09,0],[0,0,0]]),sigma*D('.75'))
    close('lab zero covariance original portfolio SD',m.portfolio_volatility(w,[[.04,0],[0,.09]]),root(F(18,625)))
    close('lab risk shares reconcile',math.fsum(r['percent']),1)
    close('lab budget-preserving marginal direction',r['marginal'][0]-r['marginal'][1],ratio_root(F(-7,500),F(21,625)))
    close('E25 consistent permutation restores risk',m.portfolio_volatility([.4,.6],[[.09,.01],[.01,.04]]),sigma)
    ck('E25 inconsistent permutation changes risk',not math.isclose(m.portfolio_volatility([.4,.6],c),float(sigma),rel_tol=1e-6))
    close('E18 supplemental unnormalized doubled volatility',root(4*F(21,625)),2*sigma)
    for label,fn in [
      ('PSD extension untested direction volatility',lambda:m.portfolio_volatility([1,0],[[1,2],[2,1]])),
      ('PSD extension untested direction attribution',lambda:m.component_volatility([1,0],[[1,2],[2,1]])),
      ('F148 negative exact tiny requested form rejected',lambda:m.portfolio_variance([.5,.5],[[1e-300,-2e-300],[-2e-300,1e-300]])),
      ('F148 reported attribution cancellation rejected',lambda:m.component_volatility([10**18+1,-10**18],[[1,1],[1,1]],True)),
      ('F148 nonboolean short policy rejected',lambda:m.portfolio_volatility([1],[[1]],'yes')),
      ('F148 nonboolean scaling assumption rejected',lambda:m.scale_volatility(.1,252,'yes')),
      ('F148 unreportable scaled result rejected',lambda:m.scale_volatility(1e308,4)),
      ('F148 nonzero scaled result underflow rejected',lambda:m.scale_volatility(1e-300,1e-300)),
      ('F148 variance underflow rejected',lambda:m.portfolio_variance([.1,.9],[[1e-323,0],[0,0]])),
      ('F148 variance overflow rejected',lambda:m.portfolio_variance([1.5,-.5],[[1e308,0],[0,1e308]],True)),
      ('F148 huge integer realized ValueError',lambda:m.realized_sample_volatility([10**1000,0])),
      ('F148 huge integer matrix ValueError',lambda:m.portfolio_volatility([1],[[10**1000]])),
      ('E17 zero-risk attribution undefined',lambda:m.component_volatility([.5,.5],[[1,-1],[-1,1]])),
      ('E18 doubled budget rejected',lambda:m.portfolio_volatility([1.2,.8],c)),
      ('scaling assumptions false rejected',lambda:m.scale_volatility(.1,252,False)),
      ('nonpositive periods rejected',lambda:m.scale_volatility(.1,0)),
      ('nonfinite returns rejected',lambda:m.realized_sample_volatility([0,math.nan])),
      ('short permission required',lambda:m.portfolio_volatility([1.2,-.2],c)),
    ]:reject(label,fn)
    ck('lab input fixtures preserved',w==[.6,.4] and c==[[.04,.01],[.01,.09]])
    report=dict(assets=['fictional A','fictional B'],weights=w,covariance=c,horizon='one synthetic period',currency='fictional common USD',dates=None,covariance_units='squared decimal simple-return units',main_attribution=r,
      standalone_volatilities=['.2','.3'],covariance_weighted_exposures=['.028','.042'],daily_annualization=dict(daily='.01',days=252,assumptions='hypothetical stable independent equal-day return increments'),
      target_model=dict(starting_volatility='.12',target_volatility='.09',scale='.75',risky_cash_weights=[.75,.25],covariance=[[.0144,0],[0,0]],achieved=target,cash_assumption='hypothetical zero covariance/variance; no real cash guarantee',costs='omitted'),fixture_sha256=hashlib.sha256(json.dumps([w,c]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
