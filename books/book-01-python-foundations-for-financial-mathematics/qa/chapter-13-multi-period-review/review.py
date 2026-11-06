"""Section 13.5 exact multi-period returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.05-multi-period-returns.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1305-') as tmp:
        Path(tmp,'multi_period_returns.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['multi_period_returns.py']),('isolated import',['-c','import multi_period_returns']),('exact compilation',['-m','compileall','-q','multi_period_returns.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['multi_period_returns.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_multi');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    from decimal import Decimal as D, localcontext
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    def equiv(g,exp):
        with localcontext() as ctx:
            ctx.prec=65
            return (D(g.numerator)/D(g.denominator))**(D(exp.numerator)/D(exp.denominator))-1
    for label,rs,want in [
        ('E1 two gains',[.1,.1],'.21'),('E2 gain and loss',[.2,-.2],'-.04'),
        ('E3 two losses',[-.1,-.1],'-.19'),('E4 three periods',[.1,-.1,.1],'.089'),
        ('E5 four periods',[.1,-.1,.05,-.02],'.01871'),('E14 total loss',[.2,-1,.5],'-1')]:
        num(label,lambda:m.cumulative_return(rs),F(want))
    num('E6 demo wealth',lambda:m.wealth_path(10000,[.1,-.1,.05,-.02])[-1],F('10187.10'))
    seq=m.wealth_path(100,[.05,-.02,.04])
    ck('E7–E9 exact index path',all(math.isclose(x,float(y),rel_tol=1e-12) for x,y in zip(seq,map(F,('100','105','102.9','107.016')))))
    num('E10 endpoint return',lambda:m.endpoint_return(100,108.9),F('.089'))
    ck('E11 arithmetic sum differs',sum(map(F,('.10','-.10','.05','-.02')))==F('.03'))
    num('E12 geometric mean',lambda:m.geometric_mean([.1,-.1]),equiv(F('.99'),F(1,2)))
    num('E13 annualization',lambda:m.annualized_return([.1,.1],1),F('.1'))
    first=F(110,100)-1;second=F(144,160)-1
    ck('E15 E16 supplemental contribution boundary',first==F('.10') and 110+50==160 and second==F('-.1'))
    num('E17 exact linking of supplied flow-free subperiods',lambda:m.time_weighted([float(first),float(second)]),F('-.01'))
    ps=[100,103,99.91,104.9055,102.80739]
    rs=m.price_returns(ps)
    num('E18 price series telescopes',lambda:m.cumulative_return(rs),F(str(ps[-1]))/100-1)
    days=list(map(F,('.03','-.02','.04','-.01','.02'))); floats=list(map(float,days))
    wp=m.wealth_path(25000,floats);ix=m.wealth_path(100,floats)
    g=F(1)
    for k,r in enumerate(days,1):
        g*=1+r
        num(f'project day {k} cumulative factor',lambda:1+m.cumulative_return(floats[:k]),g)
        num(f'project day {k} wealth',lambda:wp[k],25000*g)
        num(f'project day {k} index',lambda:ix[k],100*g)
    ck('project supplied daily gross and arithmetic mean',list(map(float,[1+r for r in days]))==[1.03,.98,1.04,.99,1.02] and sum(days)/5==F('.012'))
    num('project geometric mean',lambda:m.geometric_mean(floats),equiv(g,F(1,5)))
    num('project 252-day annualization',lambda:m.annualized_return(floats,252),equiv(g,F(252,5)))
    num('project independent wealth reconciliation',lambda:wp[-1]/wp[0],g)
    ck('project stressed wealth remains zero',m.wealth_path(25000,[.03,-.02,-1,-.01,.02])[3:]==[0,0,0])
    num('F99 tiny linked return',lambda:m.cumulative_return([1e-30]),F('1e-30'))
    num('F99 tiny gain survives recovery in geometric mean',lambda:m.geometric_mean([-.2,1e-30,.25]),equiv(1+F('1e-30'),F(1,3)))
    num('F54 finite linked result despite intermediate overflow',lambda:m.cumulative_return([1e170,1e170]+[-.999999]*30),(1+F('1e170'))**2*F('1e-6')**30-1)
    for label,fn in [
        ('F54 overflowed wealth rejected',lambda:m.wealth_path(1e308,[1])),
        ('F54 positive wealth underflow rejected',lambda:m.wealth_path(5e-324,[-.5])),
        ('F54 unrepresentable endpoint return rejected',lambda:m.endpoint_return(1e-308,1e308)),
        ('F99 positive gross cannot report total loss',lambda:m.annualized_return([-.99],252)),
        ('zero price series remains explicitly unsupported',lambda:m.price_returns([100,0])),
    ]:reject(label,fn)
    demo=commands[0]['stdout'].splitlines()
    ck('exact demo outputs',demo==['Wealth path: [10000.0, 11000.0, 9900.0, 10395.0, 10187.1]',
        'Cumulative return: 1.8710%',f'Geometric mean per period: {float(equiv(F("1.01871"),F(1,4))):.4%}'])
    ck('F99 final project answers written','26,501.60' in source.read_text() and '6.00638048%' in source.read_text())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[15,16,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
