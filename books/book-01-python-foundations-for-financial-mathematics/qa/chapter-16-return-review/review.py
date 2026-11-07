"""Section 16.3 exact portfolio return lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.03-portfolio-return.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1603-') as tmp:
        Path(tmp,'portfolio_return.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['portfolio_return.py']),('isolated import',['-c','import portfolio_return']),('exact compilation',['-m','compileall','-q','portfolio_return.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['portfolio_return.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('portfolio_return_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 weighted return',lambda:m.period_return([.6,.4],[.1,-.05]),F(1,25)),
        ('E2 contribution A',lambda:m.contribution([.6,.4],[.1,-.05])[0],F(3,50)),
        ('E2 contribution B',lambda:m.contribution([.6,.4],[.1,-.05])[1],F(-1,50)),
        ('E3 equal weight',lambda:m.period_return([.5,.5],[.1,-.1]),0),
        ('E4 zero allocation',lambda:m.period_return([1,0],[0,.5]),0),
        ('E5 signed return',lambda:m.period_return([1.2,-.2],[.1,.05],True),F(11,100)),
        ('E8 no-flow NAV return',lambda:m.value_return(100,104),F(1,25)),
        ('E11 drift A',lambda:m.buy_and_hold([.5,.5],[[.1,0]])['ending_weights'][0],F(11,21)),
        ('E12 partial bankruptcy',lambda:m.period_return([.5,.5],[-1,0]),F(-1,2)),
        ('E13 linked return',lambda:m.constant_mix([1],[[.1],[-.1]])['cumulative_return'],F(-1,100)),
        ('F144 integer NAV increment',lambda:m.value_return(10**18,10**18+1),F(1,10**18)),
        ('F144 cancellation before net return',lambda:m.period_return([1e308,-1e308,1],[2,2,.1],True),F(1,10)),
        ('F144 accepted-budget no-return buy hold',lambda:m.buy_and_hold([.5,.50000000005],[[0,0]])['cumulative_return'],0),
        ('F144 tiny buy hold gain',lambda:m.buy_and_hold([1],[[1e-18]])['cumulative_return'],F(1,10**18)),
        ('F144 tiny constant mix gain',lambda:m.constant_mix([1],[[1e-18]])['cumulative_return'],F(1,10**18)),
        ('F144 oversized interim BH then bankruptcy',lambda:m.buy_and_hold([1],[[1e308],[1e308],[-1]])['cumulative_return'],-1),
        ('F144 oversized interim mix then bankruptcy',lambda:m.constant_mix([1],[[1e308],[1e308],[-1]])['cumulative_return'],-1),
    ]:num(label,fn,want)
    w=[.5,.5];rows=[[.2,0],[0,.2]];bh=m.buy_and_hold(w,rows);cm=m.constant_mix(w,rows)
    for i,want in enumerate([F(1,10),F(1,11)]):close('lab buy-hold period '+str(i),bh['period_returns'][i],want,atol=0)
    for i in range(2):close('lab constant-mix period '+str(i),cm['period_returns'][i],F(1,10),atol=0)
    close('E16 buy hold cumulative',bh['cumulative_return'],F(1,5),atol=0)
    close('E17 constant mix cumulative',cm['cumulative_return'],F(21,100),atol=0)
    for i in range(2):close('lab ending buy-hold allocation '+str(i),bh['ending_weights'][i],F(1,2),atol=0)
    close('E18 path-specific premium',cm['cumulative_return']-bh['cumulative_return'],F(1,100),atol=0)
    # Supplemental fee account: after period 1 values .6/.5, equal-weight trades .05 each.
    fee_cases=[]
    for rate in [F(0),F(1,1000),F(1,10)]:
        traded=F(1,10);fee=rate*traded;post_rebalance=F(11,10)-fee;terminal=post_rebalance*F(11,10)
        num('lab supplemental funded-fee terminal rate '+str(rate),lambda terminal=terminal:m.value_return(1,float(terminal)),terminal-1)
        fee_cases.append(dict(rate=str(rate),gross_traded=str(traded),fee=str(fee),post_rebalance_wealth=str(post_rebalance),terminal_wealth=str(terminal),net_return=str(terminal-1)))
    cash_weights=[.45,.45,.1];cash_rows=[[.2,0,0],[0,.2,0]];cash_bh=m.buy_and_hold(cash_weights,cash_rows);cash_cm=m.constant_mix(cash_weights,cash_rows)
    close('lab separate cash buy hold',cash_bh['cumulative_return'],F(9,50),atol=0)
    close('lab separate cash constant mix',cash_cm['cumulative_return'],F(1881,10000),atol=0)
    final_loss=m.buy_and_hold([1],[[-1]])
    ck('terminal bankruptcy has no ending weights',final_loss['cumulative_return']==-1 and final_loss['ending_weights'] is None)
    for label,fn in [
        ('incomplete weights rejected',lambda:m.period_return([.6,.3],[.1,.1])),
        ('unequal return length rejected',lambda:m.period_return([1,0],[.1])),
        ('E9/E22 nonzero external flow rejected',lambda:m.value_return(100,120,10)),
        ('nonfinite NAV rejected',lambda:m.value_return(100,math.inf)),
        ('below asset total loss rejected',lambda:m.period_return([1],[-1.01])),
        ('missing return rejected',lambda:m.period_return([1],[None])),
        ('F144 inconsistent contribution return domain rejected',lambda:m.contribution([1],[-1.01])),
        ('F144 nonboolean short policy rejected',lambda:m.period_return([1],[.1],allow_short='yes')),
        ('buy hold after depletion rejected',lambda:m.buy_and_hold([1],[[-1],[.1]])),
        ('F144 implicit bankrupt-asset refill rejected',lambda:m.constant_mix([.5,.5],[[-1,0],[.1,0]])),
        ('F144 constant mix after depletion rejected',lambda:m.constant_mix([1],[[-1],[.1]])),
        ('F144 BH false total loss rejected',lambda:m.buy_and_hold([1],[[-.99]]*10)),
        ('F144 mix false total loss rejected',lambda:m.constant_mix([1],[[-.99]]*10)),
        ('F144 unreportable NAV return rejected',lambda:m.value_return(1e-308,1e308)),
        ('F144 false NAV total loss rejected',lambda:m.value_return(1e308,1e-308)),
        ('F144 unreportable contribution rejected',lambda:m.contribution([1e308,-1e308,1],[2,2,.1])),
    ]:reject(label,fn)
    ck('source inputs preserved',w==[.5,.5] and rows==[[.2,0],[0,.2]])
    project=dict(start_weights=w,return_rows=rows,frequency='hypothetical common period',dates=None,units='decimal total returns; unit initial wealth',external_flows=0,asset_distributions='already included in supplied total returns',
        fixture_sha256=hashlib.sha256(json.dumps([w,rows]).encode()).hexdigest(),buy_and_hold=bh,constant_mix=cm,first_period_values=['3/5','1/2'],between_period_no_cost_trades=['-1/20','1/20'],
        fee_cases=fee_cases,fee_scope='supplemental exact account, fees funded between periods; source path engines remain cost-free',cash_weights=cash_weights,cash_return_rows=cash_rows,cash_buy_and_hold=cash_bh,cash_constant_mix=cash_cm,
        timing='period 1 close available before hypothetical between-period rebalance; period 2 begins after rebalance; real availability/fills/costs not provided')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,lab_step_records=12,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
