"""Section 13.1 exact investment returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.01-measuring-investment-returns.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1301-') as tmp:
        Path(tmp,'measuring_investment_returns.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['measuring_investment_returns.py']),('isolated import',['-c','import measuring_investment_returns']),('exact compilation',['-m','compileall','-q','measuring_investment_returns.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['measuring_investment_returns.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_returns');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D
    def numeric(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    for label,fn,want in [
        ('E2 price gain',lambda:m.price_return(50,57),F(7,50)),
        ('E3 loss',lambda:m.price_return(200,170),-F(3,20)),
        ('E4 dividend',lambda:m.holding_period_return(100,105,3),F(8,100)),
        ('E5 fee',lambda:m.holding_period_return(100,105,3,1),F(7,100)),
        ('E6 gross',lambda:m.gross_return(.12),F('1.12')),
        ('E7 positive gross on negative return',lambda:m.gross_return(-.3),F('.7')),
        ('E8 cumulative return',lambda:m.compound_returns([.1,-.1]),-F('.01')),
        ('E9 recovery',lambda:m.compound_returns([-.2,.25]),F(0)),
        ('E10 annualized 21%',lambda:m.annualize(.21,2),F('.1')),
        ('E11 annualized 44%',lambda:m.annualize(.44,2),F('.2')),
        ('E12 real return',lambda:m.real_return(.08,.03),F(5,103)),
        ('E13 total return',lambda:m.holding_period_return(100,104,2),F('.06')),
        ('E17 log transform',lambda:m.log_return(.1),D('1.1').ln()),
        ('E18 log inverse',lambda:m.return_from_log(float(D('1.08').ln())),F('.08')),
        ('portfolio fixed weights',lambda:m.weighted_portfolio_return([.6,.4],[.1,-.05]),F('.04')),
        ('total loss',lambda:m.compound_returns([.1,-1,.2]),-1),
        ('F95 tiny linked gain survives gross rounding',lambda:m.compound_returns([1e-30]),F('1e-30')),
        ('F95 tiny real return survives ratio rounding',lambda:m.real_return(1e-30,0),F('1e-30')),
        ('F54 finite linked product despite intermediate overflow',lambda:m.compound_returns([1e170,1e170]+[-.999999]*30),(1+F('1e170'))**2*F('1e-6')**30-1),
        ('F54 scaled HPR despite intermediate overflow',lambda:m.holding_period_return(1e307,1e308,1e308,1e308),9),
    ]:numeric(label,fn,want)
    rows=[(1000,1040,10,2),(1048,1005,12,3),(1014,1090,0,4)]
    totals=[];gross=F(1)
    for k,(a,b,i,c) in enumerate(rows,1):
        r=F(b+i-c-a,a);totals.append(m.holding_period_return(a,b,i,c));gross*=1+r
        numeric(f'project {k} pre-flow return',lambda:m.price_return(a,b),F(b-a,a))
        numeric(f'project {k} total return',lambda:totals[-1],r)
        numeric(f'project {k} gross',lambda:m.gross_return(totals[-1]),1+r)
        if k<len(rows):ck(f'project {k} net ending equals next beginning',b+i-c==rows[k][0])
    numeric('project linked return equals terminal wealth ratio',lambda:m.compound_returns(totals),gross-1)
    ck('F95 project describes carried cash and the wealth identity','includes cash retained from prior periods' in source.read_text() and '8.60%' in source.read_text())
    for label,fn in [
        ('F95 negative closing wealth outside unlevered model',lambda:m.holding_period_return(100,0,0,1)),
        ('F95 long-only asset return below total loss',lambda:m.weighted_portfolio_return([1],[-1.1])),
        ('F54 compound overflow rejected',lambda:m.compound_returns([1e308,1e308])),
        ('F54 log inverse overflow rejected',lambda:m.return_from_log(1000)),
        ('F54 annualized saturation rejected',lambda:m.annualize(-.99,.001)),
        ('F54 input outside finite float range',lambda:m.price_return(10**500,1)),
    ]:reject(label,fn)
    expected=['Price return: 5.00%','Total return with dividend and costs: 7.00%',
              'Two-period compounded return: -1.00%','Annualized two-year 21%: 10.00%','Inflation-adjusted 8%: 4.8544%']
    ck('exact demo outputs',commands[0]['stdout'].splitlines()==expected,expected=expected)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[14,15,16],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
