"""Section10.2 exact calendar timeline lab and independent day-count review."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.02-cash-flow-timelines.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value,independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-102-') as tmp:
        Path(tmp,'cash_flow_timelines.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['cash_flow_timelines.py']),('exact compilation',['-m','compileall','-q','cash_flow_timelines.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==10 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='' if args==['cash_flow_timelines.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_cashflow102');sys.modules[m.__name__]=m
    try:exec(compile(code,str(source),'exec'),m.__dict__)
    finally:sys.modules.pop(m.__name__,None)
    from datetime import date,datetime
    from decimal import Decimal as D,localcontext
    c=m.CashFlow;origin=date(2026,1,1);one=date(2027,1,1)
    borrower=[c(origin,10000,'draw'),c(one,-11000,'repay')]
    ck('P1 borrower perspective',m.schedule(borrower,origin)==[(0,10000,'draw'),(1,-11000,'repay')])
    close('P2 timezero payment',m.npv([c(origin,-250)],origin,.08),F(-250))
    close('P3 ACT365F',m.year_fraction(origin,one),F(1))
    close('P4 ACT360',m.year_fraction(origin,one,'ACT/360'),F(73,72))
    close('P5 leapyear',m.year_fraction(date(2024,1,1),date(2025,1,1)),F(366,365))
    close('P6 same-day total',m.npv([c(origin,100,'a'),c(origin,150,'b')],origin,.1),F(250))
    close('P7 annual discount',m.npv([c(one,110)],origin,.1),F(100))
    flows=[c(origin,-100),c(one,110)]
    close('P8 zero NPV',m.npv(flows,origin,.1),F(0))
    close('P9 reordered NPV',m.npv(flows[::-1],origin,.1),F(0))
    from itertools import permutations
    nonzero=[c(origin,-100),c(one,40),c(date(2028,1,1),80)]
    vals=[m.npv(order,origin,.1) for order in permutations(nonzero)]
    ck('P9 nonzero stream all six permutations',all(math.isclose(x,float(F(300,121)),abs_tol=1e-10,rel_tol=1e-12) for x in vals),actual_values=vals,independent_reference=str(F(300,121)))
    a=[c(origin,1,'first'),c(origin,2,'second')]
    ck('P10 preserve rows stablelabels',m.schedule(a,origin)==[(0,1,'first'),(0,2,'second')])
    close('zero rate generator',m.npv(iter(flows),origin,0),F(10))
    close('empty schedule valid',m.npv([],origin,.05),F(0))
    with localcontext() as ctx:
        ctx.prec=100
        year= D(366)/365
        leap_pv=D(110)*(-year*D('1.10').ln()).exp()
        act360_pv=D(110)*(-(D(365)/360)*D('1.10').ln()).exp()
    close('leapyear actual valuation',m.npv([c(date(2025,1,1),110)],date(2024,1,1),.1),leap_pv)
    close('ACT360 actual valuation',m.npv([c(one,110)],origin,.1,'ACT/360'),act360_pv)
    close('negative rate',m.npv([c(one,90)],origin,-.1),F(100))
    for label,fn in [('past event',lambda:m.year_fraction(origin,date(2025,1,1))),('bool cash',lambda:c(origin,True)),('invalid rate',lambda:m.npv([],origin,-1)),('unsupported basis with event',lambda:m.npv([c(one,110)],origin,.1,'30/360')),('discount factor underflow',lambda:m.npv([c(date(2099,1,1),100)],origin,1e308)),('nonzero PV underflow',lambda:m.npv([c(one,5e-324)],origin,1)),('empty bad basis',lambda:m.npv([],origin,.05,'30/360')),('empty bad origin',lambda:m.npv([],'2026-01-01',.05)),('intraday CashFlow',lambda:c(datetime(2026,1,1,12),100)),('intraday daycount',lambda:m.year_fraction(datetime(2026,1,1),datetime(2026,1,1,12)))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=10,conceptual_only_prompts=[10],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
