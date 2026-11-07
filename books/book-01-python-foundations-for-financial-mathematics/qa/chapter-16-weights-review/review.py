"""Section 16.2 exact portfolio weights lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.02-portfolio-weights.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1602-') as tmp:
        Path(tmp,'portfolio_weights.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['portfolio_weights.py']),('isolated import',['-c','import portfolio_weights']),('exact compilation',['-m','compileall','-q','portfolio_weights.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['portfolio_weights.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('weights_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    values=m.market_values([2,3],[100,50]);weights=m.weights_from_values(values)
    close('E2 share weight A',weights[0],F(4,7),atol=0);close('E2 share weight B',weights[1],F(3,7),atol=0)
    exp=m.exposures([1.2,-.2])
    for k,v in [('net',1),('gross',F(7,5)),('long',F(6,5)),('short',F(-1,5))]:close('E6-E8 '+k,exp[k],v,atol=0)
    for label,fn,want in [
        ('E9 HHI equal',lambda:m.concentration_hhi([.5,.5]),F(1,2)),
        ('E10 HHI concentrated',lambda:m.concentration_hhi([1,0]),1),
        ('E11 effective holdings',lambda:1/m.concentration_hhi([.25]*4),4),
        ('E12 drift A',lambda:m.drifted_weights([.5,.5],[.1,0])[0],F(11,21)),
        ('E12 drift B',lambda:m.drifted_weights([.5,.5],[.1,0])[1],F(10,21)),
        ('E14 initial sell trade',lambda:m.target_trades([600,400],[.5,.5])[0],-100),
        ('E14 initial buy trade',lambda:m.target_trades([600,400],[.5,.5])[1],100),
        ('F143 large position normalization',lambda:m.weights_from_values([1e308,1e308])[0],F(1,2)),
        ('F143 integer net exposure',lambda:m.exposures([10**18+1,-10**18])['net'],1),
        ('F143 signed normalization cancellation',lambda:m.weights_from_values([1e308,1e308,-1e308,-1e308,1],False)[-1],1),
        ('F143 target trade despite oversized intermediate NAV',lambda:m.target_trades([1e308,1e308],[1,0])[0],1e308),
        ('F143 drift normalized oversized growth',lambda:m.drifted_weights([1.00000000005,0],[1.7976931348623157e308,0])[0],1),
    ]:num(label,fn,want)
    ck('E1 values to weights',m.weights_from_values([600,400])==[.6,.4])
    ck('E3 cash budget',m.validate_weights([.6,.3,.1])==[.6,.3,.1])
    ck('E5 long-only',m.validate_weights([.7,.3])==[.7,.3])
    ck('E17 tolerance',m.validate_weights([.6,.399999999999])==[.6,.399999999999])
    try:tolerance_trades=m.target_trades([5e15,5e15],[.5,.50000000005])
    except Exception as exc:ck('F143 accepted-target tolerance preserves dollar budget',False,exception=repr(exc))
    else:ck('F143 accepted-target tolerance preserves dollar budget',abs(math.fsum(tolerance_trades))<=1e-6,actual=tolerance_trades,total_trade=math.fsum(tolerance_trades),absolute_budget_tolerance=1e-6)
    start=[600,400];r=[.1,-.05];end=[660,380];w=m.weights_from_values(start);drift=m.drifted_weights(w,r)
    close('lab initial HHI',m.concentration_hhi(w),F(13,25),atol=0)
    close('lab drift A',drift[0],F(33,52),atol=0);close('lab drift B',drift[1],F(19,52),atol=0)
    initial_trades=m.target_trades(start,[.5,.5]);end_trades=m.target_trades(end,[.5,.5])
    ck('lab initial and post-return stages distinct',initial_trades==[-100,100] and end_trades==[-140,140])
    close('E15 initial turnover',sum(abs(v) for v in initial_trades)/(2*1000),F(1,10),atol=0)
    close('lab post-return turnover',sum(abs(v) for v in end_trades)/(2*1040),F(7,52),atol=0)
    close('E16 initial cost quote',sum(abs(v) for v in initial_trades)*.001,F(1,5),atol=0)
    cost=F(28,100);post_cost=1040-cost;funded_targets=[post_cost/2]*2;funded_trades=[funded_targets[i]-end[i] for i in range(2)]
    ck('lab funded post-return cost budget',sum(funded_trades)==-cost and sum(abs(v) for v in funded_trades)*F(1,1000)==cost)
    funded_shares=[funded_targets[0]/110,funded_targets[1]/F('47.5')]
    actual_funded_values=m.market_values(list(map(float,funded_shares)),[110,47.5])
    for i,v in enumerate(actual_funded_values):close('lab funded target market value '+str(i),v,funded_targets[i])
    ck('lab explicit minimum-cash target',m.validate_weights([.475,.475,.05])==[.475,.475,.05])
    cash_trades=m.target_trades([660,380,0],[.475,.475,.05])
    ck('lab no-cost cash-reserve trades',cash_trades==[-166,114,52])
    for label,fn in [
        ('E4 missing allocation rejected',lambda:m.validate_weights([.6,.3])),
        ('E18 nonpositive NAV rejected',lambda:m.weights_from_values([1,-2],False)),
        ('long-only short rejected',lambda:m.weights_from_values([120,-20])),
        ('signed HHI rejected',lambda:m.concentration_hhi([1.2,-.2])),
        ('invalid positive price rejected',lambda:m.market_values([1],[0])),
        ('quantity price mismatch rejected',lambda:m.market_values([1,2],[100])),
        ('missing quantity rejected',lambda:m.market_values([1,None],[100,50])),
        ('nonfinite value rejected',lambda:m.weights_from_values([math.inf,1])),
        ('bankruptcy drift rejected',lambda:m.drifted_weights([.5,.5],[-1,0])),
        ('F143 infinite tolerance rejected',lambda:m.validate_weights([.6,.3],tol=math.inf)),
        ('F143 NaN tolerance rejected',lambda:m.validate_weights([.6,.4],tol=math.nan)),
        ('F143 invalid normalization policy rejected',lambda:m.weights_from_values([600,400],long_only='yes')),
        ('F143 unreportable individual position rejected',lambda:m.market_values([2],[1e308])),
        ('F143 unreportable gross exposure rejected',lambda:m.exposures([1e308,-1e308,1])),
        ('F143 vanished positive allocation rejected',lambda:m.weights_from_values([1e-308,1e308])),
    ]:reject(label,fn)
    ck('lab input positions preserved',start==[600,400] and end==[660,380] and r==[.1,-.05])
    project=dict(initial_values=start,initial_weights=w,initial_hhi=m.concentration_hhi(w),asset_returns=r,supplemental_portfolio_return='.04',end_values=end,end_wealth=1040,end_weights=drift,target=[.5,.5],
        initial_pre_cost_trades=initial_trades,initial_turnover=.1,initial_hypothetical_cost='.20',post_return_pre_cost_trades=end_trades,post_return_turnover=str(F(7,52)),
        post_return_hypothetical_cost=str(cost),funded_wealth=str(post_cost),funded_targets=list(map(str,funded_targets)),funded_trades=list(map(str,funded_trades)),funded_target_shares=list(map(str,funded_shares)),
        minimum_cash_target=[.475,.475,.05],minimum_cash_no_cost_trades=cash_trades,
        fixture_sha256=hashlib.sha256(json.dumps([start,r,end]).encode()).hexdigest(),units='fictional USD values, decimal same-period returns; fractional-share design',valuation_times=['synthetic initial','synthetic after return'],dates=None,
        execution_scope='source pre-cost calculations and supplemental cost/cash designs only; no orders, financing, taxes or constrained optimizer')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,lab_step_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
