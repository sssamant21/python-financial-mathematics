"""Portfolio engine project and independent rational/moment benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.15-chapter-project-portfolio-risk-and-return-engine.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.15-chapter-project-portfolio-risk-and-return-engine.md'])
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
    with tempfile.TemporaryDirectory(prefix='book1-1615-') as tmp:
        Path(tmp,'portfolio_risk_return_engine.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['portfolio_risk_return_engine.py']),('isolated import',['-c','import portfolio_risk_return_engine']),('exact compilation',['-m','compileall','-q','portfolio_risk_return_engine.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['portfolio_risk_return_engine.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    w=[.5,.3,.2];mu=[.08,.05,.02];cov=[[.04,.006,0],[.006,.09,0],[0,0,.0004]]
    base=m.report(w,mu,cov);q=F(4979,250000);sd=root(q)
    close('E1 supplemental budget',sum(F(str(x)) for x in w),1)
    for name,want in [('expected_return',F(59,1000)),('variance',q),('volatility',sd)]:close('E2/E11/E12 source '+name,base[name],want)
    for i,want in enumerate([F(1,25),F(3,200),F(1,250)]):close('E3 supplemental expected contribution '+str(i),F(str(w[i]))*F(str(mu[i])),want)
    ck('E4/E5 matrix dimension and symmetry',len(cov)==3 and all(len(row)==3 for row in cov) and all(cov[i][j]==cov[j][i] for i in range(3) for j in range(3)))
    for i,want in enumerate([F(1,100),F(81,10000),F(1,62500)]):close('E7-E9 supplemental diagonal '+str(i),F(str(w[i]))**2*F(str(cov[i][i])),want)
    close('E10 supplemental AB cross',2*F(1,2)*F(3,10)*F(3,500),F(9,5000))
    for i,want in enumerate([F(109,10000),F(9,1000),F(1,62500)]):
      close('E16-E18 source variance contribution '+str(i),base['variance_contributions'][i],want)
      close('E20 source volatility contribution '+str(i),base['volatility_contributions'][i],root(want*want/q))
    close('E19 source variance reconciliation',math.fsum(base['variance_contributions']),q);close('E20 source volatility reconciliation',math.fsum(base['volatility_contributions']),sd)
    for number,expected in [(13,'.0436'),(14,'.06'),(15,'.00016')]:
      block=re.search(r'### Exercise '+str(number)+r'.*?\*\*Worked solution:\*\* (.*?)(?=\n\n)',source_bytes.decode(),re.S).group(1)
      ck('F156 E'+str(number)+' derivative prompt/answer alignment',expected in block and ('2' in block or 'twice' in block),worked_solution=block,independent_reference=expected,scope='text derivative alignment plus independent 2*Sigma-w derivation, no source gradient export')
    for i,want in enumerate([F(109,2500),F(3,50),F(1,6250)]):close('E13-E15 independent derivative from source VC '+str(i),2*F(str(base['variance_contributions'][i]))/F(str(w[i])),want)
    ck('zero-risk volatility attribution remains undefined',m.report([1],[0],[[0]])['volatility_contributions'] is None)
    series=[[.01,-.01,.02,0],[.02,0,.03,-.01],[.001]*4]
    def paircov(a,b):return sum((F(str(a[i]))-F(str(a[j])))*(F(str(b[i]))-F(str(b[j]))) for i in range(len(a)) for j in range(i+1,len(a)))/(len(a)*(len(a)-1))
    sample=m.sample_covariance(series);smeans=[sum(F(str(v)) for v in row)/4 for row in series]
    for i in range(3):
      for j in range(3):close('lab source sample covariance '+str((i,j)),sample[i][j],paircov(series[i],series[j]))
    observed=m.report(w,list(map(float,smeans)),sample)
    close('lab local historical-moment route expectation',observed['expected_return'],F(57,10000));close('lab local historical-moment route variance',observed['variance'],F(79,600000))
    num('E21 separate written sample covariance',lambda:m.sample_covariance([[1,2,3],[2,4,6]])[0][1],2)
    drift=m.drift([.5,.5],[.1,0]);close('E24 source drift A',drift['ending_weights'][0],F(11,21));close('E24 source drift B',drift['ending_weights'][1],F(10,21));close('E25 ending NAV from source return',100*(1+drift['portfolio_return']),105)
    trade=m.rebalance([.4,.6],[.5,.5],100);close('E26 source buy',trade['trades'][0],10);close('E26 source sell',trade['trades'][1],-10);close('E27 source turnover',trade['one_way_turnover'],F(1,10));close('E28 source gross traded',trade['gross_traded'],20)
    chained=m.rebalance(drift['ending_weights'],[.5,.5],105)
    close('lab drift-to-rebalance sale',chained['trades'][0],F(-5,2));close('lab drift-to-rebalance buy',chained['trades'][1],F(5,2));close('lab drift-to-rebalance turnover',chained['one_way_turnover'],F(1,42))
    ck('E29 deliberately breached cap',not m.within_caps(w,[.4,.4,.3]));ck('lab original caps pass',m.within_caps(w,[.6,.4,.3]))
    stressed=m.stress(w,mu,cov,2);close('E30 coherent stress variance',stressed['variance'],4*q);close('E30 coherent stress SD',stressed['volatility'],2*sd)
    ck('stress expectation unchanged and attribution scales',stressed['expected_return']==base['expected_return'] and all(math.isclose(stressed['variance_contributions'][i],4*base['variance_contributions'][i],rel_tol=1e-12) and math.isclose(stressed['volatility_contributions'][i],2*base['volatility_contributions'][i],rel_tol=1e-12) for i in range(3)))
    for label,fn,want in [
      ('F156 explicit budget policy normalized mean',lambda:m.report([1.00000000005],[1],[[1]])['expected_return'],1),
      ('F156 explicit budget policy normalized variance',lambda:m.report([1.00000000005],[1],[[1]])['variance'],1),
      ('F156 integer expected-return cancellation',lambda:m.report([.5,.5],[10**18+2,-10**18],[[0,0],[0,0]])['expected_return'],1),
      ('F156 integer sample centering',lambda:m.sample_covariance([[10**18,10**18+1]])[0][0],F(1,2)),
      ('F156 large constant sample mean',lambda:m.sample_covariance([[1e308,1e308]])[0][0],0),
      ('F156 finite covariance after denominator',lambda:m.sample_covariance([[-1e154,0,1e154]])[0][0],1e308),
      ('F156 tiny drift return retained',lambda:m.drift([1],[1e-308])['portfolio_return'],F(1,10**308)),
      ('F156 large NAV turnover avoids denominator overflow',lambda:m.rebalance([.4,.6],[.5,.5],1e308)['one_way_turnover'],F(1,10)),
      ('F156 zero covariance huge multiplier remains zero',lambda:m.stress([1],[0],[[0]],1e308)['variance'],0),
      ('F156 stress finite after intermediate square overflow',lambda:m.stress([1],[0],[[1e-300]],1e200)['variance'],10**100),
    ]:num(label,fn,want)
    try:v=m.within_caps([.50000000001,.49999999999],[.5,1]);ck('F156 tiny cap breach not hidden',v is False,actual=v)
    except Exception as e:ck('F156 tiny cap breach not hidden',False,exception=repr(e))
    for label,fn in [
      ('PSD extension invalid direction rejected',lambda:m.report([1,0],[0,0],[[1,2],[2,1]])),
      ('F156 zero multiplier cannot hide invalid covariance',lambda:m.stress([1],[0],[[-1]],0)),
      ('F156 negative tiny variance not clipped',lambda:m.report([1],[0],[[-1e-300]])),
      ('F156 unreportable required variance rejected',lambda:m.report([.1,.9],[0,0],[[1e-323,0],[0,0]])),
      ('F156 unreportable gross trade ValueError',lambda:m.rebalance([1,0],[0,1],1e308)),
      ('F156 budget outside absolute tolerance rejected',lambda:m.report([1.0000000005],[0],[[0]])),
      ('F156 invalid cap weights rejected',lambda:m.within_caps([-.1,1.1],[1,1])),
      ('F156 malformed report ValueError',lambda:m.report(None,None,None)),
      ('F156 invalid drift return type ValueError',lambda:m.drift([1],[None])),
      ('F156 huge integer input ValueError',lambda:m.report([1],[10**1000],[[0]])),
      ('F156 covariance underflow ValueError',lambda:m.sample_covariance([[0,1e-200]])),
      ('F156 positive wealth cannot report false total loss',lambda:m.drift([1,1e-308],[-1,0])),
      ('exhausted NAV rejected',lambda:m.drift([.5,.5],[-1,-1])),
      ('misaligned rebalance rejected',lambda:m.rebalance([1],[.5,.5],100)),
    ]:reject(label,fn)
    ck('lab fixtures preserved',w==[.5,.3,.2] and mu==[.08,.05,.02])
    project=dict(assets=['fictional A','fictional B','cash-like C'],weights=w,original_means=mu,original_covariance=cov,original_report=base,
      historical_series_asset_major=series,historical_means=list(map(str,smeans)),historical_covariance=sample,historical_report=observed,drift=drift,written_trade_example=trade,drift_to_rebalance=chained,stress_2x=stressed,
      units='decimal simple returns and squared covariance; fictional USD NAV',timing='synthetic t0 forecasts, four historical common labels, separate t0-t1 two-asset realized-return fixture',dates=None,missingness='complete common observations, no imputation',scope='separate forecast/history/drift models, no costs, actual IDs/timestamps/NAV/FX integration or independent acceptance',fixture_sha256=hashlib.sha256(json.dumps([w,mu,cov,series]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,acceptance_checklist_records=12,historical_unique_methods_added=0,project_report=project)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
