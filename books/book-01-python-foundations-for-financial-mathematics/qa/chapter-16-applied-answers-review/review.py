"""Chapter 16 applied answers and independent rational/linked-source benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.16-exercises-and-applied-problems.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.16-exercises-and-applied-problems.md'])
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
    with tempfile.TemporaryDirectory(prefix='book1-1616-') as tmp:
        Path(tmp,'chapter16_applied_problems.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['chapter16_applied_problems.py']),('isolated import',['-c','import chapter16_applied_problems']),('exact compilation',['-m','compileall','-q','chapter16_applied_problems.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['chapter16_applied_problems.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    linked_modules={};linked_calls=[]
    def module(file):
      if file not in linked_modules:
        path=BOOK/'chapter-16'/file;raw=path.read_bytes();listing=next(x for x in re.findall(rb'^```python\n(.*?)^```',raw,re.M|re.S) if b'import unittest' in x)
        mod=types.ModuleType(file);exec(compile(listing,str(path),'exec'),mod.__dict__)
        linked_modules[file]=(mod,dict(path=str(path.relative_to(BOOK)),source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing).hexdigest()))
      return linked_modules[file][0]
    def call(file,name,args,label):
      try:value=getattr(module(file),name)(*args)
      except Exception as exc:
        linked_calls.append(dict(label=label,path=file,function=name,args=repr(args),exception=repr(exc)))
        raise
      if name=='simplex_grid':value=list(value)
      linked_calls.append(dict(label=label,path=file,function=name,args=repr(args),result=repr(value)))
      return value
    w=[.5,.3,.2];mu=[.08,.05,.02];cov=[[.04,.006,0],[.006,.09,0],[0,0,.0004]];q=F(4979,250000)
    base=m.portfolio_stats(w,mu,cov)
    close('E1 supplemental normalized positions',F(40,100)+F(35,100)+F(25,100),1);close('E2/E37 supplemental gross',abs(F(6,5))+abs(F(-1,5)),F(7,5))
    num('E3 source realized return',lambda:m.drift([.4,.6],[.1,-.05])['return'],F(1,100))
    for key,want in [('mean',F(59,1000)),('variance',q),('volatility',root(q))]:close('E4/E15/E16 source '+key,base[key],want)
    close('E5 supplemental covariance conversion',F(1,2)*F(1,5)*F(3,10),F(3,100));close('E6 supplemental inverse correlation',F(3,500)/(F(1,5)*F(3,10)),F(1,10))
    for label,weights,c,var in [('E7/E8',[.6,.4],[[.04,.006],[.006,.09]],F(99,3125)),('E9',[.5,.5],[[.04,.06],[.06,.09]],F(1,16)),('E10',[.6,.4],[[.04,-.06],[-.06,.09]],0)]:
      r=m.portfolio_stats(weights,[0,0],c);close(label+' variance',r['variance'],var);close(label+' SD',r['volatility'],root(var))
    file9='16.09-two-asset-portfolios.md';file12='16.12-efficient-portfolio-concepts.md';file13='16.13-portfolio-constraints.md';file14='16.14-rebalancing-mathematics.md';file15='16.15-chapter-project-portfolio-risk-and-return-engine.md'
    gmv=call(file9,'minimum_variance_weight',(.2,.3,0),'E11/case B analytical GMV');close('E11 linked GMV weight',gmv['w1'],F(9,13))
    optimum=m.portfolio_stats([gmv['w1'],1-gmv['w1']],[.08,.04],[[.04,0],[0,.09]])
    close('E12/case B source GMV mean',optimum['mean'],F(22,325));close('case B GMV variance',optimum['variance'],F(9,325))
    for number,want in [(17,'.0436'),(18,'.06'),(19,'.00016')]:
      solution=re.search(r'### Exercise '+str(number)+r'.*?\*\*Worked solution:\*\* (.*?)(?=\n\n)',source_bytes.decode(),re.S).group(1)
      ck('F157 E'+str(number)+' variance derivative alignment',want in solution and '2' in solution,worked_solution=solution,independent_reference=want)
    for i,want in enumerate([F(109,10000),F(9,1000),F(1,62500)]):
      close('E20-E22 source VC '+str(i),base['variance_contributions'][i],want)
      problem=re.search(r'### Exercise '+str(20+i)+r'.*?\*\*Problem:\*\* (.*?)(?=\n\n)',source_bytes.decode(),re.S).group(1)
      ck('F157 E'+str(20+i)+' covariance-weighted label',('covariance-weighted' in problem or 'Σw' in problem),problem=problem)
    close('E23 source VC sum',math.fsum(base['variance_contributions']),q);close('E24 source RC A',base['volatility_contributions'][0],root(F(109,10000)**2/q))
    sharpe=call(file12,'sharpe_ratio',(.08,.2,.02),'E25 Sharpe');close('E25 linked source Sharpe',sharpe,F(3,10))
    reject('E26 linked zero-Sharpe undefined',lambda:call(file12,'sharpe_ratio',(.02,0,.02),'E26 undefined Sharpe rejection'))
    a=dict(expected_return=.08,variance=.02);b=dict(expected_return=.06,variance=.03)
    ck('E27 linked dominance',call(file12,'dominates',(a,b),'E27 dominance'))
    a=dict(expected_return=.08,variance=.04);b=dict(expected_return=.06,variance=.02)
    ck('E28 linked tradeoff',not call(file12,'dominates',(a,b),'E28 tradeoff'))
    target=call(file9,'target_return_weight',(.07,.08,.04),'E29/case B equality threshold');close('E29 linked target weight',target['w1'],F(3,4))
    target_stats=m.portfolio_stats([.75,.25],[.08,.04],[[.04,0],[0,.09]]);close('case B minimum target variance',target_stats['variance'],F(9,320))
    reject('E30 linked target infeasible',lambda:call(file9,'target_return_weight',(.1,.08,.04),'E30 infeasible target rejection'))
    grid=call(file12,'simplex_grid',(3,4),'E31 grid count');ck('E31 fifteen grid points',len(grid)==15)
    case_a=call(file13,'check_constraints',(w,[0]*3,[.45,1,1]),'case A equity position cap');ck('case A source cap breach',not case_a['feasible'])
    case_e=call(file13,'check_constraints',(w,[0]*3,[.6,.4,.3],{'sector':[0,1]},{'sector':(0,.7)}),'case E full proposal caps/sector');ck('case E budget/positions pass but sector fails',case_e['violations']==['group sector outside bounds'])
    close('E33 linked sector exposure',case_e['group_exposures']['sector'],F(4,5))
    for label,value,want in [('E32 position breach',F(1,2)-F(2,5),F(1,10)),('E34 sector breach',F(4,5)-F(7,10),F(1,10)),('case A five-point cap breach',F(1,2)-F(9,20),F(1,20)),('case E expected-return shortfall',F(3,50)-F(59,1000),F(1,1000))]:close(label,value,want)
    ck('E35 independent lower conflict',not call(file13,'necessary_budget_bounds',([.6,.6],[1,1]),'E35 lower conflict'));ck('E36 independent upper conflict',not call(file13,'necessary_budget_bounds',([0,0],[.4,.4]),'E36 upper conflict'))
    drift=m.drift([.5,.5],[.1,0]);close('E38 source drift return',drift['return'],F(1,20));close('E38 source drift A',drift['weights'][0],F(11,21));close('E39 source NAV105',100*(1+drift['return']),105)
    trade=m.rebalance([.4,.6],[.5,.5],100);close('E40 source buy',trade['trades'][0],10);close('E41 source turnover',trade['one_way_turnover'],F(1,10));close('E42 source-derived gross',sum(abs(x) for x in trade['trades']),20);close('E43 supplemental cost',F(1,1000)*20,F(1,50))
    case_c=m.rebalance(drift['weights'],[.5,.5],105);close('case C frictionless sale',case_c['trades'][0],F(-5,2));close('case C frictionless buy',case_c['trades'][1],F(5,2));close('case C turnover',case_c['one_way_turnover'],F(1,42))
    ck('E44 linked threshold trigger',call(file14,'band_trigger',([.56,.44],[.5,.5],.05),'E44 absolute band'))
    ck('E45 linked no trigger',not call(file14,'band_trigger',([.52,.48],[.5,.5],.05),'E45 no band breach'))
    ck('case C linked no trade trigger',not call(file14,'band_trigger',(drift['weights'],[.5,.5],.05),'case C no policy trigger'))
    stress=call(file15,'stress',(w,mu,cov,2),'E46/case D source engine stress');direct=m.portfolio_stats(w,mu,[[4*x for x in row] for row in cov])
    close('E46/case D linked stress variance',stress['variance'],4*q);close('E46/case D linked stress SD',stress['volatility'],2*root(q));close('case D assessment direct route',direct['variance'],4*q)
    num('E47 source sample covariance',lambda:m.sample_covariance([1,2,3],[2,4,6]),2);close('E48 supplemental sample denominator',60-1,59)
    for label,fn,want in [
      ('F157 normalized tolerated budget mean',lambda:m.portfolio_stats([1.00000000005],[1],[[1]])['mean'],1),
      ('F157 integer expected return cancellation',lambda:m.portfolio_stats([.5,.5],[10**18+2,-10**18],[[0,0],[0,0]])['mean'],1),
      ('F157 integer sample centering',lambda:m.sample_covariance([10**18,10**18+1],[10**18,10**18+1]),F(1,2)),
      ('F157 huge constant sample mean',lambda:m.sample_covariance([1e308,1e308],[1e308,1e308]),0),
      ('F157 finite covariance after division',lambda:m.sample_covariance([-1e154,0,1e154],[-1e154,0,1e154]),1e308),
      ('F157 tiny return retained',lambda:m.drift([1],[1e-308])['return'],F(1,10**308)),
      ('F157 large NAV turnover stable',lambda:m.rebalance([.4,.6],[.5,.5],1e308)['one_way_turnover'],F(1,10)),
    ]:num(label,fn,want)
    for label,fn in [
      ('PSD extension invalid joint covariance rejected',lambda:m.portfolio_stats([1,0],[0,0],[[1,2],[2,1]])),
      ('F157 budget outside absolute tolerance rejected',lambda:m.portfolio_stats([1.0000000005],[0],[[0]])),
      ('F157 nonzero variance underflow rejected',lambda:m.portfolio_stats([.1,.9],[0,0],[[1e-323,0],[0,0]])),
      ('F157 malformed stats ValueError',lambda:m.portfolio_stats(None,None,None)),
      ('F157 huge integer data ValueError',lambda:m.sample_covariance([10**1000,0],[1,0])),
      ('F157 sample covariance underflow ValueError',lambda:m.sample_covariance([0,1e-200],[0,1e-200])),
      ('F157 positive wealth cannot report false total loss',lambda:m.drift([1,1e-308],[-1,0])),
      ('exhausted NAV rejected',lambda:m.drift([.5,.5],[-1,-1])),
    ]:reject(label,fn)
    project=dict(base=base,case_A_caps=case_a,case_B_gmv=optimum,case_B_target=target_stats,case_C_drift=drift,case_C_trades=case_c,case_D_stress=stress,case_E_constraints=case_e,linked_modules=[v[1] for v in linked_modules.values()],linked_source_calls=linked_calls,
      assets=['fictional A','fictional B','cash-like C'],units='decimal simple-return forecasts, squared covariance, fictional USD NAV',dates=None,scope='synthetic cases and current-source linked API calls only; no external acceptance or actual integration',fixture_sha256=hashlib.sha256(json.dumps([w,mu,cov]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=0,chapter_wide_answer_records=50,applied_case_records=5,rubric_area_records=7,lab_step_records=12,historical_unique_methods_added=0,project_report=project)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
