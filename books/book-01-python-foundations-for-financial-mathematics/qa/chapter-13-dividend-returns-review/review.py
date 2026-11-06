"""Section 13.7 exact dividend returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.07-dividends-and-total-return.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1307-') as tmp:
        Path(tmp,'dividends_total_return.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['dividends_total_return.py']),('isolated import',['-c','import dividends_total_return']),('exact compilation',['-m','compileall','-q','dividends_total_return.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['dividends_total_return.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_dividends');exec(compile(code,str(source),'exec'),m.__dict__)
    import csv
    def num(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    withheld=3*(1-F('.15'))
    ck('E8 E10 supplemental withholding and dividend cash',withheld==F('2.55') and 10*2==20)
    for label,fn,want in [
        ('E1 price gain',lambda:m.price_return(100,105),F('.05')),
        ('E2 dividend contribution',lambda:m.cash_dividend_yield(100,3),F('.03')),
        ('E3 total gain',lambda:m.holding_period_total_return(100,105,3),F('.08')),
        ('E4 fee deducted once',lambda:m.holding_period_total_return(100,105,3,1),F('.07')),
        ('E5 ex-dividend price drop offset',lambda:m.holding_period_total_return(100,98,2),0),
        ('E6 dividend yield',lambda:m.cash_dividend_yield(200,4),F('.02')),
        ('E7 positive total despite lower price',lambda:m.holding_period_total_return(100,95,7),F('.02')),
        ('E9 net-of-withholding return',lambda:m.holding_period_total_return(100,105,float(withheld)),F('.0755')),
        ('E11 new shares',lambda:m.reinvested_shares(10,2,50)-10,F('.4')),
        ('E12 final market value',lambda:m.reinvested_shares(10,2,50)*55,572),
        ('E13 reinvested return',lambda:m.reinvested_total_return(10,50,10.4,55),F('.144')),
        ('E14 cash-held return',lambda:m.holding_period_total_return(500,550,20),F('.14')),
        ('E15 split neutral',lambda:m.split_adjusted_price_return(100,50,2),0),
        ('E16 split gain',lambda:m.split_adjusted_price_return(100,55,2),F('.10')),
        ('E17 linked return',lambda:m.link_total_returns([.08,-.02]),F('.0584')),
        ('F101 tiny dividend change survives gross rounding',lambda:m.holding_period_total_return(1,1,1e-30),F('1e-30')),
        ('F95 tiny linked gain',lambda:m.link_total_returns([1e-30]),F('1e-30')),
        ('F54 finite reinvested return despite overflowed notionals',lambda:m.reinvested_total_return(1e308,1e308,1e308,1.1e308),F('.1')),
        ('F54 finite split adjustment despite intermediate overflow',lambda:m.split_adjusted_price_return(1e308,1e308,2),1),
        ('F54 finite shares despite intermediate dividend ratio overflow',lambda:m.reinvested_shares(1e-308,1e308,1e-308),F('1e308')),
    ]:num(label,fn,want)
    initial=F(20)*50;distribution=F(20)*2;increment=distribution/48
    shares=m.reinvested_shares(20,2,48)
    num('project fractional new shares',lambda:shares-20,increment)
    num('project ending shares',lambda:shares,20+increment)
    num('project final market value',lambda:shares*54,1125)
    num('project reinvested total',lambda:m.reinvested_total_return(20,50,shares,54),F('.125'))
    num('project alternative cash-held total',lambda:m.holding_period_total_return(float(initial),20*54,float(distribution)),F('.12'))
    ck('project purchase consumes dividend exactly once',increment*48==distribution and 20*54+distribution==1120)
    ledger=[('initial purchase',20,-1000,0,50,1000),('dividend received',20,40,40,48,960),
            ('reinvestment',shares,-40,0,48,shares*48),('final valuation',shares,0,0,54,shares*54)]
    with (HERE/'project-ledger.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(['event','shares','cash_movement','cash_balance','price','share_market_value'])
        writer.writerows(ledger)
    ck('exact demo outputs',commands[0]['stdout'].splitlines()==['Price return: 5.00%','Total return: 8.00%','Net return: 7.00%'])
    for label,fn in [
        ('negative ending net wealth rejected',lambda:m.holding_period_total_return(100,0,0,1)),
        ('F54 nonrepresentable dividend yield rejected',lambda:m.cash_dividend_yield(1e-308,1e308)),
        ('F54 nonrepresentable linked return rejected',lambda:m.link_total_returns([1e308,1e308])),
        ('F54 share result overflow rejected',lambda:m.reinvested_shares(1e308,1e308,1e-308)),
        ('F101 distinguish near-total loss from zero wealth',lambda:m.price_return(1e308,1e-308)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
