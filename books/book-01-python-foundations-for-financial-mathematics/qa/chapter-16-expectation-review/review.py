"""Section 16.4 exact expected portfolio return lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.04-expected-portfolio-return.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1604-') as tmp:
        Path(tmp,'expected_portfolio_return.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['expected_portfolio_return.py']),('isolated import',['-c','import expected_portfolio_return']),('exact compilation',['-m','compileall','-q','expected_portfolio_return.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['expected_portfolio_return.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('expectation_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 weighted expectation',lambda:m.expected_portfolio_return([.6,.4],[.08,.04]),F(8,125)),
        ('E2 equal weights',lambda:m.expected_portfolio_return([.5,.5],[.1,0]),F(1,20)),
        ('E3 cash',lambda:m.expected_portfolio_return([.5,.4,.1],[.08,.04,.02]),F(29,500)),
        ('E4 zero weight',lambda:m.expected_portfolio_return([1,0],[.03,.99]),F(3,100)),
        ('E5 three assets',lambda:m.expected_portfolio_return([.2,.3,.5],[.1,.06,.02]),F(6,125)),
        ('E6 signed expectation',lambda:m.expected_portfolio_return([1.2,-.2],[.1,.05],True),F(11,100)),
        ('E7 one asset',lambda:m.expected_portfolio_return([1],[.07]),F(7,100)),
        ('E9 scenario A',lambda:m.scenario_expected_returns([.25,.75],[[.2,0],[0,.1]])[0],F(1,20)),
        ('E10 scenario B',lambda:m.scenario_expected_returns([.25,.75],[[.2,0],[0,.1]])[1],F(3,40)),
        ('E11 scenario portfolio',lambda:m.scenario_portfolio_distribution([.5,.5],[.25,.75],[[.2,0],[0,.1]])['mean'],F(1,16)),
        ('E12 scenario variance',lambda:m.scenario_portfolio_distribution([1],[.5,.5],[[.1],[-.1]])['variance'],F(1,100)),
        ('E13 scenario SD',lambda:m.scenario_portfolio_distribution([1],[.5,.5],[[.1],[-.1]])['sd'],F(1,10)),
        ('E14 historical mean',lambda:m.historical_mean_returns([[.1],[.3]])[0],F(1,5)),
        ('E15 forecast error',lambda:m.forecast_error([.05],[.02])[0],F(-3,100)),
        ('F145 signed product cancellation',lambda:m.expected_portfolio_return([1e308,-1e308,1],[2,2,.1],True),F(1,10)),
        ('F145 integer forecast-error precision',lambda:m.forecast_error([10**18],[10**18+1])[0],1),
        ('F145 large historical mean',lambda:m.historical_mean_returns([[1e308],[1e308]])[0],1e308),
        ('F145 normalized probability constant mean',lambda:m.scenario_expected_returns([.5,.50000000005],[[.1],[.1]])[0],F(1,10)),
        ('F145 normalized probability constant variance',lambda:m.scenario_portfolio_distribution([1],[.5,.50000000005],[[.1],[.1]])['variance'],0),
        ('F145 zero-mass huge scenario variance',lambda:m.scenario_portfolio_distribution([1],[0,1],[[1e308],[0]])['variance'],0),
        ('F145 rare large scenario finite weighted variance',lambda:m.scenario_portfolio_distribution([1],[1e-308,1],[[1e308],[0]])['variance'],1e308),
    ]:num(label,fn,want)
    w=[.5,.4,.1];forecast=[.08,.04,.02];prob=[.25,.75];rows=[[.2,0,.02],[0,.1,.02]]
    mu=m.scenario_expected_returns(prob,rows);distribution=m.scenario_portfolio_distribution(w,prob,rows)
    for i,want in enumerate([F(1,20),F(3,40),F(1,50)]):close('lab scenario asset mean '+str(i),mu[i],want,atol=0)
    for i,want in enumerate([F(51,500),F(21,500)]):close('lab scenario portfolio return '+str(i),distribution['scenario_returns'][i],want,atol=0)
    num('lab scenario route through asset means',lambda:m.expected_portfolio_return(w,mu),F(57,1000))
    close('lab direct scenario mean',distribution['mean'],F(57,1000),atol=0)
    # Probability-weighted pairwise variance identity p1*p2*(r1-r2)^2.
    close('lab independent scenario variance',distribution['variance'],F(1,4)*F(3,4)*F(3,50)**2,atol=0)
    close('lab independent scenario SD',distribution['sd'],root(F(27,40000)),atol=0)
    hist=m.historical_mean_returns([[.1],[.3]])[0];revised=[hist,.04,.02]
    num('lab labelled historical substitution',lambda:m.expected_portfolio_return(w,revised),F(59,500))
    num('lab original-forecast outcome error',lambda:m.forecast_error([.058],[.02])[0],F(-19,500))
    with localcontext() as ctx:
        ctx.prec=80
        annual=D('1.01')**12-1
    ck('E21/E22 arithmetic vs deterministic compound',annual!=D('.12'),arithmetic_reference='.12',compound_reference=str(annual),scope='supplemental derivation, not an exported source annualization function')
    for label,fn in [
        ('invalid budget rejected',lambda:m.expected_portfolio_return([.5,.4],[.1,.2])),
        ('long-only short rejected',lambda:m.expected_portfolio_return([1.2,-.2],[.1,.05])),
        ('F145 explicit short policy required',lambda:m.scenario_portfolio_distribution([1.2,-.2],[1],[[.1,.05]])),
        ('F145 nonboolean short policy rejected',lambda:m.expected_portfolio_return([1],[.1],allow_short='yes')),
        ('bad probability mass rejected',lambda:m.scenario_expected_returns([.2,.2],[[.1],[.2]])),
        ('negative probability rejected',lambda:m.scenario_expected_returns([1.2,-.2],[[.1],[.2]])),
        ('ragged scenario rows rejected',lambda:m.scenario_expected_returns([.5,.5],[[.1],[.1,.2]])),
        ('nonfinite scenario rejected',lambda:m.scenario_expected_returns([1],[[math.inf]])),
        ('missing historical data rejected',lambda:m.historical_mean_returns([[None]])),
        ('unequal error dimensions rejected',lambda:m.forecast_error([.1],[.1,.2])),
        ('F145 unreportable forecast error rejected',lambda:m.forecast_error([-1e308],[1e308])),
        ('F145 unreportable required scenario variance rejected',lambda:m.scenario_portfolio_distribution([1],[.5,.5],[[-1e308],[1e308]])),
    ]:reject(label,fn)
    def reject_value(label,fn):
        try:value=fn()
        except ValueError as exc:ck(label,True,exception=repr(exc))
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:ck(label,False,actual=repr(value))
    reject_value('F145 outer scenario shape has ValueError contract',lambda:m.scenario_portfolio_distribution([1],[1],None))
    ck('lab input models preserved',w==[.5,.4,.1] and forecast==[.08,.04,.02] and prob==[.25,.75] and rows==[[.2,0,.02],[0,.1,.02]])
    project=dict(asset_ids=['fictional A','fictional B','cash-like C'],weights=w,original_forecast=forecast,original_expected_portfolio=m.expected_portfolio_return(w,forecast),
        original_contributions=['.04','.016','.002'],scenario_probabilities=prob,scenario_rows=rows,scenario_asset_means=mu,scenario_portfolio=distribution,
        historical_A_observations=[.1,.3],historical_A_mean=hist,revised_forecast=revised,revised_expected=m.expected_portfolio_return(w,revised),
        hypothetical_realized_portfolio_return=.02,forecast_error=m.forecast_error([.058],[.02])[0],forecast_version='synthetic original t0',outcome_time='synthetic t1',dates=None,
        units='decimal one-period simple returns',currency='fictional common USD',risk_free_scope='cash-like assumed mean only, not accepted risklessness',
        fixture_sha256=hashlib.sha256(json.dumps([w,forecast,prob,rows]).encode()).hexdigest(),model_scope='distinct forecasts/scenarios/historical estimate; no empirical calibration or financing')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,lab_step_records=12,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
