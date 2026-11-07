"""Rebalancing lab and independent Decimal fee/cash-accounting benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.14-rebalancing-mathematics.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.14-rebalancing-mathematics.md'])
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
    with tempfile.TemporaryDirectory(prefix='book1-1614-') as tmp:
        Path(tmp,'rebalancing_mathematics.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['rebalancing_mathematics.py']),('isolated import',['-c','import rebalancing_mathematics']),('exact compilation',['-m','compileall','-q','rebalancing_mathematics.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['rebalancing_mathematics.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    start=[.5,.5];returns=[.1,0];target=[.5,.5];drift=m.drift(start,returns)
    close('E1 source period return',drift['portfolio_return'],F(1,20));close('E2 source drift A',drift['ending_weights'][0],F(11,21));close('E3 source drift B',drift['ending_weights'][1],F(10,21));close('E4 source ending NAV scaled',100*drift['ending_nav_per_unit'],105)
    for r in [[0,0],[.1,.1]]:ck('E5/E6 equal-return no drift '+str(r),m.drift([.4,.6],r)['ending_weights']==[.4,.6])
    plan=m.trade_plan([.4,.6],target,100)
    for label,value,want in [('E7 buy',plan['buys'],10),('E8 sell',plan['sells'],10),('E9 turnover',plan['one_way_turnover'],F(1,10)),('E10 gross traded',plan['buys']+plan['sells'],20)]:close(label,value,want)
    zero=m.net_after_proportional_cost([.4,.6],target,100,0)
    close('E11 exact zero fee',zero['cost'],0);close('E11 zero-fee NAV',zero['post_cost_nav'],100)
    close('E12 supplemental pre-cost notional fee',F(1,1000)*20,F(1,50));close('E13 supplemental pre-cost NAV approximation',100-F(1,50),F(4999,50))
    for label,fn,want in [
      ('E14 band breached',lambda:m.band_trigger([.4,.6],target,.05),True),
      ('E15 band not breached',lambda:m.band_trigger([.49,.51],target,.02),False),
      ('E16 absolute band breached',lambda:m.band_trigger([.56,.44],target,.05),True),
      ('F155 exact threshold equality does not trigger',lambda:m.band_trigger([.55,.45],target,.05),False),
    ]:
      try:v=fn()
      except Exception as e:ck(label,False,exception=repr(e))
      else:ck(label,v is want,actual=v,expected=want)
    close('E17 supplemental relative deviation',abs(F(24,100)-F(1,5))/F(1,5),F(1,5))
    # General oracle: Decimal bisection of normalized fee, distinct from source piecewise solution.
    def fee_oracle(a,b,c):
      with localcontext() as ctx:
        ctx.prec=80;a=[D(str(x)) for x in a];b=[D(str(x)) for x in b];c=D(str(c));a=[x/sum(a) for x in a];b=[x/sum(b) for x in b]
        if c==0 or a==b:return D(0)
        lo=D(0);hi=D(1)
        for _ in range(400):
          mid=(lo+hi)/2;residual=mid-c*sum(abs(b[i]*(1-mid)-a[i]) for i in range(len(a)))
          if residual>=0:hi=mid
          else:lo=mid
        return (lo+hi)/2
    fee_cases=[]
    for a,b,nav,c in [([.4,.6],[.5,.5],100,.001),([.8,.2],[.5,.5],100,.1),([.2,.3,.5],[.6,.2,.2],250,.001),([.2,.3,.5],[.6,.2,.2],250,.9)]:
      result=m.net_after_proportional_cost(a,b,nav,c);expected=fee_oracle(a,b,c)*D(str(nav))
      close('source fee vs Decimal bisection '+str((a,c)),result['cost'],expected)
      close('source NAV conservation '+str((a,c)),result['post_cost_nav']+result['cost'],nav)
      close('source fee/gross identity '+str((a,c)),result['cost'],F(str(c))*F(str(result['total_traded'])))
      ck('source trade cash conservation '+str((a,c)),abs(math.fsum(result['trade_dollars'])+result['cost'])<=float(F(1,10**12)*F(str(nav))),signed_trade_sum=math.fsum(result['trade_dollars']),fee=result['cost'],absolute_tolerance=nav*1e-12)
      fee_cases.append(result)
    pre=m.trade_plan(drift['ending_weights'],target,105);cost=m.net_after_proportional_cost(drift['ending_weights'],target,105,.001)
    close('lab frictionless sale A',pre['trade_dollars'][0],F(-5,2));close('lab frictionless purchase B',pre['trade_dollars'][1],F(5,2));close('lab one-way turnover',pre['one_way_turnover'],F(1,42));close('lab gross notional',pre['buys']+pre['sells'],5)
    close('lab exact fee',cost['cost'],F(1,200));close('lab post-cost NAV',cost['post_cost_nav'],F(20999,200));close('lab fee-funded sale',cost['trade_dollars'][0],F(-1001,400));close('lab fee-funded purchase',cost['trade_dollars'][1],F(999,400))
    holdings=[F(55),F(50)];reconstructed=[float(holdings[i])+cost['trade_dollars'][i] for i in range(2)]
    for i,value in enumerate(reconstructed):close('lab reconstructed ending holding '+str(i),value,F(20999,400))
    ck('lab five-point band no trigger',not m.band_trigger(drift['ending_weights'],target,.05))
    for label,fn,want in [
      ('F155 tiny return retained',lambda:m.drift([1],[1e-308])['portfolio_return'],F(1,10**308)),
      ('F155 tolerated weight budget normalized',lambda:m.drift([1.00000000005],[0])['portfolio_return'],0),
      ('F155 no-trade fee exactly zero',lambda:m.net_after_proportional_cost([.4,.6],[.4,.6],100,.001)['cost'],0),
      ('F155 tiny positive fee retained',lambda:m.net_after_proportional_cost([.4,.6],target,100,1e-100)['cost'],F(2,10**99)),
      ('F155 scale-free large NAV fee',lambda:m.net_after_proportional_cost([.4,.6],target,1e308,.001)['cost'],F(2,10**4)*10**308),
    ]:num(label,fn,want)
    for label,fn in [
      ('F155 positive NAV cannot report false total loss',lambda:m.drift([1,1e-308],[-1,0])),
      ('F155 unreportable required return ValueError',lambda:m.trade_plan([1,0],[0,1],10**1000)),
      ('F155 unreportable gross output ValueError',lambda:m.net_after_proportional_cost([1,0],[0,1],1e308,0)),
      ('F155 huge integer input ValueError',lambda:m.drift([1],[10**1000])),
      ('exhausted NAV rejected',lambda:m.drift([.5,.5],[-1,-1])),
      ('invalid simple return rejected',lambda:m.drift([1],[-1.1])),
      ('invalid cost rate rejected',lambda:m.net_after_proportional_cost([.5,.5],target,100,1)),
      ('negative band rejected',lambda:m.band_trigger([.5,.5],target,-.1)),
      ('negative NAV rejected',lambda:m.trade_plan([.5,.5],target,-1)),
    ]:reject(label,fn)
    ck('lab input fixtures preserved',start==[.5,.5] and target==[.5,.5] and returns==[.1,0])
    report=dict(assets=['fictional A','fictional B'],initial_nav=100,initial_weights=start,returns=returns,drift=drift,pretrade_holdings=[55,50],pretrade_nav=105,frictionless_plan=pre,cost_rate=.001,cost_plan=cost,reconstructed_post_cost_holdings=reconstructed,general_fee_cases=fee_cases,
      units='common fictional USD dollar NAV, decimal simple returns/weights',timing='synthetic t0 holdings, t1 total returns, t1-close rebalance at fixed values',dates=None,external_flows='none',scope='static continuous-dollar plan, not actual orders, fills, tax, settlement or out-of-sample strategy',fixture_sha256=hashlib.sha256(json.dumps([100,start,returns,target,.001]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
