"""Section 15.3 exact variance lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.03-variance-and-standard-deviation.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1503-') as tmp:
        Path(tmp,'variance_standard_deviation.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['variance_standard_deviation.py']),('isolated import',['-c','import variance_standard_deviation']),('exact compilation',['-m','compileall','-q','variance_standard_deviation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['variance_standard_deviation.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('variance');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def root(f):
        f=F(f)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(f.numerator)/D(f.denominator)).sqrt()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    x=[.02,-.01,.03,0];r=list(map(F,('.02','-.01','.03','0')))
    # Pairwise identity, independent of implementation's centered sum.
    ss=sum((a-b)**2 for a,b in combinations(r,2))/len(r)
    for ddof in (0,1):
        report=m.moments(x,ddof)
        for k,v in dict(count=4,mean=F(1,100),sum_squared_deviations=ss,variance=ss/(4-ddof),standard_deviation=root(ss/(4-ddof)),ddof=ddof).items():
            close('E1-E8 '+str(ddof)+' '+k,report[k],v,atol=0)
    for label,fn,want in [
        ('E9 constant zero',lambda:m.moments([.05]*3)['variance'],0),
        ('E10 singleton population',lambda:m.moments([.05],0)['variance'],0),
        ('E11 two-point sample',lambda:m.moments([0,.02])['variance'],F(1,5000)),
        ('E12 shifted variance',lambda:m.moments([v+.03 for v in x])['variance'],ss/3),
        ('E13 scaled variance',lambda:m.moments([2*v for v in x])['variance'],4*ss/3),
        ('E14 squared-percent units',lambda:m.moments([2,-1,3,0])['variance'],F(10,3)),
        ('E15 downside all-n',lambda:m.downside_deviation(x),F(1,200)),
        ('E17 annualized',lambda:m.scaled_volatility(.01,252),root(F(252,10000))),
        ('E19 portfolio variance',lambda:m.portfolio_variance(.5,.04,.5,.09,0),F(13,400)),
        ('E20 portfolio SD',lambda:math.sqrt(m.portfolio_variance(.5,.04,.5,.09,0)),root(F(13,400))),
        ('E21 perfect positive',lambda:m.portfolio_variance(.5,.04,.5,.09,.06),F(1,16)),
        ('E22 perfect negative',lambda:m.portfolio_variance(.5,.04,.5,.09,-.06),F(1,400)),
        ('E23 outlier variance',lambda:m.moments([.01,.01,.01,.09],0)['variance'],F(3,2500)),
        ('project annualized sample SD',lambda:m.scaled_volatility(m.moments(x)['standard_deviation'],252),root(F(21,250))),
        ('project stress variance',lambda:m.moments([.02,-.01,.13,0])['variance'],F(1,240)),
        ('F129 exact constant variance',lambda:m.moments([.05]*3)['variance'],0),
        ('F129 large constant mean',lambda:m.moments([1e308,1e308])['mean'],1e308),
        ('F129 integer spread',lambda:m.moments([10**18,10**18+2])['variance'],2),
        ('F129 tiny downside avoids squared underflow',lambda:m.downside_deviation([-1e-200]),1e-200),
        ('F129 large downside avoids squared overflow',lambda:m.downside_deviation([-1e200]),1e200),
        ('F129 valid large covariance',lambda:m.portfolio_variance(.5,1e200,.5,1e200,1e200),1e200),
    ]:num(label,fn,want)
    # Zero expectations use strict equality: an absolute tolerance can hide a constant-series residual.
    ck('F129 exact zero on constant input',m.moments([.05]*3)['variance']==0)
    for label,fn in [
        ('E10 single sample undefined',lambda:m.moments([.05])),
        ('empty rejected',lambda:m.moments([])),
        ('missing rejected',lambda:m.moments([1,None])),
        ('nonfinite rejected',lambda:m.moments([math.inf,0])),
        ('boolean ddof rejected',lambda:m.moments([1,2],True)),
        ('invalid ddof rejected',lambda:m.moments([1,2],2)),
        ('negative annualization rejected',lambda:m.scaled_volatility(.1,-1)),
        ('bad threshold rejected',lambda:m.downside_deviation(x,math.nan)),
        ('F129 zero variance forbids covariance',lambda:m.portfolio_variance(.5,0,.5,0,-1e-9)),
        ('F129 tiny infeasible covariance rejected',lambda:m.portfolio_variance(.5,1e-20,.5,1e-20,2e-20)),
        ('F129 annualization overflow rejected',lambda:m.scaled_volatility(1e308,252)),
        ('F129 unreportable moment variance rejected',lambda:m.moments([-1e308,1e308])),
    ]:reject(label,fn)
    ck('project source fixture preserved',x==[.02,-.01,.03,0])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),
             commands=commands,checks=checks,workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(source_returns=x,dates=None,frequency='hypothetical daily',units='decimal simple returns',source='synthetic manuscript fixture',corporate_actions='not applicable; supplied returns',
                fixture_sha256=hashlib.sha256(json.dumps(x).encode()).hexdigest(),population=m.moments(x,0),sample=m.moments(x),downside=m.downside_deviation(x),
                annualization_factor=252,annualized=m.scaled_volatility(m.moments(x)['standard_deviation'],252),stress_returns=[.02,-.01,.13,0],stress_sample=m.moments([.02,-.01,.13,0]),
                portfolio_variance=m.portfolio_variance(.5,.04,.5,.09,0)))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
