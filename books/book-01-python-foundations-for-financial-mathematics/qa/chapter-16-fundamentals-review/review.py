"""Section 16.1 exact portfolio fundamentals lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.01-portfolio-fundamentals.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1601-') as tmp:
        Path(tmp,'portfolio_fundamentals.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['portfolio_fundamentals.py']),('isolated import',['-c','import portfolio_fundamentals']),('exact compilation',['-m','compileall','-q','portfolio_fundamentals.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['portfolio_fundamentals.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('portfolio_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E2 market value',lambda:m.portfolio_value([2,3],[100,50]),350),
        ('E8 weighted return',lambda:m.portfolio_return([.6,.4],[.1,-.05]),F(1,25)),
        ('E12 signed return',lambda:m.portfolio_return([1.2,-.2],[.1,.05],False),F(11,100)),
        ('E14 drift A',lambda:m.post_return_weights([.5,.5],[.1,0])[0],F(11,21)),
        ('E14 drift B',lambda:m.post_return_weights([.5,.5],[.1,0])[1],F(10,21)),
        ('E16 expected return',lambda:m.portfolio_return([.6,.4],[.08,.04]),F(8,125)),
        ('F142 mixed tuple/list contract',lambda:m.portfolio_value((2,3),[100,50]),350),
        ('F142 cancellation before reporting value',lambda:m.portfolio_value([2,-1],[1e308,1e308]),1e308),
        ('F142 large values normalize A',lambda:m.weights_from_values([1e308,1e308])[0],F(1,2)),
        ('F142 product cancellation return',lambda:m.portfolio_return([1e308,-1e308,1],[2,2,.1],False),F(1,10)),
        ('F142 unreportable grown values normalize',lambda:m.post_return_weights([1.00000000005,0],[1.7976931348623157e308,0])[0],1),
    ]:num(label,fn,want)
    ck('E3 values-to-weights',m.weights_from_values([600,400])==[.6,.4])
    ck('E4 full investment',m.checked_weights([.6,.4])==[.6,.4])
    ck('E6 explicit cash slot',m.checked_weights([.6,.3,.1])==[.6,.3,.1])
    ck('E7 equal weights',m.checked_weights([.5,.5])==[.5,.5])
    ck('E11 long-only',m.checked_weights([.7,.3])==[.7,.3])
    ck('E12/E13 signed net/gross arithmetic',sum(map(F,('1.2','-.2')))==1 and sum(abs(F(v)) for v in ['1.2','-.2'])==F(7,5))
    q0=[6,8];p0=[100,50];r=[.1,-.05];p1=[110,47.5]
    initial=m.portfolio_value(q0,p0);w=m.weights_from_values([600,400]);rp=m.portfolio_return(w,r);end=m.portfolio_value(q0,p1);drift=m.post_return_weights(w,r)
    for label,value,want in [('lab initial value',initial,1000),('lab end value',end,1040),('lab realized return',rp,F(1,25)),('lab end/initial reconciliation',end/initial-1,F(1,25)),('lab drift A',drift[0],F(33,52)),('lab drift B',drift[1],F(19,52))]:close(label,value,want)
    # No-cost target notional 624/416 versus current 660/380: sell/buy 36.
    q_free=[F(624,110),F(416)/F('47.5')]
    num('lab no-cost rebalanced value',lambda:m.portfolio_value(list(map(float,q_free)),p1),1040)
    # Fund .1% transaction cost from the portfolio itself: V'=1040-.001*(280-.2*V').
    rate=F(1,1000);post_cost=(F(1040)-rate*280)/(1-rate*F(1,5));cost=1040-post_cost
    target_values=[F(3,5)*post_cost,F(2,5)*post_cost];q_cost=[target_values[0]/110,target_values[1]/F('47.5')]
    num('lab funded cost rebalanced value',lambda:m.portfolio_value(list(map(float,q_cost)),p1),post_cost)
    ck('lab self-financing cost budget',cost==rate*(abs(target_values[0]-660)+abs(target_values[1]-380)))
    for label,fn in [
        ('E5 sum less than one rejected',lambda:m.checked_weights([.6,.3])),
        ('negative long-only rejected',lambda:m.checked_weights([1.2,-.2])),
        ('return lengths rejected',lambda:m.portfolio_return([.6,.4],[.1])),
        ('missing return rejected',lambda:m.portfolio_return([.6,.4],[.1,None])),
        ('nonfinite return rejected',lambda:m.portfolio_return([.6,.4],[.1,math.inf])),
        ('boolean quantity rejected',lambda:m.portfolio_value([True],[100])),
        ('zero price rejected',lambda:m.portfolio_value([1],[0])),
        ('negative value allocation rejected',lambda:m.weights_from_values([1,-1])),
        ('zero total values rejected',lambda:m.weights_from_values([0,0])),
        ('bankruptcy drift rejected',lambda:m.post_return_weights([.5,.5],[-1,0])),
        ('F142 infinite tolerance rejected',lambda:m.checked_weights([.6,.3],tol=math.inf)),
        ('F142 NaN tolerance rejected',lambda:m.checked_weights([.6,.4],tol=math.nan)),
        ('F142 negative tolerance rejected',lambda:m.checked_weights([.6,.4],tol=-1)),
        ('F142 nonboolean policy rejected',lambda:m.checked_weights([.6,.4],long_only='yes')),
        ('F142 unreportable value rejected',lambda:m.portfolio_value([2],[1e308])),
        ('F142 vanished positive allocation rejected',lambda:m.weights_from_values([1e-308,1e308])),
    ]:reject(label,fn)
    ck('lab source fixtures unchanged',q0==[6,8] and p0==[100,50] and r==[.1,-.05])
    project=dict(quantities=q0,initial_prices=p0,initial_values=[600,400],initial_wealth=initial,initial_weights=w,asset_returns=r,expected_returns=[.08,.04],expected_portfolio_return=m.portfolio_return(w,[.08,.04]),
        end_prices=p1,end_values=[660,380],end_wealth=end,realized_return=rp,drifted_weights=drift,target_weights=[.6,.4],no_cost_trade_values=[-36,36],no_cost_target_quantities=list(map(str,q_free)),
        hypothetical_cost_rate=str(rate),cost_funding_equation="V'=1040-.001*(280-.2*V')",funded_cost=str(cost),post_cost_wealth=str(post_cost),post_cost_target_quantities=list(map(str,q_cost)),
        units='fictional USD prices/wealth; decimal one-period total returns; fractional shares',valuation_times=['synthetic start','synthetic end'],dates=None,external_flows=0,fx='single currency',
        fixture_sha256=hashlib.sha256(json.dumps([q0,p0,r]).encode()).hexdigest(),execution_scope='supplemental rebalance design/source valuation calls; no actual trades, taxes, spread, lots or margin model')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,lab_step_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
