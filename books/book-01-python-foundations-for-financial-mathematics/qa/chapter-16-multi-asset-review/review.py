"""Multi-asset workflow and independent rational/scenario benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.10-multi-asset-portfolios.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.10-multi-asset-portfolios.md'])
    blocks=re.findall(rb'^```python\n(.*?)^```',source_bytes,re.M|re.S)
    code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def close(label,value,want):
        ck(label,math.isclose(value,float(want),rel_tol=1e-12,abs_tol=0),actual=float(value) if math.isfinite(value) else repr(value),independent_reference=str(want),relative_tolerance=1e-12,absolute_tolerance=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:
            if value is None:ck(label,False,actual='None',independent_reference=str(want))
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
    with tempfile.TemporaryDirectory(prefix='book1-1610-') as tmp:
        Path(tmp,'multi_asset_portfolios.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['multi_asset_portfolios.py']),('isolated import',['-c','import multi_asset_portfolios']),('exact compilation',['-m','compileall','-q','multi_asset_portfolios.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['multi_asset_portfolios.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    w=[.5,.3,.2];mu=[.08,.05,.02];cov=[[.04,.006,0],[.006,.09,0],[0,0,.0004]]
    f=lambda x:F(str(x))
    def quad(weights,c):return sum(f(weights[i])*f(c[i][j])*f(weights[j]) for i in range(len(weights)) for j in range(len(weights)))
    result=m.portfolio_statistics(w,mu,cov)
    for field,want in [('expected_return',F(59,1000)),('variance',F(4979,250000)),('volatility',root(F(4979,250000)))]:close('E1/E10/E11 main '+field,result[field],want)
    for i,want in enumerate([F(109,10000),F(9,1000),F(1,62500)]):close('lab variance contribution '+str(i),result['variance_contributions'][i],want)
    close('E18 source contribution sum',math.fsum(result['variance_contributions']),F(4979,250000))
    close('E2 supplemental weight budget',sum(map(f,w)),1)
    for i in range(3):
      close('E3-E5 supplemental expected contribution '+str(i),f(w[i])*f(mu[i]),[F(1,25),F(3,200),F(1,250)][i])
      close('E6-E8 supplemental diagonal term '+str(i),f(w[i])**2*f(cov[i][i]),[F(1,100),F(81,10000),F(1,62500)][i])
    close('E9 supplemental cross term',2*f(w[0])*f(w[1])*f(cov[0][1]),F(9,5000))
    for amounts in [[50,30,20],[500,300,200]]:ck('E12/E13 source normalized '+str(amounts),m.normalize_allocations(amounts)==w)
    num('E14 zero-weight assets',lambda:m.portfolio_statistics([1,0,0],mu,cov)['expected_return'],F(2,25))
    two=m.drifted_weights([.5,.5],[.1,0])
    close('E19 drift A',two[0],F(11,21));close('E19 drift B',two[1],F(10,21))
    close('E20 supplemental realized portfolio return',F(1,2)*F(1,10),F(1,20))
    zero=m.scenario_statistics([.5,.5],[.5,.5],[[.1,0],[0,.1]])
    close('E21 source scenario mean',zero['expected_return'],F(1,20));close('E22 source scenario variance',zero['variance'],0)
    num('E23 permitted signed expected return',lambda:m.portfolio_statistics([1.2,-.2],[.1,.05],[[.04,0],[0,.09]],True)['expected_return'],F(11,100))
    realized=[.1,-.05,0];normalized=m.normalize_allocations([50,30,20]);drift=m.drifted_weights(normalized,realized)
    drift_reference=[F(110,207),F(57,207),F(40,207)]
    for i,v in enumerate(drift_reference):close('lab source drift '+str(i),drift[i],v)
    updated=m.portfolio_statistics(drift,mu,cov)
    close('lab source chained updated mean',updated['expected_return'],sum(drift_reference[i]*f(mu[i]) for i in range(3)))
    close('lab source chained updated variance',updated['variance'],sum(drift_reference[i]*f(cov[i][j])*drift_reference[j] for i in range(3) for j in range(3)))
    prob=[.25,.75];rows=[[.1,-.05,.02],[-.1,.04,.02]];scenario=m.scenario_statistics(w,prob,rows)
    pr=[F(39,1000),F(-17,500)];variance=F(1,4)*F(3,4)*(pr[0]-pr[1])**2
    for i,v in enumerate(pr):close('lab source scenario return '+str(i),scenario['scenario_returns'][i],v)
    close('lab source scenario mean',scenario['expected_return'],F(-63,4000));close('lab source scenario variance',scenario['variance'],variance);close('lab source scenario SD',scenario['volatility'],root(variance))
    # Supplemental scenario moments feed exact source portfolio_statistics: same model.
    smu=[sum(f(prob[k])*f(rows[k][i]) for k in range(2)) for i in range(3)]
    scov=[[F(3,16)*(f(rows[0][i])-f(rows[1][i]))*(f(rows[0][j])-f(rows[1][j])) for j in range(3)] for i in range(3)]
    alternative=m.portfolio_statistics(w,list(map(float,smu)),[list(map(float,row)) for row in scov])
    close('lab same-model source moment route mean',alternative['expected_return'],F(-63,4000));close('lab same-model source moment route variance',alternative['variance'],variance)
    for label,fn,want in [
      ('policy extension explicit signed scenario permission',lambda:m.scenario_statistics([1.2,-.2],[1],[[.1,.05]],True)['expected_return'],F(11,100)),
      ('F151 normalized tolerated budget mean',lambda:m.portfolio_statistics([1.00000000005],[1],[[1]])['expected_return'],1),
      ('F151 normalized tolerated budget variance',lambda:m.portfolio_statistics([1.00000000005],[1],[[1]])['variance'],1),
      ('F151 allocation total overflow avoided',lambda:m.normalize_allocations([1e308,1e308])[0],F(1,2)),
      ('F151 scenario mass normalized constant mean',lambda:m.scenario_statistics([1],[.5,.50000000005],[[.1],[.1]])['expected_return'],F(1,10)),
      ('F151 scenario mass normalized constant variance',lambda:m.scenario_statistics([1],[.5,.50000000005],[[.1],[.1]])['variance'],0),
      ('F151 zero-probability huge shock variance',lambda:m.scenario_statistics([1],[0,1],[[1e308],[0]])['variance'],0),
      ('F151 rare-large finite scenario variance',lambda:m.scenario_statistics([1],[1e-308,1],[[1e308],[0]])['variance'],1e308),
      ('F151 expected integer cancellation',lambda:m.portfolio_statistics([.5,.5],[10**18+2,-10**18],[[0,0],[0,0]])['expected_return'],1),
      ('F151 normalized drift at finite-return limit',lambda:m.drifted_weights([1.00000000005],[1.7976931348623157e308])[0],1),
    ]:num(label,fn,want)
    for label,fn in [
      ('PSD extension positive supplied direction rejected',lambda:m.portfolio_statistics([1,0],[0,0],[[1,2],[2,1]])),
      ('F151 nonboolean short policy rejected',lambda:m.portfolio_statistics([1],[0],[[1]],'yes')),
      ('policy extension default signed scenario rejected',lambda:m.scenario_statistics([1.2,-.2],[1],[[.1,.05]])),
      ('F151 nonzero normalized allocation underflow rejected',lambda:m.normalize_allocations([1e-300,1e308])),
      ('F151 nonzero variance underflow rejected',lambda:m.portfolio_statistics([.1,.9],[0,0],[[1e-323,0],[0,0]])),
      ('F151 variance overflow ValueError',lambda:m.portfolio_statistics([1.5,-.5],[0,0],[[1e308,0],[0,1e308]],True)),
      ('F151 unreconcilable contribution outputs rejected',lambda:m.portfolio_statistics([10**18+1,-10**18],[0,0],[[1,1],[1,1]],True)),
      ('F151 huge integer inputs ValueError',lambda:m.normalize_allocations([10**1000,1])),
      ('F151 malformed scenario outer ValueError',lambda:m.scenario_statistics([1],[1],None)),
      ('F151 zero-diagonal covariance row rejected',lambda:m.portfolio_statistics([1,0],[0,0],[[1,1e-20],[1e-20,0]])),
      ('negative allocations rejected',lambda:m.normalize_allocations([-1,2])),
      ('exhausted NAV rejected',lambda:m.drifted_weights([.5,.5],[-1,-1])),
      ('unleveraged return below minus one rejected',lambda:m.drifted_weights([1],[-1.1])),
      ('bad scenario mass rejected',lambda:m.scenario_statistics([1],[.4],[[.1]])),
      ('short static weights require permission',lambda:m.portfolio_statistics([1.2,-.2],[0,0],[[1,0],[0,1]])),
    ]:reject(label,fn)
    ck('lab input fixtures preserved',w==[.5,.3,.2] and mu==[.08,.05,.02] and realized==[.1,-.05,0])
    report=dict(assets=['fictional A','fictional B','cash-like C'],weights=w,original_means=mu,covariance=cov,original_statistics=result,realized_returns=realized,normalized_allocations=normalized,drifted_weights=drift,updated_statistics=updated,
      scenario_probabilities=prob,scenario_rows=rows,scenario_statistics=scenario,scenario_implied_means=list(map(str,smu)),scenario_implied_covariance=[[str(x) for x in row] for row in scov],same_model_moment_route=alternative,
      units='decimal simple returns and squared decimal covariance',horizon='one common synthetic period',currency='fictional common USD',dates=None,scenario_scope='separate alternative model from original 5.9-percent forecast',fixture_sha256=hashlib.sha256(json.dumps([w,mu,cov,realized,prob,rows]).encode()).hexdigest(),scope='local source API chain only; no actual NAV/FX/as-of source integration or costs')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
